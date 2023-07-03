from PIL import Image
import cv2
import pytesseract
import os
import numpy as np
import pandas as pd
import re
from pdf2image import convert_from_bytes

def get_conf(page_gray):
    df = pytesseract.image_to_data(page_gray, output_type='data.frame')
    df.drop(df[df.conf==-1].index.values,inplace=True)
    df.reset_index()
    return df.conf.mean()

def deskew(image):
    gray = cv2.bitwise_not(image)
    temp_arr = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(temp_arr>0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

OCR_dic = {}
file_list = ['vsco.pdf']

for file in file_list:
    pdf_file = convert_from_bytes(open(os.path.join('/Users/sameepshah/Documents/Vardhaman Surgical Co./python_parsing',file), 'rb').read())
    # create a df to save each pdf's text
    pages_df = pd.DataFrame(columns=['conf','text'])
    for (i,page) in enumerate(pdf_file) :
        try:
            # transfer image of pdf_file into array
            page_arr = np.asarray(page)
            # transfer into grayscale
            page_arr_gray = cv2.cvtColor(page_arr,cv2.COLOR_BGR2GRAY)
            # deskew the page
            page_deskew = deskew(page_arr_gray)
            # cal confidence value
            page_conf = get_conf(page_deskew)
            # extract string
            new_row = pd.DataFrame(columns=['conf' 'text'], data={'conf': page_conf,'text': pytesseract.image_to_string(page_deskew)})
            pages_df = pd.concat([pages_df, new_row], ignore_index=True)
        except:
            # if can't extract then give some notes into df
            new_row = pd.DataFrame(columns=['conf' 'text'], data={'conf':-1, 'text': 'N/A'})
            pages_df = pd.concat([pages_df, new_row], ignore_index=True)
            continue
    # save df into a dict with filename as key        
    OCR_dic[file]=pages_df
    print('{} is done'.format(file))
    
print(OCR_dic[file_list[1]])