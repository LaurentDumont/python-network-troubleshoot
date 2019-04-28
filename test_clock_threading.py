#!/usr/bin/python3

import curses
import time
import threading
import pingparsing
import json


class Ping(threading.Thread):
    """ Clock curses string class. Updates every second. Easy to install """

    def __init__(self, stdscr, show_seconds=True):
        """ Create the clock """
        self.target = 'google.com'
        self.ping_count = 2
        super(Ping, self).__init__()
        self._target=self.ping
        self.daemon = True
        self.stdscr = stdscr
        self.start()

    def ping(self):
        """ If seconds are showing, update the clock each second """
        while True: 
            ping_parser = pingparsing.PingParsing()
            transmitter = pingparsing.PingTransmitter()
            transmitter.destination_host = self.target
            transmitter.count = self.ping_count
            ping_result = transmitter.ping()
            ping_result_json = json.loads(json.dumps(ping_parser.parse(ping_result).as_dict()))
            begin_x = 0; begin_y = 0
            height = 5; width = 40
            ping_win_section = curses.newwin(height, width, begin_y, begin_x)
            ping_win_section.addstr('Ping statistics : \n')
            ping_win_section.addstr('Round Trip Time Average is : {} \n'.format(str(ping_result_json['rtt_avg'])))
            ping_win_section.addstr('Round Trip Time Average is : {} \n'.format(str(ping_result_json['rtt_avg'])))
            ping_win_section.refresh()
            ping_win_section.clear()
            time.sleep(5)



def run(stdscr):
    
    ping = Ping(stdscr)

    # End with any key

    while 1:
        event = stdscr.getch()
        break


if __name__=="__main__":
    stdscr = curses.initscr()
    curses.wrapper(run)