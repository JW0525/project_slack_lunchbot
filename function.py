from PIL import Image, ImageChops
import pytesseract
import os
import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys


class Recognition:
    ## 이미지 여백 제거
    def trimWhiteSpace(self, src):
        img = cv2.imread(src) # Read in the image and convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = 255 * (gray < 128).astype(np.uint8) # To invert the text to white
        coords = cv2.findNonZero(gray) # Find all non-zero points (text)
        x, y, w, h = cv2.boundingRect(coords) # Find minimum spanning bounding box
        rect = img[y:y+h, x:x+w] # Crop the image - note we do this on the original image
        # cv2.imshow("Cropped", rect) # Show it
        resize_rect = cv2.resize(rect, (1085, 760)) # 사이즈 통일
        cv2.imwrite("src/results/trimmed_whiteSpace.png", resize_rect) # Save the image
        return "src/results/trimmed_whiteSpace.png", resize_rect

    ## 이미지 크롭
    def CropImage(self, src):
        image = Image.open(src)
        size = image.size
        crop = image.crop((92, 140, size[0], size[1]-100))
        # crop.show()
        crop.save('src/results/cropped_image.png')
        return 'src/results/cropped_image.png', crop'

















    ##제글자 추출
    def ExtractText(self, src):
        img = cv2.imread(src, cv2.IMREAD_COLOR)
        copy_img = img.copy()
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('gray.jpg', img2)
        blur = cv2.GaussianBlur(img2, (3,3), 0)
        cv2.imwrite('blur.jpg', blur)
        canny = cv2.Canny(blur, 100, 200)
        cv2.imwrite('canny.jpg', canny)

        contours, hierarchy  = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        box1 = []
        f_count = 0
        select = 0
        plate_width = 0

        for i in range(len(contours)):
           cnt = contours[i]
           area = cv2.contourArea(cnt)
           x,y,w,h = cv2.boundingRect(cnt)
           rect_area = w * h  #area size
           aspect_ratio = float(w)/h # ratio = width/height

           if  (aspect_ratio >= 0.2) and (aspect_ratio <= 1.0) and (rect_area >= 100) and (rect_area <= 700):
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 1)
                box1.append(cv2.boundingRect(cnt))

        for i in range(len(box1)): ##Buble Sort on python
           for j in range(len(box1) - (i + 1)):
                if box1[j][0] > box1[j + 1][0]:
                     temp = box1[j]
                     box1[j] = box1[j + 1]
                     box1[j + 1] = temp

        #to find number plate measureing length between rectangles
        for m in range(len(box1)):
           count = 0
           for n in range(m + 1,(len(box1) - 1)):
                delta_x = abs(box1[n + 1][0] - box1[m][0])
                if delta_x > 150:
                     break
                delta_y = abs(box1[n + 1][1] - box1[m][1])
                if delta_x == 0:
                     delta_x = 1
                if delta_y == 0:
                     delta_y = 1
                gradient = float(delta_y) / float(delta_x)
                if gradient < 0.25:
                    count = count + 1
           #measure number plate size
           if count > f_count:
                select = m
                f_count = count;
                plate_width=delta_x
        cv2.imwrite('snake.jpg', img)

        number_plate=copy_img[box1[select][1]-10:box1[select][3]+box1[select][1]+20,box1[select][0]-10:140+box1[select][0]]
        resize_plate=cv2.resize(number_plate,None,fx=1.8,fy=1.8,interpolation=cv2.INTER_CUBIC+cv2.INTER_LINEAR)
        plate_gray=cv2.cvtColor(resize_plate,cv2.COLOR_BGR2GRAY)
        ret,th_plate = cv2.threshold(plate_gray,150,255,cv2.THRESH_BINARY)

        cv2.imwrite('plate_th.jpg',th_plate)
        kernel = np.ones((3,3),np.uint8)
        er_plate = cv2.erode(th_plate,kernel,iterations=1)
        er_invplate = er_plate
        cv2.imwrite('er_plate.jpg',er_invplate)

        result = pytesseract.image_to_string(Image.open(src), lang = 'kor')
        return result


    ## 이미지 csv 파일로 변환
    def createFileList(myDir, format = '.jpg'):
        fileList = []
        print(myDir)
        for root, dirs, files in os.walk(myDir, topdown = False):
            for name in files:
                if name.endswith(format):
                    fullName = os.path.join(root, name)
                    fileList.append(fullName)

        # load the original image
        myFileList = createFileList(src)

        for file in myFileList:
            print(file)
            img_file = Image.open(file)

            # get original image parameters...
            width, height = img_file.size
            format = img_file.format
            mode = img_file.mode

            # Make image Greyscale
            img_grey = img_file.convert('L')

            # Save Greyscale values
            value = np.asarray(img_grey.getdata(), dtype=np.int).reshape((img_grey.size[1], img_grey.size[0]))
            value = value.flatten()
            print(value)
            with open("img_pixels.csv", 'a') as f:
                writer = csv.writer(f)
                writer.writerow(value)

        return fileList


    ## 테이블 감지
    def DetectImageTable(self, src):
        table_image_contour = cv2.imread(src, 0)
        table_image = cv2.imread(src)
        ## Inverse Image Thresholding 데이터를 향상
        ret, thresh_value = cv2.threshold(
            table_image_contour, 180, 255, cv2.THRESH_BINARY_INV)
        ## 이미지 확장
        kernel = np.ones((5,5),np.uint8)
        dilated_value = cv2.dilate(thresh_value, kernel, iterations = 1)
        ## 계층구조 추가
        contours, hierarchy = cv2.findContours(
            dilated_value, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        ## 직사각형 상자의 좌표 계산 및 배치
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            # bounding the images
            if y < 50:
                table_image = cv2.rectangle(table_image, (x, y), (x + w, y + h), (0, 0, 255), 1)

        plt.imshow(table_image)
        plt.show()
        ## 윤곽선이 포함 된 테이블을 렌더링
        a = cv2.namedWindow('detecttable', cv2.WINDOW_NORMAL)
        plt.imsave('savefig_default.png', table_image)
        return table_image

    ## Cropping each cell to the text
    def crop_to_text(self, image):
        MAX_COLOR_VAL = 255
        BLOCK_SIZE = 15
        SUBTRACT_FROM_MEAN = -2

        img_bin = cv2.adaptiveThreshold(
            image,
            MAX_COLOR_VAL,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            BLOCK_SIZE,
            SUBTRACT_FROM_MEAN,
        )

        img_h, img_w = image.shape
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (int(img_w * 0.5), 1))
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, int(img_h * 0.7)))
        horizontal_lines = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, horizontal_kernel)
        vertical_lines = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, vertical_kernel)
        both = horizontal_lines + vertical_lines
        cleaned = img_bin - both

        # Get rid of little noise.
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        opened = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)
        opened = cv2.dilate(opened, kernel)

        contours, hierarchy = cv2.findContours(opened, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        bounding_rects = [cv2.boundingRect(c) for c in contours]
        NUM_PX_COMMA = 6
        MIN_CHAR_AREA = 5 * 9
        char_sized_bounding_rects = [(x, y, w, h) for x, y, w, h in bounding_rects if w * h > MIN_CHAR_AREA]
        if char_sized_bounding_rects:
            minx, miny, maxx, maxy = math.inf, math.inf, 0, 0
            for x, y, w, h in char_sized_bounding_rects:
                minx = min(minx, x)
                miny = min(miny, y)
                maxx = max(maxx, x + w)
                maxy = max(maxy, y + h)
            x, y, w, h = minx, miny, maxx - minx, maxy - miny
            cropped = image[y:min(img_h, y+h+NUM_PX_COMMA), x:min(img_w, x+w)]
        else:
            # If we morphed out all of the text, assume an empty image.
            cropped = MAX_COLOR_VAL * np.ones(shape=(20, 100), dtype=np.uint8)
        bordered = cv2.copyMakeBorder(cropped, 5, 5, 5, 5, cv2.BORDER_CONSTANT, None, 255)
        return bordered




