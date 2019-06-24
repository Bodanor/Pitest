import curses
import signal
import time

import RPi.GPIO as GPIO

BootMenu = ['Test du module HC-SR04', 'Test du module Bluetooth', 'Paramètres du Rover', 'Quitter']
HCMenu = ['Test de connection avec le module']
BluetoothMenu = ['There is nothing here ! Come back when the next update will be released !']
Rover = ['There is nothing here ! Come back when the next update will be released !']


def get_terminal_yx(stdscr, y, x):
    y, x = stdscr.getmaxyx()
    return y, x


def print_title(stdscr, title):
    h = 0
    w = 0
    h, w = get_terminal_yx(stdscr, h, w)

    if title == "main":

        title1 = "+------------------------------+"
        title2 = "|        Chris & Julien        |"
        title3 = "+------------------------------+"
        h = 0
        w = 0
        h, w = get_terminal_yx(stdscr, h, w)
        x = w // 2 - len(title1) // 2
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(0, x, title1)
        x = w // 2 - len(title2) // 2
        stdscr.addstr(1, x, title2)
        x = w // 2 - len(title3) // 2
        stdscr.addstr(2, x, title3)
        stdscr.attroff(curses.color_pair(2))
        stdscr.refresh()

    elif title == "HC_SR04":

        title1 = "+-----------------------------------------------------------+"
        title2 = "|   Mesure de distance par le capteur ultrasonore HC-SR04   |"
        title3 = "+-----------------------------------------------------------+"
        x = w // 2 - len(title1) // 2
        stdscr.addstr(1, x, title1)
        x = w // 2 - len(title2) // 2
        stdscr.addstr(2, x, title2)
        x = w // 2 - len(title3) // 2
        stdscr.addstr(3, x, title3)
        stdscr.refresh()


def print_menu(stdscr, current_tab, previous_menu, menu):
    stdscr.clear()
    h = 0
    w = 0
    h, w = get_terminal_yx(stdscr, h, w)

    for idx, row in enumerate(menu):

        x = w // 2 - len(row) // 2
        y = h // 2 - len(menu) // 2 + idx
        if menu == BootMenu:

            if idx == current_tab:

                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(1))

            else:

                stdscr.addstr(y, x, row)

            stdscr.addstr(h - 1, 0, "Press q to quit")


        elif menu == HCMenu:

            if idx == current_tab:

                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(1))

            else:

                stdscr.addstr(y, x, row)

            stdscr.attron(curses.color_pair(5))
            stdscr.addstr(0, 0, BootMenu[previous_menu])
            stdscr.attroff(curses.color_pair(5))
            stdscr.addstr(h - 1, 0, "Press b to go back to the main menu")

        elif menu == BluetoothMenu:

            if idx == current_tab:

                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(1))

            else:

                stdscr.addstr(y, x, row)

            stdscr.attron(curses.color_pair(5))
            stdscr.addstr(0, 0, BootMenu[previous_menu])
            stdscr.attroff(curses.color_pair(5))
            stdscr.addstr(h - 1, 0, "Press b to go back to the main menu")

        elif menu == Rover:

            if idx == current_tab:

                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(1))

            else:

                stdscr.addstr(y, x, row)

            stdscr.attron(curses.color_pair(5))
            stdscr.addstr(0, 0, BootMenu[previous_menu])
            stdscr.attroff(curses.color_pair(5))
            stdscr.addstr(h - 1, 0, "Press b to go back to the main menu")

    stdscr.refresh()


def HC_SR04_Module(stdscr, previous_menu):
    curses.curs_set(1)
    h = 0
    w = 0
    h, w = get_terminal_yx(stdscr, h, w)

    stdscr.attron(curses.color_pair(2))
    print_title(stdscr, "HC_SR04")
    stdscr.attroff(curses.color_pair(2))

    stdscr.addstr(h - 1, 0, "Press Control c to exit test")

    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(0, 0, HCMenu[previous_menu])
    stdscr.attroff(curses.color_pair(3))

    GPIO.setmode(GPIO.BOARD)
    stdscr.addstr(6, 0, "Trig (Transmitter) -->")
    stdscr.addstr(7, 0, "Echo (Receiver) -->")
    Trig = stdscr.getstr(6, 22, 2)
    Echo = stdscr.getstr(7, 19, 2)
    curses.curs_set(0)
    Trig = int(Trig)
    Echo = int(Echo)
    GPIO.setup(Trig, GPIO.OUT)
    GPIO.setup(Echo, GPIO.IN)

    GPIO.output(Trig, False)
    h, w = get_terminal_yx(stdscr, h, w)
    x = w //2 - len("Waiting for sensor to settle...")//2
    y = h//2
    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(y, x, "Waiting for sensor to settle...")
    stdscr.attroff(curses.color_pair(1))
    stdscr.refresh()
    time.sleep(2)
    while 1:

        stdscr.clear()
        h = 0
        w = 0
        h, w = get_terminal_yx(stdscr, h, w)

        GPIO.output(Trig, True)
        time.sleep(0.00001)
        GPIO.output(Trig, False)

        while GPIO.input(Echo) == 0:
            Start = time.time()

        while GPIO.input(Echo) == 1:
            End = time.time()

        distance = round((End - Start) * 17150, 2)

        if distance < 10:

            stdscr.attron(curses.color_pair(1))
            str = ("Distance :{} cm".format(distance))
            x = w // 2 - len(str) // 2
            y = h // 2
            stdscr.addstr(y, x, str)
            stdscr.attroff(curses.color_pair(1))

        elif distance > 60:

            stdscr.attron(curses.color_pair(3))
            str = ("Distance :{} cm".format(distance))
            x = w // 2 - len(str) // 2
            y = h // 2
            stdscr.addstr(y, x, str)
            stdscr.attroff(curses.color_pair(3))

        else:

            stdscr.attron(curses.color_pair(4))
            str = ("Distance :{} cm".format(distance))
            x = w // 2 - len(str) // 2
            y = h // 2
            stdscr.addstr(y, x, str)
            stdscr.attroff(curses.color_pair(4))
        stdscr.addstr(h - 1, 0, "Press Control c to exit test")
        stdscr.addstr(6, 0, "Trig (Transmitter) -->{}".format(Trig))
        stdscr.addstr(7, 0, "Echo (Receiver) -->{}".format(Echo))

        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(0, 0, HCMenu[previous_menu])
        stdscr.attroff(curses.color_pair(3))

        stdscr.attron(curses.color_pair(2))
        print_title(stdscr, "HC_SR04")
        stdscr.attroff(curses.color_pair(2))
        time.sleep(1)
        stdscr.refresh()


def main(stdscr):

    curses.echo()
    original_sigint_handler = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    curses.curs_set(0)

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_CYAN)

    current_tab = 0
    previous_tab = 0
    print_menu(stdscr, current_tab, previous_tab, BootMenu)
    print_title(stdscr, "main")

    while 1:

        key = stdscr.getch()
        stdscr.clear()

        if key == curses.KEY_UP and current_tab > 0:

            current_tab -= 1

        elif key == curses.KEY_DOWN and current_tab < len(BootMenu) - 1:

            current_tab += 1

        elif key == curses.KEY_ENTER or key in [10, 13] and current_tab == 0:

            print_menu(stdscr, current_tab, previous_tab, HCMenu)

            while 1:

                key = stdscr.getch()
                stdscr.clear()

                if key == curses.KEY_UP and current_tab > 0:

                    current_tab -= 1

                elif key == curses.KEY_DOWN and current_tab < len(HCMenu) - 1:

                    current_tab += 1


                elif key == curses.KEY_ENTER or key in [10, 13] and current_tab == 0:

                    signal.signal(signal.SIGINT, original_sigint_handler)

                    try:

                        while 1:
                            HC_SR04_Module(stdscr, previous_tab)

                    except KeyboardInterrupt:

                        GPIO.cleanup()
                        signal.signal(signal.SIGINT, signal.SIG_IGN)



                elif key == ord('b') or key == ord('B'):

                    previous_tab = 0
                    current_tab = 0
                    break

                else:

                    curses.beep()

                print_menu(stdscr, current_tab, previous_tab, HCMenu)
                stdscr.refresh()

        elif key == curses.KEY_ENTER or key in [10, 13] and current_tab == 1:

            current_tab = 0
            previous_tab = 1
            print_menu(stdscr, current_tab, previous_tab, BluetoothMenu)

            while 1:

                key = stdscr.getch()
                stdscr.clear()

                if key == curses.KEY_UP and current_tab > 0:

                    current_tab -= 1

                elif key == curses.KEY_DOWN and current_tab < len(BluetoothMenu) - 1:

                    current_tab += 1

                elif key == ord('b') or key == ord('Q'):

                    previous_tab = 0
                    current_tab = 1
                    break

                else:

                    curses.beep()

                print_menu(stdscr, current_tab, previous_tab, BluetoothMenu)
                stdscr.refresh()

        elif key == curses.KEY_ENTER or key in [10, 13] and current_tab == 2:

            current_tab = 0
            previous_tab = 2
            print_menu(stdscr, current_tab, previous_tab, Rover)

            while 1:

                key = stdscr.getch()
                stdscr.clear()

                if key == curses.KEY_UP and current_tab > 0:

                    current_tab -= 1

                elif key == curses.KEY_DOWN and current_tab < len(Rover) - 1:

                    current_tab += 1

                elif key == ord('b') or key == ord('Q'):

                    previous_tab = 0
                    current_tab = 2
                    break

                else:

                    curses.beep()

                print_menu(stdscr, current_tab, previous_tab, Rover)
                stdscr.refresh()


        elif key == curses.KEY_ENTER or key in [10, 13] and current_tab == 3:

            exit(1)

        elif key == ord('q') or key == ord('Q'):

            exit(1)

        else:

            curses.beep()

        print_menu(stdscr, current_tab, previous_tab, BootMenu)
        print_title(stdscr, "main")
        stdscr.refresh()


curses.wrapper(main)
