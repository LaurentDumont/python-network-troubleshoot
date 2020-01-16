import argparse

parser = argparse.ArgumentParser(description='Network troubleshooting script.')
parser.add_argument('interface_name', metavar='interface_name', type=str, help='Interface name for DHCP and CDP packet generators.')
args = parser.parse_args()
print(args)
print(args.accumulate(args.interface_name))
