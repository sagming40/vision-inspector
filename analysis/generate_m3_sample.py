# generate_m3_sample.py
# M3 테스트용 작은 흑백 이미지 생성 — 반전 전/후 차이가 눈에 확 띄게 설계

import cv2
import numpy as np

# 300x300 크기, 회색(128)로 배경 채움
# np.full: "이 크기만큼 전부 이 값으로 채워라" — 페인트 롤러로 벽 전체 칠하는 것과 비슷
img = np.full((300, 300), 128, dtype=np.uint8)

# 흰 사각형 — 반전되면 검게 바뀔 자리
cv2.rectangle(img, (50, 50), (150, 150), 255, -1)

# 검은 원 — 반전되면 하얗게 바뀔 자리
cv2.circle(img, (200, 200), 50, 0, -1)

cv2.imwrite("../samples/test_m3_small.png", img)
print("생성 완료: samples/test_m3_small.png")
