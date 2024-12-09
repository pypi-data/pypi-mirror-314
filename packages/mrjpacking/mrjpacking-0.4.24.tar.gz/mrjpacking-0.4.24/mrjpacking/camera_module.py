import cv2
from pygrabber.dshow_graph import FilterGraph

def get_camera_names():
    # Sử dụng pygrabber để lấy danh sách các tên camera
    graph = FilterGraph()
    camera_names = graph.get_input_devices()
    return camera_names

def is_camera_in_use(index):
    # Kiểm tra trạng thái camera, nếu không mở được nghĩa là đang bận
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    if not cap.isOpened():
        return True  # Camera đang bận
    cap.release()
    return False  # Camera không bận

def list_available_cameras():
    available_cameras = []
    camera_names = get_camera_names()
    num_cameras = len(camera_names)

    for index in range(num_cameras):
        # Lấy tên camera
        cam_name = camera_names[index] if index < len(camera_names) else f"Unknown Camera {index}"

        # Kiểm tra trạng thái camera
        if is_camera_in_use(index):
            cam_name += " (Camera hiện tại đang bận)"
        available_cameras.append((index, cam_name))

    # Hiển thị danh sách camera với trạng thái
    if available_cameras:
        print(f"\nĐã tìm thấy {len(available_cameras)} camera:")
        for i, (cam_index, cam_name) in enumerate(available_cameras):
            print(f"{i + 1}. {cam_name}")
        choice = int(input("Chọn camera (nhập số): ")) - 1
        selected_index = available_cameras[choice][0]
        selected_name = available_cameras[choice][1]

        # Kiểm tra lại camera đã chọn để mở
        cap = cv2.VideoCapture(selected_index, cv2.CAP_DSHOW)
        if cap.isOpened():
            print(f"Camera đã được chọn: {selected_name}")
            return cap
        else:
            print("\nLỗi: Không thể mở camera, kiểm tra lại kết nối hoặc thiết bị.")
            return None
    else:
        print("\nKhông tìm thấy camera nào khả dụng.")
        return None

def init_camera():
    cap = list_available_cameras()
    if cap is None:
        return None
    return cap

def release_camera(cap):
    if cap:
        cap.release()

def read_frame(cap):
    ret, frame = cap.read()
    return ret, frame
