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
import subprocess
import logging as log
import re

from i3a import __version__ as version

DEFAULT_PARENTS = ['^kitty', '^alacritty', '^st', '^XTerm', '^foot']

Window = collections.namedtuple('Window', ('pid', 'ppid', 'winid', 'pwinid'))


def prepare_args():
    parser = argparse.ArgumentParser(
        description='i3a-swallow - automatic swallowing of child windows')

    parser.add_argument('-e', '--exclude-class', action='append', dest='excluded',
        help='class/app_ids of windows which shouldn\'t trigger swallowing of '
             'their parents. Empty by default, can be given more than once')
    parser.add_argument('-p', '--parent', action='append', dest='parents',
        help='class/app_ids of parent windows whose children should be '
            'swallowed; By default contains some popular terminals. Can be '
            'given more than once')

    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--version', action='version',
                        version='%(prog)s {}'.format(version))

    return parser.parse_args()


def compile_re(patterns):
    return [re.compile(pat) for pat in patterns]


def class_or_app_id(cont):
    return cont.app_id if cont.app_id else cont.window_class


def has_any_class(cont, classes):
    app_id_or_class = class_or_app_id(cont)
    if not app_id_or_class:
        log.warning('Window {} (winid: {}): no app_id/class'.format(
            cont.window_title, cont.id))
        return False

    return any(c.search(app_id_or_class) for c in classes)

def ps_ppid(pid):
    cmd = ['ps', '-q', str(pid), '-o', 'ppid=']
    cp = subprocess.run(cmd, text=True, capture_output=True)
    if cp.returncode != 0:
        return None
    return int(cp.stdout.strip())

def ps_ppids(pid):
    '''Finds all parents of a given PID, in case there's intermediate parent
    (e.g. a shell running in WM-managed terminal window)'''
    ppids = []

    curr = pid
    while curr and curr != 1:
        curr = ps_ppid(curr)
        if curr and curr != 1:
            ppids.append(curr)

    return ppids


def xprop_pid(xwin_id):
    cmd = ['xprop', '-id', str(xwin_id), '_NET_WM_PID']

    try:
        cp = subprocess.run(cmd, text=True, capture_output=True)
    except FileNotFoundError:
        log.error('xprop not found: it is mandatory for X11 (i3)')
        return None

    if cp.returncode != 0:
        return None
    _, _, pid = cp.stdout.partition('=')
    pidstr = pid.strip()
    return int(pidstr) if pidstr else None


def get_pid(cont):
    if hasattr(cont, 'pid') and cont.pid:  # sway
        return cont.pid
    return xprop_pid(cont.window)  # i3


def find_by_pid(tree, pid):
    for cont in tree.leaves():
        if cont.pid == pid:  # sway
            return cont
        elif cont.pid is None and xprop_pid(cont.window) == pid:  # i3
            return cont


def is_on_scratchpad(win):
    return win.scratchpad() == win.workspace()


class Swallower:
    def __init__(self, args):
        self.args = args
        self.children = {}  # map child: parent
        self.parents = {}   # map parent: [child, ...]

    async def win_new(self, i3, e):
        if has_any_class(e.container, self.args.excluded):
            log.debug('excluded swallow of {} parent'.format(class_or_app_id(e.container)))
            return

        pid = get_pid(e.container)
        if not pid:
            log.error('couldn\'t get PID for window {}'.format(e.container.id))
            return

        tree = await self.i3.get_tree()
        for ppid in ps_ppids(pid):
            parent = find_by_pid(tree, ppid)

            if not parent:
                continue

            if is_on_scratchpad(parent):
                self._manage(e.container, parent)
                log.debug('next child of {}'.format(self._rep(parent)))
                return

            if not has_any_class(parent, self.args.parents):
                log.debug('excluded swallow of {}'.format(class_or_app_id(parent)))
                return

            self._manage(e.container, parent)
            await parent.command('move scratchpad')
            log.debug('swallowed {}'.format(self._rep(parent)))
            return

    async def win_close(self, i3, e):
        parent_id, remaining = self._unmanage(e.container)
        if not parent_id:
            if e.container.id in self.parents:
                log.debug('cleaning {}'.format(self._rep(e.container)))
                self._clean_parent(e.container)
            return

        tree = await self.i3.get_tree()
        pwin = tree.find_by_id(parent_id)
        if pwin:
            if remaining:
                log.debug('not unswallowing: remaining children of {}'.format(self._rep(pwin)))
                return
            if not is_on_scratchpad(pwin):
                log.debug('not unswallowing: not on scratchpad {}'.format(self._rep(pwin)))
                return
            await pwin.command('scratchpad show; floating toggle')
            log.debug('unswallowed: {}({})'.format(class_or_app_id(pwin), parent_id))

    def _rep(self, cont):
        return '{}({}):{}'.format(class_or_app_id(cont), cont.id, self.parents.get(cont.id, []))

    def _manage(self, cont, parent):
        self.children[cont.id] = parent.id
        self.parents.setdefault(parent.id, []).append(cont.id)

    def _unmanage(self, cont):
        parent_id = self.children.pop(cont.id, None)
        if parent_id is None:
            return None, None

        remaining = self.parents[parent_id]
        remaining.remove(cont.id)
        if not remaining:
            del self.parents[parent_id]

        return parent_id, remaining

    def _clean_parent(self, cont):
        for ch in self.parents.pop(cont.id, []):
            del self.children[ch]

    async def run(self):
        self.i3 = await Connection(auto_reconnect=True).connect()
        self.i3.on(Event.WINDOW_CLOSE, self.win_close)
        self.i3.on(Event.WINDOW_NEW, self.win_new)
        log.debug('i3a-swallow is ready')
        await self.i3.main()


def sigint_handler(sig):
    sys.exit(int(sig))


def main():
    args = prepare_args()

    loglevel = log.DEBUG if args.debug else log.INFO
    log.basicConfig(format='%(message)s', level=loglevel)

    if not args.parents:
        args.parents = DEFAULT_PARENTS

    if not args.excluded:
        args.excluded = []

    log.debug('excluded: {}'.format(', '.join(args.excluded)))
    log.debug('parents: {}'.format(', '.join(args.parents)))

    args.excluded = compile_re(args.excluded)
    args.parents = compile_re(args.parents)

    swallower = Swallower(args)
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(
        signal.SIGINT, functools.partial(sigint_handler, signal.SIGINT))
    loop.run_until_complete(swallower.run())
    return 0
