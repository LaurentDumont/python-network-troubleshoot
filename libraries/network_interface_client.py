import os
import re

def get_interface_speed(interface_name):
  interface_output_stream = os.popen('sudo ethtool '+interface_name+' | grep "Speed:"')
  interface_output = interface_output_stream.read()
  interface_speed = re.findall('\d+', interface_output)
  interface_speeds = ['10', '100', '1000']
  local_speed = interface_speed[0]
  if local_speed in interface_speeds:
     return local_speed
  else:
     return "NOT FOUND"
