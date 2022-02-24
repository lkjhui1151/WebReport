import csv
import json
from docxtpl import *
import pandas
import os

doc = DocxTemplate("D:/github/WebReport/patch/pic.docx")

# print(Content)
doc.replace_media("D:/github/WebReport/patch/1.jpg",
                  "D:/github/WebReport/patch/2.png")
doc.save("D:/github/WebReport/patch/generated_doc.docx")
os.system("D:/github/WebReport/patch/generated_doc.docx")
