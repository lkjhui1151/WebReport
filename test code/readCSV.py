import csv

file = open("D:/github/WebReport/test code/A2.csv", "r")
csv_file = csv.reader(file)

for row in csv_file:
    # lists_from_csv.append(row)
    print(row)
