import cv2
import numpy as np
import random
import os
# 한글이 깨져서 pip install pillow 하여 PIL 사용
from PIL import ImageFont, ImageDraw, Image

# 랜덤 이름 제작
first_name_samples = "김이박최정강조윤장임한오서신권황안송전홍유고문양손배백허남심노"
middle_name_samples = "민서예지도하주윤채현지유승시재수한은"
last_name_samples = "준윤우원호후서연아은진재린율영인빈"


def random_name():
    result = ""
    result += random.choice(first_name_samples)
    result += random.choice(middle_name_samples)
    result += random.choice(last_name_samples)
    return result


# 랜덤 주민번호 제작
def random_num():
    result = ""
    result += str(random.randrange(100000, 1000000))
    result += " - "
    result += str(random.randrange(1000000, 10000000))
    return result


# 폴더의 모든 사진 불러오기
def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images


# 이름, 주민번호에 사용될 폰트 불러오기
font = ImageFont.truetype('fonts\\KoPubBatangMedium.ttf', 20)
numfont = ImageFont.truetype('fonts\\gulim.ttf', 15)


images = load_images_from_folder('data\\faces\\archive')

for idx in range(len(images)):
    
    # 민증 템플릿 불러오기
    template = cv2.imread('data\\min.jpg')
    # 얼굴사진 빈칸에 맞게 리사이즈 
    reimg = cv2.resize(images[idx], dsize=(130, 159), interpolation=cv2.INTER_CUBIC)

    rows, cols, channels = reimg.shape # 픽셀값 저장

    # 빈칸 위치에 얼굴사진 넣기
    template[15:rows+15,230:cols+230] = reimg 

    # 이미지에 글자 넣는 과정
    img = Image.fromarray(template)
    draw = ImageDraw.Draw(img)

    name = random_name()
    num = random_num()
    # 이름 넣기
    draw.text((82, 63), name, font=font, fill=(0, 0, 0))
    # 주민번호 넣기
    draw.text((50, 94), num, font=numfont, fill=(0, 0, 0))

    img = np.array(img)
    # 인덱스 앞에 0으로 채워서 4자리 맞추기
    fileno = str(idx).rjust(4, '0')
    cv2.imwrite(f'results\\{fileno}.jpg', img)
    cv2.waitKeyEx()
    cv2.destroyAllWindows()