from shoplift_detector.camera_stream import detect_from_camera
from shoplift_detector.video_processor import detect_from_video

if __name__ == "__main__":
    # Exemple d'utilisation
    # Lancer une détection depuis la caméra
    detect_from_camera()

    # Ou analyser une vidéo existante
    video_path = "examples/test_video.mp4"
    detect_from_video(video_path)
