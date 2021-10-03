import cv2
import base64
import numpy as np
import string
import random


# base64 -> OpenCV image
def base64_to_image(image_base64):
    image_base64 = image_base64.split('base64,')[1]
    image_bytes = base64.b64decode(image_base64)
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    return cv2.imdecode(image_array, flags=cv2.IMREAD_COLOR)


# image -> base64
def image_to_base64(image_path):
    with open(image_path, 'rb') as f:
        image_base64 = base64.b64encode(f.read())
    return f'data:image/jpeg;base64,{image_base64.decode("utf-8")}'


def get_random_string(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


if __name__ == '__main__':
    image_path = 'E:/sample1.jpg'
    
    image_base64 = image_to_base64(image_path)

    with open('E:/sample1_to_base64.txt', 'w') as f:
        f.write(image_base64)
    