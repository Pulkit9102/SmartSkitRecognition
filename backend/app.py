from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import numpy as np
from PIL import Image
import io
import os
import json
from serpapi import GoogleSearch
from dotenv import load_dotenv
import cv2
import numpy as np


load_dotenv()

app = Flask(__name__)
CORS(app)

def is_skin_image(file):
    file_bytes = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    img = cv2.resize(img, (100, 100))
    img = cv2.GaussianBlur(img, (5,5), 0)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower = np.array([0, 20, 70], dtype=np.uint8)
    upper = np.array([20, 255, 255], dtype=np.uint8)

    mask = cv2.inRange(hsv, lower, upper)

    skin_ratio = np.sum(mask > 0) / (100 * 100)

    return skin_ratio > 0.2

# Paths relative to this file's location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'skin_disease_model.h5')
CLASS_NAMES_PATH = os.path.join(BASE_DIR, 'model', 'class_names.json')
SERP_API_KEY = os.getenv('SERP_API_KEY', '')

model = None
class_names = []


def load_model_and_classes():
    global model, class_names

    try:
        import tf_keras as keras
    except ImportError:
        try:
            import tensorflow as tf
            keras = tf.keras
        except Exception as e:
            print("TensorFlow not available:", str(e))
            model = None
            keras = None

    if 'keras' not in dir():
        keras = None

    if keras is not None:
        try:
            if os.path.exists(MODEL_PATH):
                model = keras.models.load_model(MODEL_PATH)
                print("Model loaded successfully!")
            else:
                print(f"Model not found at {MODEL_PATH}")
        except Exception as e:
            print(f"Error loading model: {str(e)}")

    try:
        if os.path.exists(CLASS_NAMES_PATH):
            with open(CLASS_NAMES_PATH, 'r') as f:
                class_names = json.load(f)
            print(f"Classes loaded: {class_names}")
        else:
            print(f"Class names not found at {CLASS_NAMES_PATH}")
    except Exception as e:
        print(f"Error loading class names: {str(e)}")


def preprocess_image(image, target_size=(64, 64)):
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image = image.resize(target_size)
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    return image_array


def get_serpapi_recommendations(disease_name):
    if not SERP_API_KEY:
        return {'recommendations': [], 'search_query': f'{disease_name} skin disease treatment recommendations'}

    try:
        params = {
            'engine': 'google',
            'q': f'{disease_name} skin disease treatment recommendations',
            'api_key': SERP_API_KEY,
            'num': 5
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        recommendations = []
        if 'organic_results' in results:
            for result in results['organic_results'][:5]:
                recommendations.append({
                    'title': result.get('title', ''),
                    'link': result.get('link', ''),
                    'snippet': result.get('snippet', '')
                })
        return {'recommendations': recommendations, 'search_query': params['q']}
    except Exception as e:
        return {'recommendations': [], 'search_query': '', 'error': str(e)}


def search_similar_images(disease_name):
    if not SERP_API_KEY:
        return {'images': []}

    try:
        params = {
            'engine': 'google_images',
            'q': f'{disease_name} skin disease',
            'api_key': SERP_API_KEY,
            'num': 5
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        images = []
        if 'images_results' in results:
            for img in results['images_results'][:5]:
                images.append({
                    'thumbnail': img.get('thumbnail', ''),
                    'source': img.get('source', ''),
                    'link': img.get('link', '')
                })
        return {'images': images}
    except Exception as e:
        return {'images': [], 'error': str(e)}


@app.route('/', methods=['GET'])
def root():
    return jsonify({'message': 'Skin Disease Detection backend is running', 'health': '/api/health'})


@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return Response(status=204)


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'classes_loaded': len(class_names) > 0,
        'serpapi_configured': bool(SERP_API_KEY)
    })


@app.route('/api/classes', methods=['GET'])
def get_classes():
    return jsonify({'classes': class_names, 'total': len(class_names)})


@app.route('/api/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500

    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    try:
        file = request.files['image']

        # 🔥 STEP 1: Skin check
        if not is_skin_image(file):
            return jsonify({
                'prediction': 'Invalid Image',
                'message': 'Please upload a clear skin image',
                'confidence': 0,
                'all_predictions': [],
                'recommendations': {},
                'similar_images': {}
            })

        # 🔥 VERY IMPORTANT (reset pointer)
        file.seek(0)

        # 🔥 STEP 2: Your original logic
        image = Image.open(io.BytesIO(file.read()))
        processed_image = preprocess_image(image)

        predictions = model.predict(processed_image)
        predicted_class_idx = int(np.argmax(predictions[0]))
        confidence = float(predictions[0][predicted_class_idx])

        all_predictions = []
        for idx, prob in enumerate(predictions[0]):
            if idx < len(class_names):
                all_predictions.append({
                    'disease': class_names[idx],
                    'confidence': float(prob)
                })

        all_predictions.sort(key=lambda x: x['confidence'], reverse=True)

        predicted_disease = class_names[predicted_class_idx] if predicted_class_idx < len(class_names) else 'Unknown'

        use_serpapi = request.form.get('use_serpapi', 'true').lower() == 'true'

        if use_serpapi and SERP_API_KEY:
            recommendations = get_serpapi_recommendations(predicted_disease)
            similar_images = search_similar_images(predicted_disease)
        else:
            recommendations = {
                'recommendations': [],
                'search_query': f'{predicted_disease} skin disease treatment recommendations'
            }
            similar_images = {'images': []}

        return jsonify({
            'prediction': predicted_disease,
            'confidence': confidence,
            'all_predictions': all_predictions[:5],
            'recommendations': recommendations,
            'similar_images': similar_images
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("Loading model...")
    load_model_and_classes()
    print("Starting server on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
