using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
// P/Invoke 쓰려면 이 네임스페이스 필수 —
// "네이티브(비관리) 코드랑 소통하는 도구함"
using System.Runtime.InteropServices;

namespace VisionApp
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
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

            // 화면에 결과 띄우기 — 7이 나오면 국경 넘기 성공
            int result = Add(3, 4);
            // 생성자 안이라 창이 뜨는 시점에 바로 한 번 실행됨
            MessageBox.Show($"Add(3,4) = {result}");
        }
    }
}
