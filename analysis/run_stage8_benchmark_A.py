# run_stage8_benchmark_A.py
# 목적: "⑧ 블롭·면적 계산" 순수 반복문 버전(A)을 정식 프로토콜(워밍업10/실측100)로 측정.
# 주의: 1회 150ms대 걸리는 연산이라, 110회 돌리면 총 15~20초 정도 걸림. 창 닫지 말고 대기.

import cv2
from benchmark import run_benchmark, print_stats
from pipeline_stage import grayscale_cv2, blur_cv2, threshold_cv2, morphology_cv2, blob_area_pure_python

img = cv2.imread("../samples/test_1920x1080.png")

if img is None:
    raise FileNotFoundError("이미지를 불러오지 못했습니다. 경로/파일명을 확인해 보세요.")

# --- ④~⑦ 전처리는 측정 범위 밖 (⑧번만 측정하므로 미리 끝내놓는다) ---
gray = grayscale_cv2(img)
blurred = blur_cv2(gray)
binary = threshold_cv2(blurred)
morphed = morphology_cv2(binary)
print(f"전처리 완료: shape={morphed.shape}, dtype={morphed.dtype}")

if __name__ == "__main__":
    print("정식 측정 시작 (워밍업 10회 + 실측 100회, 15 ~ 20초 소요 예상)...")
    stats = run_benchmark(
        blob_area_pure_python,
        args=(morphed,),
        label="pure_python_blob_1920x1080"
    )
    print_stats(stats)
