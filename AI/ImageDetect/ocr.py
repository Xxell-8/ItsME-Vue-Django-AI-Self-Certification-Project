import cv2
from PIL import Image
import pytesseract

# tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

def ocr_tesseract():
    img = cv2.imread('ocr_sample.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    custom_config = r'--psm 11 --oem 3'
    text = pytesseract.image_to_string(gray, lang='kor', config=custom_config)

    print(text)

if __name__ == '__main__':
    ocr_tesseract()