""" Standard Libraries imports """

import curses
import time
import threading
import json
import requests
import socket


""" This party libraries """

import pingparsing


class IpAddress(threading.Thread):
    """ Get the current IP address of the device """
    def __init__ (self):
        super(IpAddress, self).__init__()
        self._target=self.GetIpAddress
        self.daemon = True
        self.start()


    def GetIpAddress(self):
        begin_x = 110; begin_y = 0
        height = 5; width = 50
        internal_ip_window = curses.newwin(height, width, begin_y, begin_x)
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                current_internal_ip  = s.getsockname()[0]
                internal_ip_window.addstr('Internal IP :\n', curses.A_STANDOUT)
                internal_ip_window.addstr('{}'.format(current_internal_ip))
                internal_ip_window.refresh()
                internal_ip_window.clear()
                time.sleep(10)
            except:
                continue


class Ping(threading.Thread):
    """ Ping a target and return some statistics. """

    def __init__(self):
        self.target = 'google.com'
        self.ping_count = 2
        super(Ping, self).__init__()
        self._target=self.ping
        self.daemon = True
        self.start()

    def ping(self):
        begin_x = 0; begin_y = 0
        height = 10; width = 50
        ping_win_section = curses.newwin(height, width, begin_y, begin_x)
        while True:
            try:
                ping_parser = pingparsing.PingParsing()
                transmitter = pingparsing.PingTransmitter()
                transmitter.destination_host = self.target
                transmitter.count = self.ping_count
                ping_result = transmitter.ping()
                ping_result_json = json.loads(json.dumps(ping_parser.parse(ping_result).as_dict()))
                ping_win_section.addstr('Ping statistics for {}: \n'.format(self.target), curses.A_STANDOUT)
                ping_win_section.addstr('Round Trip Time Minimum is : {} ms\n'.format(str(ping_result_json['rtt_min'])))
                ping_win_section.addstr('Round Trip Time Maximum is : {} ms\n'.format(str(ping_result_json['rtt_max'])))
                ping_win_section.addstr('Round Trip Time Average is : {} ms\n'.format(str(ping_result_json['rtt_avg'])))
                ping_win_section.addstr('Average packet loss : {} \n'.format(str(ping_result_json['packet_loss_rate'])))
                ping_win_section.refresh()
                ping_win_section.clear()
                time.sleep(2)
            except: 
                continue


class PublicAddress(threading.Thread):
    """ Get the public address of the device where the script is running. """

    def __init__(self):
        super(PublicAddress, self).__init__()
        self._target=self.GetPublicAddress
        self.daemon = True
        self.start()

    def GetPublicAddress(self):
        begin_x = 50; begin_y = 0
        height = 5; width = 50
        public_ip_win_section = curses.newwin(height, width, begin_y, begin_x)
        while True:
            try:
                public_ip_data = requests.get('https://api.ipify.org?format=json')
                public_ip_json = json.loads(public_ip_data.text)
                public_ip_only = public_ip_json['ip']
                public_ip_win_section.addstr('Getting public IP address : \n', curses.A_STANDOUT)
                public_ip_win_section.addstr(public_ip_only)
                public_ip_win_section.refresh()
                public_ip_win_section.clear()
                time.sleep(10)
            except:
               continue


def run(stdscr):

    curses.curs_set(0)
    Ping()
    PublicAddress()
    IpAddress()

    # End with any key

    while True:
        key_press = stdscr.getch()
        if key_press != curses.KEY_RESIZE:
            curses.endwin()
            break
        else:
            continue


if __name__ == "__main__":
    stdscr = curses.initscr()
    curses.wrapper(run)
    curses.endwin()