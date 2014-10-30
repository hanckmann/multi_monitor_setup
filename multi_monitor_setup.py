#!/usr/bin/python2

import sys
import argparse
import subprocess


def main(argv):
    # Set input arguments
    show_gui     = False
    restore_bg   = True
    align_bottom = True
    dry_run      = False
    screen_order = ['DP2', 'DP1', 'eDP1']
    primary      = 'eDP1'

    # Set fixed arguments
    randr_conf      = 'xrandr'
    gui_conf        = 'arandr'
    restore_bg_conf = 'nitrogen'

    # Parse input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-g','--show_gui',   action="store_true",
                        help='show gui')
    parser.add_argument('-r','--restore_bg', action="store_true",
                        help='restore the background settigns')
    parser.add_argument('-t','--align_top',  action="store_true",
                        help='align the screens at the top')
    parser.add_argument('-d','--dry_run',    action="store_true",
                        help='prints the settings and command to screen without performing the command')
    parser.add_argument('-s','--screen_order', action='store', default=screen_order, type=str, nargs='*',
                        help='list of screen names in order, screens which are not provided or are unavailable will be ignored. Get a list of available screens using "xrandr -q".')
    parser.add_argument('-p','--primary', action='store', default=primary, type=str, nargs=1,
                        help='The name of the primary screen. Get a list of available screens using "xrandr -q".')
    args = parser.parse_args(argv)
    if args.show_gui:
        show_gui = True
    if args.restore_bg:
        restore_bg = True
    if args.align_top:
        align_bottom = False
    if args.dry_run:
        dry_run = True
    if args.screen_order:
        screen_order = args.screen_order
    if args.primary:
        primary = args.primary
    #print 'show_gui     ' + str(show_gui)
    #print 'restore_bg   ' + str(restore_bg)
    #print 'align_bottom ' + str(align_bottom)
    #print 'dry_run      ' + str(dry_run)
    #print 'screen_order ' + str(screen_order)
    #print 'primary      ' + str(primary)

    # Get randr status
    p = subprocess.Popen([randr_conf, '-q'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    randr_out, randr_error = p.communicate()
    if randr_error:
        print 'Error in capturing randr status:'
        print randr_error
        exit(3)

    # Process randr_status
    lines = randr_out.split('\n')
    screens = dict()
    screen = None
    for line in lines:
        # Find the screen id
        if not screen:
            words = line.split(' ')
            if len(words) > 2:
                if words[1] == 'connected':
                    screen = words[0]
                    id_line = False
        else:
            words = line.split(' ')
            for word in words:
                if 'x' in word:
                    xy = word.split('x')
                    x = int(xy[0])
                    y = int(xy[1])
                    screens[screen] = (x,y)
                    screen = None

    # Build or check screen_order
    if screen_order[0]:
        screen_order_temp = [screen for screen in screen_order if screen in screens] # intersection of screens and screen_order, keeping the order of screen_order
        screen_order = screen_order_temp
    if not screen_order:
        screen_order = list()
        for key in screens.keys():
            screen_order.append(key)

    from_top = 0;
    if align_bottom:
        for screen in screen_order:
            xy = screens[screen]
            from_top = max(from_top, xy[1])

    randr_args = list()
    randr_args.append(randr_conf)
    from_left = 0
    for screen in screen_order:
        if screen in screens:
            xy = screens[screen]
            randr_args.append('--output')
            randr_args.append(screen)
            randr_args.append('--mode')
            mode = str(xy[0]) + 'x' + str(xy[1])
            randr_args.append(mode)
            randr_args.append('--pos')
            pos = str(from_left) + 'x' + str(from_top - xy[1])
            randr_args.append(pos)
            from_left += xy[0]
            if screen == primary:
                randr_args.append('--primary')

    # Execute
    if not dry_run:
        p = subprocess.Popen(randr_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        randr_out, randr_error = p.communicate()
        if randr_error:
            print 'Error in setting randr to:'
            print randr_args
            print 'Error:'
            print randr_error
            exit(9)
    else:
        print ' '.join(randr_args)

    if show_gui:
        print randr_args
        p = subprocess.Popen([gui_conf,], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if restore_bg:
        p = subprocess.Popen([restore_bg_conf,'--restore'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if __name__ == '__main__':
    main(sys.argv[1:])
