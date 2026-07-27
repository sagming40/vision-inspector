# 📓 개발 일지 (Dev Log) — VisionInspector

M0~M7 마일스톤을 진행하며 겪은 문제, 배운 것, 고민했던 것을 기록한다.
설계 결정의 "이유"는 `decisions.md`, 성능 수치는 `benchmark.md`에 따로 있다.
여기는 그 사이에 있는 "과정" — 시행착오, 트러블슈팅, 깨달음을 남긴다.

---

## 2026-07-24 · M0 (솔루션 뼈대 세우기)

### 오늘 한 일
- `Dev_Repos\vision-inspector\` 최상위 폴더 및 `docs\`, `samples\` 생성
- Visual Studio 2022로 빈 솔루션(`VisionInspector.sln`) 생성
- C++ DLL 프로젝트(`VisionCore`), C# WPF 프로젝트(`VisionApp`) 를 각각 `src\` 밑에 추가
- 두 프로젝트 플랫폼을 `x64`로 통일 (구성 관리자에서 확인)
- 설계 문서 5종(`architecture.md`, `pipeline.md`, `decisions.md`, `benchmark.md`, `roadmap.md`) + `README.md` + `.gitignore` 작성
- `git init` → 첫 커밋 → GitHub 원격 리포지토리 생성 및 push

### 겪었던 이슈들

**1. "솔루션과 프로젝트를 같은 디렉터리에 배치" 체크박스를 못 보고 지나감**
빈 솔루션 생성 시 이 옵션을 끄지 않아서, `vision-inspector\VisionInspector\VisionInspector.sln` 처럼 폴더가 한 겹 더 생겨버림. VS를 닫고 `.sln` 파일을 한 단계 위로 옮기고 빈 폴더와 `.vs\` 캐시를 삭제하는 것으로 해결. 이후로 솔루션 생성 화면에서 이 체크박스부터 확인하는 습관이 생김.

**2. `.gitignore` 파일명 앞의 점(`.`)이 누락됨**
Windows 탐색기에서 이름 바꾸기로 파일을 저장했는데, 처음엔 점 없이 `gitignore`로 저장돼서 Git이 이 파일을 완전히 무시(일반 파일로 취급)하는 상태였음. 탐색기 유형란에 "Git Ignore 원본 파일"로 표시되는지 직접 확인해야 한다는 걸 배움.

**3. "플랫폼 대상(PlatformTarget)"과 "솔루션 플랫폼(상단 드롭다운)"이 서로 다른 값이라는 걸 모르고 헷갈림**
프로젝트 속성 → 빌드 → 플랫폼 대상을 `x64`로 바꿨는데도, 빌드 로그에는 계속 "구성: Debug Any CPU"로 표시됨. 실제 컴파일은 이미 x64로 되고 있었지만(속성 값이 진짜 설정), 상단 툴바/로그의 이름표는 별개로 관리되는 값이라 따로 맞춰야 했음. **구성 관리자(빌드 → 구성 관리자)** 에서 두 프로젝트의 플랫폼 열을 직접 `x64`로 지정하고 나서야 로그에도 "Debug x64"로 정확히 표시됨.

**4. Git 커밋 메시지 작성 중 vim이 열려서 당황함**
`git commit` (옵션 없이)을 치니 터미널 안에서 vim 편집기가 열렸는데, 일반 텍스트 에디터처럼 조작이 안 되고 하단에 `-- INSERT --` 표시만 뜬 채 저장/종료 방법을 몰라 멈춤. `Esc`로 입력 모드를 빠져나온 뒤 `:wq` 입력 후 Enter로 저장·종료한다는 걸 배움 — vim은 "모드"가 있는 에디터라 Enter만으로는 저장되지 않는다는 점을 체감.

### 오늘 배운 것 / 느낀 점
- OneDrive 자동 백업이 걸린 폴더에 프로젝트를 두면 Visual Studio 빌드 산출물과 동기화가 충돌할 수 있다는 것을 미리 확인하고, 동기화 안 되는 위치(`Dev_Repos\`)를 골라 시작함 — 문제가 생기기 전에 예방한 첫 사례.
- `.gitignore`가 제대로 작동하는지는 "만들었다"로 끝나는 게 아니라, `git status`로 `bin/`, `obj/`, `x64/`, `.vs/` 가 실제로 추적 목록에서 빠지는지 반드시 눈으로 확인해야 한다는 걸 체감함.
- 커밋을 "언어 기준"이 아니라 "의미 단위"로 나눈다는 원칙을 이번 첫 커밋에 그대로 적용 — 문서, `.gitignore`, 두 프로젝트 뼈대를 하나의 완결된 상태(M0 완료)로 묶어 한 커밋으로 처리함.
- 문서(`architecture.md`, `benchmark.md` 등)를 코드보다 먼저 만들어두니, 이후 작업에서 "왜 이렇게 하기로 했는지"를 다시 설명할 필요 없이 바로 참조할 수 있어 편리했음.

### 다음에 할 일
- M1: Python + OpenCV로 기본 이미지 처리(반전/그레이스케일/엣지) 프로토타입 구현 및 fps 측정

---

## 2026-07-25 · M1 (Python 프로토타입 + 성능 측정)

### 오늘 한 일
- venv 세팅, opencv-python/numpy/pillow 설치
- 테스트용 1920x1080 샘플 이미지 생성 (`generate_sample.py`, 결함 15개 배치)
- 벤치마크 하네스(`benchmark.py`) 구현 — 워밍업 10회 + 실측 100회 자동화
- 하네스 검증 (`test_harness.py`) — `time.sleep(0.01)`로 sanity check, 평균 10.309ms/fps 97로 정확도 확인
- ④~⑦ cv2 표준 파이프라인 단계별 측정 (그레이스케일 → 블러 → 이진화 → 모폴로지)
- ⑧ 블롭 검출 A안(순수 반복문 flood fill) 구현 + 측정

### 겪었던 이슈들

**1. `(venv)` 안 붙은 채 실행해서 `ModuleNotFoundError`**
새 터미널 세션이 activate 안 된 상태였는데, 첫 실행(`test_harness.py`)이 표준 라이브러리(`time`, `csv`, `statistics`)만 써서 우연히 안 걸렸다가, cv2를 쓰는 스크립트(`run_stage4_benchmark.py`)에서 뒤늦게 드러남. 이후로 "`ModuleNotFoundError` 뜨면 프롬프트 앞 `(venv)`부터 확인"을 습관으로 정함.

**2. `im` 계열 함수 오타 반복 (`inread`, `inwrite`)**
`cv2.imread`, `cv2.imwrite`를 칠 때 `m`이 `n`으로 바뀌는 오타가 두 번 남. 파일 경로 오타(`test_1920_1080.png` — `x` 자리에 언더바)도 한 번. 매번 traceback 마지막 줄이 정확히 원인을 가리켜줘서 빠르게 잡음. `cv2.imread`는 파일을 못 찾아도 예외를 던지지 않고 조용히 `None`을 반환하기 때문에, `if img is None: raise ...`로 직접 확인하는 방어 코드를 넣어둔 게 이번에 실제로 유용했음.

**3. 파일 위치 어긋남 — 상대경로(`../`) 기준점 착각**
`analysis/` 폴더 밖(프로젝트 루트)에서 `generate_sample.py`를 생성·실행해서, 코드 안의 `../samples/...` 경로가 의도한 위치가 아닌 한 칸 더 위(`Dev_Repos/samples`)를 가리키게 됨. 상대경로는 "지금 서 있는 폴더" 기준이라는 걸 직접 겪고 나서 확실히 체감. 파일을 올바른 위치로 옮기고 실행 위치를 고정하는 것으로 해결.

### 오늘 배운 것 / 느낀 점
- `decisions.md` ADR-005의 가설(H1: cv2 표준 구간은 언어별 차이 없음, H3: 커스텀 로직에서만 진짜 차이 남)이 실측으로 검증되기 시작하는 걸 숫자로 직접 확인함 — ④~⑦ 단계를 다 합쳐도 3ms 남짓인데, ⑧번 순수 반복문 하나가 152.655ms(fps 6.55)로 나옴. 말로만 알던 논거가 실제 수치로 눈앞에 나타나니 확실히 다르게 와닿음.
- 재귀 대신 스택(리스트)을 직접 관리하는 flood fill 패턴을 이번에 처음 손으로 짜봄 — "재귀 깊이 제한 때문에 큰 덩어리를 채우면 위험하다"는 이유를 이해하고 나서야 왜 이 구조가 필요한지 납득이 감.
- 벤치마크 결과를 해석할 때 평균만 보지 않고 표준편차·최소/최대까지 같이 봐야 한다는 걸 체감 — 연산이 무거워질수록(블러, 모폴로지) 편차도 커지는 패턴이 반복적으로 확인됨.
- 커밋을 파일 단위로 쪼개서 여러 번 나눠 하는 습관을 이번 세션에서 제대로 시행 — "환경설정 → 하네스 검증 → 단계별 측정" 순서로 히스토리를 남기니 나중에 되짚어보기 훨씬 쉬움.

### 다음에 할 일
- ⑧ B안(numpy 벡터화) 구현 + 측정 — A/C만 비교하면 "느린 쪽만 골라 비교했다"는 반박이 성립하므로 B가 반드시 필요 (ADR-005)
- B안 완료 후 `benchmark.md` 3.3 표를 A/B 2열 구조로 정리

---

## 2026-07-26 · M1 (계속 — numpy 벡터화 B안 + 마무리)

### 오늘 한 일
- ⑧ 블롭 검출 B안(numpy 벡터화, 반복적 라벨 전파 방식) 구현 + 측정
- A/B 결과값 완전 일치 검증 (블롭 15개, 면적 리스트 동일) 후 성능만 비교
- M1 마무리: README/roadmap 상태 갱신

### 겪었던 이슈들

**1. `analysis/` 폴더가 계획(`roadmap.md`)과 다른 위치에 생성됨**
원래 계획은 `src/analysis/`였는데, M1 시작할 때 `mkdir analysis`를 프로젝트 루트에서 실행해서 `src/` 밖에 만들어짐. 이미 여러 스크립트가 이 위치 기준 상대경로(`../samples/...`)로 작성돼 있어서, 지금 옮기면 경로를 전부 고치고 재검증해야 하는 부담이 큼. 폴더 위치가 이 프로젝트의 핵심 논거(언어 간 성능 비교)에 영향을 주는 요소는 아니라고 판단해, 옮기는 대신 `roadmap.md`의 폴더 구조를 실제 상태에 맞게 수정하는 쪽을 선택함.

**2. `for` 루프가 함수 밖으로 빠져 `NameError` 발생**
`blob_area_numpy` 함수의 `return` 문 뒤에 전파 로직(`for` 루프)을 이어서 작성했는데, 들여쓰기가 없어서 파이썬이 이를 함수 몸통이 아니라 파일 최상위 코드로 인식함. `height`, `width`, `binary_img` 등 함수 안에서만 존재하는 변수를 찾지 못해 에러 발생. `return`은 항상 함수의 마지막에 와야 하고, 그 뒤에 오는 코드는 같은 들여쓰기 레벨 안에 있어야 실행된다는 걸 체감.

**3. `labels`/`lables` 오타로 인한 조용한 로직 오류**
변수명 오타(`b`와 `l` 위치가 바뀜)로 `labels`와 `lables`라는 서로 다른 두 변수가 동시에 존재하게 됨. 파이썬은 오타 난 변수명도 새 변수로 순순히 받아들이기 때문에 에러 없이 실행은 됐지만, 실제로는 전파 로직이 두 변수를 뒤섞어 참조하면서 결과가 틀어짐. `ModuleNotFoundError`처럼 소리 내며 멈추는 에러보다, 이런 "조용히 다른 계산을 하는" 오타가 훨씬 위험하다는 걸 체감.

**4. 면적 세기 로직이 `for` 루프 안에 들여쓰기되어 매 반복마다 조기 종료**
전파 루프가 끝난 뒤 실행돼야 할 "라벨별 픽셀 수 세기" 코드가 `for` 루프와 같은 들여쓰기에 있어서, 첫 반복 직후 바로 `return`되어 버림. 전파가 채 끝나기도 전에 결과를 세는 상태였음. 스페이스 4칸 차이가 "루프 안이냐 밖이냐"를 완전히 바꾼다는 걸 직접 겪고 확실히 체감 — C++/C#의 중괄호와 가장 크게 다른 지점.

### 오늘 배운 것 / 느낀 점
- **numpy 벡터화가 항상 빠른 게 아니라는 걸 실측으로 확인함.** B안(numpy)이 A안(순수 반복문)보다 오히려 **15배 느리게** 나옴 (152.655ms vs 2295.805ms). 원인을 진단 스크립트로 확인해보니, 전파 루프가 106회 반복되는데 매 반복마다 207만 개 픽셀 전체를 훑는 구조라서, A안이 "필요한 곳만 국소적으로 방문"하는 것보다 총 연산량이 훨씬 컸음. "numpy 쓰면 무조건 빠르다"가 아니라 "알고리즘의 반복 구조가 벡터화와 맞아야 이득이 난다"는 걸 배움.
- 결과를 먼저 성급히 받아들이지 않고, 진단용 스크립트(`diagnose_stage8_iterations.py`)를 따로 만들어 "왜 느린지"를 추측이 아니라 숫자로 확인하는 과정을 거침 — 나중에 근거를 댈 때 "아마 이래서 그럴 것"보다 "실제로 106번 반복했다"는 게 훨씬 설득력 있다는 걸 체감.

### 다음에 할 일
- M2: C++ DLL ↔ C# P/Invoke 연동 — `Add(int,int)` export부터 시작

---

## 2026-07-26 · M2 (C++ DLL ↔ C# P/Invoke 연동)

### 오늘 한 일
- `VisionCore.cpp` 신설, `extern "C"` + `__declspec(dllexport)` + `__stdcall`로 `Add(int,int)` export
- `dumpbin /exports`로 이름이 안 뭉개졌는지 확인 (`Add`로 정상 노출, ILT는 Debug 빌드 흔적)
- `MainWindow.xaml.cs`에 `[DllImport]`로 `Add` 선언, 생성자에서 호출 → `Add(3,4) = 7` 팝업 확인
- `VisionApp.csproj`에 `Target(AfterTargets="Build")` 추가해 `VisionCore.dll` 자동 복사
- 시작 프로필에서 "네이티브 코드 디버깅 사용" 체크, F10으로 C++ 함수 내부 진입·반환값 확인

### 겪었던 이슈들

**1. `VisionCore.cpp` 첫 줄에 `#include "pch.h"` 누락 → `C1010`**
새 `.cpp` 파일을 "C++ 파일" 템플릿으로 추가하면서 `pch.h` include가 자동으로 안 붙었음.
`VisionCore.vcxproj`에 `PrecompiledHeader=Use`가 이미 설정되어 있어, 이 프로젝트의 모든 `.cpp`는 반드시 첫 줄에 `#include "pch.h"`가 있어야 한다는 걸 에러 메시지(`C1010`)가 그대로 알려줌. `dllmain.cpp`와 첫 줄을 맞추는 것으로 해결.

**2. P/Invoke 선언과 호출 코드를 `namespace`/`class` 바깥에 작성 → 컴파일 자체가 안 됨**
`[DllImport]`, `extern` 선언, `Add(3,4)` 호출 전부를 클래스 밖에 그대로 붙여넣어서 "네임스페이스에서 명령문을 쓸 수 없다"는 에러가 다수 발생. C#은 모든 코드가 클래스 안에 있어야 한다는 것, 특히 실행문(`Add(3,4)` 호출)은 반드시 메서드 안에 있어야 한다는 걸 체감. `extern` 선언은 클래스 몸통(필드처럼), 호출부는 생성자 안으로 재배치해 해결.

**3. F5 실행 시 `VisionCore.dll`을 직접 실행하려다 실패**
`'...VisionCore.dll'은(는) 올바른 Win32 애플리케이션이 아닙니다` 에러 발생.
최근 `VisionCore.cpp`를 열어 작업하면서 VS가 시작 프로젝트를 `VisionCore`로 자동 전환해둔 상태였음.
DLL은 그 자체로 실행 가능한 대상이 아니라는 것, 시작 프로젝트는 항상 실행 파일(`VisionApp`)을 가리켜야 한다는 걸 직접 겪고 확인. 솔루션 탐색기에서 "시작 프로젝트로 설정"으로 해결.

**4. 최신 VS 버전에서 "네이티브 코드 디버깅 사용" 위치가 프로젝트 속성에서 사라짐**
과거엔 프로젝트 속성 → 디버그 탭에 있었는데, 지금 버전은 "디버그 시작 프로필 UI"로 이동됨.
프로젝트 속성 페이지 자체가 최신 VS에서 계속 개편되고 있어, 문서/자료의 스크린샷과 실제 화면이 다를 수 있다는 걸 체감 — 화면에 없으면 이동된 위치부터 찾아야 함.

### 오늘 배운 것 / 느낀 점
- `extern "C"`를 빼면 C++ 컴파일러가 함수 이름을 name mangling으로 꼬아버려서 (`?Add@@YAHHH@Z` 형태) C#이 이름으로 찾을 수 없다는 걸 `dumpbin` 실측으로 직접 확인함. ADR-002/004에 적어둔 이론을 눈으로 검증한 첫 사례.
- 호출 규약(`__stdcall`)이 어긋나면 컴파일은 되는데 런타임에만 문제가 생긴다는 게 ADR-004의 핵심 경고였는데, 이번엔 처음부터 양쪽에 명시해서 이 문제 자체를 겪지 않음 — "안 겪은 버그"도 설계가 제대로 작동한 증거로 남겨둘 만함.
- 네이티브 디버깅이 켜졌는지는 추측이 아니라 출력 창 로그로 확인 가능하다는 걸 배움 — 다른 시스템 DLL은 전부 "기호 로드가 비활성화"인데 `VisionCore.dll`만 "기호가 로드되었습니다"로 표시되는 차이가 결정적 증거였음.
- 커밋 메시지 타입은 "그 사이 내가 뭘 확인했는지"가 아니라 "diff가 실제로 무엇을 바꿨는지" 기준으로 정해야 한다는 걸 다시 짚음 — `launchSettings.json` 설정 값 하나 추가한 커밋에 `feat`을 붙일 뻔했다가 `chore`로 정정.

### 다음에 할 일
- M3: `Invert(unsigned char* data, int length)` 구현 — 배열(포인터) 전달로 진짜 픽셀 처리 시작
- 값 전달 vs 참조(주소) 전달 차이, GC pinning이 왜 필요한지 `decisions.md`에 정리

---

## 2026-07-26 ~ 2026-07-27 · M3 (배열 넘기기 — 진짜 픽셀 처리)

### 오늘 한 일
- `VisionCore.cpp`에 `Invert(unsigned char*, int)` export, `dumpbin`으로 이름 노출 확인
- 반전 로직(`255 - data[i]`) 구현
- C# `[DllImport]`로 `Invert` 선언, `byte[] {0,100,255}` 테스트 배열로 호출 → `{255,155,0}` 확인 — 원본 배열이 실제로 바뀌는 것으로 값 전달과 참조 전달의 차이를 실측
- `docs/decisions.md`에 ADR-007(값 전달 vs 참조 전달) 신설, ADR-006에 pinning 실측 검증 섹션 추가
- 300x300 흑백 테스트 이미지(`generate_m3_sample.py`) 생성, `VisionApp/Assets`에 Resource로 편입
- `MainWindow.xaml`에 `<Image>` 컨트롤 추가, 원본 이미지 화면 표시 확인
- `BitmapImage` → `WriteableBitmap`(Gray8) → `CopyPixels`로 `byte[]` 변환, 픽셀값(128) 검증
- 변환된 `byte[]`를 `Invert`에 통과시킨 뒤 `WritePixels`로 새 `WriteableBitmap` 조립, `MyImage.Source` 교체 → 화면에서 반전 확인 (M3 완료 조건 충족)

### 겪었던 이슈들

**1. P/Invoke 선언을 C++ 파일(`VisionCore.cpp`)에 잘못 작성**
`[DllImport]`, `public static extern` 같은 C# 문법을 그대로 `.cpp` 파일에 붙여넣어서 `E1277`, `C2059` 등 에러가 대거 발생. C++ 컴파일러가 대괄호 특성 문법과 `public` 키워드를 이해하지 못해 벌어진 일. 코드를 올바른 C# 파일(`MainWindow.xaml.cs`)로 옮겨서 해결. M2 때 겪었던 "class 바깥에 실행문 작성" 문제의 사촌 격 실수.

**2. P/Invoke 선언·호출 코드를 class 몸통 안, 생성자 밖에 작성**
`testData` 선언과 `Invert` 호출, `MessageBox.Show`까지를 생성자(`MainWindow()`) 바깥, class 몸통 바로 밑에 작성해서 컴파일러가 이를 실행문이 아니라 생성자 오버로드 선언 시도로 오인 (`CS0501` 등). "필드/메서드 선언 자리"와 "실행문이 와야하는 자리"가 C#에서 엄격히 구분된다는 걸 다시 한번 체감. 생성자 안으로 이동해 해결.

**3. 지역 변수 이름 중복 (`CS0128`)**
`Invert` 결과를 담을 `result`(string)와 `Add` 결과를 담을 `result`(int)를 같은 생성자 범위 안에 동시에 선언해서 충돌. 타입이 달라도 이름이 같으면 안 된다는 것, 그리고 "이미 정의되어 있습니다" 류 메시지는 구조 오류가 아니라 이름 충돌이라는 패턴으로 구분해서 읽어야 한다는 걸 배움.

**4. `dumpbin` 실행 경로 추측 실패**
아까 M2 때 기억으로 `src\VisionCore\x64\Debug`를 짐작해서 시도했으나 `LNK1181` (파일 없음). 실제로는 솔루션 산출물 경로가 솔루션 루트 바로 밑 `x64\Debug`에 생기는 구조였음. `dir /s /b`로 실제 파일 위치를 직접 찾아서 해결 — 추측 대신 검색으로 확인하는 습관의 중요성을 다시 확인.

**5. 테스트 이미지가 `.gitignore`의 `test_*.png` 규칙에 걸림**
`VisionApp/Assets/test_m3_small.png`가 M1 때 정한 "검증용 이미지 전체 무시" 규칙에 걸려 추적이 안 되는 문제. 처음엔 파일명 앞에 언더바(`_`)를 붙여 우회하려 했으나, 이는 "왜 언더바가 붙었는지"가 코드/파일명만으로 드러나지 않아 지양 — 대신 `.gitignore`에 `!src/VisionApp/Assets/test_m3_small.png` 예외 규칙을 추가해 의도가 문서에 명시적으로 남도록 처리.

### 오늘 배운 것 / 느낀 점
- ADR-006(pinning)과 ADR-007(값/참조 전달)이 이론으로만 있던 게, `{0,100,255}` → `{255,155,0}` 실측 한 번으로 "사실"로 격상되는 과정을 직접 봄. 문서에 검증 섹션을 따로 두는 이유를 체감.
- `stride`가 이론값(`width`)과 항상 같지 않다는 것 — 이번엔 우연히 같았지만 (`Gray8` + 정렬 여유 없음), 실제 값은 반드시 `BackBufferStride`로 직접 물어봐야 한다는 걸 배움. "당연히 같겠지"라고 넘겼으면 나중에 다른 포맷에서 바로 버그로 이어졌을 지점.
- 같은 구조 오류(선언과 실행문 위치 착각)가 M2, M3에서 형태만 바뀌어 반복됨 — 다음부턴 에러가 무더기로 뜨면 개별 메시지보다 "이 코드가 지금 `{ }` 몇 겹 안에 있는지"부터 먼저 확인하는 습관을 들이기로 함.

### 다음에 할 일
- M4: C++ DLL에 OpenCV 연결 (그레이스케일 → 블러 → 엣지 → 임계값)
- WPF에 임계값 조절 슬라이더(MVVM, `INotifyPropertyChanged`) 추가
- fps 재측정 → M1 수치와 비교해 `benchmark.md` 갱신 ("Python N fps → C++ M fps" 비교표가
  이 프로젝트에서 가장 중요한 산출물임을 로드맵이 강조하고 있음, 서두르지 말 것)

---

## 2026-07-27 ~ 2026-07-28 · M4 (OpenCV 투입 + 성능 재측정 — 시작)

### 오늘 한 일
- vcpkg 클론(`C:\vcpkg`) → 부트스트랩(`bootstrap-vcpkg.bat`) → `integrate install`로 VS 전역 연동
- `vcpkg install opencv:x64-windows`로 OpenCV 4.12.0 설치 (약 11분 소요, dnn 모듈 포함)
- `VisionCore.cpp`에 `#include <opencv2/opencv.hpp>` 추가, 빌드 검증
- `GetMatInfo(unsigned char* data, int width, int height, int* outRows, int* outCols)` 구현
  — byte 배열을 `cv::Mat`으로 감싸고 rows/cols를 되돌려주는 최소 단위 검증 함수
- C# `[DllImport]`로 `GetMatInfo` 선언 및 호출, `rows=300, cols=300`으로 원본 width/height와 일치 확인
- `VisionApp.csproj`에 `CopyOpenCVRuntimeDlls` 타겟 추가 — OpenCV 런타임 dll(z.dll, opencv_core4.dll)을
  VisionApp 출력 폴더로 자동 복사되게 함

### 겪었던 이슈들

**1. `#include <opencv2/opencv.hpp>`를 못 찾음 (`C1083: No such file or directory`)**
`vcpkg integrate install`을 실행하고 VS를 재시작해도 해결 안 됨. 직접 파일 시스템을 뒤져보니 vcpkg가 설치한 OpenCV 4.x 헤더는 `include\opencv2\...`가 아니라 **`include\opencv4\opencv2\...`** 구조였음 (다른 버전 OpenCV와의 충돌을 막기 위한 vcpkg의 관례로 추정). `integrate install`이 자동으로 등록해주는 경로는 `include`까지만이라, `opencv4` 한 겹을 프로젝트 속성 → C/C++ → 일반 → 추가 포함 디렉터리에 수동으로 더 추가해야 했음.

**2. 빌드는 되는데 실행하면 `DllNotFoundException: Unable to load DLL 'VisionCore.dll' or one of its dependencies`**
`dumpbin /exports`로 VisionCore.dll 자체는 이름이 잘 노출된 것을 이미 확인한 상태라 원인이 다른 곳에 있다고 판단. 디버그 출력 로그를 자세히 읽어보니 VisionCore.dll은 로드됐다가 곧바로 다시 언로드되는 패턴이 보였음 — "DLL 자체를 못 찾음"이 아니라 "DLL은 찾았는데 그 DLL이 필요로 하는 다른 DLL을 못 찾음"에 해당하는 흐름. `dumpbin /dependents opencv_core4.dll`로 의존성 목록을 직접 뽑아보니 `z.dll`이 빠져있었음.

원인: vcpkg의 applocal deployment(런타임 dll 자동 복사 기능)는 **VisionCore 프로젝트 자신의 출력 폴더(x64\Release)까지만** 책임지고, VisionCore.dll이 VisionApp 프로젝트로 한 번 더 실려 이동하는 것까지는 감안하지 않음. `VisionCore.dll` 자체는 M2 때 만든 csproj 자동 복사 규칙 덕에 VisionApp까지 넘어왔지만, `z.dll`/`opencv_core4.dll`은 그 규칙 대상이 아니었던 것.

임시로 손수 복사해 문제 재현/해결을 확인한 뒤, `VisionApp.csproj`에 OpenCV 런타임 dll 전용 자동 복사 타겟(`CopyOpenCVRuntimeDlls`)을 추가. `z.dll`을 일부러 지우고 재빌드 → 자동으로 다시 채워지는 것까지 확인해 자동화가 실제로 동작함을 검증함.

**3. `.csproj` 자동 복사 코드에서 `MSB3094` 발생**
`CopyOpenCVRuntimeDlls` 타겟 작성 중 `DestinationFiles="$(OutDir)"`로 잘못 씀. 소스 파일이 2개(z.dll, opencv_core4.dll)인데 목적지가 1개라 "참조하는 항목 수는 같아야 한다"는 에러 발생. `DestinationFolder`(폴더에 넣기, 개수 제약 없음)와 `DestinationFiles`(소스 개수와 1:1 대응하는 결과 파일명 지정, 개수 반드시 일치)가 이름은 비슷해도 완전히 다른 속성이라는 걸 이 에러로 확인. 기존 `CopyVisionCoreDll` 타겟이 쓰던 `DestinationFolder`로 통일해 해결.

### 오늘 배운 것 / 느낀 점
- `DllNotFoundException`은 "DLL 자체가 없다"와 "DLL은 있는데 그 의존 파일이 없다"를 구분해서 알려주지 않는다는 걸 실측으로 확인함. 메시지 하나만 보고 판단하지 말고 `dumpbin /dependents`로 직접 의존성 트리를 확인하는 습관이 필요하다는 걸 체감.
- 패키지 매니저(vcpkg)의 자동화는 "그 패키지 매니저가 직접 건드리는 프로젝트"까지만 책임진다는 것. 우리 구조(VisionCore → VisionApp으로 dll이 한 번 더 실려가는 구조)처럼 프로젝트 경계를 넘어가는 지점은 자동화 범위 밖일 수 있어서, 그 경계마다 별도로 확인해야 함.
- MSBuild `Copy` 태스크의 `DestinationFolder`와 `DestinationFiles`는 이름이 비슷해 보이지만 전혀 다른 속성 — 전자는 "폴더에 넣어라"(개수 제약 없음), 후자는 "소스 개수와 1:1로 대응하는결과 파일명을 지정해라"(개수 안 맞으면 `MSB3094` 에러)라는 것을 에러로 직접 확인.

### 다음에 할 일
- M4 로드맵 다음 항목: 그레이스케일 → 블러 → 엣지 → 임계값 파이프라인을 C++ + OpenCV로 구현
- 완료되면 WPF에 임계값 조절 슬라이더(MVVM) 추가
- 파이프라인 완성 후 fps 재측정 → `benchmark.md`의 M4 비교표(A/B/C 3열) 채우기

---
