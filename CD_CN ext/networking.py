import os

commands = ["ipconfig", "ping google.com",
            "tracert google.com", "netstat", "arp -a","hostname"]

for cmd in commands:
    print("\n", cmd)
    os.system(cmd)