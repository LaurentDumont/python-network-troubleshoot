from scapy.all import get_if_hwaddr, conf, Ether, IP, UDP, TCP, BOOTP, DHCP, RandInt, srp1


def get_dhcp_offer(interface_name):
    conf.checkIPaddr=False
    # Select correct interface.
    interface = interface_name
    localmac = get_if_hwaddr(interface)
    # Create DHCP DISCOVER packet
    dhcp_discover = Ether(src=localmac, dst='ff:ff:ff:ff:ff:ff')/IP(src='0.0.0.0', dst='255.255.255.255')/UDP(dport=67, sport=68)/BOOTP(chaddr="8c859039f517",xid=RandInt())/DHCP(options=[('message-type', 'discover'), 'end'])
    # Send DISCOVER packet and wait for OFFER packet.
    dhcp_offer = srp1(dhcp_discover,iface=interface, verbose=False)
    return dhcp_offer


def parse_dhcp_options(dhcp_offer):
    dhcp_options_dict = {'server_id': '',
                    'lease_time': '',
                    'subnet_mask': '',
                    'router': '',
                    'name_server': [],
                    'domain': '',
    }
    
    for option in dhcp_offer[DHCP].options:
      if option[0] in dhcp_options_dict:
        if option[0] == 'name_server':
          #Skip the first element of the list which is 'name_server' - we just want to IP addresses of the name servers.
          for element in option[1:]:
            dhcp_options_dict['name_server'].append(element)
          dhcp_options_dict['name_server'] = list_dns_servers
        if option[0] == 'domain':
          dhcp_options_dict['domain'] = option[1].decode('utf-8')
        else:
          dhcp_options_dict[option[0]] = option[1]
    
        return parsed_dhcp_options


def parse_dhcp_server_ip(dhcp_offer):
    dhcp_server_ip = dhcp_offer[Ether][DHCP].options[1][1]
    return dhcp_server_ip


def parse_lease_time(dhcp_offer):
    lease_time = dhcp_offer[Ether][DHCP].options[2][1]
    #DHCP lease is in seconds. Return the value in minutes.
    lease_time = lease_time/60
    return lease_time


def parse_dhcp_domain_name(dhcp_offer):
    try:
      domain_name = dhcp_offer[Ether][DHCP].options[8][1].decode("utf-8")
      return domain_name
    except:
      return None


def parse_dns_servers(dhcp_offer):
    #For brievity, we only get the first two DNS servers specified. Up to 4 can be sent by the DHCP server.
    try:
      dns = dhcp_offer[Ether][DHCP].options[5]
      dns_servers = []
      dns_servers.extend([dns[1], dns[2]])
      return dns_servers
    except:
      return "NOT FOUND"

