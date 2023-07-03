import os
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
import re

filePath = "/Users/sameepshah/Documents/Vardhaman Surgical Co./python_parsing/vsco.pdf"
doc = convert_from_path(filePath)
path, fileName = os.path.split(filePath)
fileBaseName, fileExtension = os.path.split(fileName)

output = ""

for page_number, page_data in enumerate(doc):
    txt = pytesseract.image_to_string(page_data).encode("utf-8")
    output += "Page # {} {} ".format(str(page_number), txt)
    
output = output.replace("MRP", " ")
output = output.replace("\n", " ")
output = output.replace("\r", " ")
output = output.replace("UNIVERSAL", "")
output = output.replace("STANDARD", "")
output = output.replace("[", "")
output = output.strip()

print(output)