# run_stage6_benchmark.py
# 목적: "⑥ 이진화" 단계 하나만 떼어서 벤치마크 하네스에 넣어 측정.

import cv2
from benchmark import run_benchmark, print_stats
from pipeline_stage import grayscale_cv2, blur_cv2, threshold_cv2

img = cv2.imread("../samples/test_1920x1080.png")

if img is None:
    raise FileNotFoundError("이미지를 불러오지 못했습니다. 경로/파일명을 확인해 보세요.")

# --- 이진화는 ⑤번 결과(블러 처리된 그레이스케일)를 입력으로 받는다 ---
gray = grayscale_cv2(img)
blurred = blur_cv2(gray)
print(f"블러 준비 완료: shape={blurred.shape}, dtype={blurred.dtype}")

if __name__ == "__main__":
    stats = run_benchmark(
        threshold_cv2,
        args=(blurred,),
        label="cv2_threshold_1920x1080"
    )
    print_stats(stats)

# --- 눈으로 확인용: 정식 파이프라인 로직엔 필요 없음 ---
# 이진화 결과가 실제로 배경/결함을 잘 나눴는지 이미지로 저장해서 확인.
binary_result = threshold_cv2(blurred)
cv2.imwrite("test_binary.png", binary_result)
print("검증용 이미지 저장됨: test_binary.png")
    