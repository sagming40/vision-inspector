# VisionInspector — 로드맵

각 마일스톤은 **끝나면 뭔가 동작하는 물건이 남는다**는 원칙으로 잘랐다.
어디서 멈춰도 보여줄 게 있어야 포트폴리오다.

---

## 폴더 구조

```
vision-inspector/
├─ VisionInspector.sln          ← C++ / C# 프로젝트를 한 솔루션에
├─ src/
│  ├─ VisionCore/               ← C++ DLL (엔진)
│  ├─ VisionApp/                ← C# WPF (UI)
│  └─ analysis/                 ← Python (분석)
├─ samples/                     ← 테스트 이미지
├─ docs/
│  ├─ decisions.md              ← 왜 이렇게 했는지 기록 (면접 대비 핵심)
│  └─ benchmark.md              ← 성능 측정 기록
└─ README.md
```

> `docs/decisions.md` 를 절대 빼먹지 말 것.
> 3개월 뒤 면접장에서 "그때 왜 그렇게 하셨죠"에 답하는 건 기억이 아니라 이 파일이다.

---

## M0 — 뼈대 세우기  `약 1일`

- [ ] GitHub 리포 생성 (`vision-inspector`), `.gitignore` 는 VisualStudio 템플릿
- [ ] 위 폴더 구조 그대로 생성
- [ ] 빈 솔루션에 C++ DLL 프로젝트 + C# WPF 프로젝트 추가
- [ ] **둘 다 x64 로 통일** ← 나중에 `BadImageFormatException` 안 만나려면 지금 해야 함

**완료 조건:** 두 프로젝트 모두 빌드 성공, 첫 커밋 완료

---

## M1 — Python 프로토타입 + 성능 측정  `2~3일`

**이 단계를 건너뛰면 프로젝트 전체의 명분이 사라진다.**

- [ ] Python + OpenCV 로 이미지 반전 / 그레이스케일 / 엣지 검출 구현
- [ ] 동영상(또는 이미지 연속 처리)으로 **fps 측정**
- [ ] `docs/benchmark.md` 에 수치 기록

**완료 조건:** "Python 단독으로는 N fps" 라는 숫자가 문서에 적혀 있음

---

## M2 — 국경 넘기 (C++ DLL ↔ C# P/Invoke)  `3~5일` ⚠️ 최대 고비

- [ ] C++ 에 `Add(int,int)` 하나만 export
      → `extern "C"` + `__declspec(dllexport)` + `__stdcall`
- [ ] `dumpbin /exports` 로 이름이 안 뭉개졌는지 눈으로 확인
- [ ] C# 에서 `[DllImport]` 로 호출 → **`Add(3,4) == 7` 화면에 출력**
- [ ] `.csproj` 에 DLL 자동 복사 설정 추가
- [ ] 프로젝트 속성 → 디버그 → **네이티브 코드 디버깅 사용 체크**
- [ ] F11 로 C# → C++ 함수 안으로 진입되는지 확인

**완료 조건:** C# 버튼 눌러서 C++ 함수가 계산한 값이 화면에 뜬다

> 여기서 대부분 막힌다. 여기만 넘으면 나머지는 같은 원리의 반복이다.

---

## M3 — 배열 넘기기 (진짜 픽셀 처리)  `3~5일`

- [ ] C++ `Invert(unsigned char* data, int length)` 구현
- [ ] C# `byte[]` 로 넘겨서 이미지가 실제로 반전되는지 확인
- [ ] **값 전달 vs 참조(주소) 전달** 차이를 `docs/decisions.md` 에 정리
- [ ] GC pinning 이 왜 필요한지 정리

**완료 조건:** WPF 화면의 이미지가 C++ 코드로 인해 바뀐다

---

## M4 — OpenCV 투입 + 성능 재측정  `1~2주`

- [ ] C++ DLL 안에 OpenCV 연결 (그레이스케일 → 블러 → 엣지 → 임계값)
- [ ] WPF 에 임계값 조절 슬라이더 (MVVM, `INotifyPropertyChanged`)
- [ ] 실시간 미리보기
- [ ] **fps 재측정 → M1 수치와 비교하여 `benchmark.md` 갱신**

**완료 조건:** "Python N fps → C++ M fps" 비교표 완성.
**이게 이 프로젝트에서 제일 가치 있는 산출물이다.**

---

## M5 — 판정 + DB 저장  `1~2주`

- [ ] 결함 영역 면적 기준으로 OK / NG 판정 로직
- [ ] MariaDB 스키마 설계 (검사시각, 결과, 수치, 이미지 경로)
- [ ] C# 에서 검사 이력 INSERT
- [ ] WPF 에 이력 조회 화면

**완료 조건:** 검사할 때마다 DB에 행이 쌓이고 화면에서 조회된다

---

## M6 — Python 분석 레이어  `1주`

- [ ] MariaDB 에서 이력 조회 → pandas
- [ ] 불량률 추이 / 시간대별 통계 → matplotlib (한글 폰트 `Malgun Gothic`)
- [ ] 리포트 자동 생성

**완료 조건:** 스크립트 한 번 돌리면 통계 리포트가 나온다

---

## M7 (선택) — 학습 모델 배포

- [ ] Python 에서 간단한 CNN 학습 → ONNX export
- [ ] C++ 쪽에서 ONNX Runtime 으로 추론

> "Python으로 학습하고 C++로 배포" — 실무 패턴 그대로.
> M6까지 12월 전에 끝났을 때만 손댈 것.

---

## 일정 감각

M0~M4 까지가 포트폴리오로서 **최소 완성체**.
수업 병행 기준으로 대략 2~3개월. M5~M6 포함이면 4~6개월.

**절대 M4까지를 서둘러 넘기지 말 것.** 성능 비교표 없는 M5는 껍데기다.
