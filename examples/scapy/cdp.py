C:\RH>python
Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 27 2018, 04:59:51) [MSC v.1914 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> #! /usr/bin/env python
... from scapy.all import *
>>> load_contrib("cdp")
>>>
>>> def cdp_monitor_callback(pkt):
...   ip = "0.0.0.0"
...   if (CDPMsgDeviceID in pkt):
...     device=pkt["CDPMsgDeviceID"].val.decode()
...     hostname=device.split(".")[0]
...     if (CDPAddrRecordIPv4 in pkt):
...       ip=pkt["CDPAddrRecordIPv4"].addr
...     return "Device: {0} IP: {1}".format(hostname,ip)
...
>>> interface="VirtualBox Host-Only Ethernet Adapter"
>>> capturefilter="ether dst 01:00:0c:cc:cc:cc"
>>>
>>> # run it for max. 99 Packets
... p=sniff(prn=cdp_monitor_callback, iface=interface, count=99, filter=capturefilter, store=0)