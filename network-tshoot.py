#!/usr/bin/python3

import curses
import time
import threading
import pingparsing
import json
import requests


class Ping(threading.Thread):
    """ Ping curses class. Ping a target and return some data."""

    def __init__(self, stdscr):
        self.target = 'google.com'
        self.ping_count = 2
        super(Ping, self).__init__()
        self._target=self.ping
        self.daemon = True
        self.stdscr = stdscr
        self.start()

    def ping(self):
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
            time.sleep(2)

class PublicAddress(threading.Thread):

    def __init__(self, stdscr):
        super(PublicAddress, self).__init__()
        self._target=self.GetPublicAddress
        self.daemon = True
        self.stdscr = stdscr
        self.start()

    def GetPublicAddress(self):
        while True:
            begin_x = 50; begin_y = 0
            height = 5; width = 40
            public_ip_data = requests.get('https://api.ipify.org?format=json')
            public_ip_json = json.loads(public_ip_data.text)
            public_ip_only = public_ip_json['ip']
            public_ip_win_section = curses.newwin(height, width, begin_y, begin_x)
            public_ip_win_section.addstr('Getting public IP address : \n')
            public_ip_win_section.addstr(public_ip_only)
            public_ip_win_section.refresh()
            public_ip_win_section.clear()
            time.sleep(10)


def run(stdscr):

    ping = Ping(stdscr)
    public_address = PublicAddress(stdscr)

    # End with any key

    while 1:
        event = stdscr.getch()
        break


if __name__=="__main__":
    stdscr = curses.initscr()
    curses.wrapper(run)