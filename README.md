Multi Monitor Setup
===================

Easy multi monitor setup tool for Linux. It helps when using a minimal windowmanager.

Installation
------------

This is a one file python application. Simply download it, make it executable
(chmod +x), and run it.

Usage
-----
multi_monitor_setup.py [-h] [-g] [-r] [-t] [-d] [-s [SCREEN_ORDER [SCREEN_ORDER ...]]]

optional arguments:
  -h, --help            show this help message and exit
  -g, --show_gui        show gui
  -r, --restore_bg      restore the background settigns
  -t, --align_top       align the screens at the top
  -d, --dry_run         prints the settings and command to screen without
                        performing the command
  -s [SCREEN_ORDER [SCREEN_ORDER ...]], --screen_order [SCREEN_ORDER [SCREEN_ORDER ...]]
                        list of screen names in order, screens which are not
                        provided or are unavailable will be ignored. Get a
                        list of available screens using "xrandr -q".

Additional notes:
- The setting to restore the background is currently not working since I always restore the background.
- It is possible to set a standard screen order in the python source directly. This way there is no need to provide them as arguments.
- To restore the background, it is assumed that nitrogen is installed (and used). This can be changed in the source code.
- To set the new monitor layout, xrandr is used. This can be changed in the source code.
- As a GUI, arandr is used. This can be changed in the source code.
- to find the names of the attached screens use "xrandr -q"

A usage example would be:
        multi_monitor_setup.py -t -s VGA-0 LVDS -d
This would show the xrandr command to set VGA-0 as the left monitor, and LVDS as the right monitor and aligns the top of the monitor.
        multi_monitor_setup.py -s HDMI-0 LVDS VGA-0 -d
This would show the xrandr command to set HDMI-0 as the left monitor, LVDS as the middle monitor, and VGA-0 as the right monitor. The monitors will be bottom aligned.
