# i3a

i3a is a set of scripts used for automation of i3 and sway window manager
layouts.

## Automation list

### i3a-master-stack

Provides automatic master-stack layout, which is known from e.g. DWM. The
following kinds of the layout are possible:

- master-stack area with DWM-like stack (stack windows are split)
- master-stack area with i3-like stack (stack windows are actual stack)

To use, run `i3a-master-stack` with selected options (`i3a-master-stack
--help` for details). One way to run it automatically is via a systemd
user service.

1.  Create the following file in _~/.config/systemd/user/i3a-master-stack_:

```
[Unit]
Description=i3a-master-stack

[Service]
ExecStart=%h/.local/bin/i3a-master-stack --stack=dwm --stack-size=35
Restart=on-failure
```

2.  Add the following entry to your i3 or sway configuration file:

```
exec "systemctl --user restart i3a-master-stack.service"
```

### i3a-swap

Swap currently focused window between master and stack areas from
i3a-master-stack (technically it doesn't require running i3-master-stack).

To use it, add the following binding to your i3 or sway configuration file:

```
bindsym $mod+f exec i3a-swap
```

### i3a-swallow

Provides automatic "swallowing": when a program runs a child process, the
parent is automatically hidden (moved to the scratchpad), which looks like if
it was replaced, or "swallowed" by the child window. It is especially useful
for graphical programs (video player, document viewer etc.) run from the
terminal.

Provides a means of filtering both parent programs which can be swallowed and
child programs which can trigger swallowing.

To use it, run `i3a-swallow` with selected options. One way to run it
automatically is via a systemd user service.

1.  Create the following file in _~/.config/systemd/user/i3a-swallow_:

```
[Unit]
Description=i3a-swallow

[Service]
ExecStart=%h/.local/bin/i3a-swallow
Restart=on-failure
```

2.  Add the following entry to your i3 or sway configuration file:

```
exec "systemctl --user restart i3a-swallow.service"
```

### i3a-move-to-empty

Moves currently focused container to the first empty workspace. Keep in mind
that this script relies on numbering of the workspaces.

To use it, add the following binding to your i3 or sway configuration file:

```
bindsym $mod+w exec i3a-move-to-empty
```

### i3a-resize-compass

Extension of `resize` command. Currently focused window will automatically
grow or shrink in a direction passed to i3a-resize-compass.

```
bindsym $mod+Up exec i3a-resize-compass up 2ppt
bindsym $mod+Down exec i3a-resize-compass down 2ppt
bindsym $mod+Right exec i3a-resize-compass right 2ppt
bindsym $mod+Left exec i3a-resize-compass left 2ppt
```

### i3a-cycle-focus

Change the currently focused window up or down, cycling the tiled windows
within the current workspace.

```
bindsym $mod+j exec i3a-cycle-focus down
bindsym $mod+k exec i3a-cycle-focus up 
```

### i3a-scale-cycle

**sway-specific**

Changes output's scale factor to the next or previous one on a given list.
Current scale factor is then printed for each requested output (or all
available outputs if none was explicitly set).

`-f, --scale-factors` is a comma-separated list of factors which i3a-scale
will cycle so it must be escaped in configuration file:

```
bindsym $mod+s exec "i3a-scale-cycle -f 1.0,1.5,2.0 -o HDMI-1 -o HDMI-2 --next"
```

## Installation

- [PyPI](https://pypi.org/project/i3a/)
- [AUR](https://aur.archlinux.org/packages/i3a/) (Arch Linux - unofficial)
