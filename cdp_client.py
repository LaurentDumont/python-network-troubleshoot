from scapy.all import *

load_contrib('cdp')
cdp_packet = sniff(iface='eno1', count=1, filter='ether dst 01:00:0c:cc:cc:cc', store=1)
device_name = cdp_packet[0]["CDPMsgDeviceID"].val.decode()
port_name = cdp_packet[0]["CDPMsgPortID"].iface.decode()
platform_version = cdp_packet[0]["CDPMsgPlatform"].val.decode()
software_version = cdp_packet[0]["CDPMsgSoftwareVersion"].val.decode()
#Is 0 for half and 1 for full duplex.
duplex_status = cdp_packet[0]["CDPMsgDuplex"].duplex
primary_vlan = cdp_packet[0]["CDPMsgNativeVLAN"].vlan
vlan = cdp_packet[0]["CDPMsgNativeVLAN"].vlan
management_ip_address = cdp_packet[0]["CDPAddrRecordIPv4"].addr
