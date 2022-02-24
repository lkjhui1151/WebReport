from unittest import result


data = [
    {
        "Risk": "Medium",
        "Host": "192.168.8.246",
        "Name": "SSL Self-Signed Certificate",
        "Group": "ESXi Host"
    },
    {
        "Risk": "None",
        "Host": "192.168.8.246",
        "Name": "SSL Cipher Block Chaining Cipher Suites Supported",
        "Group": "ESXi Host"
    },
    {
        "Risk": "Medium",
        "Host": "192.168.8.246",
        "Name": "SSL Self-Signed Certificate",
        "Group": "ESXi Host"
    },
]

# data = [dict(t) for t in {tuple(d.items()) for d in data}]
seen = set()
new_l = []
for d in data:
    t = tuple(d.items())
    if t not in seen:
        seen.add(t)
        new_l.append(d)

print(new_l)
