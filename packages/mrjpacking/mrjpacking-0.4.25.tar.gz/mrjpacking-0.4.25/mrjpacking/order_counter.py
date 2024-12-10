import os
from datetime import datetime
from .constants import display_all_orders

def count_orders_today(data_directory):
    """Đếm tổng số đơn quét được trong ngày và hiển thị mã vận đơn theo bưu cục."""
    today = datetime.now().date()
    count = 0
    orders_info = []  # Danh sách lưu mã vận đơn và thời gian quét

    for folder_name in os.listdir(data_directory):
        folder_path = os.path.join(data_directory, folder_name)
        if os.path.isdir(folder_path):
            # Lấy thời gian tạo của thư mục
            creation_time = os.path.getctime(folder_path)
            creation_date = datetime.fromtimestamp(creation_time).date()

            # Kiểm tra xem thư mục có được tạo trong ngày hôm nay không
            if creation_date == today:
                count += 1
                # Lưu mã vận đơn và thời gian quét
                orders_info.append((folder_name, datetime.fromtimestamp(creation_time)))

    orders_info_sorted = sorted(orders_info, key=lambda x: x[1])  # Sắp xếp theo thời gian

    # Hiển thị thông tin mã vận đơn theo bưu cục
    if orders_info_sorted:
        display_all_orders(orders_info_sorted)

    return count
