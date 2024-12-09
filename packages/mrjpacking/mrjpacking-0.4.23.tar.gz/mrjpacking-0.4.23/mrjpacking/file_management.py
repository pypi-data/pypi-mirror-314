import os
import cv2
import time
import shutil
import datetime
import keyboard
from .menu import print_title
from tkinter import Tk
from tkinter.filedialog import askdirectory
from .constants import MAX_FOLDER_AGE_SECONDS

def print_table(folders):
    """In bảng chứa thông tin các thư mục theo dạng bảng với khung"""
    # Độ rộng cột
    name_width = max([len(folder['Tên']) for folder in folders]) + 6
    date_width = 30
    age_width = 35

    # Header
    print(f"+{'-' * name_width}+{'-' * date_width}+{'-' * age_width}+")
    print(f"| {'Tên':^{name_width - 2}} | {'Ngày Tạo':^{date_width - 2}} | {'Thời Gian':^{age_width - 2}} |")
    print(f"+{'-' * name_width}+{'-' * date_width}+{'-' * age_width}+")

    # Dữ liệu
    for folder in folders:
        print(f"| {folder['Tên']:<{name_width - 2}} | {folder['Ngày Tạo']:<{date_width - 2}} | {folder['Thời Gian']:<{age_width - 2}} |")
        print(f"+{'-' * name_width}+{'-' * date_width}+{'-' * age_width}+")


def clear_console():
    """Xóa màn hình console"""
    os.system('cls' if os.name == 'nt' else 'clear')


def list_old_folders(data_directory):
    """Liệt kê các thư mục đã được tạo quá 30 ngày"""
    current_time = time.time()
    old_folders = []

    for folder_name in os.listdir(data_directory):
        folder_path = os.path.join(data_directory, folder_name)
        if os.path.isdir(folder_path):
            folder_creation_time = os.path.getctime(folder_path)
            folder_age = current_time - folder_creation_time

            if folder_age >= MAX_FOLDER_AGE_SECONDS:
                creation_time_formatted = datetime.datetime.fromtimestamp(folder_creation_time).strftime('%Y-%m-%d %H:%M:%S')
                age_days = folder_age // (24 * 3600)
                age_hours = (folder_age % (24 * 3600)) // 3600
                age_minutes = (folder_age % 3600) // 60

                old_folders.append({
                    'Tên': folder_name,
                    'Ngày Tạo': creation_time_formatted,
                    'Thời Gian': f"{int(age_days)} ngày, {int(age_hours)} giờ, {int(age_minutes)} phút"
                })
    return old_folders

def delete_old_folders(data_directory):
    current_time = time.time()
    for folder_name in os.listdir(data_directory):
        folder_path = os.path.join(data_directory, folder_name)
        if os.path.isdir(folder_path):
            folder_creation_time = os.path.getctime(folder_path)
            folder_age = current_time - folder_creation_time
            if folder_age >= MAX_FOLDER_AGE_SECONDS:
                shutil.rmtree(folder_path)
                print(f"\nĐã xóa thư mục: {folder_name} vì đã đủ 30 ngày.")

def ask_to_delete_old_folders(data_directory):
    old_folders = list_old_folders(data_directory)
    folder_count = len(old_folders)
    if old_folders:
        print("\nCác thư mục đã tạo quá 30 ngày:")
        print_table(old_folders)  # In theo dạng bảng
        # for folder in old_folders:
        #     print(f"- {folder}")
        answer = input("Bạn có muốn xóa {folder_count} thư mục này không? (y/n): ").strip().lower()
        if answer == 'y':
            delete_old_folders(data_directory)
    else:
        print("\nKhông có thư mục nào quá hạn để xóa.")

def select_data_directory():

    print_title()

    """Hàm này cho phép người dùng chọn thư mục lưu hoặc nhập đường dẫn."""
    print("\nChọn thư mục lưu trữ hoặc nhập đường dẫn trực tiếp:")
    selected_dir = input("Nhập đường dẫn lưu trữ (hoặc bấm Enter để mở thư mục chọn): ").strip()

    # Nếu người dùng không nhập, yêu cầu họ chọn thư mục
    if not selected_dir:
        try:
            import tkinter as tk
            from tkinter import filedialog

            root = tk.Tk()
            root.withdraw()  # Ẩn cửa sổ chính
            selected_dir = filedialog.askdirectory()  # Mở hộp thoại chọn thư mục
        except ImportError:
            print("Không thể sử dụng giao diện đồ họa. Vui lòng nhập đường dẫn thủ công.")
    
    # Kiểm tra nếu người dùng vẫn không chọn hoặc nhập, thoát chương trình
    if not selected_dir or not os.path.exists(selected_dir):
        print("Không chọn thư mục. Chương trình sẽ kết thúc.")
        exit()

    print(f"Thư mục lưu trữ đã chọn: {selected_dir}")
    return selected_dir

def create_tracking_directory(data_dir, tracking_id):
    """Tạo thư mục cho mã vận đơn mới."""
    tracking_dir = os.path.join(data_dir, tracking_id)
    os.makedirs(tracking_dir, exist_ok=True)
    return tracking_dir

def save_files(tracking_dir, frame_with_timestamp, frame):
    """Lưu hình ảnh và video vào thư mục."""
    # Lưu hình ảnh
    image_filename = os.path.join(tracking_dir, f"label_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    cv2.imwrite(image_filename, frame_with_timestamp)

    # Lưu video
    video_filename = os.path.join(tracking_dir, f"packing_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.avi")
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    writer = cv2.VideoWriter(video_filename, fourcc, 20.0, (frame.shape[1], frame.shape[0]))

    return image_filename, video_filename, writer