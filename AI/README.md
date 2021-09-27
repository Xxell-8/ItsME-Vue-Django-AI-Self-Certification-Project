## AI 기초 구현



#### 1. ImageDetect (세라)

- `imageDetect.py` : 저장된 이미지를 불러와 신분증(카드) 부분 추출
- `objectDetect.py`: 실시간 웹캠 촬영을 통해 신분증(카드) 부분 추출
  - 아직 구현 안 된 상태입니다요!
- `ocr.py` : pytesseract 활용해서 한글 OCR 추출
  - 추출은 되는데, 정확성은 떨어집니당 ~



#### 2. OCR (기웅)

- 사용법

  터미널 창에

```
$ python ocr.py <신분증 이미지 경로>
```

​	입력하시면 단계별로 이미지와 결과가 출력됩니다. Esc를 누르면 이미지창이 닫히고 다음 단계로 넘어갑니다.



- `ocr.py`
  - `image_detection`
    - 세라님의 `imageDetect.py`의 코드와 동일
    - 저장된 이미지를 불러와 신분증(카드) 부분 추출
    - 경계선으로 신분증을 찾기때문에 배경에 줄무늬가 없어야 잘 나옵니다.
  - `text_detection`
    - tesseract를 활용했고 이미지 전처리를 통해 정확도를 높였습니다.
    - 빛의 밝기, 반사에 따라 결과가 다르게 나옵니다.
  - `text_recognition`
    - tesseract를 활용하여 한글을 인식
    - 정확도를 올릴 필요가 있습니다.

