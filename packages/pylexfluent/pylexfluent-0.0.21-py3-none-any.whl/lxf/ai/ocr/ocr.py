import os
import re
from typing import List
import cv2
import pytesseract
from pdf2image import convert_from_path, convert_from_bytes
from pathlib import Path

from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
import numpy as np


from tqdm import tqdm

from lxf import settings






def check_path() ->None:
    """
    """
    data_path =Path("./data")
    if not data_path.exists: data_path.mkdir()
    image_path=Path("./data/images")    
    if not image_path.exists(): image_path.mkdir()
    temp_path=Path("./data/images/temp")
    if not temp_path.exists() : temp_path.mkdir()
    temp_document_path=Path("./data/temp-document")
    if not temp_document_path.exists() : temp_document_path.mkdir()
    temp_document_images_path = Path("./data/temp-document/images")
    if not temp_document_images_path.exists(): temp_document_images_path.mkdir()

# Credits to https://becominghuman.ai/how-to-automatically-deskew-straighten-a-text-image-using-opencv-a0c30aed83df
def getSkewAngle(cvImage) -> float:
    check_path()
    # Prep image, copy, convert to gray scale, blur, and threshold
    newImage = cvImage.copy()
    
    gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)

    thresh, img_bw = cv2.threshold(gray,150,250,cv2.THRESH_BINARY)
    #cv2.imwrite("./data/images//temp/deskew_img_bw.png", img_bw)

    no_noise = noise_removal(img_bw)
    #cv2.imwrite("./data/images/temp/deskwe_no_noise.jpg", no_noise)

    blur = cv2.GaussianBlur(no_noise, (9, 9), 0)
    #cv2.imwrite("./data/images/temp/deskew_blur.jpg",blur)    

    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    #cv2.imwrite("./data/images/temp/deskew_thresh.jpg",thresh)
    # Apply dilate to merge text into meaningful lines/paragraphs.
    # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
    # But use smaller kernel on Y axis to separate between different blocks of text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 9))
    dilate = cv2.dilate(thresh, kernel, iterations=1)
    #cv2.imwrite("./data/images/temp/deskew_dilate.jpg",dilate)
    
    # Find all contours
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)
    for c in contours:
        rect = cv2.boundingRect(c)
        x,y,w,h = rect
        cv2.rectangle(newImage,(x,y),(x+w,y+h),(0,255,0),2)

    # Find largest contour and surround in min area box
    largestContour = contours[0]
    #print (len(contours))
    minAreaRect = cv2.minAreaRect(largestContour)
    box = np.intp(cv2.boxPoints(minAreaRect))
    cv2.drawContours(newImage, [box], 0, (0,0,255), 3)
    #cv2.imwrite("./data/images/temp/boxes.jpg", newImage)
    # Determine the angle. Convert it to the value that was originally used to obtain skewed image
    angle = minAreaRect[-1]
    #print(f"Deskew angle:{angle}")
    if angle < -45:
        angle = 90 + angle
    return -1.0 * angle

# Deskew image
def deskew(cvImage,correction_angle:float=1):
    angle = getSkewAngle(cvImage)
    print(f"Angle à corriger {angle}")
    if (abs(angle)<5):
        if angle>0 :
            correction_angle=-correction_angle
        else :
            correction_angle=correction_angle
        print(f"Facteur de correction d'angle retenue {correction_angle}")
        angle= correction_angle * angle
        print(f"Angle finale retenue {angle}")
        print("Rotation")
        return rotateImage(cvImage,angle )
    else :
        return cvImage
    
# Rotate the image around its center
def rotateImage(cvImage, angle: float):
    newImage = cvImage.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage

def to_gray(image):
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    return gray

def noise_removal(image):
    import numpy as np
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    return (image)

def thin_font(image):
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones((2,2),np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return (image)

def remove_borders(image):
    contours, hiearchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntsSorted = sorted(contours, key=lambda x:cv2.contourArea(x))
    cnt = cntsSorted[-1]
    x, y, w, h = cv2.boundingRect(cnt)
    crop = image[y:y+h, x:x+w]
    return (crop)

def sortKeyColunm(x, hmax,hmoy,wmoy):
    x,y,w,h = cv2.boundingRect(x)
    col = x//wmoy
    line = y//hmoy
    return x+col*hmax+line*hmoy

def sortKeyRow(x,xmax,href,wref) :
    x,y,w,h = cv2.boundingRect(x)
    nb_cols=max(xmax//wref,1)
    col = max(x//wref,1)
    line = max(y//href,1)
    return line*nb_cols+col

def detect_struct(image,
                  max_high:float=1900.0,
                  min_high:float=80.0,
                  max_wide:float=1500.00,
                  min_wide:float=60.00,
                  intermediate_files:bool=False,
                  threshold_min:float=150.00,
                  threshold_max:float=255.00,
                  filter:bool=True,
                  max_box:bool=False,
                  hmoy_filter_correction:float=0.5,
                  wmoy_filter_correction:float=0.5,
                  kernel_dilated_size:any=(10,10),
                  kernel_blur_size:any=(17,19), 
                  column_direction:bool=False):
    """
    Compute the ROI of the image 
    """
    check_path()
    # Deskew
    image = deskew(image,correction_angle=0.8)
    # convert to gray
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    if intermediate_files : cv2.imwrite("./data/images/temp/gray.png",gray)
    thresh, img_bw = cv2.threshold(gray,threshold_min,threshold_max,cv2.THRESH_BINARY)
    if intermediate_files : cv2.imwrite("./data/images/temp/img_bw.png", img_bw)
    #no_noise = noise_removal(gray)
    #cv2.imwrite("./data/images/temp/no_noise.jpg", no_noise)
    # blur
    blur = cv2.GaussianBlur(img_bw,kernel_blur_size,0)
    if intermediate_files : cv2.imwrite ("./data/images/temp/blur_0.png",blur)
    # threshold 
    #thresh=cv2.threshold(no_noise,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
    thresh=cv2.threshold(blur,threshold_min,threshold_max,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
    if intermediate_files : cv2.imwrite("./data/images/temp/thresh_0.png",thresh)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,kernel_dilated_size)
    if intermediate_files : cv2.imwrite("./data/images/temp/kernel.png",kernel)
    dilate = cv2.dilate(thresh, kernel, iterations=1)
    if intermediate_files : cv2.imwrite("./data/images/temp/dilate_0.png",dilate)
    cnts = cv2.findContours(dilate,cv2.RETR_LIST,cv2.CHAIN_APPROX_TC89_KCOS)
    cnts = cnts[0] if len(cnts)==2 else cnts[1]
    ymax=0.0
    xmax=0.0
    xmin=10000000.0
    ymin=10000000.0
    hmin=10000000.0
    wmax=0.0
    wmin=10000000.0
    hmax=0.0
    wmoy=0.0
    hmoy=0.0
    
    n=len(cnts)
    for cnt in cnts:
        x,y,w,h =cv2.boundingRect(cnt)
        if y>ymax : ymax=y
        if x>xmax : xmax=x
        if x<xmin : xmin=x
        if y<ymin : ymin=y
        if w>wmax : wmax=w
        if w<wmin : wmin=w
        if h>hmax : hmax=h
        if h<hmin : hmin=h
        wmoy+=w/n
        hmoy+=h/n
    if intermediate_files : print(f"h Max={ymax} h moyen = {hmoy} w moyen = {wmoy}")
    # trier les ROIS en fonction du mode de direction choisi 
    if column_direction :
        cnts = sorted(cnts,key=lambda x: sortKeyColunm(x,ymax,hmoy,wmoy),reverse=True)
    else :
        cnts = sorted(cnts,key=lambda x: sortKeyRow(x,xmax,hmin,wmin),reverse=True)
    rois=[]
    base_image = image.copy()  
    lg=len(cnts)  
    if max_box:
            # We take only the greatest bounding rectangle
            roi = base_image[ymin:ymin+hmax,xmin:xmin+wmax]
            rois.append(roi)
            cv2.rectangle(image,(xmin,ymin),(xmin+wmax,ymin+hmax),(0,255,0),2)        
    else:
        for i in range(lg) :
            c=cnts[lg-i-1]
            x,y,w,h = cv2.boundingRect(c)
            
            if (filter==True) :
                # We filter by max_high and maw_wide
                if (h>hmoy_filter_correction*hmoy and h<max_high) and (w>wmoy_filter_correction*wmoy and w<max_wide):
                    roi = base_image[y:y+h,x:x+w]
                    rois.append(roi)     
                    cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
            else :
                # We take all 
                roi = base_image[y:y+h,x:x+w]
                rois.append(roi)
                cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)

            
    if intermediate_files : 
        cv2.imwrite("./data/images/temp/bbox.png",image)
        i=0
        for roi in rois:
            i+=1
            cv2.imwrite(f"./data/images/temp/rois_{i}.png",roi)
    return rois

def sanitize_text(text:str)->str:
    regex=r"\n"
    subst=" "
    result = re.sub(regex, subst, text, 0, re.MULTILINE)
    regex=r" {2,}"
    result = re.sub(regex, subst, result, 0, re.MULTILINE)
    regex=r"\. "
    subst=".\n"
    result = re.sub(regex, subst, result, 0, re.MULTILINE)
    return result

def recognize_rois(text:List[str],rois,intermediate_files:bool, sanitize:bool, threshold_limit:float=150)->List[str]:
        # Telesserac config
        # Add -l LANG[+LANG] to the command line to use multiple languages together for recognition
        #     -l eng+deu
        # quiet to suppress messages
        # pdf This creates a pdf with the image and a separate searchable text layer with the recognized text.
        # Use --oem 1 for LSTM/neural network, --oem 0 for Legacy Tesseract.
        # –psm 3 - Fully automatic page segmentation, but no OSD. (Default)
        # –psm 6 - Assume a single uniform block of text.
        # –psm 11  Use pdftotext for preserving layout for text output
        # Use -c preserve_interword_spaces=1 to preserve spaces
        # hocr to get the HOCR output
        # <?xml version="1.0" encoding="UTF-8"?>
        # <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
        #     "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        # <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
        #  <head>
        #   <title></title>
        #   <meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
        #   <meta name='ocr-system' content='tesseract 5.0.1-64-g3c22' />
        #   <meta name='ocr-capabilities' content='ocr_page ocr_carea ocr_par ocr_line ocrx_word ocrp_wconf'/>
        #  </head>
        #  <body>
        #   <div class='ocr_page' id='page_1' title='image "images/eurotext.png"; bbox 0 0 640 500; ppageno 0; scan_res 300 300'>
        #    <div class='ocr_carea' id='block_1_1' title="bbox 61 41 574 413">
        #     <p class='ocr_par' id='par_1_1' lang='eng' title="bbox 61 41 574 413">
        #      <span class='ocr_line' id='line_1_1' title="bbox 65 41 515 71; baseline 0.013 -11; x_size 25; x_descenders 5; x_ascenders 6">
        #       <span class='ocrx_word' id='word_1_1' title='bbox 65 41 111 61; x_wconf 96'>The</span>
        #       <span class='ocrx_word' id='word_1_2' title='bbox 128 42 217 66; x_wconf 95'>(quick)</span>
        #       <span class='ocrx_word' id='word_1_3' title='bbox 235 43 330 68; x_wconf 95'>[brown]</span>
        #       <span class='ocrx_word' id='word_1_4' title='bbox 349 44 415 69; x_wconf 94'>{fox}</span>
        #       <span class='ocrx_word' id='word_1_5' title='bbox 429 45 515 71; x_wconf 96'>jumps!</span>
        #      </span>

        # ...

        #      <span class='ocr_line' id='line_1_12' title="bbox 61 385 444 413; baseline 0.013 -9; x_size 24; x_descenders 4; x_ascenders 5">
        #       <span class='ocrx_word' id='word_1_62' title='bbox 61 385 119 405; x_wconf 92'>salta</span>
        #       <span class='ocrx_word' id='word_1_63' title='bbox 135 385 200 406; x_wconf 92'>sobre</span>
        #       <span class='ocrx_word' id='word_1_64' title='bbox 216 392 229 406; x_wconf 83'>o</span>
        #       <span class='ocrx_word' id='word_1_65' title='bbox 244 388 285 407; x_wconf 80'>cdo</span>
        #       <span class='ocrx_word' id='word_1_66' title='bbox 300 388 444 413; x_wconf 92'>preguigoso.</span>
        #      </span>
        #     </p>
        #    </div>
        #   </div>
        #  </body>
        # </html>
        # TSV to get the TSV output :
        # level   page_num        block_num       par_num line_num        word_num        left    top     width   height  conf    text
        # 1       1       0       0       0       0       0       0       640     500     -1
        # 2       1       1       0       0       0       61      41      513     372     -1
        # 3       1       1       1       0       0       61      41      513     372     -1
        # 4       1       1       1       1       0       65      41      450     30      -1
        # 5       1       1       1       1       1       65      41      46      20      96.063751       The
        # 5       1       1       1       1       2       128     42      89      24      95.965691       (quick)
        # 5       1       1       1       1       3       235     43      95      25      95.835831       [brown]
        # 5       1       1       1       1       4       349     44      66      25      94.899742       {fox}
        # 5       1       1       1       1       5       429     45      86      26      96.683357       jumps!
    check_path()
    text=[]
    custom_config = r'--oem 1 --oem 3 --psm 6 '        
    for i,image_roi in tqdm(enumerate(rois),desc="Analyse des ROI ",disable=not settings.enable_tqdm):
        img_gray = to_gray(image_roi)
        if intermediate_files : 
            cv2.imwrite(f"./data/images/temp/rois_{i+1}_ngray.jpg",img_gray)
        thresh, img_bw = cv2.threshold(img_gray,threshold_limit,255,cv2.THRESH_TRUNC)
        if intermediate_files : 
            cv2.imwrite(f"./data/images//temp/rois_{i+1}_bw.png", img_bw)
        img_nonoise = noise_removal(img_bw)
        if intermediate_files : 
            cv2.imwrite(f"./data/images/temp/rois_{i+1}_no_noise.jpg",img_nonoise)
        img = img_bw
        text.append(pytesseract.image_to_string(img,lang="fra",config=custom_config))


    return text


async def doOcr_from_pdf(path_filename:str,intermediate_files:bool=False,rois_filter:bool=True, threshold_limit:float=180,sanitize:bool=True):

    check_path()
    document_path = Path('./data/temp-document/images')
    pages = convert_from_path(path_filename)
    texts=""
    text_rois=[]
    for i in tqdm(range(len(pages)),desc="Analyse des pages ",disable=not settings.enable_tqdm):
        ## Save image to file
        pages[i].save(f"{document_path}/page_{i}.jpeg",'JPEG')
        page = cv2.imread(f"{document_path}/page_{i}.jpeg")    
        
        #detection
        rois = detect_struct(page,
                             filter=rois_filter, 
                             threshold_min=threshold_limit,
                             hmoy_filter_correction=0.05,
                             wmoy_filter_correction=0.05,
                             min_high=50,
                             min_wide=50,
                             kernel_dilated_size=(19,7),
                             kernel_blur_size=(17,9)
                             )
        # recognition
        text_rois=recognize_rois(text_rois,rois,intermediate_files,sanitize, threshold_limit=threshold_limit)
        if text_rois != None : temp = " ".join(text_rois)
        if sanitize : 
            texts += sanitize_text(temp)
    return texts

async def doOcr_from_image(path_filename:str,intermediate_files:bool=False, rois_filter:bool=True, threshold_limit:float=180, sanitize:bool=True):

    check_path()
    text=[]
    page = cv2.imread(path_filename.__str__())        
    #detection
    rois = detect_struct(page,filter=rois_filter, threshold_min=threshold_limit)
    # recognition
    text=recognize_rois(text,rois,intermediate_files,sanitize, threshold_limit=threshold_limit)
    texts=""
    if text != None : texts = " ".join(text)
    if sanitize : 
        texts = sanitize_text(texts)
    return texts    

