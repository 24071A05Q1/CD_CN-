import os

commands = ["ipconfig", "ping google.com",
            "tracert google.com", "netstat", "arp -a","hostname","nslookup","getmac","route print -4","pathping"]

for cmd in commands:
    print("\n", cmd)
    os.system(cmd)
