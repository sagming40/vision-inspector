# run_stage5_benchmark.py
# 목적: "⑤ 블러" 단계 하나만 떼어서 벤치마크 하네스에 넣어 측정.

import cv2
from benchmark import run_benchmark, print_stats
from pipeline_stage import grayscale_cv2, blur_cv2

img = cv2.imread("../samples/test_1920x1080.png")

if img is None:
    raise FileNotFoundError("이미지를 불러오지 못했습니다. 경로/파일명을 확인해보세요.")

# --- 중요: 블러는 ④번 결과(그레이스케일)를 입력으로 받는다 ---
# 벤치마크 '시작 전'에 미리 그레이스케일까지만 해놓는다.
# 이유는 ④ 때와 같음 — "이 단계 자체"만 측정함. 앞 단계 측정까지 포함하면 안됨.
gray = grayscale_cv2(img)
print(f"그레이스케일 준비 완료: shape={gray.shape}")  # (1080, 1920) — 채널 축 없어진 것 확인

if __name__ == "__main__":
    stats = run_benchmark(
        blur_cv2,
        args=(gray,),
        label="cv2_blur_1920x1080"
    )
    print_stats(stats)
