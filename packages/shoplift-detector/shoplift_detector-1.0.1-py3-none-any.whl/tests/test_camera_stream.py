import unittest
from shoplift_detector.camera_stream import CameraStream


class TestCameraStream(unittest.TestCase):
    def test_initialization(self):
        """Test l'initialisation de la classe CameraStream"""
        stream = CameraStream(source=0)
        self.assertIsInstance(stream, CameraStream)

    def test_stream_setup(self):
        """Vérifier que la connexion au flux est correctement établie"""
        stream = CameraStream(source=0)
        self.assertTrue(stream.initialize_stream(), "Échec de la connexion au flux vidéo.")

    def test_read_frame(self):
        """Vérifier la lecture de la vidéo depuis la caméra"""
        stream = CameraStream(source=0)
        if stream.initialize_stream():
            ret, frame = stream.get_frame()
            self.assertTrue(ret, "Échec de la récupération du frame depuis la caméra.")
            self.assertIsNotNone(frame, "Le frame récupéré est vide.")
        else:
            self.skipTest("Caméra non disponible")


if __name__ == "__main__":
    unittest.main()
