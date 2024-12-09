import os
import subprocess

def search_tracking_id(data_directory):
    while True:
        tracking_id = input("\nNhập mã vận đơn (hoặc gõ 'exit' để thoát): ").strip()

        if tracking_id.lower() == 'exit':
            break

        tracking_dir = os.path.join(data_directory, tracking_id)
        if os.path.exists(tracking_dir):
            print(f"Mở thư mục: {tracking_dir}")
            if os.name == 'nt':  # Windows
                os.startfile(tracking_dir)
            elif os.name == 'posix':  # MacOS, Linux
                subprocess.call(['open', tracking_dir] if os.uname().sysname == 'Darwin' else ['xdg-open', tracking_dir])
        else:
            print("\nKhông tìm thấy mã đơn hàng.")
