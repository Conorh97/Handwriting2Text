import cv2
import os
import numpy as np

DOWNLOAD_DIRECTORY = '{}/tmp-images'.format(os.getcwd())


def round_down(num, divisor):
    return num - (num % divisor)


def remove_shadow(image):
    rgb_planes = cv2.split(image)

    result_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((5, 5), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        result_planes.append(diff_img)

    return cv2.merge(result_planes)


def process_image(filename):
    image = cv2.imread('{}/{}'.format(DOWNLOAD_DIRECTORY, filename))
    image = cv2.resize(image, None, fx=0.5, fy=0.5)
    image = remove_shadow(image)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    th, threshed = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (6, 3))
    dilated = cv2.dilate(threshed, kernel, iterations=2)

    components = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    j = 0
    for component in sorted(components, key=lambda c: (round_down(c.tolist()[0][0][1], 20), c.tolist()[0][0][0])):
        if cv2.contourArea(component) < 300:
            continue

        (x, y, w, h) = cv2.boundingRect(component)
        word = image[y - 5:y + h + 5, x - 5:x + w + 5]
        cv2.imwrite('{}/{}-{}'.format(DOWNLOAD_DIRECTORY, j, filename), word)
        j += 1