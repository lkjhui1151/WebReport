import csv
context = {}

with open('./A2.csv', encoding="utf8") as read_f:
    reader = csv.DictReader(read_f, delimiter=',')
    for row in reader:
        if row['Group'] in context:
            if not row['Host'] in context[row['Group']]:
                context[row['Group']][row['Host']] = {"Critical":0 ,"High":0,"Medium":0,"Low":0,"Summary":0}
        else :
            context[row['Group']]={row['Host']:{"Critical":0 ,"High":0,"Medium":0,"Low":0,"Summary":0}}


        if row['Risk']!="None":
            if row['Risk'] == "Critical":
                    context[row['Group']][row['Host']]["Critical"]+=1
            elif row['Risk'] == "High":
                context[row['Group']][row['Host']]["High"]+=1
            elif row['Risk'] == "Medium":
                context[row['Group']][row['Host']]["Medium"]+=1
            elif row['Risk'] == "Low":
                context[row['Group']][row['Host']]["Low"]+=1
            context[row['Group']][row['Host']]["Summary"]=context[row['Group']][row['Host']]["Critical"]+context[row['Group']][row['Host']]["High"]+context[row['Group']][row['Host']]["Medium"]+context[row['Group']][row['Host']]["Low"]

print(context)