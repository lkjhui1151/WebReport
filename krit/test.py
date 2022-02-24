from audioop import add


ip = ['192.168.10.0', '192.167.20.0', '192.166.30.0']
host = ['192.168.10.1', '192.167.20.1', '192.168.10.2', '192.166.30.1', '192.167.20.2',
        '192.166.30.2', '192.168.10.3', '192.167.20.3', '192.166.30.3', '192.168.10.4', ]

dictlist = {}
sub_host = []
classIP = {}
total = []
hostConvert = []

for i in host:
    x = i.split('.')
    ips = x[0]+"."+x[1]+"."+x[2]+"."+"0"
    hostConvert.append(ips)

for i in hostConvert:
    if i in dictlist:
        dictlist[i] += 1
    else:
        dictlist[i] = 1


count = 0
for i in ip:
    addr = i.split('.')
    for j in host:
        sub = j.split('.')

        if addr[0] == sub[0]:

            if addr[1] == sub[1]:

                if addr[2] == sub[2]:
                    sub_host.append(j)
                    count += 1

                    if count >= dictlist[i]:

                        classIP["class"] = i
                        classIP["host"] = sub_host
                        total.append(classIP)
                        sub_host = []
                        classIP = {}
                        count = 0
                        break

print(total)
