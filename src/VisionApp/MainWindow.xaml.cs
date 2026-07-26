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

            // 화면에 결과 띄우기 — 7이 나오면 국경 넘기 성공
            int addresult = Add(3, 4);
            // 생성자 안이라 창이 뜨는 시점에 바로 한 번 실행됨
            MessageBox.Show($"Add(3,4) = {addresult}");
        }
    }
}
