// VisionCore.cpp
// C++ DLL이 "밖으로 내놓는" 함수들을 모아두는 파일
// 여기 없는 함수는 C#이 아무리 불러도 찾지 못함 — 이 파일이 청고 정문 명함판이다.
#include "pch.h"
#include <opencv2/opencv.hpp>  // OpenCV 부품 상자 열어보기 — 내용물은 아직 쓰지 않음 

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
	// length는 "이 창고에 상자가 몇 개 있는지" 알려주는 숫자.
	// 이게 없으면 어디서 멈춰야 할지 몰라서 다른 메모리까지 침범하게 됨.
	for (int i = 0; i < length; i++)
	{
		// data[i] = 시작 주소에서 i칸 떨어진 그 자리의 실제 값
		// 255에서 빼는 것 = 흑백 반전 공식 (0 <-> 255, 100 <-> 155 ...)
		data[i] = 255 - data[i];
	}
}

// GetMatInfo — 두루마리(byte 배열)를 표(cv::mat)로 잘라서 정리해보고,
// 표 형태로 잘 정리 됐는지 행/열 값을 돌려받아 확인하는 함수
extern "C" __declspec(dllexport) void __stdcall GetMatInfo(
	unsigned char* data,	// C#이 넘겨준 픽셀 데이터의 시작 주소 (두루마리)
	int width,			    // 원본 이미지의 가로 픽셀 수 (C#만 알고 있는 정보라 직접 알려줘야 함)
	int height,				// 원본 이미지의 세로 픽셀 수
	int* outRows,			// 결과를 담을 그릇 1 — C#이 미리 준비해둔 주소 (ADR-006: C#이 버퍼 소유)
	int* outCols)			// 결과를 담을 그릇 2
{
	// cv::Mat(세로 크기, 가로 크기, 픽셀 타입, 원본 데이터 주소)
	// CV_8UC1 = "8bit(0~255) 부호없는 정수, 채널 1개(흑백)" 라는 뜻의 OpenCV 표기법
	// 주의: 여기서 새로 데이터를 복사하는 게 아니라, 기존 data 주소를 그대로 "표 형식"으로 감싸기만 함
	cv::Mat mat(height, width, CV_8UC1, data);

	// 표로 잘 정리됐다면 rows/cols에 우리가 넣어준 height/width가 그대로 보여야 정상
	*outRows = mat.rows;
	*outCols = mat.cols;
}
