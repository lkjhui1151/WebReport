# import datetime

# today = datetime.date.today()
# yearBE = today.year + 543

# print(yearBE)
# import datetime
# from pythainlp.util import thai_strftime

# x = datetime.datetime.now()

# year = x.year
# day = x.strftime("%d")
# month = x.strftime("%m")

# date = datetime.datetime(year, int(month), int(day))
# now = thai_strftime(date, "%d %B %Y")

# print(now)
csvFilePath = r'D:/github/WebReport/backend/api/sources/All Dell cloud.csv'

name = csvFilePath.split("/")
name = name[-1].split(".csv")
print(name)