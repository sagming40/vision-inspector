# diagnose_stage8_iterations.py
# 목적: blob_area_numpy의 전파 루프가 실제로 몇 번 반복하고 멈추는지 확인.
# (정식 함수는 그대로 두고, 반복 횟수 세는 카운터만 추가한 진단용 복제본)

import cv2
import numpy as np
from pipeline_stage import grayscale_cv2, blur_cv2, threshold_cv2, morphology_cv2

img = cv2.imread("../samples/test_1920x1080.png")
gray = grayscale_cv2(img)
blurred = blur_cv2(gray)
binary = threshold_cv2(blurred)
morphed = morphology_cv2(binary)

height, width = morphed.shape
labels = np.arange(height * width, dtype=np.int64).reshape(height, width)
labels = np.where(morphed == 255, labels, np.iinfo(np.int64).max)

iteration_count = 0  # <- 여기가 추가된 부분

for _ in range(max(height, width)):
    iteration_count += 1  # <- 여기도 추가된 부분
    
    shifted = np.full_like(labels, np.iinfo(np.int64).max)
    shifted[1:, :] = labels[:-1, :]
    new_labels = np.minimum(labels, shifted)

    shifted = np.full_like(labels, np.iinfo(np.int64).max)
    shifted[:-1, :] = labels[1:, :]
    new_labels = np.minimum(new_labels, shifted)

    shifted = np.full_like(labels, np.iinfo(np.int64).max)
    shifted[:, 1:] = labels[:, :-1]
    new_labels = np.minimum(new_labels, shifted)

    shifted = np.full_like(labels, np.iinfo(np.int64).max)
    shifted[:, :-1] = labels[:, 1:]
    new_labels = np.minimum(new_labels, shifted)

    new_labels = np.where(morphed == 255, new_labels, np.iinfo(np.int64).max)

    if np.array_equal(new_labels, labels):
        break
    labels = new_labels

print(f"실제 반복 횟수: {iteration_count}회 (최대 가능 횟수: {max(height, width)}회)")
