from importlib import import_module


import datetime

date = datetime.datetime.now()

dateNow = "Date "+date.strftime("%B")+" " +
date.strftime("%d")+" "+date.strftime("%Y")

print()
