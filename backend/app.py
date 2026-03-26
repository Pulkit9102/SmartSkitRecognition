from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import numpy as np
from PIL import Image
import io
import os
import json
from serpapi import GoogleSearch
from dotenv import load_dotenv
from config.db import init_mongo_db

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

try:
    from routes.auth_routes import auth_bp

    app.register_blueprint(auth_bp)
    AUTH_ENABLED = True
except Exception as auth_import_error:
    AUTH_ENABLED = False
    print(f"Auth module unavailable: {auth_import_error}")

# Configuration
MODEL_PATH = os.path.join('..', 'model', 'skin_disease_model.h5')
CLASS_NAMES_PATH = os.path.join('..', 'model', 'class_names.json')
SERP_API_KEY = os.getenv('SERP_API_KEY', '')

# Global variables for model
model = None
class_names = []

def load_model_and_classes():
    """Load the trained model and class names.

    TensorFlow/Keras import is done lazily so the backend can start even when
    TensorFlow isn't installed yet. This allows installing other dependencies
    (Flask, etc.) without TF blocking the install process.
    """
    global model, class_names

    # Try to import TensorFlow/Keras here (lazy import)
    try:
        # Import inside the function so missing TensorFlow doesn't crash the app at startup
        import tensorflow as tf
        from tensorflow import keras
    except Exception as e:
        print("TensorFlow not available or failed to import:", str(e))
        print("Model functionality will be disabled until TensorFlow is installed and the model is trained.")
        model = None
    else:
        try:
            if os.path.exists(MODEL_PATH):
                model = keras.models.load_model(MODEL_PATH)
                print("Model loaded successfully!")
            else:
                print(f"Model not found at {MODEL_PATH}. Please train the model first.")
        except Exception as e:
            print(f"Error loading model: {str(e)}")

    try:
        if os.path.exists(CLASS_NAMES_PATH):
            with open(CLASS_NAMES_PATH, 'r') as f:
                class_names = json.load(f)
            print(f"Class names loaded: {class_names}")
        else:
            print(f"Class names not found at {CLASS_NAMES_PATH}")
    except Exception as e:
        print(f"Error loading class names: {str(e)}")

def preprocess_image(image, target_size=(224, 224)):
    """Preprocess image for model prediction"""
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    image = image.resize(target_size)
    image_array = np.array(image)
    image_array = image_array / 255.0  # Normalize
    image_array = np.expand_dims(image_array, axis=0)
    
    return image_array

def get_serpapi_recommendations(disease_name):
    """Get recommendations using SerpAPI"""
    if not SERP_API_KEY:
        return {
            'error': 'SerpAPI key not configured',
            'recommendations': []
        }
    
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
        
        # Extract organic results
        if 'organic_results' in results:
            for result in results['organic_results'][:5]:
                recommendations.append({
                    'title': result.get('title', ''),
                    'link': result.get('link', ''),
                    'snippet': result.get('snippet', '')
                })
        
        return {
            'recommendations': recommendations,
            'search_query': params['q']
        }
    
    except Exception as e:
        return {
            'error': str(e),
            'recommendations': []
        }

def search_similar_images(disease_name):
    """Search for similar images using SerpAPI"""
    if not SERP_API_KEY:
        return {'error': 'SerpAPI key not configured', 'images': []}
    
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
        return {'error': str(e), 'images': []}

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'classes_loaded': len(class_names) > 0,
        'serpapi_configured': bool(SERP_API_KEY),
        'auth_enabled': AUTH_ENABLED
    })

@app.route('/', methods=['GET'])
def root():
    """Root endpoint to avoid 404 when opening backend URL in a browser."""
    return jsonify({
        'message': 'Smart Skin Recognition backend is running',
        'health_endpoint': '/api/health'
    })

@app.route('/favicon.ico', methods=['GET'])
def favicon():
    """Return empty favicon response to avoid noisy 404 logs."""
    return Response(status=204)

@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict skin disease from uploaded image"""
    if model is None:
        return jsonify({'error': 'Model not loaded. Please train the model first.'}), 500
    
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    try:
        # Read and preprocess image
        file = request.files['image']
        image = Image.open(io.BytesIO(file.read()))
        processed_image = preprocess_image(image)
        
        # Make prediction
        predictions = model.predict(processed_image)
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx])
        
        # Get all predictions with confidence scores
        all_predictions = []
        for idx, prob in enumerate(predictions[0]):
            if idx < len(class_names):
                all_predictions.append({
                    'disease': class_names[idx],
                    'confidence': float(prob)
                })
        
        # Sort by confidence
        all_predictions.sort(key=lambda x: x['confidence'], reverse=True)
        
        predicted_disease = class_names[predicted_class_idx] if predicted_class_idx < len(class_names) else 'Unknown'
        
        # Get recommendations from SerpAPI
        use_serpapi = request.form.get('use_serpapi', 'true').lower() == 'true'
        recommendations = {}
        similar_images = {}
        
        if use_serpapi and SERP_API_KEY:
            recommendations = get_serpapi_recommendations(predicted_disease)
            similar_images = search_similar_images(predicted_disease)
        
        return jsonify({
            'prediction': predicted_disease,
            'confidence': confidence,
            'all_predictions': all_predictions[:5],  # Top 5 predictions
            'recommendations': recommendations,
            'similar_images': similar_images
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/classes', methods=['GET'])
def get_classes():
    """Get list of disease classes"""
    return jsonify({
        'classes': class_names,
        'total': len(class_names)
    })

@app.route('/api/search-recommendations', methods=['POST'])
def search_recommendations():
    """Search for recommendations for a specific disease"""
    data = request.get_json()
    
    if not data or 'disease' not in data:
        return jsonify({'error': 'Disease name not provided'}), 400
    
    disease_name = data['disease']
    recommendations = get_serpapi_recommendations(disease_name)
    similar_images = search_similar_images(disease_name)
    
    return jsonify({
        'disease': disease_name,
        'recommendations': recommendations,
        'similar_images': similar_images
    })

if __name__ == '__main__':
    print("Loading model and class names...")
    mongo_db = init_mongo_db() if AUTH_ENABLED else None
    if AUTH_ENABLED and mongo_db is not None:
        print("MongoDB connected for authentication")
    elif AUTH_ENABLED:
        print("MongoDB not configured. Auth endpoints will be unavailable until configured.")
    else:
        print("Auth routes are disabled due to missing auth dependencies.")
    load_model_and_classes()
    print("Starting Flask server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
