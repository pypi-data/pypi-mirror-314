import os
from . import menu
from .constants import clear_screen 
from . import tracking_module as search
from . import file_management as file_manager
from .motion_detector import start_packing_process
from .order_counter import count_orders_today
from .cache_cleaner import  clear_cache_and_exit

def main():
    try:
        # Chọn thư mục lưu trữ
        data_dir = file_manager.select_data_directory()
        cache_dir = os.path.join(os.path.dirname(__file__), '__pycache__')

        while True:
            
            choice = menu.display_menu()

            if choice == '1':
                start_packing_process(data_dir, cache_dir)
            elif choice == '2':
                search.search_tracking_id(data_dir)
            elif choice == '3':
                file_manager.ask_to_delete_old_folders(data_dir)
            elif choice == '4':
                count = count_orders_today(data_dir)
                print(f"\nTổng số đơn được quét trong ngày: {count}")
            elif choice == '5':
                clear_screen()
            elif choice == '6':
                clear_cache_and_exit(cache_dir)
                break
            else:
                print("\nLựa chọn không hợp lệ, vui lòng thử lại.")
    except KeyboardInterrupt:
        print("\nDừng chương trình.")

if __name__ == "__main__":
    main()
