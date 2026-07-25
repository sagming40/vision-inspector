# generate_sample.py
# 목적: 카메라 없이 테스트용 "가짜 검사 이미지"를 만든다.
# 비유: 실제 공장 라인 카메라가 없으니, 대신 그 역할을 해줄 모형(mock)을 손으로 그리는 것.

import numpy as np
from PIL import Image, ImageDraw
import random

WIDTH, HEIGHT = 1920, 1080

def make_sample(path: str, seed: int = 42):
    # 랜덤 시드 고정 : 매번 같은 이미지가 나와야 벤치마크 조건이 일정해진다.
    # 비유: 실험할 때마다 다른 시약을 쓰면 결과 비교가 무의미해지는것과 같음.
    random.seed(seed)
    
    # 배경: 회색 금속 표면 느낌 (완전 단색이면 너무 쉬워서 노이즈를 살짝 섞는다.)
    img = Image.new("RGB", (WIDTH, HEIGHT), (180, 180, 180))
    draw = ImageDraw.Draw(img)
    
    # 결함 후보 = 어두운 원/타원 몇 개를 무작위 위치에 그린다.
    # 비유: 실제 불량품의 스크래치/이물질 자리를 대신하는 스탠드인(stand-in) 배우들.
    defect_count = random.randint(5, 15)
    for _ in range(defect_count):
        cx, cy = random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)
        r = random.randint(5, 40)
        gray = random.randint(20, 80) # 배경보다 확실히 어둡게 -> 나중에 threshold로 구분
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(gray, gray, gray))
        
    img.save(path)
    print(f"saved: {path} (defects placed: {defect_count})")

if __name__ == "__main__":
    make_sample("../samples/test_1920x1080.png")
            