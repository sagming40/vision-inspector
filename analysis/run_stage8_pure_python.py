# run_stage8_pure_python.py
# 목적: "⑧ 블롭 · 면적 계산" 순수 반복문 버전(A) — 일단 1회만 실행해서 소요 시간 가늠.

import time
import cv2
from pipeline_stage import grayscale_cv2, blur_cv2, threshold_cv2, morphology_cv2, blob_area_pure_python

img = cv2.imread("../samples/test_1920x1080.png")

if img is None:
    raise FileNotFoundError("이미지를 불러오지 못했습니다. 경로/파일명을 확인해 보세요.")

# --- ④~⑦ 전처리는 이미 검증된 cv2 버전으로 미리 다 끝내놓는다 ---
# ⑧번만 순수 반복문으로 측정함. 앞 단계는 측정 범위에서 제외.
gray = grayscale_cv2(img)
blurred = blur_cv2(gray)
binary = threshold_cv2(blurred)
morphed = morphology_cv2(binary)
print(f"전처리 완료: shape={morphed.shape}, dtype={morphed.dtype}")

# --- 딱 1회만 실행하면서 시간 측정 ---
print("블롭 검출 시작... (시간이 좀 걸릴 수 있음)")
start = time.perf_counter()
areas = blob_area_pure_python(morphed)
end = time.perf_counter()

elapsed_ms = (end - start) * 1000
print(f"소요 시간: {elapsed_ms:.2f} ms")
print(f"검출된 블롭 개수: {len(areas)}")
print(f"각 블롭 면적: {areas}") 
 