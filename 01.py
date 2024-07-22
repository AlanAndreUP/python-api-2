from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import face_recognition
from PIL import Image
from io import BytesIO
import datetime
import os

app = Flask(__name__)
CORS(app)  # Habilitar CORS

# Configuración de la conexión a MongoDB
mongo_client = MongoClient("mongodb+srv://223208:bRJCca6JSUpWBpT2@cluster0.swir3km.mongodb.net")
db = mongo_client["passengers_db"]
collection = db["passenger_count"]

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    try:
        file = request.files['image']
        img = Image.open(file.stream)  # Cambiar la forma en que se lee la imagen
        img_array = face_recognition.load_image_file(file)
        face_locations = face_recognition.face_locations(img_array)
        face_count = len(face_locations)

        record = {
            "timestamp": datetime.datetime.now(),
            "face_count": face_count
        }

        collection.insert_one(record)
        return jsonify({"face_count": face_count}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
