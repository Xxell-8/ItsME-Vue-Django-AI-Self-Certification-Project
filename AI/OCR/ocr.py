from imutils.object_detection import non_max_suppression
import pytesseract
import cv2
import time
import numpy as np

min_confidence = 0.5
width, height = 320, 320

def text_detection(file_name):
    # 이미지 load
    image = cv2.imread(file_name)
    orig = image.copy()
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)     # gray scale로 변경
    # _ ,image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    # image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    cv2.imshow('Image Binarization', image)
    cv2.waitKey(0)
    print(image.shape)
    h, w = image.shape[:2]

    # 새로운 width, height 설정
    new_h, new_w = width, height
    ratio_w = w / float(new_w)
    ratio_h = h / float(new_h)

    # 이미지 resize
    image = cv2.resize(image, (new_w, new_h))
    h, w = image.shape[:2]

    # EAST text detector model의 layer를 정의
    layer_names = [
        'feature_fusion/Conv_7/Sigmoid',
        'feature_fusion/concat_3'
    ]

    # 미리 학습된 EAST text detector 불러오기
    print("[INFO] loading EAST text detector...")
    net = cv2.dnn.readNet('./frozen_east_text_detection.pb')

    # blob 객체로 생성 및 forward 실행
    blob = cv2.dnn.blobFromImage(image, 1.0, (w, h), (123.68, 116.78, 103.94), swapRB=True, crop=False)
    start = time.time()
    net.setInput(blob)
    scores, geometry = net.forward(layer_names)
    end = time.time()
    print("[INFO] text detection took {:.6f} seconds".format(end - start))

    # bounding box의 좌표와 확률값 저장
    # 초기화
    num_rows, num_cols = scores.shape[2:]
    rects = []          # box의 좌표 저장
    confidences = []    # box의 확률 저장

    for y in range(num_rows):
        scores_data = scores[0, 0, y]
        x_data0 = geometry[0, 0, y]
        x_data1 = geometry[0, 1, y]
        x_data2 = geometry[0, 2, y]
        x_data3 = geometry[0, 3, y]
        angle_data = geometry[0, 4, y]

        for x in range(num_cols):
            if scores_data[x] < min_confidence: continue

            offset_x, offset_y = x * 4.0, y * 4.0

            angle = angle_data[x]
            cos = np.cos(angle)
            sin = np.sin(angle)

            h = x_data0[x] + x_data2[x]
            w = x_data1[x] + x_data3[x]

            end_x = int(offset_x + (cos * x_data1[x]) + (sin * x_data2[x]))
            end_y = int(offset_y + (sin * x_data1[x]) + (cos * x_data2[x]))
            start_x = int(end_x - w)
            start_y = int(end_y - h)

            rects.append((start_x, start_y, end_x, end_y))
            confidences.append(scores_data[x])

    # Non-Maximum Suppression(NMS) 적용
    # NMS: 곂쳐져 있는 검출 박스를 제거하는 방법
    boxes = non_max_suppression(np.array(rects), probs=confidences)

    for start_x, start_y, end_x, end_y in boxes:
        start_x = int(start_x * ratio_w)
        start_y = int(start_y * ratio_h)
        end_x = int(end_x * ratio_w)
        end_y = int(end_y * ratio_h)
        # 이미지에 bounding box 추가
        cv2.rectangle(orig, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

    cv2.imshow('Text Detection', orig)
    cv2.waitKey(0)

    return boxes

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

def text_recognition(file_name):
    config = '-l kor --oem 3 --psm 4'
    image = cv2.imread(file_name)
    result = pytesseract.image_to_string(image, config=config)
    return result


if __name__ == '__main__':
    print(text_detection('./warped_sample.jpg'))
    # print(text_recognition('./warped_sample.jpg'))