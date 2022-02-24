import csv
import json
from docxtpl import *
import pandas
import os

doc = DocxTemplate("D:/github/WebReport/test.docx")

Content = {
    'name': [
        {
            'address': "192.168.1.1"
        },
        {
            'address': "192.168.1.3"
        },
        {
            'address': "192.168.1.2"
        }
    ]
}

# print(Content['name'][0]['address'])

# number = []
# for i in range(len(Content['name'])):
items = sorted(Content['name'], key=lambda d: tuple(map(int, d['address'].split('.'))))

print(items)

# doc.render(Content)
# doc.save("generated_doc.docx")
# os.system("generated_doc.docx")
