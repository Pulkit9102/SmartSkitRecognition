"""
Simple Skin Disease Classification Model
Uses ResNet50 features + Logistic Regression (no TensorFlow required)
"""

import os
import json
import numpy as np
from PIL import Image
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Try to import torch (PyTorch) for feature extraction
try:
    import torch
    import torchvision.models as models
    import torchvision.transforms as transforms
    FEATURE_EXTRACTOR = 'pytorch'
    print("✓ Using PyTorch for feature extraction")
except ImportError:
    FEATURE_EXTRACTOR = 'simple'
    print("! PyTorch not found. Using simple pixel features.")
    print("  For better accuracy, install PyTorch: pip install torch torchvision")

class Config:
    """Configuration parameters"""
    DATASET_DIR = "dataset"
    MODEL_DIR = "trained_model"
    IMAGE_SIZE = (224, 224)
    RANDOM_STATE = 42
    TEST_SIZE = 0.2
    
    # Create model directory
    os.makedirs(MODEL_DIR, exist_ok=True)

class SimpleFeatureExtractor:
    """Extract simple features from images (fallback if no PyTorch)"""
    
    def __init__(self, image_size=(224, 224)):
        self.image_size = image_size
    
    def extract(self, image_path):
        """Extract color histogram and basic statistics"""
        img = Image.open(image_path).convert('RGB')
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
    
    def extract(self, image_path):
        """Extract features from image"""
        img = Image.open(image_path).convert('RGB')
        img_tensor = self.transform(img).unsqueeze(0)
        
        with torch.no_grad():
            features = self.model(img_tensor)
        
        return features.squeeze().numpy()

def load_dataset(dataset_dir):
    """Load images and labels from dataset directory"""
    print("\n📂 Loading dataset...")
    
    train_dir = os.path.join(dataset_dir, "train")
    val_dir = os.path.join(dataset_dir, "validation")
    
    if not os.path.exists(train_dir):
        raise FileNotFoundError(f"Training directory not found: {train_dir}")
    
    # Get class names
    class_names = sorted([d for d in os.listdir(train_dir) 
                         if os.path.isdir(os.path.join(train_dir, d))])
    
    if len(class_names) == 0:
        raise ValueError("No disease folders found in dataset/train/")
    
    print(f"Found {len(class_names)} disease classes: {', '.join(class_names)}")
    
    # Initialize feature extractor
    if FEATURE_EXTRACTOR == 'pytorch':
        extractor = PyTorchFeatureExtractor()
    else:
        extractor = SimpleFeatureExtractor()
    
    def load_split(split_dir, split_name):
        """Load images from a split directory"""
        X, y = [], []
        image_count = 0
        
        for class_name in class_names:
            class_dir = os.path.join(split_dir, class_name)
            if not os.path.exists(class_dir):
                continue
            
            images = [f for f in os.listdir(class_dir) 
                     if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
            
            print(f"  {split_name} - {class_name}: {len(images)} images")
            
            for img_file in images:
                img_path = os.path.join(class_dir, img_file)
                try:
                    features = extractor.extract(img_path)
                    X.append(features)
                    y.append(class_name)
                    image_count += 1
                except Exception as e:
                    print(f"    ⚠ Error loading {img_file}: {e}")
        
        return np.array(X), np.array(y), image_count
    
    # Load training data
    X_train, y_train, train_count = load_split(train_dir, "Training")
    
    # Load validation data
    X_val, y_val, val_count = None, None, 0
    if os.path.exists(val_dir):
        X_val, y_val, val_count = load_split(val_dir, "Validation")
    
    print(f"\n✓ Loaded {train_count} training images and {val_count} validation images")
    
    return X_train, y_train, X_val, y_val, class_names

def train_model(X_train, y_train, X_val, y_val, class_names):
    """Train a Logistic Regression classifier"""
    print("\n🧠 Training model...")
    
    # Encode labels
    label_encoder = LabelEncoder()
    y_train_encoded = label_encoder.fit_transform(y_train)
    
    # Train classifier
    print("  Training Logistic Regression classifier...")
    model = LogisticRegression(
        max_iter=1000,
        random_state=Config.RANDOM_STATE,
        multi_class='multinomial',
        solver='lbfgs',
        C=1.0
    )
    
    model.fit(X_train, y_train_encoded)
    
    # Training accuracy
    train_acc = model.score(X_train, y_train_encoded)
    print(f"  Training accuracy: {train_acc*100:.2f}%")
    
    # Validation accuracy
    if X_val is not None and len(X_val) > 0:
        y_val_encoded = label_encoder.transform(y_val)
        val_acc = model.score(X_val, y_val_encoded)
        print(f"  Validation accuracy: {val_acc*100:.2f}%")
        
        # Classification report
        y_pred = model.predict(X_val)
        print("\n📊 Classification Report:")
        print(classification_report(y_val_encoded, y_pred, 
                                   target_names=class_names))
        
        # Confusion matrix
        plot_confusion_matrix(y_val_encoded, y_pred, class_names)
    
    return model, label_encoder

def plot_confusion_matrix(y_true, y_pred, class_names):
    """Plot confusion matrix"""
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=class_names, yticklabels=class_names)
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    
    output_path = os.path.join(Config.MODEL_DIR, 'confusion_matrix.png')
    plt.savefig(output_path)
    print(f"  Saved confusion matrix to {output_path}")
    plt.close()

def save_model(model, label_encoder, class_names):
    """Save the trained model and metadata"""
    print("\n💾 Saving model...")
    
    # Save model
    model_path = os.path.join(Config.MODEL_DIR, 'model.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"  ✓ Saved model to {model_path}")
    
    # Save label encoder
    encoder_path = os.path.join(Config.MODEL_DIR, 'label_encoder.pkl')
    with open(encoder_path, 'wb') as f:
        pickle.dump(label_encoder, f)
    print(f"  ✓ Saved label encoder to {encoder_path}")
    
    # Save class names
    class_names_path = os.path.join(Config.MODEL_DIR, 'class_names.json')
    with open(class_names_path, 'w') as f:
        json.dump(class_names, f, indent=2)
    print(f"  ✓ Saved class names to {class_names_path}")
    
    # Save feature extractor type
    config_path = os.path.join(Config.MODEL_DIR, 'config.json')
    with open(config_path, 'w') as f:
        json.dump({
            'feature_extractor': FEATURE_EXTRACTOR,
            'image_size': Config.IMAGE_SIZE,
            'num_classes': len(class_names),
            'class_names': class_names
        }, f, indent=2)
    print(f"  ✓ Saved config to {config_path}")

def main():
    """Main training pipeline"""
    print("=" * 60)
    print("  SIMPLE SKIN DISEASE CLASSIFICATION MODEL TRAINING")
    print("=" * 60)
    
    # Load dataset
    X_train, y_train, X_val, y_val, class_names = load_dataset(Config.DATASET_DIR)
    
    if len(X_train) == 0:
        print("\n❌ No training images found!")
        print("Please add images to dataset/train/<disease_name>/ folders")
        return
    
    # Train model
    model, label_encoder = train_model(X_train, y_train, X_val, y_val, class_names)
    
    # Save model
    save_model(model, label_encoder, class_names)
    
    print("\n" + "=" * 60)
    print("  ✅ TRAINING COMPLETE!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Model saved to 'trained_model/' directory")
    print("2. Update backend/app.py to use the new model")
    print("3. Start the backend: cd backend && python app.py")
    print("4. Start the frontend: cd frontend && npm start")
    print("5. Test by uploading skin disease images!")
    
    if FEATURE_EXTRACTOR == 'simple':
        print("\n💡 TIP: For better accuracy, install PyTorch:")
        print("   pip install torch torchvision")
        print("   Then run this script again to retrain with deep features")

if __name__ == "__main__":
    main()
