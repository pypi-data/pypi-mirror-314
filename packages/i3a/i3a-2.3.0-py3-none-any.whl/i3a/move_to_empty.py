# SPDX-License-Identifier: GPL-3.0-or-later

# Copyright (C) 2020 Michał Góral.
#
import sys
from i3ipc import Connection

def get_workspaces(tree):
    workspaces = set()
    for window in tree.leaves():
        ws = window.workspace()
        if ws:
            workspaces.add(ws.name)
    return workspaces

def main():
    i3 = Connection()
    tree = i3.get_tree()

    window = tree.find_focused()
    if not window:
        sys.exit(1)

    # Focused window is the only client of current workspace. Moving it to
    # an empty workspace won't give us anything.
    if len(window.workspace().leaves()) < 2:
        sys.exit(0)

    used = get_workspaces(tree)

    workspaces = [str(i) for i in range(1, 11)]
    for ws in workspaces:
        if ws not in used:
            i3.command('move container to workspace {}'.format(ws))
            i3.command('[con_id="{}"] focus'.format(window.id))
            sys.exit(0)
    sys.exit(1)

