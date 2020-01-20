import os
import re

def get_interface_speed(interface_name):
  interface_output_stream = os.popen('ethtool '+interface_name+' | grep "Speed:"')
  interface_output = interface_output_stream.read()
  interface_speed = re.findall('\d+', interface_output)
  if interface_speed != '1000' or '100' or '10':
    interface_speed = 'NOT FOUND'
  return interface_speed
