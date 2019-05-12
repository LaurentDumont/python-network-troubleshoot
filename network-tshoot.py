""" Standard Libraries imports """

import curses
import time
import threading
import json
import requests
import socket
import struct
from dhcp_client import *
from cdp_client import *

""" Third party libraries """

import pingparsing


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
        height =7; width = 50
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


class IpAddress(threading.Thread):
    """ Get the current IP address of the device """
    def __init__ (self):
        super(IpAddress, self).__init__()
        self._target=self.GetIpAddress
        self.daemon = True
        self.start()

    def GetDnsServers(self):
        nameservers = []
        with open("/etc/resolv.conf") as dns_config_file:
            for line in dns_config_file:
                if "nameserver" in line:
                    dns_server = line.split()
                    nameservers.append(dns_server[1])
        return(nameservers)

    def GetIpAddress(self):
        begin_x = 50; begin_y = 0
        height = 20; width = 50
        ip_window = curses.newwin(height, width, begin_y, begin_x)
        while True:
            try:
                #Internal IP Address
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                current_internal_ip  = s.getsockname()[0]
                ip_window.addstr('Internal IP :\n', curses.A_STANDOUT)
                ip_window.addstr('{}\n'.format(current_internal_ip))
                #External IP Address
                public_ip_data = requests.get('https://api.ipify.org?format=json')
                public_ip_json = json.loads(public_ip_data.text)
                public_ip_only = public_ip_json['ip']
                ip_window.addstr('Public IP address: \n', curses.A_STANDOUT)
                ip_window.addstr('{}\n'.format(public_ip_only))
                #Default gateway
                with open("/proc/net/route") as fh:
                    for line in fh:
                        fields = line.strip().split()
                        if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                            continue
                        def_gw = socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))
                ip_window.addstr('Default gateway: \n', curses.A_STANDOUT)
                ip_window.addstr('{}\n'.format(def_gw))
                ip_window.addstr('DNS Servers: \n', curses.A_STANDOUT)
                dns_servers = IpAddress.GetDnsServers(self)
                for server in dns_servers:
                    ip_window.addstr('{}\n'.format(server))
                dhcp_offer = get_dhcp_offer()
                lease_time = parse_lease_time(dhcp_offer)
                dhcp_server_ip = parse_dhcp_server_ip(dhcp_offer)
                dhcp_domain_name = parse_dhcp_domain_name(dhcp_offer)
                ip_window.addstr('DHCP lease time: \n', curses.A_STANDOUT)
                ip_window.addstr(str(lease_time) + ' Minutes\n')
                ip_window.addstr('DHCP Server IP: \n', curses.A_STANDOUT)
                ip_window.addstr(str(dhcp_server_ip) + '\n')
                if dhcp_domain_name != None:
                  ip_window.addstr('DHCP Domain name: \n', curses.A_STANDOUT)
                  ip_window.addstr(str(dhcp_domain_name) + '\n')
                else:
                  ip_window.addstr('No Domain name from DHCP \n', curses.A_STANDOUT)
                ip_window.refresh()
                ip_window.clear()
                time.sleep(10)
            except:
                continue


class CdpInformation(threading.Thread):
    """ Get CDP information from remote Cisco equipment. """
    def __init__ (self):
        super(CdpInformation, self).__init__()
        self._target=self.GetCDPInformation
        self.daemon = True
        self.start()


    def GetCDPInformation(self):
        begin_x = 0; begin_y = 7
        height = 20; width = 20
        cdp_window = curses.newwin(height, width, begin_y, begin_x)
        while True:
            try:
                cdp_window.addstr('CDP Information: \n', curses.A_STANDOUT)
                cdp_packet = get_cdp_packet()
                cdp_device_name = get_cdp_device_name(cdp_packet)
                cdp_switchport = get_cdp_port_name(cdp_packet)
                #cdp_platform = get_cdp_platform_version(cdp_packet)
                #cdp_platform_software = get_cdp_software_version(cdp_packet)
                #cdp_duplex = get_cdp_duplex(cdp_packet)
                #vlan = get_cdp_vlan(cdp_packet)
                #management_address = get_cdp_management_address(cdp_packet)
                cdp_window.addstr('Device Name: \n', curses.A_STANDOUT)
                cdp_window.addstr(cdp_device_name + '\n')
                cdp_window.addstr('Switchport: \n', curses.A_STANDOUT)
                cdp_window.addstr(cdp_switchport + '\n')
                cdp_window.refresh()
                cdp_window.clear()
                time.sleep(10)
            except:
                continue


def run(stdscr):

    curses.curs_set(0)
    Ping()
    IpAddress()
    CdpInformation()

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