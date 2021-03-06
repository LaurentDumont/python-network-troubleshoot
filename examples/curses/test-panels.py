#!/usr/bin/python
from time import sleep
import curses, curses.panel

COLUMNS=40
ROWS=30

side = 60    # <
top  = 126   # ~
bottom = 95  # _

def make_panel(h,l, y,x, str):
 win = curses.newwin(h,l, y,x)
 win.erase()
 win.border(side, side,  top, bottom,    side,    side,     side,     side)
# win.box(curses.ACS_RARROW,curses.ACS_BULLET)
 win.addstr(2, 2, str)

 panel = curses.panel.new_panel(win)
 return win, panel

def test(stdscr):
 try:
  curses.curs_set(0)
 except:
  pass
#stdscr.border(left, right, top, bottom, ulcorne, urcorner, blcorner, brcorner)
# stdscr.border(side, side,  top, bottom,  side,    side,     side,     side)
# stdscr.box(124, 45)
 curses.start_color()
#                                                         
# curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
 curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
 curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
 string = "panels forever"
 stdscr.addstr(0, (COLUMNS/2-(len(string)/2)), string, curses.color_pair(1)|curses.A_BOLD)
 sleep(.5)
 stdscr.addstr(0, (COLUMNS/2-(len(string)/2)), string, curses.color_pair(2))

 win1, panel1 = make_panel(10,12, 5,5, "PANEL 1")
 win2, panel2 = make_panel(10,12, 8,8, "PANEL 2")
 curses.panel.update_panels(); stdscr.refresh()
 sleep(1)

 panel1.top(); curses.panel.update_panels(); stdscr.refresh()
 sleep(1)
 curses.flash()

 for i in range(20):
  panel2.move(8, 8+i)
  curses.panel.update_panels(); stdscr.refresh()
  sleep(0.08)

 sleep(1)

if __name__ == '__main__':
 curses.wrapper(test)