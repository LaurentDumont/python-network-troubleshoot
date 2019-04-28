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
                ping_win_section.addstr('Ping statistics for {}: \n'.format(self.target))
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

    def __init__(self, stdscr):
        super(PublicAddress, self).__init__()
        self._target=self.GetPublicAddress
        self.daemon = True
        self.stdscr = stdscr
        self.start()

    def GetPublicAddress(self):
        begin_x = 70; begin_y = 0
        height = 5; width = 50
        public_ip_win_section = curses.newwin(height, width, begin_y, begin_x)
        while True:
           try:
               public_ip_data = requests.get('https://api.ipify.org?format=json')
               public_ip_json = json.loads(public_ip_data.text)
               public_ip_only = public_ip_json['ip']
               public_ip_win_section.addstr('Getting public IP address : \n')
               public_ip_win_section.addstr(public_ip_only)
               public_ip_win_section.refresh()
               public_ip_win_section.clear()
               time.sleep(10)
           except:
               continue


def run(stdscr):

    curses.curs_set(0)
    Ping(stdscr)
    PublicAddress(stdscr)

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
    stdscr.addstr('Something went wrong')
    curses.endwin()