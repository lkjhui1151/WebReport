from unittest import result


data = [
    {
        "Risk": "Medium",
        "Host": "192.168.81.246",
        "Name": "SSL Self-Signed Certificate",
        "Port": "443",
        "Group": "ESXi Host"
    },
    {
        "Risk": "None",
        "Host": "192.168.83.246",
        "Name": "SSL Cipher Block Chaining Cipher Suites Supported",
        "Group": "ESXi Host",
        "Group": "ESXi Host"
    },
    {
        "Risk": "Medium",
        "Host": "192.168.81.246",
        "Name": "SSL Self-Signed Certificate",
        "Port": "80",
        "Group": "ESXi Host"
    },
    {
        "Risk": "Medium",
        "Host": "192.168.81.246",
        "Name": "SSL Self-Signed Certificate",
        "Port": "80",
        "Group": "ESXi Host"
    }
]

data = [dict(t) for t in {tuple(d.items()) for d in data}]
# newlist = sorted(data, key=lambda d: d['Host'].split("."))

for i in data:
    print(i)

# print(newlist)
# seen = set()
# new_l = []
# for d in data:
#     t = tuple(d.items())
#     if t not in seen:
#         seen.add(t)
#         new_l.append(d)

# print(new_l)
