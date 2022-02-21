import csv

with open('D:/github/WebReport/test code/A2.csv', encoding="utf8") as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        name = row['Group']
        print(name)
