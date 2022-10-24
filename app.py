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

from function import Recognition
from imageToXlsx import extractXlsx

src = 'src/images/b93927bd-e957-440d-accc-b4320e29de85.png'

# trimmedWhiteSpace = Recognition().trimWhiteSpace(src)
# croppedImage = Recognition().CropImage(trimmedWhiteSpace[0])
# csvData = extractXlsx(croppedImage[0])

Recognition().removeCell('src/results/output.xlsx')



#
# file = pd.read_csv('new.txt', delimiter = '\t')
# new_csv_file = file.to_csv( './new.csv')


