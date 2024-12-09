# SPDX-License-Identifier: GPL-3.0-or-later

# Copyright (C) 2020 Michał Góral.

from i3ipc.aio import Connection
from i3ipc import Event

import sys
import asyncio
import signal
import collections
import functools
import argparse
import logging as log

from i3a import __version__ as version

FLOATING_MODES = ('auto_on', 'user_on')
STACKMARK = '__i3a_stack'
INTERNAL_MOVE_MARK = '__i3a_internalmove'

def prepare_args():
    parser = argparse.ArgumentParser(
        description='i3a-master-stack - automatic master-stack layout for i3 and sway')

    parser.add_argument('--stack', choices=('dwm', 'i3'), default='i3',
                        help='choose visual type of stacking')
    parser.add_argument('--stack-size', type=int, default=50,
                        help='percentage size of stack area')

    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--version', action='version',
                        version='%(prog)s {}'.format(version))

    return parser.parse_args()

# Depth-first traversal of leaf nodes. It is more useful for determining which
# node on the stack is the last one (if user decided to e.g. split some middle
# stack windows, breadth-first, implemented by i3ipc-python, would yield
# incorrect results and new windows would be created in that split)
def leaves_dfs(root):
    stack = collections.deque([root])
    while len(stack) > 0:
        n = stack.pop()
        if not n.nodes and n.type == "con" and n.parent.type != "dockarea":
            yield n
        stack.extend(reversed(n.nodes))


def get_workspaces(tree):
    workspaces = {}
    for window in leaves_dfs(tree):
        w = window.workspace()
        if w is None:
            continue
        workspaces.setdefault(w.name, []).append(window)
    return workspaces


def tiled_nodes(tree, wsname):
    workspaces = get_workspaces(tree)
    ws = workspaces.get(wsname, [])
    return [l for l in ws if l.floating not in FLOATING_MODES]


# Deducts master-stack area contents by parent ids.
def master_stack(tree, node, exclude_node=False):
    cont = tree.find_by_id(node.id)
    if cont is None:
        return None, None

    if cont.floating in FLOATING_MODES:
        return None, None

    wsname = cont.workspace().name
    tiled = tiled_nodes(tree, wsname)

    if exclude_node:
        try:
            tiled.remove(cont)
        except ValueError:
            pass

    if not tiled:
        return None, None

    if len(tiled) == 1:
        return tiled[0], []

    if tiled[0].parent == tiled[1].parent:
        return None, tiled

    return tiled[0], tiled[1:]

class Autotiler:
    def __init__(self, args):
        self.args = args
        self.i3 = None

    async def _node_removed(self, tree, e):
        # Support only focused workspace; background workspaces will be rebuilt
        # after workspace::focus event. This is suboptimal, but moving
        # stack->master in the background steals the focus (at least on sway),
        # which is an inacceptable user interrupt
        master, stack = master_stack(tree, tree.find_focused())

        if master and not stack:
            await self.cmd('[con_id="{}"] split horizontal'.format(master.id))
            return

        if not master and stack:
            await self.intermove(stack[0], 'move left')
            if len(stack) > 1:  # stack[0] becomes a new master, resize remains
                await self.cmd('[con_id="{}"] resize set {} ppt 0 ppt'.format(stack[-1].id, self.args.stack_size))

    async def _node_added(self, tree, e):
        master, stack = master_stack(tree, e.container, exclude_node=True)
        curr = tree.find_by_id(e.container.id)

        if not master and stack:
            await self.intermove(stack[0], 'move left')
            return
        if not master and not stack:
            return

        if not stack:
            await self.cmd('[con_id="{}"] split horizontal'.format(master.id))
            await self.make_stack(curr)
            await self.cmd('[con_id="{}"] resize set {} ppt 0 ppt'.format(curr.id, self.args.stack_size))
        else:
            await self.cmd('[con_id="{}"] mark --add {}'.format(stack[-1].id, STACKMARK))

            # Compound command are A LOT faster than separate ones; running
            # additional focus after "intermove" left a visible visual glitch
            # of "jumping" window when new window was spawned when focus was on
            # a master window. There's still a minor artifact with compound command,
            # but it's more bearable now
            move_cmd = 'move window to mark {}'.format(STACKMARK)
            if curr.workspace() == tree.find_focused().workspace():
                move_cmd += ", focus"
            await self.intermove(curr, move_cmd)

    async def win_close(self, i3, e):
        log.debug('called win_close()')

        if e.container.type == 'floating_con':
            return

        tree = await self.i3.get_tree()
        await self._node_removed(tree, e)

    async def win_new(self, i3, e):
        log.debug('called win_new()')

        if e.container.type == 'floating_con':
            return

        tree = await self.i3.get_tree()
        await self._node_added(tree, e)

    async def win_move(self, i3, e):
        if await self.rmmovemarks(e.container):
            log.debug('win_move() skipped for id={}'.format(e.container.id))
            return

        log.debug('called win_move()')

        if e.container.type == 'floating_con':
            return

        tree = await self.i3.get_tree()

        curr = tree.find_by_id(e.container.id)
        foc = tree.find_focused()

        if foc.workspace() == curr.workspace():
            return

        w1_master, w1_stack = master_stack(tree, foc)
        w2_master, w2_stack = master_stack(tree, curr, exclude_node=True)

        await self._node_removed(tree, e)
        await self._node_added(tree, e)

    async def win_float(self, i3, e):
        log.debug('called win_float()')

        tree = await self.i3.get_tree()
        if e.container.type == 'con':
            await self._node_added(tree, e)
        elif e.container.type == 'floating_con':
            await self._node_removed(tree, e)

    async def workspace_focus(self, i3, e):
        log.debug('called workspace_focus()')
        tiled = [node for node in e.current.leaves()
                 if node.floating not in FLOATING_MODES]

        # Rebuild workspace's master. This is intended to fix a layout after
        # closing a window in the background workspace, the first time we focus
        # that workspace.
        if len(tiled) > 1 and tiled[0].parent == tiled[1].parent:
            await self.intermove(tiled[0], 'move left')
            if len(tiled) > 1:  # tiled[0] becomes a new master, resize remains
                await self.cmd('[con_id="{}"] resize set {} ppt 0 ppt'.format(tiled[-1].id, self.args.stack_size))

    async def make_stack(self, node):
        # this works only when there are exactly 2 nodes, which is a caller
        # responsibility to check
        await self.cmd('[con_id="{}"] split vertical'.format(node.id))

        if self.args.stack == 'i3':
            await self.cmd('[con_id="{}"] layout stacking'.format(node.id))

    async def cmd(self, cmd):
        log.debug(cmd)
        await self.i3.command(cmd)

    async def intermove(self, node, cmd):
        movemark = INTERNAL_MOVE_MARK + '_{}'.format(node.id)
        # Note: compound commands separated with a colon retain their criteria
        # ("con_id"); compound commands separated with semicolon don't.
        await self.cmd('[con_id="{}"] mark --add {}, {}'.format(node.id, movemark, cmd))

    async def rmmovemarks(self, node):
        removed = False
        for mark in node.marks:
            if mark.startswith(INTERNAL_MOVE_MARK):
                await self.cmd('[con_id="{}"] mark --toggle {}'.format(node.id, mark))
                removed = True
        return removed

    async def run(self):
        self.i3 = await Connection(auto_reconnect=True).connect()
        self.i3.on(Event.WINDOW_CLOSE, self.win_close)
        self.i3.on(Event.WINDOW_NEW, self.win_new)
        self.i3.on(Event.WINDOW_MOVE, self.win_move)
        self.i3.on(Event.WINDOW_FLOATING, self.win_float)
        self.i3.on(Event.WORKSPACE_FOCUS, self.workspace_focus)
        log.debug('i3a-master-stack is ready')
        await self.i3.main()


def sigint_handler(sig):
    sys.exit(int(sig))


def main():
    args = prepare_args()

    if not 0 < args.stack_size < 100:
        log.error('--stack-size must be a value between 1-99')
        return 1

    loglevel = log.DEBUG if args.debug else log.INFO
    log.basicConfig(format='%(message)s', level=loglevel)

    autotiler = Autotiler(args)
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(
        signal.SIGINT, functools.partial(sigint_handler, signal.SIGINT))
    loop.run_until_complete(autotiler.run())
    return 0
