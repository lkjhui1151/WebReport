import csv
import json
from docxtpl import *
import pandas
import os

doc = DocxTemplate("D:/github/WebReport/test.docx")

Content = {
    'name': [
        {
            'name2': "ssss"
        }
    ]
}

doc.render(Content)
doc.save("generated_doc.docx")
os.system("generated_doc.docx")
