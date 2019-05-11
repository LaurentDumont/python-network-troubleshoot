from scapy.all import get_if_hwaddr, conf, Ether, IP, UDP, TCP, BOOTP, DHCP, RandInt, srp1


def get_dhcp_offer():
    conf.checkIPaddr=False
    # Select correct interface.
    interface = 'wlp3s0'
    localmac = get_if_hwaddr(interface)
    # Create DHCP DISCOVER packet
    dhcp_discover = Ether(src=localmac, dst='ff:ff:ff:ff:ff:ff')/IP(src='0.0.0.0', dst='255.255.255.255')/UDP(dport=67, sport=68)/BOOTP(chaddr="8c859039f517",xid=RandInt())/DHCP(options=[('message-type', 'discover'), 'end'])
    # Send DISCOVER packet and wait for OFFER packet.
    dhcp_offer = srp1(dhcp_discover,iface=interface, verbose=False)
    return dhcp_offer


def parse_dhcp_server_ip(dhcp_offer):
    dhcp_server_ip = dhcp_offer[Ether][DHCP].options[1][1]
    return dhcp_server_ip


def parse_lease_time(dhcp_offer):
    lease_time = dhcp_offer[Ether][DHCP].options[2][1]
    #DHCP lease is in seconds. Return the value in minutes.
    lease_time = lease_time/60
    return lease_time


def parse_dhcp_domain_name(dhcp_offer):
    domain_name = dhcp_offer[Ether][DHCP].options[8][1].decode("utf-8")
    return domain_name