""" Standard Libraries imports """

import curses
import time
import threading
import json
import requests
import socket
import struct
from libraries.dhcp_client import *
from libraries.cdp_client import *
from libraries.network_interface_client import *
from libraries.iperf import *
import argparse

""" Third party libraries """

import pingparsing


class Ping(threading.Thread):
    """ Ping a target and return some statistics. """

    def __init__(self):
        self.target = 'perf.laurentdumont.ca'
        self.ok_message = 'AVG PING IS OK'
        self.notok_message = 'AVG PING IS NOT OK'
        self.ping_count = 2
        super(Ping, self).__init__()
        self._target=self.ping
        self.daemon = True
        self.start()

    def ping(self):
        begin_x = 0; begin_y = 0
        height = 8; width = 40
        ping_win_section = curses.newwin(height, width, begin_y, begin_x)
        while True:
            try:
                ping_parser = pingparsing.PingParsing()
                transmitter = pingparsing.PingTransmitter()
                transmitter.destination_host = self.target
                transmitter.count = self.ping_count
                ping_result = transmitter.ping()
                ping_result_json = json.loads(json.dumps(ping_parser.parse(ping_result).as_dict()))
                ping_win_section.addstr('Ping : {}: \n'.format(self.target), curses.A_STANDOUT)
                ping_win_section.addstr('Round Trip Time Minimum is : {} ms\n'.format(str(ping_result_json['rtt_min'])))
                ping_win_section.addstr('Round Trip Time Maximum is : {} ms\n'.format(str(ping_result_json['rtt_max'])))
                ping_win_section.addstr('Round Trip Time Average is : {} ms\n'.format(str(ping_result_json['rtt_avg'])))
                if ping_result_json['packet_loss_rate'] > 10:
                    ping_win_section.addstr('Average packet loss : {} \n'.format(str(ping_result_json['packet_loss_rate'])))
                else:
                    ping_win_section.addstr('Average packet loss : {} \n'.format(str(ping_result_json['packet_loss_rate'])), curses.color_pair(2))
                if ping_result_json['rtt_avg'] < 60:
                  ping_win_section.addstr(self.ok_message, curses.color_pair(2))
                else:
                  ping_win_section.addstr(self.notok_message, curses.color_pair(1))
                ping_win_section.refresh()
                ping_win_section.clear()
                time.sleep(2)
            except: 
                continue


class IpAddress(threading.Thread):
    """ Get the current IP address of the device """
    def __init__ (self, interface_name):
        super(IpAddress, self).__init__()
        self._target=self.GetIpAddress
        self.daemon = True
        self.interface_name = interface_name
        self.start()

    def GetIpAddress(self):
        begin_x = 43; begin_y = 0
        height = 30; width = 50
        ip_window = curses.newwin(height, width, begin_y, begin_x)
        while True:
            #Internal IP address
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("google.ca", 80))
            current_internal_ip  = s.getsockname()[0]
            ip_window.addstr('Internal IP: \n', curses.A_STANDOUT)
            ip_window.addstr('{}\n'.format(str(current_internal_ip)))
            #External IP address
            public_ip_data = requests.get('https://api.ipify.org?format=json')
            public_ip_json = json.loads(public_ip_data.text)
            public_ip_only = public_ip_json['ip']
            ip_window.addstr('Public IP address: \n', curses.A_STANDOUT)
            ip_window.addstr('{}\n'.format(public_ip_only))
            ip_window.addstr('Default Gateway: \n', curses.A_STANDOUT)
            #Default gateway
            with open("/proc/net/route") as fh:
                for line in fh:
                    fields = line.strip().split()
                    if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                        continue
                    def_gw = socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))
            ip_window.addstr('{}\n'.format(def_gw))
            dhcp_offer = get_dhcp_offer(self.interface_name)
            dhcp_options = parse_dhcp_options(dhcp_offer)
            #DNS Servers
            ip_window.addstr('DNS Servers: \n', curses.A_STANDOUT)
            for server in dhcp_options['name_server']:
                ip_window.addstr('{}\n'.format(server))
            lease_time = dhcp_options['lease_time']
            dhcp_server_ip = dhcp_options['server_id']
            dhcp_domain_name = dhcp_options['domain']
            ip_window.addstr('DHCP lease time: \n', curses.A_STANDOUT)
            ip_window.addstr(str(lease_time) + ' Minutes\n')
            ip_window.addstr('DHCP Server IP: \n', curses.A_STANDOUT)
            ip_window.addstr(str(dhcp_server_ip) + '\n')
            ip_window.addstr('DHCP Domain name: \n', curses.A_STANDOUT)
            ip_window.addstr(str(dhcp_domain_name) + '\n')
            #interface_speed = get_interface_speed(self.interface_name)
            #ip_window.addstr('Interface speed: \n', curses.A_STANDOUT)
            #if interface_speed == 'NOT FOUND':
            #  ip_window.addstr(str(interface_speed) + '\n', curses.color_pair(1))
            #ip_window.addstr(str(interface_speed) + '\n', curses.color_pair(3))
            ip_window.refresh()
            ip_window.clear()
            time.sleep(10)



class CdpInformation(threading.Thread):
    """ Get CDP information from remote Cisco equipment. """
    def __init__ (self, interface_name):
        super(CdpInformation, self).__init__()
        self._target=self.GetCDPInformation
        self.daemon = True
        self.interface_name = interface_name
        self.start()

    def get_color_highlight(self, string):
        if string == 'NOT FOUND':
          return 1
        return 3

    def GetCDPInformation(self):
        begin_x = 0; begin_y = 8
        height = 30; width = 30
        cdp_window = curses.newwin(height, width, begin_y, begin_x)
        cdp_packet = get_cdp_packet(self.interface_name)
        while True:
            try:
                cdp_window.addstr('CDP Information: \n', curses.A_STANDOUT)
                cdp_packet = get_cdp_packet(self.interface_name)
                cdp_device_name = get_cdp_device_name(cdp_packet)
                cdp_switchport = get_cdp_port_name(cdp_packet)
                cdp_platform = get_cdp_platform_version(cdp_packet)
                cdp_platform_software = get_cdp_software_version(cdp_packet)
                cdp_duplex = get_cdp_duplex(cdp_packet)
                cdp_vlan = get_cdp_vlan(cdp_packet)
                cdp_management_address = get_cdp_management_address(cdp_packet)
                cdp_window.addstr('Device Name: \n', curses.A_STANDOUT)
                cdp_window.addstr(cdp_device_name + '\n', curses.color_pair(CdpInformation.get_color_highlight(self, cdp_device_name)))
                cdp_window.addstr('Switchport: \n', curses.A_STANDOUT)
                cdp_window.addstr(cdp_switchport + ' | ' + cdp_duplex + '\n', curses.color_pair(CdpInformation.get_color_highlight(self, cdp_switchport)))
                cdp_window.addstr('Switch model: \n', curses.A_STANDOUT)
                cdp_window.addstr(cdp_platform + '\n', curses.color_pair(CdpInformation.get_color_highlight(self, cdp_platform)))
                cdp_window.addstr('Switch version: \n', curses.A_STANDOUT)
                cdp_window.addstr(cdp_platform_software + '\n', curses.color_pair(CdpInformation.get_color_highlight(self, cdp_platform_software)))
                cdp_window.addstr('Switchport VLAN: \n', curses.A_STANDOUT)
                cdp_window.addstr(str(cdp_vlan) + ' | ' + str(cdp_management_address) + '\n', curses.color_pair(CdpInformation.get_color_highlight(self, cdp_vlan)))
                #cdp_window.addstr('Switch MGMT IP:' +, curses.A_STANDOUT)
                #cdp_window.addstr(cdp_management_address+ '\n', curses.color_pair(CdpInformation.get_color_highlight(self, cdp_management_address)))
                cdp_window.refresh()
                cdp_window.clear()
                time.sleep(300)
            except:
                continue


class Iperf(threading.Thread):
    """ Run a reverse Iperf test towards a target """

    def __init__(self):
        super(Iperf, self).__init__()
        self._target=self.iperf
        self.daemon = True
        self.start()

    def iperf(self):
        begin_x = 43; begin_y = 18
        height = 8; width = 100
        iperf_win_section = curses.newwin(height, width, begin_y, begin_x)
        while True and perf_test_enabled():
            try:           
                iperf_win_section.addstr('Download speed \n', curses.A_STANDOUT)
                download_speed = download_test()
                iperf_win_section.addstr(str(download_speed) + ' Mbps \n')
                iperf_win_section.refresh()
                iperf_win_section.clear()
                time.sleep(30)
            except:
                continue


def run(stdscr):
    curses.curs_set(0)
    parser = argparse.ArgumentParser(description='Network troubleshooting script.')
    parser.add_argument('interface_name', metavar='interface_name', type=str, help='Interface name for DHCP and CDP packet generators.')
    args = parser.parse_args()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    interface_name = args.interface_name
    Ping()
    IpAddress(interface_name)
    CdpInformation(interface_name)
    Iperf()

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
