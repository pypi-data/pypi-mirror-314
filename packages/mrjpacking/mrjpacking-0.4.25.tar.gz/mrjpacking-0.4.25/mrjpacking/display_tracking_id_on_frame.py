import cv2
from .constants import TEXT_COLOR

def display_tracking_id_on_frame(frame, tracking_id):
    """
    Hiển thị mã vận đơn ở góc dưới bên phải khung hình.
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.8
    thickness = 2

    # Lấy kích thước khung hình
    frame_height, frame_width = frame.shape[:2]

    # Tính toán vị trí cho văn bản (góc dưới bên phải)
    text_size, _ = cv2.getTextSize(tracking_id, font, font_scale, thickness)
    text_x = frame_width - text_size[0] - 10  # Cách lề phải 10 pixels
    text_y = frame_height - 10  # Cách lề dưới 10 pixels

    # Vẽ văn bản lên khung hình
    cv2.putText(frame, tracking_id, (text_x, text_y), font, font_scale, TEXT_COLOR, thickness)
    return frame
