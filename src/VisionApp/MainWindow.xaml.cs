using System.Reflection;
// P/Invoke 쓰려면 이 네임스페이스 필수 —
// "네이티브(비관리) 코드랑 소통하는 도구함"
using System.Runtime.InteropServices;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Media.TextFormatting;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace VisionApp
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        // data: C#의 byte[] 배열을 넘기면, .NET이 알아서 그 배열을 잠깐 고정시켜서
        //		 C++에 "이 주소 부터 시작이야"라고 넘겨줌 (자동 핀 고정)
        [DllImport("VisionCore.dll", CallingConvention = CallingConvention.StdCall)]
        public static extern void Invert(byte[] data, int length);

        // GetMatInfo — C++ 쪽에서 byte 배열을 cv::Mat(표)로 감싸본 뒤,
        // 행(rows)/열(cols) 값을 다시 돌려주는 함수
        [DllImport("VisionCore.dll")]
        public static extern void GetMatInfo(
            byte[] data,        // 픽셀 데이터 배열 (M3때 만든 것과 같은 방식)
            int width,          // 원본 이미지 가로 크기 — 직접 알고 있어야 함
            int height,         // 원본 이미지 세로 크기
            out int rows,       // C++이 값을 채워 넣을 자리 — "출력 전용 상자"라는 뜻
            out int cols);      // 마찬가지

        // "VisionCore.dll" 이라는 사무실의 Add라는 창구로 전화 걸 거다, 라는 선언.
        // CallingConvention.StdCall — C++ 쪽 __stdcall이랑 반드시 짝을 맞춰야 함.
        // 여기 하나만 어긋나도 컴파일은 되는데 실행하면 값이 이상하게 나오거나 죽음.
        [DllImport("VisionCore.dll", CallingConvention = CallingConvention.StdCall)]

        // extern: "이 함수 몸체는 C#이 아니라 바깥(DLL)에 있다"는 뜻.
        // 이름(Add)은 C++쪽 명함에 적힌 이름과 대소문자까지 똑같아야 찾아짐.
        private static extern int Add(int a, int b);

        public MainWindow()
        {
            InitializeComponent();

            // 반전 전 원본값을 눈으로 확인할 수 있게 미리 정해둔 테스트용 배열
            byte[] testData = { 0, 100, 255 };

            // 여기서 C++로 "주소"가 넘어감 — testData 자체가 그 자리에서 바뀔지가 관건
            Invert(testData, testData.Length);

            // 호출이 끝난 뒤 "같은" 배열을 다시 읽음.
            // 복사본이었다면 여기 값은 그대로 {0, 100, 255}일 것이고,
            // 진짜 주소 전달이었다면 {255, 100, 0}으로 바뀌어 있을 것.
            string result = string.Join(", ", testData);
            MessageBox.Show($"Invert 결과: {result}");

            // 1. 화면에 뜬 것과 같은 파일을 다시 코드로 불러옴 (같은 팩 URI 사용)
            BitmapImage bitmapImage = new BitmapImage(new Uri("pack://application:,,,/Assets/test_m3_small.png"));

            // 2. "쓸 수 있는 캔버스" 형태로 변환.
            //    PixelFormats.Gray8 — 픽셀 하나 = 1바이트(0~255) 흑백 포맷.
            //    우리가 만든 샘플 이미지가 원래 흑백이라 이 포맷이 딱 맞음.
            WriteableBitmap writeableBitmap = new WriteableBitmap(
                new FormatConvertedBitmap(bitmapImage, PixelFormats.Gray8, null, 0));

            int width = writeableBitmap.PixelWidth;
            int height = writeableBitmap.PixelHeight;
            // WriteableBitmap이 알려주는 실제 stride를 그대로 사용
            // (Gray8이라 이론상 width와 같겠지만, 메모리 정렬 여유분이 붙을 수 있어 직접 물어보는 게 안전함)
            int stride = writeableBitmap.BackBufferStride;

            // 3. 픽셀 데이터를 담을 그릇(배열) 준비. 전체 크기 = stride * height
            byte[] pixels = new byte[stride * height];

            // CopyPixels: 이 캔버스의 물감 배치를 통째로 배열로 복사.
            writeableBitmap.CopyPixels(pixels, stride, 0);

            // 4. 확인용 — 앞부분 몇 바이트만 눈의로 찍어봄
            MessageBox.Show($"width={width}, height={height}, stride={stride}\n" +
                            $"pixels[0]={pixels[0]}, pixels[1]={pixels[1]}, pixels[2]={pixels[2]}");

            // 1. 방금 읽어온 진짜 픽셀 배열을 그대로 Invert에 넘김.
            //    testData(3칸)로 검증했던 것과 완전히 같은 원리 — 이번엔 배열이 진짜 이미지일 뿐.
            Invert(pixels, pixels.Length);

            // GetMatInfo 호출 — pixels 배열이 cv::Mat으로 잘 감싸지는지,
            // 우리가 이미 알고 있는 width/height(300, 300)와 rows/cols가 일치 하는지 확인
            GetMatInfo(pixels, width, height, out int rows, out int cols);

            // 여기서 미리 알고 있던 값(width=300, height=300)과
            // C++이 돌려준 값(cols, rows)이 똑같이 나와야 "표로 잘 정리됐다"는 쯧
            MessageBox.Show($"cv::Mat 확인 — rows={rows}, cols={cols} (원본 width={width}, height={height})");

            // 2. 반전된 pixels를 담을 "새 캔버스" 준비.
            //    width, height, dpi(96, 96 — 화면 기본 해상도), 픽셀 포맷은 원본과 동일하게 맟춰야 함.
            WriteableBitmap resultBitmap = new WriteableBitmap(width, height, 96, 96, PixelFormats.Gray8, null);

            // Int32Rect(0, 0, width, height) — "왼쪽 위 (0,0)부터 전체 영역"이라는 뜻
            Int32Rect fullarea = new Int32Rect(0, 0, width, height);

            // WritePixels: 반전된 pixels 배열의 내용을 이 새 캔버스에 실제로 그려 넣음
            resultBitmap.WritePixels(fullarea, pixels, stride, 0);

            // 3. 화면의 Image 컨트롤이 보여주는 그림을 이 새 캔버스로 교체
            MyImage.Source = resultBitmap;

            // 화면에 결과 띄우기 — 7이 나오면 국경 넘기 성공
            int addresult = Add(3, 4);
            // 생성자 안이라 창이 뜨는 시점에 바로 한 번 실행됨
            MessageBox.Show($"Add(3,4) = {addresult}");
        }
    }
}
