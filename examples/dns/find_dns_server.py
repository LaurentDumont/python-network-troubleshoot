nameservers = []
with open("/etc/resolv.conf") as dns_config_file:
    for line in dns_config_file:
        if "nameserver" in line:
            dns_server = line.split()
            nameservers.append(dns_server[1])

for x in nameservers:
    print(x)