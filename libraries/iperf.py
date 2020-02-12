import iperf3
import subprocess
import json


TARGET = 'perf.laurentdumont.ca'
DURATION = '15'
ERROR_MESSAGE = 'NOT FOUND'
PERFORMANCE_PI = 'Raspberry Pi 4 Model B Rev 1.1'


def convert_bits(value):
    value = value / 1000 / 1000
    return int(value)

def perf_test_enabled():
    # Only the Rasp Pi 4 Models can do an iPerf test with good results. Pi 2/3 will not run the test.
    try:
        with open("/proc/cpuinfo") as search:
            for line in search:
                line = line.rstrip()  # remove '\n' at end of line
                if "Model" in line:
                    pi_model = line.split(':')
                    # Remove the beginning space only
                    pi_model = pi_model[1].strip()
    except Exception as e:
        pi_model = e

    if pi_model != PERFORMANCE_PI:
        return False
    return True


def download_test():
  try:
    process = subprocess.Popen(['iperf3', '-O', '2', '--time', DURATION, '--json', '--reverse', '--client', TARGET],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    results_json = json.loads(stdout)
    download_speed = results_json['end']['sum_received']['bits_per_second']
    download_speed = convert_bits(download_speed)
  except Exception as e:
    download_speed = e
  
  return download_speed
