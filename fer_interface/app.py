import base64
import json

from flask import Flask, render_template, request, jsonify

from fer_interface.fer.constants import output
from fer_interface.fer.facial_expression_recognition import FER
from fer_interface.fer.util import *

app = Flask(__name__)
fer = FER()


@app.route('/')
def index():
    init_setup()
    return render_template('index.html')


@app.route('/upload_file', methods=['GET', 'POST'])
def local_files():
    return add_info('upload_file.html')


@app.route('/process_file', methods=['POST'])
def process_file():
    uploaded_file = request.files['uploaded-file']
    # Se salveză fișierul temporar
    temp_file_path = output + 'old_images/' + generate_name('img_')
    uploaded_file.save(temp_file_path)
    # Se apelează metoda pentru a procesa fișierul temporar
    fer.predict_from_image(temp_file_path)
    # Se șterge fișierul temporar
    os.remove(temp_file_path)
    return render_template('upload_file.html')


@app.route('/web_camera', methods=['GET', 'POST'])
def web_camera():
    return add_info('web_camera.html')


@app.route('/process_file_webcamera', methods=['POST'])
def process_file_webcamera():
    file_to_process = output + "temp_webcam.jpg"
    if os.path.exists(file_to_process):
        fer.predict_from_image(file_to_process)
    return render_template('web_camera.html')


@app.route('/file-content')
def get_file_content():
    # Cod pentru citirea conținutului fișierului text
    with open('fer_interface/static/data_output/info.json', 'r') as file:
        content = file.read()
    return jsonify(content=content)


@app.route('/save_photo', methods=['POST'])
def save_photo():
    image_data = request.form['image_data']
    # Se decodează datele imaginii din formatul base64
    image_data = image_data.replace('data:image/png;base64,', '')
    image_data = image_data.encode()
    with open('fer_interface/static/data_output/temp_webcam.jpg', 'wb') as f:
        f.write(base64.b64decode(image_data))
    return "Savat cu succes!"


def add_info(url):
    try:
        with open('fer_interface/static/data_output/info.json', 'r') as file:
            data = json.load(file)
            data = json.dumps(data, indent=4)
        return render_template(url, info=data)
    except FileNotFoundError:
        return render_template(url)


if __name__ == '__main__':
    init_setup()
    app.run()
