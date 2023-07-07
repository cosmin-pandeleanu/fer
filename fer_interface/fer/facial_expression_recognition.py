import json
import os

import cv2
import numpy as np
from keras.models import model_from_json
from fer_interface.fer.constants import *
from fer_interface.fer.logging import *
from fer_interface.fer.util import generate_time_now_str


class FER:
    """
    Clasa FER este utilizată pentru gestionarea mai ușoară a componentei de AI utilizată în cadrul aplicației.
    """

    def __init__(self):
        self.model = self._load_model()

    def _load_model(self):
        """
        Metoda load_model este responsabilă de încărcarea arhitecturii modelului
        din fișierul model.JSON și a greutăților modelului din fișierul model.H5.
        :return: model
        """

        model = None
        try:
            json_file = open(model_path, 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            model = model_from_json(loaded_model_json)
        except FileNotFoundError:
            log_error(error_message="Error: File  %s  not found!" % model_path)

        # Încărcarea "greutăților" din fișierul model.h5
        if not os.path.exists(model_weights_path):
            log_error(error_message="Error: File  %s  not found!" % model_weights_path)
        model.load_weights(model_weights_path)

        return model

    def predict_from_image(self, image_path):
        """
        Metoda predict_from_image primește datele (image_path) pe care să le utilizeze pentru predicție.
        Se generează un fișier temp.jpg cu imaginea rezultată în urma procesării și un fișier info.json
        cu rezultatele obținute.
        :param image_path: Path către imaginea care urmează să fie procesată.
        """
        info = dict()  # variabilă utilizată pentru a reține datele importante obținute în urma unei procesări
        info["Data procesarii imaginii"] = generate_time_now_str()

        if not os.path.exists(facecasc_path):
            log_error(error_message="Error: File  %s  not found!" % facecasc_path)

        facecasc = cv2.CascadeClassifier(facecasc_path)
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detectează fețele în imaginea în tonuri de gri folosind clasificatorul în cascada pentru fețe.
        # scaleFactor: determină cât de mult se redimensionează ferestrele de căutare la fiecare etapă.
        # minNeighbors: specifică câți vecini ar trebui să aibă o detectare pentru a fi acceptată ca feță.
        faces = facecasc.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=10)

        info["Numarul de fete detectate"] = len(faces)

        i = 1
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 10)
            roi_gray = gray[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
            prediction = self.model.predict(cropped_img)
            # result_percentages = np.round(prediction * 100, 2).tolist()
            # print(f"Persoana {i}")
            # for j in range(0, 7):
            #     print(f"Clasa {emotion_dict[j]}: {round(result_percentages[0][j], 3)} %")
            maxindex = int(np.argmax(prediction))
            info["Persoana %s" % i] = emotion_dict[maxindex]
            cv2.putText(image, emotion_dict[maxindex], (x + 10, y - 20), cv2.FONT_HERSHEY_COMPLEX, 1.5, (255, 255, 255),
                        2)
            i += 1

        # Se salvează imaginea rezultată în urma procesării pentru a putea fi afișate ulterior in aplicație
        cv2.imwrite(output + "temp.jpg", image)
        # Se salvează rezultatele pentru a putea fi afișate ulterior in aplicație
        with open(output + 'info.json', "w") as json_file:
            json.dump(info, json_file, indent=4, sort_keys=True)
        # Se scrie un log de succes cu rezultatele obținute
        log_success(success_message=info)
