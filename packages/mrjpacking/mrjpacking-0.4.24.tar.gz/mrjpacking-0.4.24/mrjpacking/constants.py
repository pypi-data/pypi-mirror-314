import requests
import requests
import os
from packaging import version
import importlib.metadata
import datetime

FRAME_COLOR = (0, 255, 0)
TEXT_COLOR = (0, 165, 255)
frame_width, frame_height = 400, 400

MAX_FOLDER_AGE_DAYS = 30
SECONDS_IN_A_DAY = 86400
MAX_FOLDER_AGE_SECONDS = MAX_FOLDER_AGE_DAYS * SECONDS_IN_A_DAY

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def filter_orders_by_prefix(orders_info, prefix):
    """Lọc danh sách mã vận đơn theo tiền tố."""
    return [(order_id, scan_time) for order_id, scan_time in orders_info if order_id.startswith(prefix)]

def display_order_info(orders_info, title, prefix):
    """Hiển thị thông tin mã vận đơn theo tiền tố và tiêu đề tương ứng."""
    filtered_orders = filter_orders_by_prefix(orders_info, prefix)

    if filtered_orders:
        print(f"\n{title:<25} {'Ngày':<15} {'Giờ':<10}")
        print("-" * 50)
        for order_id, scan_time in filtered_orders:
            date_str = scan_time.strftime('%d-%m-%Y')
            time_str = scan_time.strftime('%H:%M:%S')
            print(f"{order_id:<25} {date_str:<15} {time_str:<10}")
        print(f"Tổng số {title}: {len(filtered_orders)}\n")

def is_viettel_post(order_id):
    """Kiểm tra mã vận đơn có phải là của Viettel Post không."""
    return len(order_id) == 13 and order_id.isdigit()

def is_vnpost(order_id):
    """Kiểm tra mã vận đơn có phải là của VNPost không."""
    return (len(order_id) >= 4 and  # Đảm bảo mã có ít nhất 4 ký tự
            order_id[:2].isalpha() and
            order_id[:2].isupper() and  # Kiểm tra ký tự đầu tiên phải là chữ in hoa
            order_id[-2:] == "VN" and  # Kiểm tra hai ký tự cuối là "VN"
            order_id[:3] not in ["NJV", "TTVN", "VNG"])  # Kiểm tra không phải là NJV, TTVN, hoặc VNG

def display_all_orders(orders_info):
    """Hiển thị mã vận đơn cho tất cả các bưu cục đã quét trong ngày."""
    post_offices = [
        ('J&T Express', '85'),
        ('Ninja Van', 'NJV'),
        ('GHN', 'VNG'),
        ('Shopee Express', 'SPXVN'),
        ('Best Express', 'TTVN'),
        ('GHTK', '15')
    ]

    for title, prefix in post_offices:
        # Lọc các đơn hàng cho bưu cục này
        filtered_orders = filter_orders_by_prefix(orders_info, prefix)
        if filtered_orders:  # Chỉ hiển thị bưu cục có đơn hàng
            display_order_info(filtered_orders, title, prefix)


def check_for_updates():
    try:
        # Gọi API của PyPI để lấy thông tin phiên bản mới nhất
        response = requests.get("https://pypi.org/pypi/mrjpacking/json", timeout=5)
        if response.status_code == 200:
            # latest_version = response.json()["info"]["version"]

            # Lấy phiên bản hiện tại của thư viện
            current_version = importlib.metadata.version("mrjpacking")
        
            return current_version
        
    except Exception as e:
        print("\nCó lỗi xảy ra khi kiểm tra phiên bản:", e)
        return None  # Trả về None nếu có lỗi xảy ra
