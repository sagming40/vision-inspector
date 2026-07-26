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


def blob_area_pure_python(binary_img: np.ndarray) -> list:
    """
    이진화된 흑백 이미지(0/255)에서 서로 붙어있는 흰 덩어리(블롭)를 찾아
    각 덩어리의 면적(픽셀 개수)을 리스트로 돌려준다.
    cv2.findContours()를 안 쓰고 순수 반복문으로 직접 구현한 버전 (A안 — 최악 기준선)
    
    비유: 강당에 흩어진 사람들 중 "어깨 맞닿은 사람들끼리 같은 팀" 으로 묶어서 
    팀별 인원수를 세는 것과 같음. 
    """
    height, width = binary_img.shape  # 이미지 세로/가로 픽셀 수
    
    # --- 1. "이 픽셀에 라벨(팀 번호)을 붙였나 붙이지 않았나"를 기록학 도화지 ---
    # 처음엔 전부 0(라벨 없음)으로 채운다. 원본이랑 똑같은 크기로 만든다.
    labels = np.zeros((height, width), dtype=np.int32)
    
    current_label = 0       # 지금까지 몇 번째 덩어리를 찾았는지
    areas = []              # 각 덩어리(라벨)별 면적(픽셀 개수)을 담을 리스트
    
    # --- 2. 이미지의 모든 픽셀을 위에서 아래로, 왼쪽에서 오른쪽으로 훑는다. ---
    for y in range(height):
        for x in range(width):
            
            # 이 픽셀이 흰색(255)이고, 아직 아무 라벨도 붙지 않았으면
            # -> "새로운 덩어리의 시작점"을 발견한 것
            if binary_img[y, x] == 255 and labels[y, x] == 0:
                
                current_label += 1  # 새 팀 번호 발급
                area = 0            # 이 팀(덩어리)에 몇 명(픽셀)이 있는지 셀 변수
                
                # --- 3. "확인해야 할 픽셀 목록" 바구니(스택) ---
                # 재귀 대신 이 리스트로 직접 관리한다. (RecursionError 방지)
                stack = [(y, x)]
                
                # --- 4. 바구니가 빌 때까지 계속 꺼내서 처리 ---
                while stack:
                    cy, cx = stack.pop()  # 바구니에서 좌표 하나 꺼냄
                    
                    # 이미 라벨이 붙은 픽셀이면 중복 처리니까 건너뜀
                    # (같은 좌표가 여러 이웃한테서 동시에 stack에 들어올 수 있어서 필요한 방어)
                    if labels[cy, cx] != 0:
                        continue
                    
                    # 라벨 붙이고, 이 덩어리의 면적 카운트 +1
                    labels[cy, cx] = current_label
                    area += 1
                    
                    # --- 5. 상하좌우 4방향 이웃을 확인해서, 흰색이고 라벨이 없으면 바구니에 추가 ---
                    neighbors = [(cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)]
                    for ny, nx in neighbors:
                        # 이미지를 벗어나지 않는지 먼저 확인 (그렇지 않으면 IndexError)
                        if 0 <= ny < height and 0 <= nx < width:
                            if binary_img[ny, nx] == 255 and labels[ny, nx] == 0:
                                stack.append((ny, nx))
                
                # 이 덩어리(팀) 탐색이 끝났으면, 최종 면적을 리스트에 기록
                areas.append(area)
                
    return areas                            


def blob_area_numpy(binary_img: np.ndarray) -> list:
    """
    이진화된 흑백 이미지(0/255)에서 서로 붙어있는 흰 덩어리(블롭)를 찾아
    각 덩어리의 면적(픽셀 개수)을 리스트로 돌려준다.
    numpy 벡터화 버전 (B안 — 공정한 비교 대상).
    
    비유: 일단 모든 사람에게 각각 다른 이름표를 달아준 다음,
    "옆 사람 번호가 나보다 작으면 그 번호로 바꿔 단다"를
    전체 인원이 동시에 반복해서, 결국 같은 무리를 같은 번호로 수렴시킨다. 
    """
    height, width = binary_img.shape
    
    # --- 1. 모든 픽셀에 고유 번호를 매긴다 (0, 1, 2, 3, ... 순서대로) ---
    # np.arange로 0부터 (전체 픽셀 수 - 1)까지 번호를 만들고, 이미지 모양으로 접는다.
    labels = np.arange(height * width, dtype=np.int64).reshape(height, width)
    
    # --- 2. 배경(검은 픽셀)은 무한대로 취급 ---
    # "무한대"로 해두면, 나중에 이웃끼리 min 비교 시 배경이 이길 일이 절대 없음.
    # (배경이 흰 덩어리의 번호를 침범하면 안 됨)
    labels = np.where(binary_img == 255, labels, np.iinfo(np.int64).max)
    
    # --- 3. 이웃끼리 번호를 비교해서 전파시키는 과정을 반복한다 ---
    # 한 번 훑을 때 상하좌우 4방향에서 "나보다 작은 이웃 번호"를 받아온다.
    # 이걸 여러 번 반복해야 덩어리 전체에 제일 작은 번호가 끝까지 퍼진다.
    for _ in range(max(height, width)):  # 최악의 경우를 대비한 반복 횟수
        
        # 위쪽 이웃과 비교: 배열을 한 칸 아래로 밀어서 "내 위쪽 픽셀 값"을 가져온다
        shifted = np.full_like(labels, np.iinfo(np.int64).max)
        shifted[1:, :] = labels[:-1, :]
        new_labels = np.minimum(labels, shifted)
        
        # 아래쪽 이웃과 비교
        shifted = np.full_like(labels, np.iinfo(np.int64).max)
        shifted[:-1, :] = labels[1:, :]
        new_labels = np.minimum(new_labels, shifted)
        
        # 왼쪽 이웃과 비교
        shifted = np.full_like(labels, np.iinfo(np.int64).max)
        shifted[:, 1:] = labels[:, :-1]
        new_labels = np.minimum(new_labels, shifted)
        
        #오른쪽 이웃과 비교
        shifted = np.full_like(labels, np.iinfo(np.int64).max)
        shifted[:, :-1] = labels[:, 1:]
        new_labels = np.minimum(new_labels, shifted)
        
        # 배경(원래 무한대였던 자리)은 다시 무한대로 되돌린다 (전파되면 안됨)
        new_labels = np.where(binary_img == 255, new_labels, np.iinfo(np.int64).max)

        if np.array_equal(new_labels, labels):
            break  # 더 이상 바뀌는게 없으면 완료 — 조기 종료
        labels = new_labels
    
    # --- 4. 라벨별로 몇 개의 픽셀이 있는지 센다 ---
    # 배경(무한대)은 결함이 아니니까 제외하고 셈.
    final_labels = labels[labels != np.iinfo(np.int64).max]
    
    # np.unique(..., return_counts=True): 서로 다른 값이 뭐가 있는지,
    # 그리고 각 값이 몇 번 나왔는지를 동시에 알려주는 numpy 함수.
    # 비유: 학생 명부에서 "몇개 반이 있고, 각 반에 몇 명씩 있나"를 한 번에 세는 것.
    unique_labels, counts = np.unique(final_labels, return_counts=True)

    # counts는 numpy 배열이라, A안(순수 반복문 버전)이 반환하는 형식과
    # 맞추기 위해 파이썬 기본 list로 변환하여 반환한다.    
    return counts.tolist()
