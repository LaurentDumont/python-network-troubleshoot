#Standard Libraries imports
import json
import curses
import threading
import time

#Third party libraries
import pingparsing
import requests


class StartPing(object):
    def __init__(self):
        self.target = 'google.com'
        self.ping_count = 2

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
            time.sleep(5)


class GetPublicAddress(object):
    def __init__(self):
        self.message = 'Message'

    def get_external_ip_address(self):
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



def gui(stdscr):
    stdscr.addstr('Dreamhack Monitoring Tool \n')
    ping_thread = threading.Thread(target=StartPing.ping)
    #public_ip_thread = threading.Thread(target=GetPublicAddress.get_external_ip_address)
    ping_thread.setDaemon(True)
    #public_ip_thread.setDaemon(True)
    ping_thread.start()
    #public_ip_thread.start()
    stdscr.refresh()
    stdscr.clear()
    

def main():
    curses.wrapper(gui)


if __name__ == "__main__":
    main()
