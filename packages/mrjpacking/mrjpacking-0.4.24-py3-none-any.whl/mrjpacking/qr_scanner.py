import cv2
import numpy as np
from .constants import FRAME_COLOR

detector = cv2.QRCodeDetector()

def preprocess_frame(frame):
    """Tiền xử lý khung hình để tăng cường phát hiện mã QR."""
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Chuyển đổi sang thang độ xám
    blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)  # Làm mờ để giảm nhiễu
    return blurred_frame

def capture_label_from_roi(frame, roi):
    """Giải mã mã QR trong vùng ROI đã phát hiện."""
    x, y, w, h = roi
    cropped_frame = frame[y:y+h, x:x+w]  # Cắt vùng chứa mã QR
    data, _, _ = detector.detectAndDecode(cropped_frame)
    return data

def detect_and_track_qr(frame):
    """Phát hiện và theo dõi mã QR trong khung hình."""
    processed_frame = preprocess_frame(frame)

    try:
        # Phát hiện và giải mã mã QR
        data, vertices, _ = detector.detectAndDecode(processed_frame)
        
        # Kiểm tra nếu phát hiện mã QR hợp lệ
        if vertices is not None and data:
            vertices = vertices[0].astype(int)
            x, y, w, h = cv2.boundingRect(vertices)

            # Tạo khung xanh cách mã QR 5 pixel
            expanded_roi = (max(0, x-5), max(0, y-5), w+10, h+10)
            cv2.polylines(frame, [vertices], isClosed=True, color=FRAME_COLOR, thickness=3)
            
            # Trả về dữ liệu và vùng được phát hiện để giải mã
            return data, expanded_roi
        else:
            # Nếu không giải mã được mã QR, tiếp tục tìm kiếm mã QR
            return None, None

    except cv2.error:
        pass

    return None, None