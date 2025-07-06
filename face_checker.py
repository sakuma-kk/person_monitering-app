# face_checker.py
import face_recognition
import cv2
import os

class FaceChecker:
    def __init__(self, known_faces_dir='known_faces'):
        self.known_encodings = []
        self.load_known_faces(known_faces_dir)
        if not self.known_encodings:
            print("[警告] known_faces フォルダに有効な顔画像が見つかりませんでした。顔チェックは無効になります。")
            self.face_check_enabled = False
        else:
            self.face_check_enabled = True

    def load_known_faces(self, directory):
        for file in os.listdir(directory):
            path = os.path.join(directory, file)
            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                self.known_encodings.append(encodings[0])

    def is_user_present(self, frame):
        if not self.face_check_enabled:
            return False
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        faces = face_recognition.face_encodings(rgb_small)
        for face_encoding in faces:
            matches = face_recognition.compare_faces(self.known_encodings, face_encoding, tolerance=0.5)
            if any(matches):
                return True
        return False
