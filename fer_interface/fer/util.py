import datetime
import os


def init_setup():
    """
    Pregătește mediul de lucru și șterge fișierele temporare.
    """
    file_paths = ['static/data_output/temp.jpg', 'static/data_output/info.json', 'static/data_output/temp_webcam.jpg']
    for file_path in file_paths:
        # Se verifică dacă fișierul există înainte de a-l șterge
        if os.path.exists(file_path):
            # Se șterge fișierul
            os.remove(file_path)
            print("The file {} has been deleted.".format(file_path))
        else:
            print("The file {} does not exist.".format(file_path))


def generate_time_now_str():
    """
    Generează un string pe baza datei și orei curente.
    :return: string-ul generat.
    """
    # Se obține ora curentă
    current_time = datetime.datetime.now()
    # Se formatează data după cum dorim (e.g., YYYY-MM-DD_HH-MM-SS)
    time_format = "%Y-%m-%d_%H-%M-%S"
    return current_time.strftime(time_format)


def generate_name(prefix):
    """
    :param prefix: prefix-ul adăugat in fața numelui.
    :return: nume.
    """
    name = prefix + generate_time_now_str()
    return name
