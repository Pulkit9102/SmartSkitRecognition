from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from PIL import Image
import io
import os
import json
from serpapi import GoogleSearch
from dotenv import load_dotenv
import cv2
import numpy as np

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


load_dotenv()

app = Flask(__name__)
CORS(app)

# --- Chatbot (OpenAI) ---
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENAI_CHAT_MODEL = os.getenv('OPENAI_CHAT_MODEL', 'gpt-4o-mini')
CHAT_HISTORY_LIMIT = 10  # last N messages kept for context

_openai_client = None
if OPENAI_API_KEY and OpenAI is not None:
    try:
        _openai_client = OpenAI(api_key=OPENAI_API_KEY)
    except Exception as e:
        print(f"OpenAI client init failed: {e}")
        _openai_client = None

CHAT_SYSTEM_PROMPT = (
    "You are a professional dermatologist assistant chatbot for the SkinCare AI app.\n"
    "You answer ONLY skincare and skin-related queries (skin conditions, hygiene, "
    "routines, sunscreen, acne, eczema, psoriasis, hair/scalp skin, general "
    "dermatology guidance).\n\n"
    "Rules:\n"
    "- Provide accurate, safe, and helpful skincare advice.\n"
    "- Do NOT give dangerous instructions or prescribe specific prescription drugs "
    "or dosages. You may mention common over-the-counter ingredients (e.g., salicylic "
    "acid, benzoyl peroxide, ceramides) at a general educational level.\n"
    "- Always recommend consulting a qualified dermatologist for diagnosis or "
    "persistent/severe symptoms.\n"
    "- Be clear, simple, and conversational. Keep replies concise.\n"
    "- If the question is unrelated to skin/skincare, politely refuse with: "
    "\"I can only help with skincare-related questions.\""
)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_skin_image(file):
    file_bytes = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if img is None:
        return False

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
        'serpapi_configured': bool(SERP_API_KEY),
        'openai_configured': _openai_client is not None,
        'openai_key_present': bool(OPENAI_API_KEY),
        'openai_sdk_available': OpenAI is not None,
    })


@app.route('/api/classes', methods=['GET'])
def get_classes():
    return jsonify({'classes': class_names, 'total': len(class_names)})


@app.route('/api/chat', methods=['POST'])
def chat():
    """Skincare-only chatbot powered by OpenAI.

    Request JSON: { "message": str, "history": [{role, content}, ...] }
    Response JSON: { "reply": str }
    """
    if _openai_client is None:
        return jsonify({'error': 'Chatbot is not configured on the server.'}), 503

    data = request.get_json(silent=True) or {}
    message = (data.get('message') or '').strip()
    history = data.get('history') or []

    if not message:
        return jsonify({'error': 'Message is required.'}), 400
    if len(message) > 2000:
        return jsonify({'error': 'Message is too long.'}), 413

    # Sanitize history: only keep role/content pairs with valid roles, last N items
    clean_history = []
    if isinstance(history, list):
        for item in history[-CHAT_HISTORY_LIMIT:]:
            if not isinstance(item, dict):
                continue
            role = item.get('role')
            content = item.get('content')
            if role in ('user', 'assistant') and isinstance(content, str) and content.strip():
                clean_history.append({'role': role, 'content': content[:2000]})

    messages = [{'role': 'system', 'content': CHAT_SYSTEM_PROMPT}]
    messages.extend(clean_history)
    messages.append({'role': 'user', 'content': message})

    try:
        response = _openai_client.chat.completions.create(
            model=OPENAI_CHAT_MODEL,
            messages=messages,
            temperature=0.4,
            max_tokens=400,
            timeout=30,
        )
        reply = (response.choices[0].message.content or '').strip()
        if not reply:
            reply = 'Sorry, I could not generate a response. Please try again.'
        return jsonify({'reply': reply})
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({'error': 'Something went wrong. Please try again.'}), 502


@app.route('/api/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500

    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    try:
        file = request.files['image']

        if not allowed_file(file.filename):
            return jsonify({
        "error": "Unsupported file format",
        "message": "Please upload only JPG, JPEG, or PNG images"
        }), 400

        # STEP 1: Skin check
        if not is_skin_image(file):
            return jsonify({
            "error": "Not a skin image",
            "message": "Please upload a clear image of skin area"
        }), 400

        # Reset pointer
        file.seek(0)

        # STEP 2: Original logic
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
