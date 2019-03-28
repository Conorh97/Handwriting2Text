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

    (cx, cy) = rectangle[0]

    matrix = cv2.getRotationMatrix2D((cx, cy), 0, 1.0)
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
            cropped = rotated[uppers[i] - 15:lowers[i] + 50, 0:width]
            cropped_thresh = cv2.threshold(cropped, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            components = cv2.findContours(cropped_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
            word_dims = []
            for component in components:
                if cv2.contourArea(component) < 100:
                    continue
                (x, y, w, h) = cv2.boundingRect(component)
                word_dims.append((x, y, w, h))

            word_dims.sort(key=lambda entry: entry[0])
            words = []
            start_x = 0
            x = 0
            y = 0
            w = 0
            h = 0
            for i, word in enumerate(word_dims):
                if x == 0 and y == 0 and w == 0 and h == 0:
                    x, _, w, h = word
                    start_x = x
                else:
                    if word_dims[i][0] - (word_dims[i - 1][0] + word_dims[i - 1][2]) >= 30:
                        word_image = cropped[y:y + h + 50, start_x - 10:start_x + w + 10]
                        words.append([(start_x, y, w, h), word_image])
                        x, _, w, h = word
                        start_x = x
                    x = word[0]
                    w += word[2]
                    if word[1] < h:
                        h = word[3]
                    if word[3] > h:
                        h = word[3]
                    if i == len(word_dims) - 1:
                        word_image = cropped[y:y + h + 50, start_x - 10:start_x + w + 10]
                        words.append([(start_x, y, w, h), word_image])

            for word in words:
                cv2.imwrite('{}/{}-{}'.format(DOWNLOAD_DIRECTORY, j, filename), word[1])
                j += 1
