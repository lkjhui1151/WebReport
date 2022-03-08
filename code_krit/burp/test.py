import re

data = "<ul>\n\t<li><a href=\"https://portswigger.net/web-security/cross-site-scripting\">Web Security Academy: Cross-site scripting</a></li>\n\t<li><a href=\"https://portswigger.net/web-security/cross-site-scripting/reflected\">Web Security Academy: Reflected cross-site scripting</a></li>\n\t<li><a href=\"https://support.portswigger.net/customer/portal/articles/1965737-Methodology_XSS.html\">Using Burp to Find XSS issues</a></li>\n</ul>"
# print(re.sub('</?[a-z]*>',"",data))
x = re.findall(r'(http\S+)\"',data)
print(x)
