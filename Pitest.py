import curses
import signal
import curses.panel

first_menu = ['HC-SR04 module Test', 'Exit']
HC_SR04_menu = ['Connection test with one module', 'Connection test with multiple modules', 'Back']


def print_title(stdscr):
    title1 = "+------------------------------+"
    title2 = "|        Chris & Julien        |"
    title3 = "+------------------------------+"

    h = 0
    w = 0
    h, w = get_terminal_size(stdscr, h, w)
    x = w // 2 - len(title1) // 2
    stdscr.attron(curses.color_pair(2))
    stdscr.addstr(0, x, title1)
    x = w // 2 - len(title2) // 2
    stdscr.addstr(1, x, title2)
    x = w // 2 - len(title3) // 2
    stdscr.addstr(2, x, title3)
    stdscr.attroff(curses.color_pair(2))
    stdscr.refresh()


def get_terminal_size(stdscr, h, w):
    h, w = stdscr.getmaxyx()
    return h, w


def print_menus(stdscr, current_tab, menu, previous_menu):
    h = 0
    w = 0
    h, w = get_terminal_size(stdscr, h, w)

    for idx, row in enumerate(menu):
        y = h // 2 - len(menu) // 2 + idx
        x = w // 2 - len(row) // 2

        if menu == first_menu:
            if idx == current_tab:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, row)

        elif menu == HC_SR04_menu:
            stdscr.attron(curses.color_pair(3))
            stdscr.addstr(3, 0, first_menu[previous_menu])
            stdscr.attroff(curses.color_pair(3))
            if idx == current_tab:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(1))

            else:
                stdscr.addstr(y, x, row)

    stdscr.refresh()


def main(stdscr):

    original_sigint_handler = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.curs_set(0)
    current_tab = 0
    previous_menu = 0

    print_title(stdscr)
    print_menus(stdscr, current_tab, first_menu, 0)
    while 1:
        key = stdscr.getch()
        if key == curses.KEY_UP and current_tab > 0:
            current_tab -= 1

        elif key == curses.KEY_DOWN and current_tab < len(first_menu) - 1:
            current_tab += 1

        elif key == curses.KEY_UP and current_tab == 0:
            current_tab = len(first_menu) - 1

        elif key == curses.KEY_DOWN and current_tab == len(first_menu) - 1:
            current_tab = 0

        elif key == curses.KEY_ENTER or key in [10, 13] and current_tab == 0:
            stdscr.clear()
            print_title(stdscr)
            print_menus(stdscr, current_tab, HC_SR04_menu, 0)
            while 1:

                key = stdscr.getch()

                if key == curses.KEY_UP and current_tab > 0:
                    current_tab -= 1

                elif key == curses.KEY_DOWN and current_tab < len(HC_SR04_menu) - 1:
                    current_tab += 1

                elif key == curses.KEY_UP and current_tab == 0:
                    current_tab = len(HC_SR04_menu) - 1

                elif key == curses.KEY_DOWN and current_tab == len(HC_SR04_menu) - 1:
                    current_tab = 0

                elif key == curses.KEY_ENTER or key in [10, 13] and current_tab == 2:
                    current_tab = 0
                    break

                stdscr.clear()
                print_title(stdscr)
                print_menus(stdscr, current_tab, HC_SR04_menu, 0)

        elif key == curses.KEY_ENTER or key in [10, 13] and current_tab == 1:
            exit(1)
        elif key == curses.KEY_RESIZE:
            continue

        stdscr.clear()
        print_title(stdscr)
        print_menus(stdscr, current_tab, first_menu, 0)


curses.wrapper(main)

