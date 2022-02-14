import cv2, imutils
from time import sleep
import scrcpy
from scrcpy import const
import random
import numpy as np
import glob, os

# color_hue = {'R':(0, 10), 'G':(45, 70), 'B':(95, 110), 'L':(12.5, 25), 'D':(140, 155), 'H':(155, 175)}
y_offset = 1315 # POCO X3 pro = 1315
screen_size = (2400, 1080)
tile_size = int(screen_size[1]/6)

rune_files = glob.glob('image/*.png')
rune_ref = {}
for file in rune_files:
    name = os.path.basename(file).split('.')[0] # get file name without extension
    img = cv2.imread(file)
    hist = cv2.calcHist([img], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    rune_ref[name] = (img, hist)

def classify_rune(img, method = 0):
    hist = cv2.calcHist([img], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    scores = {}
    for rune, (rune_img, rune_hist) in rune_ref.items():
        if method == 0: score = cv2.compareHist(hist, rune_hist, cv2.HISTCMP_CORREL)# cv2.HISTCMP_CORREL: Computes the correlation between the two histograms.
        elif method == 1: score = cv2.compareHist(hist, rune_hist, cv2.HISTCMP_CHISQR)# cv2.HISTCMP_CHISQR: Applies the Chi-Squared distance to the histograms.
        elif method == 2: score = cv2.compareHist(hist, rune_hist, cv2.HISTCMP_INTERSECT)# cv2.HISTCMP_INTERSECT: Calculates the intersection between two histograms.
        else: score = cv2.compareHist(hist, rune_hist, cv2.HISTCMP_BHATTACHARYYA)# cv2.HISTCMP_BHATTACHARYYA: Bhattacharyya distance, used to measure the “overlap” between the two histograms.
        scores[rune] = score
    return max(scores, key=lambda k: scores[k])

def get_rune(img, rune=True):
    global screen_size
    tile_list = []
    for y in range(5):
        row_buffer = []
        for x in range(6):
            tile = img[y * tile_size:(y + 1) * tile_size, x * tile_size:(x + 1) * tile_size]
            if not rune: row_buffer.append(tile)
            else: row_buffer.append(classify_rune(tile))
        tile_list.append(row_buffer)
    return tile_list


cap = cv2.VideoCapture('/dev/video2')
while True:
    frame = cap.read()[1]
    # frame = imutils.resize(frame, height=int(2400/3))
    frame = frame[y_offset:y_offset+int(screen_size[1]/6*5), :] # 1080*900
    cv2.imshow("A", imutils.resize(frame, height=512))
    key = cv2.waitKey(1)
    if key == 27: break
    elif key == ord(' '):
        rune = get_rune(frame)
        print(rune)

cv2.destroyAllWindows()