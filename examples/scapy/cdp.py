"""

https://github.com/secdev/scapy/blob/master/scapy/contrib/cdp.py

print(p[0].display())
###[ 802.3 ]### 
  dst       = 01:00:0c:cc:cc:cc
  src       = 00:21:1c:37:e8:14
  len       = 466
###[ LLC ]### 
     dsap      = 0xaa
     ssap      = 0xaa
     ctrl      = 3
###[ SNAP ]### 
        OUI       = 0xc
        code      = 0x2000
###[ Cisco Discovery Protocol version 2 ]### 
           vers      = 2
           ttl       = 180
           cksum     = 0x7f7a
           \msg       \
            |###[ Device ID ]### 
            |  type      = Device ID
            |  len       = 21
            |  val       = 'gin.cmaker.studio'
            |###[ Software Version ]### 
            |  type      = Software Version
            |  len       = 248
            |  val       = 'Cisco IOS Software, C2960 Software (C2960-LANBASEK9-M), Version 15.0(2)SE11, RELEASE SOFTWARE (fc3)\nTechnical Support: http://www.cisco.com/techsupport\nCopyright (c) 1986-2017 by Cisco Systems, Inc.\nCompiled Sat 19-Aug-17 09:34 by prod_rel_team'
            |###[ Platform ]### 
            |  type      = Platform
            |  len       = 26
            |  val       = 'cisco WS-C2960G-48TC-L'
            |###[ Addresses ]### 
            |  type      = Addresses
            |  len       = 17
            |  naddr     = 1
            |  \addr      \
            |   |###[ CDP Address IPv4 ]### 
            |   |  ptype     = NLPID
            |   |  plen      = 1
            |   |  proto     = '\xcc'
            |   |  addrlen   = 4
            |   |  addr      = 10.10.69.10
            |###[ Port ID ]### 
            |  type      = Port ID
            |  len       = 23
            |  iface     = 'GigabitEthernet0/20'
            |###[ Capabilities ]### 
            |  type      = Capabilities
            |  len       = 8
            |  cap       = Switch+IGMPCapable
            |###[ Protocol Hello ]### 
            |  type      = Protocol Hello
            |  len       = 36
            |  oui       = 0xc
            |  protocol_id= 0x112
            |  data      = '\x00\x00\x00\x00\xff\xff\xff\xff\x01\x02!\xff\x00\x00\x00\x00\x00\x00\x00!\x1c7\xe8\x00\xff\x00\x00'
            |###[ VTP Management Domain ]### 
            |  type      = VTP Management Domain
            |  len       = 4
            |  val       = ''
            |###[ Native VLAN ]### 
            |  type      = Native VLAN
            |  len       = 6
            |  vlan      = 210
            |###[ Duplex ]### 
            |  type      = Duplex
            |  len       = 5
            |  duplex    = Full
            |###[ VoIP VLAN Reply ]### 
            |  type      = VoIP VLAN Reply
            |  len       = 7
            |  status?   = 1
            |  vlan      = 211
            |###[ Trust Bitmap ]### 
            |  type      = Trust Bitmap
            |  len       = 5
            |  trust_bitmap= 0x0
            |###[ Untrusted Port CoS ]### 
            |  type      = Untrusted Port CoS
            |  len       = 5
            |  untrusted_port_cos= 0x0
            |###[ Management Address ]### 
            |  type      = Management Address
            |  len       = 17
            |  naddr     = 1
            |  \addr      \
            |   |###[ CDP Address IPv4 ]### 
            |   |  ptype     = NLPID
            |   |  plen      = 1
            |   |  proto     = '\xcc'
            |   |  addrlen   = 4
            |   |  addr      = 10.10.69.10
            |###[ CDP Generic Message ]### 
            |  type      = Power Available
            |  len       = 16
            |  val       = '\x00\x00\x00\x01\x00\x00\x00\x00\xff\xff\xff\xff'
            |###[ CDP Generic Message ]### 
            |  type      = 0x1f
            |  len       = 5
            |  val       = '\x00'
            |###[ CDP Generic Message ]### 
            |  type      = 0x1003
            |  len       = 5
            |  val       = '1'

"""

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
