from scapy.all import get_if_hwaddr, conf, Ether, IP, UDP, TCP, BOOTP, DHCP, RandInt, srp1 

conf.checkIPaddr=False

# configuration
interface = 'wlp3s0'
localmac = get_if_hwaddr(interface)

# craft DHCP DISCOVER
dhcp_discover = Ether(src=localmac, dst='ff:ff:ff:ff:ff:ff')/IP(src='0.0.0.0', dst='255.255.255.255')/UDP(dport=67, sport=68)/BOOTP(chaddr="8c859039f517",xid=RandInt())/DHCP(options=[('message-type', 'discover'), 'end'])

# send discover, wait for reply
dhcp_offer = srp1(dhcp_discover,iface=interface)
dns = dhcp_offer[Ether][DHCP].options
for element in dns:
  print(element)
