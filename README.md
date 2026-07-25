# VisionInspector

산업용 머신비전 검사 시스템의 축소 구현.
이미지에서 결함을 검출해 OK/NG를 판정하고, 이력을 누적해 통계로 환원한다.

> **상태:** ✅ M0 완료 (솔루션 뼈대 + 빌드 + 리포지토리) → 🚧 M1 진행 대기 — 2026.07

---

## 문제 정의

제조 라인의 외관 검사는 다음 세 가지를 동시에 요구한다.

1. **실시간성** — 라인 속도에 맞춰 초당 수십 프레임을 밀리지 않고 처리
2. **조작성** — 현장 작업자가 임계값 등 파라미터를 즉시 조절
3. **누적 분석** — 검사 이력을 모아 불량 추세를 파악

이 세 요구는 성격이 전혀 다르다. 하나의 언어로 전부 감당하면
어느 한쪽이 반드시 희생된다. 그래서 레이어를 나눴다.

---

## 아키텍처 요약

```
     ┌──────────────┐
     │  C# WPF UI   │  조작 · 표시
     └──────┬───────┘
            │ P/Invoke  ← 언어 경계
     ┌──────┴───────┐
     │ C++ DLL 엔진 │  OpenCV · 결함 검출
     └──────────────┘
            │
     ┌──────┴───────┐
     │   MariaDB    │  검사 이력
     └──────┬───────┘
            │
     ┌──────┴───────┐
     │Python 분석   │  통계 · 리포트
     └──────────────┘
```

| 레이어 | 언어 | 선택 근거 |
|---|---|---|
| 엔진 | C++ | 프레임 루프 · 커스텀 픽셀 연산 성능 |
| UI | C# WPF | 데스크톱 UI 생산성, 데이터 바인딩 |
| 분석 | Python | pandas / matplotlib 생태계 |
| 저장 | MariaDB | 이력 영속화 |

상세: [`docs/architecture.md`](docs/architecture.md)

---

## 성능

> ⏳ M1·M4 완료 후 기입. 지금 비어 있는 게 정상이다.

| 구현 | 해상도 | fps | 프레임당 |
|---|---|---|---|
| Python | — | — | — |
| C++ | — | — | — |

측정 조건과 원본 데이터: [`docs/benchmark.md`](docs/benchmark.md)

---

## 문서

| 파일 | 내용 |
|---|---|
| [`docs/architecture.md`](docs/architecture.md) | 레이어 구조와 경계 정의 |
| [`docs/pipeline.md`](docs/pipeline.md) | 이미지 한 장이 거치는 전 과정 |
| [`docs/decisions.md`](docs/decisions.md) | 설계 결정과 그 이유 (ADR) |
| [`docs/benchmark.md`](docs/benchmark.md) | 성능 측정 프로토콜과 결과 |
| [`docs/devlog.md`](docs/devlog.md) | 개발 일지 — 시행착오와 배운 것 |
| [`docs/roadmap.md`](docs/roadmap.md) | 마일스톤 |

---

## 빌드
 
**요구 사항**
- Visual Studio 2022 (Desktop development with C++, .NET desktop development 워크로드)
- .NET 8.0 SDK

**절차**
1. `VisionInspector.sln` 을 Visual Studio 2022로 연다
2. 상단 플랫폼 드롭다운이 **x64** 인지 확인한다 (`VisionCore`, `VisionApp` 둘 다)
3. 빌드 → 솔루션 빌드 (`Ctrl+Shift+B`)
> P/Invoke 연동(M2) 이전까지는 두 프로젝트가 서로 참조하지 않는다.
> 각자 독립적으로 빌드·실행 가능하다.

---

## 만든 사람

사공민규 · 한국폴리텍II대학 인천캠퍼스 컴퓨터공학과 (2026)
