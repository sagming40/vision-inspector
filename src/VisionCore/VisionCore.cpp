// VisionCore.cpp
// C++ DLL이 "밖으로 내놓는" 함수들을 모아두는 파일
// 여기 없는 함수는 C#이 아무리 불러도 찾지 못함 — 이 파일이 청고 정문 명함판이다.
#include "pch.h"

extern "C"
// C++은 함수명을 맘대로 꼬아버림 (name mangling)
// Add를 컴파일하면 "?Add@@YAHHH@Z" 같은 이름이 되어서 C#이 절대 찾지 못함.
// extern "C"는 "함수명을 꼬지 말고 C 스타일 그대로 내보내라"는 스위치.

__declspec(dllexport)
// 이 함수를 창고 명함에 이름을 올리는 행위. 없으면 함수는 존재하되
// DLL 밖에서는 보이지 않음 (컴파일은 성공, C#에서는 "그런 함수 없음").

int __stdcall Add(int a, int b)
// __stdcall: 호출이 끝나고 스택을 치우는 역할을 "호출받은 쪽"으로 고정.
// ADR-004에서 이미 정한 규칙 — 여기서도 명시해야
// 나중에 컴파일은 되는데 값만 슬쩍 어긋나는 사고를 막음.
{
	return a + b;
}

// "Invert" — 명단(헤더)에 새 메뉴 하나 추가하는 것
// 이 함수는 배열의 "주소"를 받아서, 그 주소가 가리키는 실제 데이터를
// 직접 뒤집어놓고 끝난다 (리턴값 없음 = void)
extern "C"
__declspec(dllexport)
void __stdcall Invert(unsigned char* data, int length)
{
	// 다음 스텝에서 채울 예정 — 틀만
}
