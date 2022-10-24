#!/usr/bin/etc python
import pandas as pd

from function import Recognition
from imageToXlsx import extractXlsx

# src = 'src/images/b93927bd-e957-440d-accc-b4320e29de85.png'
# src = 'src/images/eaac2f9f-709d-44d0-9c67-9fa70c195de8.png'
src = 'src/images/3aea24a5-9fb9-417f-b237-efc93cbd8ae4.png'

## 엑셀 파일 생성
def extractMenuList(src):
    trimmedWhiteSpace = Recognition().trimWhiteSpace(src)
    croppedImage = Recognition().CropImage(trimmedWhiteSpace[0])
    xlsxData = extractXlsx(croppedImage[0])
    revisedXlsx = Recognition().reviseCell(xlsxData)
    return revisedXlsx

def extractLunchMenuList(src):
    trimmedWhiteSpace = Recognition().trimWhiteSpace(src)
    croppedImage = Recognition().CropImage(trimmedWhiteSpace[0])
    DoubleCroppedImage = Recognition().DoubleCropImage(croppedImage[0])
    xlsxData = extractXlsx(DoubleCroppedImage[0])
    revisedXlsx = Recognition().reviseCell(xlsxData)
    return revisedXlsx

extractLunchMenuList(src)