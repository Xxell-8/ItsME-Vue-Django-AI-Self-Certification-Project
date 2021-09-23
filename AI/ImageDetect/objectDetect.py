import numpy as np
import cv2

def order_points(pts):
    rect = np.zeros((4, 2), dtype=np.float32)

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect


def auto_scan():
    try:
        # 카메라 불러오기
        cam = cv2.VideoCapture(0)
    except:
        print('Cannot load Camera!')
    
    while True:
        ret, frame = cam.read()
        if not ret:
            print('Cannot load Camera!')
            break

        k = cv2.waitKey(10)
        # ESC 키 입력 시, break
        if k == 27:
            break
        
        # 흑백 변환
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 블러로 노이즈 제거
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        # 이미지 가장자리 검출
        edged = cv2.Canny(gray, 75, 200)

        print('Step 1: Edge Detection')

        (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            screenCnt = []

            if len(approx) == 4:
                contourSize = cv2.contourArea(approx)
                camSize = frame.shape[0] * frame.shape[1]
                ratio = contourSize / camSize

                if ratio > 0.1:
                    screenCnt = approx
                break
        
        if len(screenCnt) == 0:
            cv2.imshow('webcam', frame)
            continue
        else:
            print('Step2: Find contours of paper')

            cv2.drawContours(frame, [screenCnt], -1, (0, 255, 0), 2)
            cv2.imshow('webcam', frame)

            rect = order_points(screenCnt.reshape(4, 2))
            (tl, tr, br, bl) = rect
            widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
            widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
            # compute the height of the new image
            heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
            heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
            # take the maximum of the width and height values to reach
            # our final dimensions
            maxWidth = max(int(widthA), int(widthB))
            maxHeight = max(int(heightA), int(heightB))

            dst = np.float32([[0, 0], [maxWidth-1, 0], [maxWidth-1, maxHeight-1], [0, maxHeight-1]], dtype=np.float32)

            M = cv2.getPerspectiveTransform(rect, dst)
            warped = cv2.warpPerspective(frame, M, (maxWidth, maxHeight))

            print('Step3: Apply Perspective Transform')
            break

    cam.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)

    cv2.imshow('Scanned', warped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    auto_scan()