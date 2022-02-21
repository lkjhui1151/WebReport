import mysql.connector
import shutil
import os
from win32com.client import Dispatch
from docxtpl import DocxTemplate, RichText

doc = DocxTemplate("test.docx")

context = {
    "company": {
        "name": "Plumsail",
        "email": "contact@plumsail.com"
    },
    "employees": [
        {
            "name": "Derek Clark",
            "jobTitle": "Marketing director",
            "department": "Marketing Department",
            "office": "Room 18",
            "phone": "(206) 854-9798",
            'bgSeverity': "#ff0000"
        },
        {
            "name": "Xue Li",
            "jobTitle": "Financial director",
            "department": "Financial Department",
            "office": "Room 19",
            "phone": "(206) 598-1259",
            'bgSeverity': "#ff0000"
        },
        {
            "name": "Xue Li",
            "jobTitle": "Financial director",
            "department": "Financial Department",
            "office": "Room 19",
            "phone": "(206) 598-1259"
        },
        {
            "name": "Xue Li",
            "jobTitle": "Financial director",
            "department": "Financial Department",
            "office": "Room 19",
            "phone": "(206) 598-1259"
        },
        {
            "name": "Xue Li",
            "jobTitle": "Financial director",
            "department": "Financial Department",
            "office": "Room 19",
            "phone": "(206) 598-1259"
        },
        {
            "name": "Xue Li",
            "jobTitle": "Financial director",
            "department": "Financial Department",
            "office": "Room 19",
            "phone": "(206) 598-1259"
        },
        {
            "name": "Xue Li",
            "jobTitle": "Financial director",
            "department": "Financial Department",
            "office": "Room 19",
            "phone": "(206) 598-1259"
        },
        {
            "name": "Xue Li",
            "jobTitle": "Financial director",
            "department": "Financial Department",
            "office": "Room 19",
            "phone": "(206) 598-1259"
        },
        {
            "name": "Xue Li",
            "jobTitle": "Financial director",
            "department": "Financial Department",
            "office": "Room 19",
            "phone": "(206) 598-1259"
        },
        {
            "name": "Xue Li",
            "jobTitle": "Financial director",
            "department": "Financial Department",
            "office": "Room 19",
            "phone": "(206) 598-1259"
        },
        {
            "name": "Xue Li",
            "jobTitle": "Financial director",
            "department": "Financial Department",
            "office": "Room 19",
            "phone": "(206) 598-1259"
        },
        {
            "name": "Xue Li",
            "jobTitle": "Financial director",
            "department": "Financial Department",
            "office": "Room 19",
            "phone": "(206) 598-1259"
        },
        {
            "name": "Xue Li",
            "jobTitle": "Financial director",
            "department": "Financial Department",
            "office": "Room 19",
            "phone": "(206) 598-1259"
        },
        {
            "name": "Xue Li",
            "jobTitle": "Financial director",
            "department": "Financial Department",
            "office": "Room 19",
            "phone": "(206) 598-1259"
        },
        {
            "name": "Xue Li",
            "jobTitle": "Financial director",
            "department": "Financial Department",
            "office": "Room 19",
            "phone": "(206) 598-1259"
        },
        {
            "name": "Xue Li",
            "jobTitle": "Financial director",
            "department": "Financial Department",
            "office": "Room 19",
            "phone": "(206) 598-1259"
        },
        {
            "name": "Xue Li",
            "jobTitle": "Financial director",
            "department": "Financial Department",
            "office": "Room 19",
            "phone": "(206) 598-1259"
        },
        {
            "name": "Xue Li",
            "jobTitle": "Financial director",
            "department": "Financial Department",
            "office": "Room 19",
            "phone": "(206) 598-1259"
        },
        {
            "name": "Xue Li",
            "jobTitle": "Financial director",
            "department": "Financial Department",
            "office": "Room 19",
            "phone": "(206) 598-1259"
        },
        {
            "name": "Xue Li",
            "jobTitle": "Financial director",
            "department": "Financial Department",
            "office": "Room 19",
            "phone": "(206) 598-1259"
        },
        {
            "name": "Xue Li",
            "jobTitle": "Financial director",
            "department": "Financial Department",
            "office": "Room 19",
            "phone": "(206) 598-1259"
        },
        {
            "name": "Xue Li",
            "jobTitle": "Financial director",
            "department": "Financial Department",
            "office": "Room 19",
            "phone": "(206) 598-1259"
        },
        {
            "name": "Xue Li",
            "jobTitle": "Financial director",
            "department": "Financial Department",
            "office": "Room 19",
            "phone": "(206) 598-1259"
        },
        {
            "name": "Jessica Adams",
            "jobTitle": "Marketing manager",
            "department": "Marketing Department",
            "office": "Room 23",
            "phone": "(206) 789-1598"
        },
        {
            "name": "Katsuko Kawakami",
            "jobTitle": "Analyst",
            "department": "Financial Department",
            "office": "Room 26",
            "phone": "(206) 784-1258"
        }
    ]
}

doc.render(context)
doc.save("generated_doc.docx")
os.system("generated_doc.docx")
