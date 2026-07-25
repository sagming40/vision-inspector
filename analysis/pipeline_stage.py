# pipeline_stage.py
# 목적: 파이프라인의 개별 단계를 함수 하나씩 분리해서 담아두는 곳.
# 지금은 "④ 그레이스케일" 하나만 있음. 나중에 블러/이진화/모폴로지도 여기 추가될 예정.

import cv2
import numpy as np


def grayscale_cv2(img: np.ndarray) -> np.ndarray:
    """
    3채널 컬러 이미지(BGR) -> 1채널 흑백 이미지로 변환.
    cv2.cvtColor는 OpenCV의 표준 함수 -> C++ 코드를 그대로 호출하는 것.
    Python에서 호출했다고 해도 실제 연산은 C++ 기계어가 처리한다. (가설 H1의 근거) 
    """
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def blur_cv2(img: np.ndarray) -> np.ndarray:
    """
    노이즈 제거용 가우시안 블러.
    입력은 반드시 ④ 그레이스케일을 거친 1채널 이미지여야 한다.
    (3채널 컬러를 넣으면 채널 별로 따로 블러가 걸려서 결과가 달라짐 — 순서 지켜야 함)
    """
    # (5, 5) = 블러 계산할 때 주변 몇 픽셀까지 볼지 정하는 창(window) 크기.
    # 홀수여야 함 — 중심 픽셀이 정확히 하나 있어야 "주변 평균" 개념이 성립하니까.
    # 0 = 표준편차를 커널 크기로부터 OpenCV가 알아서 계산하게 둔다는 뜻.
    return cv2.GaussianBlur(img, (5, 5), 0)


def threshold_cv2(img: np.ndarray) -> np.ndarray:
    """
    그레이스케일(블러 적용된) 이미지를 흑백 이진 이미지로 변환.
    입력은 ⑤ 블러를 거친 1채널 이미지여야 한다.
    
    우리 샘플 이미지 특성: 배경 밝기 180, 결함 밝기 20 ~ 80 대역.
    -> 임계값 128을 기준으로 잡으면 배경/결함이 확실히 갈린다.
    """
    # threshold(입력, 임계값, 임계값을 넘었을 때 줄 값, 방식)
    # THRESH_BINARY_INV = "임계값보다 어두우면 흰색(255), 밝으면 검은색(0)"
    #                   -> 결함(어두움)을 흰색으로 만드는 이유: 나중에 ⑧번에서
    #                      "흰 픽셀 = 결함 후보"로 세는 게 직관적이라서.
    # 반환값이 두 개(실제 사용된 임계값, 결과 이미지)이기 때문에 앞에 _로 첫 번째는 버림.
    _, binary = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)
    return binary  


def morphology_cv2(img: np.ndarray) -> np.ndarray:
    """
    이진화 결과의 잡티를 제거하고 구멍을 메운다.
    입력은 ⑥ 이진화를 거친 흑백(0/255) 이미지여야 한다.
    
    MORPH_OPEN  = 침식 후 팽창 (작은 흰 잡티 제거)
    MORPH_CLOSE = 팽창 후 침식 (덩어리 안 작은 구멍 메움)
    둘 다 적용해서 "잡티도 없고 구멍도 없는" 깨끗한 덩어리로 만든다.
    """
    # 커널(kernel) = 침식/팽창할 때 "어느 범위를 기준으로 깎고 부풀릴지" 정하는 도장 모양.
    # (5, 5) 정사각형 커널이면 픽셀 하나 기준으로 주변 5x5 영역을 본다는 뜻.
    kernel = np.ones((5, 5), np.uint8)
    
    # 1단계: OPEN — 자잘한 흰 잡티(노이즈) 제거
    opened = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    
    # 2단계: CLOSE — 덩어리 안 쪽의 작은 구멍 메움
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)
    
    return closed
    