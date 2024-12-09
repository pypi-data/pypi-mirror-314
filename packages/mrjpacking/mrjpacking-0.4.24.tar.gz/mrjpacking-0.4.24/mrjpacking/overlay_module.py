import cv2
import datetime
from .constants import TEXT_COLOR, FRAME_COLOR, frame_width, frame_height

def overlay_datetime(frame):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text_size = cv2.getTextSize(timestamp, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
    cv2.putText(frame, timestamp, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, TEXT_COLOR, 2, cv2.LINE_AA)
    return frame

def draw_green_frame(frame):
    frame_h, frame_w, _ = frame.shape
    top_left = ((frame_w - frame_width) // 2, (frame_h - frame_height) // 2)
    bottom_right = (top_left[0] + frame_width, top_left[1] + frame_height)
    cv2.rectangle(frame, top_left, bottom_right, FRAME_COLOR, 2)
    return frame
