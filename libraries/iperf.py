import iperf3
import subprocess
import json


TARGET = 'perf.laurentdumont.ca'
DURATION = 5
ERROR_MESSAGE = 'NOT FOUND'

def upload_test():
  try:
    client = iperf3.Client()
    client.server_hostname = TARGET
    client.duration = DURATION
    result = client.run()
    upload_result = result.sent_Mbps
  except:
    upload_result = ERROR_MESSAGE
  
  return upload_result

def download_test():
  try:
    process = subprocess.Popen(['iperf3', '--time', '15', '--json', '--reverse', '--client', 'perf.laurentdumont.ca'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    results_json = json.loads(stdout)
    download_speed = results_json['end']['streams'][0]['sender']['bits_per_second']
  except Exception as e:
    download_speed = e
  
  return download_speed
