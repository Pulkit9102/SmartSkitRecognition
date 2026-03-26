from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from PIL import Image
import io
import os
import json
import pickle
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
    print(f"⚠ Auth module unavailable: {auth_import_error}")

# Configuration
MODEL_DIR = os.path.join('..', 'model', 'trained_model')
MODEL_PATH = os.path.join(MODEL_DIR, 'model.pkl')
ENCODER_PATH = os.path.join(MODEL_DIR, 'label_encoder.pkl')
CLASS_NAMES_PATH = os.path.join(MODEL_DIR, 'class_names.json')
CONFIG_PATH = os.path.join(MODEL_DIR, 'config.json')
SERP_API_KEY = os.getenv('SERP_API_KEY', '')

# Global variables for model
model = None
label_encoder = None
class_names = []
feature_extractor = None
model_config = {}

# Feature extraction imports
try:
    import torch
    import torchvision.models as models
    import torchvision.transforms as transforms
    PYTORCH_AVAILABLE = True
except ImportError:
    PYTORCH_AVAILABLE = False

class SimpleFeatureExtractor:
    """Extract simple features from images"""
    
    def __init__(self, image_size=(224, 224)):
        self.image_size = image_size
    
    def extract(self, image):
        """Extract color histogram and basic statistics"""
        if isinstance(image, str):
            img = Image.open(image).convert('RGB')
        else:
            img = image.convert('RGB')
        
        img = img.resize(self.image_size)
        img_array = np.array(img)
        
        # Color histograms
        features = []
        for channel in range(3):
            hist, _ = np.histogram(img_array[:,:,channel], bins=32, range=(0, 256))
            features.extend(hist)
        
        # Basic statistics
        features.extend([
            img_array.mean(),
            img_array.std(),
            img_array.min(),
            img_array.max()
        ])
        
        return np.array(features)

class PyTorchFeatureExtractor:
    """Extract deep features using pre-trained ResNet50"""
    
    def __init__(self):
        # Load pre-trained ResNet50
        self.model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
        # Remove the final classification layer
        self.model = torch.nn.Sequential(*list(self.model.children())[:-1])
        self.model.eval()
        
        # Image preprocessing
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
    
    def extract(self, image):
        """Extract features from image"""
        if isinstance(image, str):
            img = Image.open(image).convert('RGB')
        else:
            img = image.convert('RGB')
        
        img_tensor = self.transform(img).unsqueeze(0)
        
        with torch.no_grad():
            features = self.model(img_tensor)
        
        return features.squeeze().numpy()

def load_model_and_classes():
    """Load the trained model and class names"""
    global model, label_encoder, class_names, feature_extractor, model_config
    
    print("\n🔄 Loading model components...")
    
    # Load config
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            model_config = json.load(f)
        print(f"✓ Loaded config: {model_config.get('feature_extractor', 'unknown')} feature extractor")
    
    # Load model
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        print("✓ Model loaded successfully!")
    else:
        print(f"⚠ Model not found at {MODEL_PATH}. Please train the model first.")
        print("  Run: cd model && python train_model_simple.py")
        return
    
    # Load label encoder
    if os.path.exists(ENCODER_PATH):
        with open(ENCODER_PATH, 'rb') as f:
            label_encoder = pickle.load(f)
        print("✓ Label encoder loaded!")
    
    # Load class names
    if os.path.exists(CLASS_NAMES_PATH):
        with open(CLASS_NAMES_PATH, 'r') as f:
            class_names = json.load(f)
        print(f"✓ Class names loaded: {', '.join(class_names)}")
    
    # Initialize feature extractor based on config
    extractor_type = model_config.get('feature_extractor', 'simple')
    
    if extractor_type == 'pytorch' and PYTORCH_AVAILABLE:
        feature_extractor = PyTorchFeatureExtractor()
        print("✓ Using PyTorch feature extractor")
    else:
        feature_extractor = SimpleFeatureExtractor()
        if extractor_type == 'pytorch':
            print("⚠ PyTorch not available, using simple feature extractor")
            print("  Install PyTorch for better accuracy: pip install torch torchvision")
        else:
            print("✓ Using simple feature extractor")
    
    print("✅ All components loaded successfully!\n")

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
        'auth_enabled': AUTH_ENABLED,
        'feature_extractor': model_config.get('feature_extractor', 'unknown'),
        'num_classes': len(class_names)
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict skin disease from uploaded image"""
    if model is None or feature_extractor is None:
        return jsonify({
            'error': 'Model not loaded. Please train the model first.',
            'help': 'Run: cd model && python train_model_simple.py'
        }), 500
    
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    try:
        # Read image
        file = request.files['image']
        image = Image.open(io.BytesIO(file.read()))
        
        # Extract features
        features = feature_extractor.extract(image)
        features = features.reshape(1, -1)
        
        # Make prediction
        prediction_encoded = model.predict(features)[0]
        predicted_disease = label_encoder.inverse_transform([prediction_encoded])[0]
        
        # Get probability scores
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(features)[0]
            
            # Create all predictions with confidence scores
            all_predictions = []
            for idx, prob in enumerate(probabilities):
                disease = label_encoder.inverse_transform([idx])[0]
                all_predictions.append({
                    'disease': disease,
                    'confidence': float(prob)
                })
            
            # Sort by confidence
            all_predictions.sort(key=lambda x: x['confidence'], reverse=True)
            confidence = all_predictions[0]['confidence']
        else:
            all_predictions = [{'disease': predicted_disease, 'confidence': 1.0}]
            confidence = 1.0
        
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
            'similar_images': similar_images,
            'model_type': model_config.get('feature_extractor', 'unknown')
        })
    
    except Exception as e:
        import traceback
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

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
    print("=" * 60)
    print("  SIMPLE SKIN DISEASE CLASSIFICATION API")
    print("=" * 60)
    mongo_db = init_mongo_db() if AUTH_ENABLED else None
    if AUTH_ENABLED and mongo_db is not None:
        print("✓ MongoDB connected for authentication")
    elif AUTH_ENABLED:
        print("⚠ MongoDB not configured. Auth endpoints will be unavailable until configured.")
    else:
        print("⚠ Auth routes are disabled due to missing auth dependencies.")
    load_model_and_classes()
    print("Starting Flask server on http://localhost:5000")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
