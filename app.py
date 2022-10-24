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
# src = 'src/images/eaac2f9f-709d-44d0-9c67-9fa70c195de8.png'

trimmedWhiteSpace = Recognition().trimWhiteSpace(src)
croppedImage = Recognition().CropImage(trimmedWhiteSpace[0])
xlsxData = extractXlsx(croppedImage[0])
revisedXlsx = Recognition().reviseCell(xlsxData)


