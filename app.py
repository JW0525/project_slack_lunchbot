#!/usr/bin/etc python
from PIL import Image
import cv2
import numpy as np
import pytesseract, re
import sys
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
import function


src = 'src/images/eaac2f9f-709d-44d0-9c67-9fa70c195de8.png'

result = pytesseract.image_to_string(Image.open(src), lang = "kor")

#print(type(result))
print(result)

with open('./people.csv', 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(result)

string = open('./people.csv').read()
new_str = re.sub('[^a-zA-Z0-9\n\.]', ' ', string)
open('./people.csv', 'w').write(new_str)



## 이미지 크기 구하기
# image1 = Image.open(src)
# print(image1.size)





# f = open('new.txt', 'w')
# result = function.Recognition().ExtractText('./inversed_image.png')
# f.write(result)
# f.close()


# result = function.Recognition().DetectImageTable(src)

# image = function.Recognition().crop_to_text('./savefig_default.png')
# cv2.imwrite("./example-table-cell-1-1-cropped.png", image)




# day_list = []
# f = open('new.txt', 'r')
# for line in f:
#     if '월' in line and '일' in line and not '월요일' in line:
#         print(line)
#         day_list.extend(line.replace('\n', '').split('  '))
#         day_list = list(filter(None, day_list))
# f.close()
#
#
#
#
#
#
# file = pd.read_csv('new.txt', delimiter = '\t')
# new_csv_file = file.to_csv( './new.csv')


