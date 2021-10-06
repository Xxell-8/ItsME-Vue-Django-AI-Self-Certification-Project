import pytesseract
import cv2
import numpy as np
import re



def text_detection(image):
    orig = image.copy()             # 원본 이미지 복사
    # 이미지 전처리
    image[:,:,0] = 0
    image[:,:,1] = 0
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)     # 바이너리 이미지로 변환
    erosion = cv2.erode(image, np.ones((2, 2), np.uint8), iterations=3)   # Erosion(침식): 바이너리 이미지에서 흰색(1) 오브젝트의 외곽픽셀을 검은색(0)으로 만든다.
    dilate = cv2.dilate(image, np.ones((2, 2), np.uint8), iterations=1)   # Dilate(팽창): 바이너리 이미지에서 검은색(0) 오브젝트의 외곽픽셀을 횐색(1)으로 만든다.
    image = cv2.subtract(dilate, erosion)    # Morph Gradient = dilate - erosion

    _, image = cv2.threshold(image, 13, 255, cv2.THRESH_OTSU)     # global threshold: 신분증 배경을 제거하기 위해

    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 9, 3)

    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel=np.ones((image.shape[0]//200, image.shape[1]//20), np.uint8), iterations=1)

    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boxes = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        if w < 23 or h < 23: continue

        cv2.rectangle(orig, (x, y), (x+w, y+h), (0, 255, 0), 2)
        boxes.append((x, y, w, h))

    return boxes


def text_recognition(image):
    min_conf = 50
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.erode(image, np.ones((2, 2), np.uint8), iterations=1)
    config = '-l kor --oem 3 --psm 6'
    data = pytesseract.image_to_data(image, config=config, output_type='data.frame', pandas_config={'dtype': {'text': str}})
    data = data[data.conf > min_conf]
    data = data.groupby('block_num')['text'].apply(list)
    if not data.empty:
        result = ''
        for char in data[1]:
            result += char
            if len(char) > 1 and char[-1] != '.':
                result += ' '
    else:
        result = ''
    return result.rstrip()


def get_name(texts):
    name_pattern = re.compile('[가-힣]{2,5}')
    for text in texts:
        m = name_pattern.match(text)
        if m:
            return m.group()
    return ''


def image_masking(image, texts, boxes):
    image = image.copy()
    customer_info = {}
    registration_number_pattern = re.compile('\d{6}[-]\d{7}')
    issue_date_pattern = re.compile('[가-힣0-9?~!@#$%&*]+[.][가-힣0-9?~!@#$%&*]+[.][가-힣0-9?~!@#$%&*]+[.]')
    idx = -1
    for i, (text, (x, y, w, h)) in enumerate(zip(texts, boxes)):
        if registration_number_pattern.match(text):
            customer_info['birth'] = text[:6]
            cv2.rectangle(image, (x+w//2, y), (x+w, y+h), (100, 100, 100), -1)
            cv2.rectangle(image, (x-h, y+h+h//4), (x+h*2+w, y+h*4+h//3*2), (100, 100, 100), -1)
            idx = i
        elif issue_date_pattern.match(text):
            cv2.rectangle(image, (x, y), (x+w, y+h), (100, 100, 100), -1)

    customer_info['name'] = ''
    customer_info['img'] = image
    if customer_info.get('birth'):
        if idx != -1 and len(texts) > idx+1:
            customer_info['name'] = get_name(texts[idx+1:])
    else:
        customer_info['birth'] = ''
    return customer_info


def ocr(image):
    image_orig = image.copy()
    area = text_detection(image)
    texts = []
    boxes = []
    for x, y, w, h in area:
        text = text_recognition(image[y:y+h, x:x+w])
        if text:
            texts.append(text)
            boxes.append((x, y, w, h))

    return image_masking(image_orig, texts, boxes)


pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
