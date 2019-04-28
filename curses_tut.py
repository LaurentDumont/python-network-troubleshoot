from curses import wrapper

def main(stdscr):
    # Clear screen
    stdscr.clear()
    stdscr.addstr('test')
    stdscr.refresh()
    stdscr.getkey()

wrapper(main)