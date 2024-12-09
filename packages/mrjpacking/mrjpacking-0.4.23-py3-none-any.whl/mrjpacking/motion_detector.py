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

def start_packing_process(data_dir, cache_dir):
    cap = camera.init_camera()
    if cap is None:
        return  # Không tìm thấy camera

    recording = False
    current_tracking_id = None
    writer = None
    last_motion_time = None

    try:
        while True:
            ret, frame = camera.read_frame(cap)
            if not ret:
                break

            # Hiển thị thời gian lên khung hình
            frame_with_timestamp = overlay.overlay_datetime(frame.copy())

            # Phát hiện và theo dõi mã QR
            label_text, qr_roi = detect_and_track_qr(frame_with_timestamp)

            # Nếu phát hiện mã QR và dữ liệu hợp lệ
            if label_text:
                if current_tracking_id != label_text:
                    print(f"Quét thành công đơn hàng: {label_text}")
                    if writer:
                        writer.release()
                        recording = False

                    tracking_dir = file_manager.create_tracking_directory(data_dir, label_text)
                    image_filename, video_filename, writer = file_manager.save_files(tracking_dir, frame_with_timestamp, frame)
                    recording = True
                    current_tracking_id = label_text
                    last_motion_time = time.time()
                    sound.play_success_sound()

            # Hiển thị mã vận đơn nếu đã quét thành công
            if current_tracking_id:
                frame_with_timestamp = display_tracking_id_on_frame.display_tracking_id_on_frame(
                    frame_with_timestamp, current_tracking_id
                )

            if recording:     
                # Tạo một khung hình chỉ với ngày giờ và mã vận đơn, không có khung xanh
                frame_for_recording = overlay.overlay_datetime(frame.copy())
                if current_tracking_id:
                    frame_for_recording = display_tracking_id_on_frame.display_tracking_id_on_frame(frame_for_recording, current_tracking_id)

                writer.write(frame_for_recording)  # Ghi khung hình vào video

                # Kiểm tra phát hiện chuyển động 
                if motion_detector.detect_motion(cap):
                    last_motion_time = time.time()
                elif last_motion_time is not None and time.time() - last_motion_time > 45:
                    print("\nKhông phát hiện chuyển động trong 45s, dừng ghi hình.")
                    writer.release()
                    break

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
