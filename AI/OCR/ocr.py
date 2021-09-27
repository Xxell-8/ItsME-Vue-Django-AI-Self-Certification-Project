import pytesseract
import cv2
import numpy as np
import argparse



def image_detection(image_path):
    # 1-1. 이미지 읽어오기
    image = cv2.imread(image_path)
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

    print('Step 1: Edge Detection')

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Edged', cv2.WINDOW_NORMAL)
    cv2.imshow('image', image)
    cv2.imshow('edged', edged)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # contour 반환
    (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # contour를 외곽이 그린 면적이 큰 순대로 정렬해 최대 5개 추출
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

    # contour를 순회하면서
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

    print('Step2: Find contours of paper')

    # contour 그리기
    cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
    cv2.imshow('outline', image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

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

    print('Step3: Apply Perspective Transform')
    cv2.imshow('warped', warped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return warped


def text_detection(image):
    orig = image.copy()             # 원본 이미지 복사

    # 이미지 전처리
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)     # 바이너리 이미지로 변환
    erosion = cv2.erode(gray, np.ones((2, 2), np.uint8), iterations=1)   # Erosion(침식): 바이너리 이미지에서 흰색(1) 오브젝트의 외곽픽셀을 검은색(0)으로 만든다.
    dilate = cv2.dilate(gray, np.ones((2, 2), np.uint8), iterations=1)   # Dilate(팽창): 바이너리 이미지에서 검은색(0) 오브젝트의 외곽픽셀을 횐색(1)으로 만든다.
    image = cv2.subtract(dilate, erosion)    # Morph Gradient = dilate - erosion
    cv2.imshow('Morph Gradient', image)
    cv2.waitKey(0)
    cv2.destroyWindow('Morph Gradient')

    mean = cv2.mean(image)

    _, image = cv2.threshold(image, mean[0]*6, 255, cv2.THRESH_BINARY)     # global threshold: 신분증 배경을 제거하기 위해
    cv2.imshow('Threshold', image)
    cv2.waitKey(0)
    cv2.destroyWindow('Threshold')
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 5, 5)
    cv2.imshow('Adaptive Threshold', image)
    cv2.waitKey(0)
    cv2.destroyWindow('Adaptive Threshold')
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel=np.ones((3, 30)), iterations=1)
    cv2.imshow('Morph Close', image)
    cv2.waitKey(0)
    cv2.destroyWindow('Morph Close')

    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boxes = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        if w < 23 or h < 23: continue

        cv2.rectangle(orig, (x, y), (x+w, y+h), (0, 255, 0), 2)
        boxes.append((x, y, w, h))
        # cv2.imshow('Box', gray[y:y+h, x:x+w])
        # cv2.waitKey(0)
        # cv2.destroyWindow('Box')

    cv2.imshow('Contour', orig)
    cv2.waitKey(0)
    cv2.destroyWindow('Contour')

    return boxes


def text_recognition(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.erode(gray, np.ones((2, 2), np.uint8), iterations=1)
    config = '-l kor --oem 3 --psm 6'
    result = pytesseract.image_to_string(image, config=config)
    cv2.imshow('Text Image', image)
    cv2.waitKey(0)
    cv2.destroyWindow('Text Image')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image_path', help='이미지 경로')
    args = parser.parse_args()

    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

    id_card = image_detection(args.image_path)
    boxes = text_detection(id_card)
    for x, y, w, h in boxes:
        print(text_recognition(id_card[y:y+h, x:x+w]))