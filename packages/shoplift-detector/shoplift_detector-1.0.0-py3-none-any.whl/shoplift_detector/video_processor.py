import cv2
from shoplift_detector.detection import ShopliftingPrediction

def detect_from_video(video_path):
    model = ShopliftingPrediction(
        model_path="shoplift_detector/models/lrcn_160S_90_90Q.h5",
        frame_width=90, frame_height=90, sequence_length=160
    )
    model.load_model()

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Erreur : Impossible de lire la vidéo {video_path}.")
        return

    _, prev_frame = cap.read()
    frames_queue = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        preprocessed_frame = model.preprocess_frame(frame, prev_frame)
        prev_frame = frame.copy()
        frames_queue.append(preprocessed_frame)

        if len(frames_queue) == model.sequence_length:
            probability, label = model.predict(frames_queue)
            print(f"Probabilité : {probability}%, Label : {label}")
            frames_queue = []

        cv2.imshow("Analyse vidéo", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
