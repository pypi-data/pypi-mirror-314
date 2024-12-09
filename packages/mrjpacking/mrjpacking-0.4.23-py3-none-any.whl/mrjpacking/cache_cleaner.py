import os
import shutil

def get_directory_size(directory):
    """
    Tính tổng dung lượng của thư mục (tính cả tệp con).
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def clear_cache(cache_dir="__pycache__"):
    """
    Xóa thư mục bộ nhớ đệm (cache) cụ thể (ví dụ: __pycache__)
    và hiển thị dung lượng đã xóa.
    """
    if os.path.exists(cache_dir):
        try:
            # Tính dung lượng thư mục trước khi xóa
            size_before_deletion = get_directory_size(cache_dir)

            # Xóa toàn bộ thư mục bộ nhớ đệm
            shutil.rmtree(cache_dir)

            # Chuyển đổi dung lượng từ bytes sang MB
            size_in_mb = size_before_deletion / (1024 * 1024)
            print(f"\nĐã xóa: {size_in_mb:.2f} MB bộ nhớ đệm.")
        except Exception as e:
            print(f"Lỗi khi xóa bộ nhớ đệm: {str(e)}")
    else:
        print(f"\nKhông còn bộ nhớ đệm.")

def clear_cache_and_exit(cache_dir):
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)
    print("Hẹn gặp lại!!!")