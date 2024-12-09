import cv2
import time
import os
import shutil
from . import camera_module as camera
from . import file_management as file_manager
from .qr_scanner import detect_and_track_qr
from . import sound_module as sound
from . import overlay_module as overlay
from . import motion_detector
from . import cache_cleaner
from . import display_tracking_id_on_frame

def detect_motion(cap, min_area=500):
    """
    Phát hiện chuyển động bằng cách so sánh sự thay đổi giữa khung hình hiện tại và khung hình trước.
    """
    ret, frame1 = cap.read()
    if not ret:
        return False

    ret, frame2 = cap.read()
    if not ret:
        return False

    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)
    gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)

    diff = cv2.absdiff(gray1, gray2)

    _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) > min_area:
            return True

    return False

# def start_packing_process(data_dir, cache_dir):
#     cap = camera.init_camera()
#     if cap is None:
#         print("Không tìm thấy camera.")
#         return  # Không tìm thấy camera

#     recording = False
#     current_tracking_id = None
#     writer = None
#     last_motion_time = None

#     # Cấu hình video ghi lại
#     video_resolution = (1920, 1080)  # Độ phân giải HD
#     original_fps = 60  # FPS của camera realtime
#     codec = cv2.VideoWriter_fourcc(*'mp4v')  # Codec cho MP4

#     try:
#         while True:
#             # Đọc frame từ camera
#             ret, frame = camera.read_frame(cap)
#             if not ret:
#                 break

#             # Hiển thị khung hình realtime
#             frame_with_timestamp = overlay.overlay_datetime(frame.copy())  # Gắn timestamp vào khung hình

#             # Phát hiện và theo dõi mã QR
#             label_text, qr_roi = detect_and_track_qr(frame_with_timestamp)

#             # Nếu phát hiện mã QR và dữ liệu hợp lệ
#             if label_text:
#                 if current_tracking_id != label_text:
#                     print(f"Quét thành công đơn hàng: {label_text}")
                    
#                     # Kết thúc ghi hình video hiện tại (nếu đang ghi)
#                     if writer:
#                         writer.release()
#                         recording = False

#                     # Tạo thư mục lưu trữ
#                     tracking_dir = file_manager.create_tracking_directory(data_dir, label_text)
                    
#                     # Lưu ảnh với tên mã vận đơn
#                     image_filename = os.path.join(tracking_dir, f"{label_text}.jpg")
#                     frame_with_timestamp = display_tracking_id_on_frame.display_tracking_id_on_frame(frame_with_timestamp, label_text)
#                     cv2.imwrite(image_filename, frame_with_timestamp)
#                     # print(f"Đã chụp và lưu hình ảnh: {image_filename}")

#                     # Tạo file video để ghi lại quá trình
#                     video_filename = os.path.join(tracking_dir, f"{label_text}.mp4")
#                     writer = cv2.VideoWriter(video_filename, codec, original_fps, video_resolution)
#                     # print(f"Đã tạo file video: {video_filename}")
                    
#                     # Bắt đầu ghi hình video mới
#                     recording = True
#                     current_tracking_id = label_text
#                     last_motion_time = time.time()
#                     sound.play_success_sound()

#             # Hiển thị mã vận đơn nếu đã quét thành công
#             if current_tracking_id:
#                 frame_with_timestamp = display_tracking_id_on_frame.display_tracking_id_on_frame(
#                     frame_with_timestamp, current_tracking_id
#                 )

#             # Ghi lại video khi đang ghi
#             if recording:
#                 # Resize frame sang độ phân giải HD để ghi video
#                 frame_for_recording = cv2.resize(frame, video_resolution)

#                 # Gắn timestamp và mã vận đơn vào frame ghi
#                 frame_for_recording = overlay.overlay_datetime(frame_for_recording)
#                 frame_for_recording = display_tracking_id_on_frame.display_tracking_id_on_frame(frame_for_recording, current_tracking_id)

#                 writer.write(frame_for_recording)  # Ghi khung hình vào video

#                 # Kiểm tra phát hiện chuyển động
#                 if motion_detector.detect_motion(cap):
#                     last_motion_time = time.time()
#                 elif last_motion_time is not None and time.time() - last_motion_time > 45:
#                     print("\nKhông phát hiện chuyển động trong 45s, dừng ghi hình.")
#                     writer.release()
#                     recording = False
#                     break

#             # Hiển thị khung hình realtime (không resize để tiết kiệm hiệu năng)
#             cv2.imshow('E-commerce Packing Process', frame_with_timestamp)
#             if cv2.waitKey(1) & 0xFF == 27:  # Nhấn ESC để thoát
#                 break

#     finally:
#         if writer:
#             writer.release()
#         camera.release_camera(cap)
#         cv2.destroyAllWindows()
#         cache_cleaner.clear_cache(cache_dir)
#         if os.path.exists(cache_dir):
#             shutil.rmtree(cache_dir)

def start_packing_process(data_dir, cache_dir):
    cap = camera.init_camera()
    if cap is None:
        print("Không tìm thấy camera.")
        return  # Không tìm thấy camera

    recording = False
    current_tracking_id = None
    writer = None
    last_motion_time = None
    fps_real_time = 0
    fps_slow_motion = 0  # FPS giảm tốc độ
    prev_time = time.time()

    # Hệ số giảm tốc độ (giảm FPS)
    slow_motion_factor = 1  # Ghi video với 70% tốc độ thời gian thực

    # Cấu hình video ghi lại
    video_resolution = (1920, 1080)  # Độ phân giải HD
    codec = cv2.VideoWriter_fourcc(*'mp4v')  # Codec cho MP4

    try:
        while True:
            # Đọc frame từ camera
            ret, frame = camera.read_frame(cap)
            if not ret:
                break

            # Tính toán FPS thực tế
            current_time = time.time()
            fps_real_time = 1 / (current_time - prev_time)
            prev_time = current_time

            # Tính FPS chậm hơn
            fps_slow_motion = max(1, int(fps_real_time * slow_motion_factor))  # Đảm bảo FPS tối thiểu là 1

            # Hiển thị khung hình realtime
            frame_with_timestamp = overlay.overlay_datetime(frame.copy())  # Gắn timestamp vào khung hình

            # Phát hiện và theo dõi mã QR
            label_text, qr_roi = detect_and_track_qr(frame_with_timestamp)

            # Nếu phát hiện mã QR và dữ liệu hợp lệ
            if label_text:
                if current_tracking_id != label_text:
                    print(f"Quét thành công đơn hàng: {label_text}")

                    # Kết thúc ghi hình video hiện tại (nếu đang ghi)
                    if writer:
                        writer.release()
                        recording = False

                    # Tạo thư mục lưu trữ
                    tracking_dir = file_manager.create_tracking_directory(data_dir, label_text)

                    # Lưu ảnh với tên mã vận đơn
                    image_filename = os.path.join(tracking_dir, f"{label_text}.jpg")
                    frame_with_timestamp = display_tracking_id_on_frame.display_tracking_id_on_frame(
                        frame_with_timestamp, label_text
                    )
                    cv2.imwrite(image_filename, frame_with_timestamp)

                    # Tạo file video để ghi lại quá trình
                    video_filename = os.path.join(tracking_dir, f"{label_text}.mp4")
                    writer = cv2.VideoWriter(video_filename, codec, fps_slow_motion, video_resolution)

                    # Bắt đầu ghi hình video mới
                    recording = True
                    current_tracking_id = label_text
                    last_motion_time = time.time()
                    sound.play_success_sound()

            # Hiển thị mã vận đơn nếu đã quét thành công
            if current_tracking_id:
                frame_with_timestamp = display_tracking_id_on_frame.display_tracking_id_on_frame(
                    frame_with_timestamp, current_tracking_id
                )

            # Ghi lại video khi đang ghi
            if recording:
                # Resize frame sang độ phân giải HD để ghi video
                frame_for_recording = cv2.resize(frame, video_resolution)

                # Gắn timestamp và mã vận đơn vào frame ghi
                frame_for_recording = overlay.overlay_datetime(frame_for_recording)
                frame_for_recording = display_tracking_id_on_frame.display_tracking_id_on_frame(
                    frame_for_recording, current_tracking_id
                )

                writer.write(frame_for_recording)  # Ghi khung hình vào video

                # Kiểm tra phát hiện chuyển động
                if motion_detector.detect_motion(cap):
                    last_motion_time = time.time()
                elif last_motion_time is not None and time.time() - last_motion_time > 45:
                    print("\nKhông phát hiện chuyển động trong 45s, dừng ghi hình.")
                    writer.release()
                    recording = False
                    break

            # Hiển thị khung hình realtime (không resize để tiết kiệm hiệu năng)
            cv2.imshow('E-commerce Packing Process', frame_with_timestamp)
            if cv2.waitKey(1) & 0xFF == 27:  # Nhấn ESC để thoát
                break

    finally:
        if writer:
            writer.release()
        camera.release_camera(cap)
        cv2.destroyAllWindows()
        cache_cleaner.clear_cache(cache_dir)
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)
