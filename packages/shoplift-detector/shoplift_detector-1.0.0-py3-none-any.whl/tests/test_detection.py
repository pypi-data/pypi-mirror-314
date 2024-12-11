import unittest
from shoplift_detector.detection import ShopliftingPrediction


class TestShopliftingPrediction(unittest.TestCase):
    def test_initialize_prediction(self):
        """Vérifier l'initialisation de la classe"""
        sp = ShopliftingPrediction(model_path="shoplift_detector/models/lrcn_160S_90_90Q.h5")
        self.assertIsInstance(sp, ShopliftingPrediction)

    def test_load_model(self):
        """Vérifier si le modèle est chargé correctement"""
        sp = ShopliftingPrediction(model_path="shoplift_detector/models/lrcn_160S_90_90Q.h5")
        sp.load_model()
        self.assertIsNotNone(sp.model, "Le modèle n'a pas été chargé correctement.")

    def test_predict(self):
        """Vérifier le fonctionnement de la prédiction"""
        sp = ShopliftingPrediction(model_path="shoplift_detector/models/lrcn_160S_90_90Q.h5")
        sp.load_model()
        input_data = [[0] * 90] * 160  # Entrée factice simulant une séquence
        prediction = sp.predict(input_data)
        self.assertIsInstance(prediction, (int, float), "La prédiction doit être un nombre.")
        self.assertGreaterEqual(prediction, 0, "La prédiction doit être positive.")


if __name__ == "__main__":
    unittest.main()
