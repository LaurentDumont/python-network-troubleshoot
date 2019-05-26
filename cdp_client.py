from scapy.all import *
load_contrib('cdp')


def get_cdp_packet():
    cdp_packet = sniff(iface='eno1', count=1, filter='ether dst 01:00:0c:cc:cc:cc', store=1)
    return cdp_packet


def get_cdp_device_name(cdp_packet):
    device_name = cdp_packet[0]["CDPMsgDeviceID"].val.decode()
    return device_name


def get_cdp_port_name(cdp_packet):
    port_name = cdp_packet[0]["CDPMsgPortID"].iface.decode()
    return port_name


def get_cdp_platform_version(cdp_packet):
    platform_version = cdp_packet[0]["CDPMsgPlatform"].val.decode()
    return platform_version


def get_cdp_software_version(cdp_packet):
    software_version_long = cdp_packet[0]["CDPMsgSoftwareVersion"].val.decode()
    software_version_split_list = software_version_long.split()
    software_version_number_with_comma = software_version_split_list[7]
    software_version_only = software_version_number_with_comma.replace(',', '')
    return software_version_only


def get_cdp_duplex(cdp_packet):
    #Is 0 for half and 1 for full duplex.
    duplex_status = cdp_packet[0]["CDPMsgDuplex"].duplex
    if duplex_status == 0:
        return 'half'
    elif duplex_status == 1:
        return 'full'
    else:
        return 'Duplex status invalid'


def get_cdp_vlan(cdp_packet):
    vlan = cdp_packet[0]["CDPMsgNativeVLAN"].vlan
    return vlan


def get_cdp_management_address(cdp_packet):
    management_ip_address = cdp_packet[0]["CDPAddrRecordIPv4"].addr
    return management_ip_address