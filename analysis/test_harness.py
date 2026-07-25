# test_harness.py
# 목적: benchmark.py의 run_benchmark()가 제대로 작동하는지 확인하는 "테스트용 테스트".
# 비유: 저울을 사고 나서 첫 재료를 재기 전에, 이미 무게를 아는 물건(1kg짜리 표준 추)을
#      먼저 올려서 "이 저울이 1kg을 1kg이라고 제대로 말하나"부터 확인하는 것.

import time
from benchmark import run_benchmark, print_stats


def dummy_10ms():
    # 정확히 10ms(0.01초) 걸린다는 걸 미리 알고 있는 함수.
    # 이게 "표준 추" 역할 -> 이미 답을 아는 문제로 도구를 검산한다.
    time.sleep(0.01)
    
    
if __name__ == "__main__":
    stats = run_benchmark(dummy_10ms, args=(), label="sanity_check")
    print_stats(stats)    
