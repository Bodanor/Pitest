import curses
import signal
# import RPi.GPIO as GPIO
import time
from playsound import playsound

menu = ['Test du module HC-SR04', 'Test du module Bluetooth', 'Paramètres du rover']
menuHC_SR04 = ['Test de connection avec le module']


def Title(stdscr):
    title1 = "================================"
    title2 = "=        Chris & Julien        ="
    title3 = "================================"
    h, w = stdscr.getmaxyx()
    x = w // 2 - len(title1) // 2
    y = h // 2
    stdscr.addstr(0, x, title1)
    x = w // 2 - len(title2) // 2
    y = h // 2
    stdscr.addstr(1, x, title2)
    x = w // 2 - len(title3) // 2
    y = h // 2
    stdscr.addstr(2, x, title3)


def signal_handler(signal, frame):
    print("Use q key")


def print_menu(stdscr, selected_menu):
    stdscr.clear()
    for idx, row in enumerate(menu):
        h, w = stdscr.getmaxyx()
        x = w // 2 - len(row) // 2
        y = h // 2 - len(menu) // 2 + idx
        if idx == selected_menu:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
        stdscr.addstr(h - 1, 0, "Appuye sur la touche q pour quitter !")
    stdscr.refresh()


def print_HC_SR04_menu(stdscr, selected_menu):
    stdscr.clear()
    for idx, row in enumerate(menuHC_SR04):
        h, w = stdscr.getmaxyx()
        x = w // 2 - len(row) // 2
        y = h // 2 - len(menuHC_SR04) // 2 + idx
        if idx == selected_menu:
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(2))
        else:
            stdscr.addstr(y, x, row)
        stdscr.addstr(h - 1, 0, "Appuie sur la touche b pour revenir en arrière !")
    stdscr.refresh()


def HC_SR04(stdscr):
    stdscr.addstr(3, 0, "Préparation du module en cours...")

    GPIO.setmode(GPIO.BOARD)

    TRIG = 7
    ECHO = 11

    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.output(TRIG, GPIO.LOW)

    time.sleep(2)
    key = stdscr.getch()
    while 1:
        time.sleep(1)

        GPIO.output(TRIG, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(TRIG, GPIO.LOW)

        while GPIO.input(ECHO) == 0:
            ultrason = time.time()

        while GPIO.input(ECHO) == 1:
            retour_ultrason = time.time()

        distance = round((retour_ultrason - ultrason) * 340 * 100 / 2, 2)
        stdscr.addstr(5, 0, "La distance est de {} cm".format(distance))
        if key == ord('e'):
            GPIO.cleanup()
            break
        stdscr.refresh()


def main(stdscr):
    curses.echo()
    signal.signal(signal.SIGINT, signal_handler)

    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
    current_menu = 0

    print_menu(stdscr, current_menu)

    while 1:
        Title(stdscr)
        key = stdscr.getch()
        stdscr.clear()
        if key == curses.KEY_UP and current_menu > 0:
            current_menu -= 1
        elif key == curses.KEY_DOWN and current_menu < len(menu) - 1:
            current_menu += 1
        elif key == curses.KEY_UP and current_menu == 0:
            print('\007')
        elif key == curses.KEY_DOWN and current_menu == len(menu) - 1:
            print('\007')

        elif key == curses.KEY_ENTER or key in [10, 13] and current_menu == 0:
            print_HC_SR04_menu(stdscr, current_menu)
            stdscr.addstr(0, 0, menu[current_menu])
            current_menu = 0
            while 1:
                key = stdscr.getch()
                stdscr.clear()
                if key == curses.KEY_UP and current_menu > 0:
                    current_menu -= 1
                elif key == curses.KEY_UP and current_menu == 0:
                    print('\007')
                    print_HC_SR04_menu(stdscr, current_menu)

                elif key == curses.KEY_DOWN and current_menu < len(menuHC_SR04) - 1:
                    current_menu += 1

                elif key == curses.KEY_DOWN and current_menu == len(menuHC_SR04) - 1:
                    print('\007')
                elif key == curses.KEY_ENTER or key in [10, 13] and current_menu == 0:
                    stdscr.clear()
                    stdscr.addstr(0, 0, menuHC_SR04[current_menu])
                    HC_SR04(stdscr)
                elif key == ord('b'):
                    break
                else:
                    print('\007')
                print_HC_SR04_menu(stdscr, current_menu)
                stdscr.addstr(0, 0, menu[current_menu])
                stdscr.refresh()

        elif key == curses.KEY_ENTER or key in [10, 13] and current_menu == 1:
            stdscr.clear()
            stdscr.addstr(0, 0, menu[current_menu])
            stdscr.refresh()
            stdscr.getch()


        elif key == curses.KEY_ENTER or key in [10, 13] and current_menu == 2:
            stdscr.clear()
            stdscr.addstr(0, 0, menu[current_menu])
            stdscr.refresh()
            stdscr.getch()


        elif key == ord('q'):
            exit(1)

        else:
            print('\007')

        print_menu(stdscr, current_menu)
        stdscr.refresh()


curses.wrapper(main)
