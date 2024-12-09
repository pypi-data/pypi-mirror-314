import pygame
import os

# Khởi tạo pygame mixer
pygame.mixer.init()

# Lấy đường dẫn đến thư mục hiện tại
current_dir = os.path.dirname(__file__)

# Đường dẫn đến file âm thanh
success_sound_path = os.path.join(current_dir, 'sound', '3beeps-108353.mp3')

# Tải file âm thanh
success_sound = pygame.mixer.Sound(success_sound_path)

def play_success_sound():
    success_sound.play()
