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
    