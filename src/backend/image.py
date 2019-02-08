import cv2
import os

DOWNLOAD_DIRECTORY = '{}/tmp-images'.format(os.getcwd())


def process_image(filename):
    image = cv2.imread('{}/{}'.format(DOWNLOAD_DIRECTORY, filename))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    th, threshed = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    pts = cv2.findNonZero(threshed)
    rectangle = cv2.minAreaRect(pts)

    (cx, cy) = rectangle[0]
    (width, height) = rectangle[1]
    angle = rectangle[2]

    if width > height:
        angle += 90

    matrix = cv2.getRotationMatrix2D((cx, cy), angle, 1.0)
    rotated = cv2.warpAffine(threshed, matrix, (image.shape[1], image.shape[0]))
    hist = cv2.reduce(rotated, 1, cv2.REDUCE_AVG).reshape(-1)

    th = 2
    height, width = image.shape[:2]

    uppers = [x for x in range(height - 1) if hist[x] <= th and hist[x + 1] > th]
    lowers = [x for x in range(height - 1) if hist[x] > th and hist[x + 1] <= th]

    rotated = cv2.bitwise_not(rotated)

    for i in range(len(uppers)):
        cropped = rotated[uppers[i]:lowers[i], 0:255]
        cv2.imwrite('{}/{}-{}'.format(DOWNLOAD_DIRECTORY, i, filename), cropped)

