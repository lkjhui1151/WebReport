import re

data = '<p> The application fails to <div>prevent users from connecting </div>'


x = re.search(r'The(.*?)from', data)

print(x) if x == None else print(x.group(0))
