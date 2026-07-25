# benchmark.py
# 목적: "워밍업 10회 버리고 100회 재기" 프로토콜을 자동화하는 스톱워치 도구.
# 비유: 육상 경기에서 선수(fn)한테 "일단 10바퀴는 몸 푸는 거고, 그다음 100바퀴 진짜 기록이다" 라고
#      알려주는 심판 + 기록지 담당.

import time
import csv
import statistics


def run_benchmark(fn, args=(), warmup=10, trials=100, label="unnamed"):
    """
    fn      : 시간을 잴 대상 함수 (예: grayscale_pure_python)
    args    : fn에 넘길 인자들 (튜플). 예: (image_array,)
    warmup  : 버릴 앞부분 실행 횟수
    trials  : 실제로 기록할 실행 횟수
    label   : 결과 CSV 파일명에 쓸 이름표 (예: "python_pure_grayscale")
    """
    
    # --- 1. 워밍업 구간: 시간을 재지 않고 그냥 실행만 한다 ---
    # 비유: 달리기 전에 스트레칭 하는 시간은 기록에 넣지 않는 것과 같음.
    for _ in range(warmup):
        fn(*args)
        
    # --- 2. 실측 구간: 실제로 시간을 측정하여 리스트에 적재한다. ---
    times_ms = []
    for _ in range(trials):
        # perf_counter() = "초 단위 스톱워치 버튼"
        # time.time()보다 훨씬 정밀함. (벤치마크에 적합)    
        start = time.perf_counter()
        fn(*args)
        end = time.perf_counter()
        
        elapsed_ms = (end - start) * 1000  # 초 → 밀리 초 변환
        times_ms.append(elapsed_ms)
        
    # --- 3. 통계 계산 ---
    # 평균만 보면 함정이 있음: 어쩌다 한번 튄 값이 평균을 왜곡할 수 있음.
    # 그래서 benchmark.md 규칙대로 여러 지표를 같이 본다.
    sorted_times = sorted(times_ms)
    stats = {
        "label": label,
        "mean_ms": statistics.mean(times_ms),
        "median_ms": statistics.median(times_ms),
        "stdev_ms": statistics.stdev(times_ms),      # 편차가 크면 = 현장에서 프레임 튐이 심하다는 뜻
        "min_ms": min(times_ms),
        "max_ms": max(times_ms),
        "p95_ms": sorted_times[int(trials * 0.95)],  # 상위 5% 튄 값 제외 후 95번째 지점
        "fps": 1000 / statistics.mean(times_ms),     # 1초에 몇 프레임 처리가 가능한지
    }
    
    # --- 4. 회차별 원본 시간을 CSV로 저장 ---
    # 요약값만 남기면 나중에 "진짜 편차가 어땠는지" 재검증할 방법이 없어짐
    csv_path = f"results_{label}.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["trial_index", "elapsed_ms"])
        for i, t in enumerate(times_ms):
            writer.writerow([i, t]) 
            
    return stats


def print_stats(stats: dict):
    # 사람이 육안으로 확인하기 편리하도록 출력만 담당하는 함수.
    print(f"--- {stats['label']} ---")
    print(f"평균(mean)   : {stats['mean_ms']:.3f} ms")
    print(f"중앙값(median): {stats['median_ms']:.3f} ms")
    print(f"표준편차(std) : {stats['stdev_ms']:.3f}")
    print(f"최소/최대     : {stats['min_ms']:.3f} / {stats['max_ms']:.3f} ms")
    print(f"p95         : {stats['p95_ms']:.3f} ms")
    print(f"fps         : {stats['fps']:.2f}")            
