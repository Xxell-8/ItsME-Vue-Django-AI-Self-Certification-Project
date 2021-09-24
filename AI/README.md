## AI 기초 구현



#### 1. ImageDetect (세라)

- `imageDetect.py` : 저장된 이미지를 불러와 신분증(카드) 부분 추출
- `objectDetect.py`: 실시간 웹캠 촬영을 통해 신분증(카드) 부분 추출
  - 아직 구현 안 된 상태입니다요!
- `ocr.py` : pytesseract 활용해서 한글 OCR 추출
  - 추출은 되는데, 정확성은 떨어집니당 ~

#### 2. OCR (기웅)

- `ocr.py`
  - `east_text_detection`
    - EAST text detextor를 활용한 text detection
    - 영어로 학습된 모델을 사용해서 한글 detection은 부정확한 것 같습니다.
  - `text_detection`
    - tesseract를 활용했고 이미지 전처리를 통해 정확도를 높였습니다.
  - `text_recognition`
    - tesseract를 활용하여 한글을 인식
    - 정확도를 올릴 필요가 있습니다.