import cv2
import os
import numpy as np

DOWNLOAD_DIRECTORY = '{}/tmp-images'.format(os.getcwd())


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
    image = remove_shadow(image)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    th, threshed = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    pts = cv2.findNonZero(threshed)
    rectangle = cv2.minAreaRect(pts)

    print(rectangle)
    (cx, cy) = rectangle[0]
    (width, height) = rectangle[1]
    angle = rectangle[2]

    #if width > height:
    #    angle += 90
    #elif angle < 0:

    angle = 0

    matrix = cv2.getRotationMatrix2D((cx, cy), angle, 1.0)
    rotated = cv2.warpAffine(threshed, matrix, (image.shape[1], image.shape[0]))
    hist = cv2.reduce(rotated, 1, cv2.REDUCE_AVG).reshape(-1)

    th = 9
    height, width = image.shape[:2]

    uppers = [x for x in range(height - 1) if hist[x] <= th and hist[x + 1] > th]
    lowers = [x for x in range(height - 1) if hist[x] > th and hist[x + 1] <= th]

    if uppers[0] > lowers[0]:
        uppers = [0] + uppers

    rotated = cv2.bitwise_not(rotated)

    j = 0
    for i in range(len(lowers)):
        if abs(uppers[i] - lowers[i]) > 32:
            cropped = rotated[uppers[i] - 5:lowers[i] + 5, 0:width]
            cv2.imwrite('{}/{}-{}'.format(DOWNLOAD_DIRECTORY, j, filename), cropped)
            j += 1

    cv2.imwrite('{}/{}-{}'.format(DOWNLOAD_DIRECTORY, "processed", filename), rotated)