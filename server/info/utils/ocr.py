import pytesseract
import cv2
import numpy as np
import re
from PIL import Image 



def image_detection(image):
    # 1-1. 이미지 읽어오기
    orig = image.copy()

    # 2-1. 이미지 리사이즈
    r = 800.0 / image.shape[0]
    dim = (int(image.shape[1] * r), 800)
    image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    # 2-2. 가장자리 검출
    # 2-2-1. 흑백 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 2-2-2. 블러로 노이즈 제거
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    # 2-2-3. 이미지 가장자리 검출
    edged = cv2.Canny(gray, 75, 200)

    # contour 반환
    (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # contour를 외곽이 그린 면적이 큰 순대로 정렬해 최대 5개 추출
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

    # contour를 순회하면서
    screenCnt = -1
    for c in cnts:
        # contour가 그리는 길이 계산
        peri = cv2.arcLength(c, True)
        # peri에 2% 정도 오차를 두고 도형을 근사해서 구함
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        # 외곽의 꼭지점이 4개면 신분증 외곽으로 계산
        # 찾은 외곽들 중 큰 순서대로 5개를 찾아 꼭지점 4개인 도형을 찾는 것
        if len(approx) == 4:
            screenCnt = approx
            break

    # contour 그리기
    if type(screenCnt) == int and screenCnt == -1:
        return None
    cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
    def order_points(pts):
        rect = np.zeros((4, 2), dtype=np.float32)

        # 넘겨받은 배열의 각 행에 대한 합을 계산
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)] # x+y 최대값
        rect[2] = pts[np.argmax(s)] # x+y 최소값

        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)] # y-x 최대값
        rect[3] = pts[np.argmax(diff)] # y-x 최소값

        return rect / r

    rect = order_points(screenCnt.reshape(4, 2))
    (tl, tr, br, bl) = rect

    # 각각의 기리를 계산
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

    # 최대 높이와 너비 계산
    maxWidth = max(int(widthA), int(widthB))
    maxHeight = max(int(heightA), int(heightB))

    # 변환될 좌표 위치 초기화
    dst = np.array([[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]], dtype=np.float32)

    # 나머지 픽셀을 옯기는 matrix 생성
    M = cv2.getPerspectiveTransform(rect, dst)
    # 최종적으로 반듯한 사각형으로 변환
    warped = cv2.warpPerspective(orig, M, (maxWidth, maxHeight))

    return warped


def text_detection(image):
    orig = image.copy()             # 원본 이미지 복사
    # 이미지 전처리
    image[:,:,0] = 0
    image[:,:,1] = 0
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)     # 바이너리 이미지로 변환
    erosion = cv2.erode(image, np.ones((2, 2), np.uint8), iterations=1)   # Erosion(침식): 바이너리 이미지에서 흰색(1) 오브젝트의 외곽픽셀을 검은색(0)으로 만든다.
    dilate = cv2.dilate(image, np.ones((2, 2), np.uint8), iterations=1)   # Dilate(팽창): 바이너리 이미지에서 검은색(0) 오브젝트의 외곽픽셀을 횐색(1)으로 만든다.
    image = cv2.subtract(dilate, erosion)    # Morph Gradient = dilate - erosion

    _, image = cv2.threshold(image, 13, 255, cv2.THRESH_BINARY)     # global threshold: 신분증 배경을 제거하기 위해

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

    if not customer_info.get('birth'):
        return None
    if idx != -1 and len(texts) > idx+1:
        customer_info['name'] = get_name(texts[idx+1:])
    else:
        customer_info['name'] = ''
    customer_info['img'] = image
    return customer_info


def ocr(image):
    image = image_detection(image)
    if image is None:
        return None
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
