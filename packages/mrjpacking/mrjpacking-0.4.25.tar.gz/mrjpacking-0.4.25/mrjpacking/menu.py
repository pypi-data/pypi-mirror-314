import shutil
import pyfiglet
from .constants import check_for_updates

current_version=check_for_updates()

def display_menu():
    try:
        # Tạo khung cho menu
        border = "*" * 30
        print("\n" + border)
        print("Chọn một công cụ:")
        print("1. Đóng hàng")
        print("2. Tìm mã vận đơn")
        print("3. Xóa đơn quá 30 ngày")
        print("4. Đơn quét được trong ngày")
        print("5. Làm sạch màn hình")
        print("6. Bấm số 6 để thoát chương trình")
        print(border)

        choice = input("Nhập lựa chọn của bạn (1-6): ").strip()
        return choice
    except KeyboardInterrupt:
        print()


def print_title():
    # Lấy chiều rộng của terminal
    terminal_width = shutil.get_terminal_size().columns
    
    # Tạo tiêu đề bằng pyfiglet
    title_text = "E-COMMERCE PACKING"
    ascii_title = pyfiglet.figlet_format(title_text, "slant")
    
    # Đo số lượng ký tự của tiêu đề
    # title_length = len(ascii_title)
    
    # Chia từng dòng của tiêu đề và căn giữa
    ascii_lines = ascii_title.splitlines()
    title_width = max(len(line) for line in ascii_lines)
    
    # Tạo viền trên
    print("=" * terminal_width)
    
    # In từng dòng của ASCII art và căn giữa mỗi dòng
    if title_width <= terminal_width:
        for line in ascii_lines:
            padding = (terminal_width - len(line)) // 2
            print(' ' * padding + line)
    else:
        # Nếu tiêu đề lớn hơn hoặc bằng chiều rộng terminal, xuống dòng
        for line in ascii_lines:
            print(line)
    
    # Tạo viền dưới
    print("=" * terminal_width)
    
    # Thêm chữ ký ở góc phải
    signature = "Design by: Justin Nguyen"
    signature_padding = terminal_width - len(signature)
    print(' ' * signature_padding + signature)

    # Thông tin liên hệ
    print(f"Version: {current_version}")
    print("Telegram: @Justin_Nguyen_97")
    print("Whatsapp: 0982579098")
    print("Email: justinnguyen.7997@gmail.com")