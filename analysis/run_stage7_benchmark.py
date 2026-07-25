# run_stage7_benchmark.py
# 목적: "⑦ 모폴로지" 단계 하나만 떼어서 벤치마크 하네스에 넣어 측정.

import cv2
from benchmark import run_benchmark, print_stats
from pipeline_stage import grayscale_cv2, blur_cv2, threshold_cv2, morphology_cv2

img = cv2.imread("../samples/test_1920x1080.png")

if img is None:
    raise FileNotFoundError("이미지를 불러오지 못했습니다. 경로/파일명을 확인해 보세요")

# --- 모폴로지는 ⑥번 결과(이진화된 흑백 이미지)를 입력으로 받는다 ---
gray = grayscale_cv2(img)
blurred = blur_cv2(gray)
binary = threshold_cv2(blurred)
print(f"이진화 준비 완료: shape={binary.shape}, dtype={binary.dtype}")

if __name__ == "__main__":
    stats = run_benchmark(
        morphology_cv2,
        args=(binary,),
        label="cv2_morphology_1920x1080"
    )
    print_stats(stats)
    
    # --- 눈으로 확인용 ---
    morph_result = morphology_cv2(binary)
    cv2.imwrite("test_morph.png", morph_result)
    print("검증용 이미지 저장됨: test_morph.png") 
