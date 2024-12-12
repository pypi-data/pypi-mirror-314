import unittest
from shoplift_detector.video_processor import VideoProcessor


class TestVideoProcessor(unittest.TestCase):
    def test_video_processor_initialization(self):
        """Vérifier l'initialisation correcte de la classe VideoProcessor"""
        vp = VideoProcessor(video_path="examples/test_video.mp4")
        self.assertIsInstance(vp, VideoProcessor)

    def test_load_video(self):
        """Vérifier que la vidéo est bien chargée"""
        vp = VideoProcessor(video_path="examples/test_video.mp4")
        self.assertTrue(vp.load_video(), "La vidéo n'a pas pu être chargée.")

    def test_process_video(self):
        """Vérifier la logique de traitement de la vidéo"""
        vp = VideoProcessor(video_path="examples/test_video.mp4")
        if vp.load_video():
            ret, frame = vp.get_next_frame()
            self.assertTrue(ret, "Échec de la lecture d'une frame.")
            self.assertIsNotNone(frame, "La frame est vide.")
        else:
            self.skipTest("Vidéo non trouvée ou chargement échoué")


if __name__ == "__main__":
    unittest.main()
