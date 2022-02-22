
import shutil
import os
from docxtpl import DocxTemplate, RichText

doc = DocxTemplate("E:/INETMS/doc/Auto gen report/VA ISO/WebReport/test2.docx")

context = {
    "Group": [
        
   {
   "Name":"A",
   "device":{
      "203.150.237.2",
      "203.150.237.7",
      "203.150.237.4",
      "203.150.237.3",
      "203.150.237.6",
      "203.150.237.5",
      "203.150.237.1"
   },
   "Total_IP":7,
   "Critical":0,
   "High":2,
   "Medium":2,
   "Low":0,
   "Info":94
},
{
   "Name":"B",
   "device":{
      "203.150.237.15",
      "203.150.237.11",
      "203.150.237.9",
      "203.150.237.14",
      "203.150.237.12",
      "203.150.237.10",
      "203.150.237.8",
      "203.150.237.13"
   },
   "Total_IP":8,
   "Critical":0,
   "High":0,
   "Medium":2,
   "Low":0,
   "Info":91
}
    ]
}

doc.render(context)
doc.save("generated_doc.docx")
os.system("generated_doc.docx")
