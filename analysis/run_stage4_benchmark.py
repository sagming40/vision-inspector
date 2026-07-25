# run_stage4_benchmark.py
# 목적: "④ 그레이스케일" 단계 하나만 떼어서 벤치마크 하네스에 넣어 측정.

import cv2
from benchmark import run_benchmark, print_stats
from pipeline_stage import grayscale_cv2

# --- 이미지 로딩은 벤치마크 '시작 전' 최초 1회 만 ---
# 비유: 요리 실력을 잴 때 장보기 시간은 재지 않는 것과 같은 이유.
img = cv2.imread("../samples/test_1920x1080.png")

if img is None:
    # 파일 경로가 틀렸거나 파일이 존재하지 않을 경우 cv2.inread는 에러를 던지지 않고
    # 조용히 None을 돌려준다. 따라서, 여기서 직접 확인해야 함.
    raise FileNotFoundError("이미지를 불러오지 못했습니다. 경로/파일명을 확인해 보세요.")

print(f"이미지 로드 완료: shape={img.shape}")  # (1080, 1920, 3)이 출력 되야 정상

if __name__ == "__main__":
    stats = run_benchmark(
        grayscale_cv2,
        args=(img,),
        label="cv2_grayscale_1920x1080"
    )
    print_stats(stats)
     