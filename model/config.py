"""
Model Configuration and Utilities

This module contains configuration classes and utility functions
that can be easily modified for different use cases.
"""

import os

class ModelConfig:
    """
    Centralized configuration for the skin disease model.
    Modify these values to customize the model behavior.
    """
    
    # Model Architecture
    BASE_MODEL = 'MobileNetV2'  # Options: 'MobileNetV2', 'ResNet50', 'EfficientNetB0'
    IMAGE_SIZE = (224, 224)
    
    # Training Parameters
    BATCH_SIZE = 32
    EPOCHS = 50
    LEARNING_RATE = 0.0001
    
    # Data Augmentation
    AUGMENTATION_CONFIG = {
        'rotation_range': 20,
        'width_shift_range': 0.2,
        'height_shift_range': 0.2,
        'shear_range': 0.2,
        'zoom_range': 0.2,
        'horizontal_flip': True,
        'fill_mode': 'nearest'
    }
    
    # Custom Layer Configuration
    DENSE_LAYERS = [512, 256]  # Hidden layer sizes
    DROPOUT_RATES = [0.5, 0.3]  # Dropout after each dense layer
    
    # Callbacks Configuration
    EARLY_STOPPING_PATIENCE = 10
    REDUCE_LR_PATIENCE = 5
    REDUCE_LR_FACTOR = 0.5
    MIN_LEARNING_RATE = 1e-7
    
    @classmethod
    def get_base_model(cls, input_shape, include_top=False):
        """Get the base model based on configuration"""
        from tensorflow.keras.applications import (
            MobileNetV2, ResNet50, EfficientNetB0
        )
        
        models = {
            'MobileNetV2': MobileNetV2,
            'ResNet50': ResNet50,
            'EfficientNetB0': EfficientNetB0
        }
        
        model_class = models.get(cls.BASE_MODEL, MobileNetV2)
        return model_class(
            input_shape=input_shape,
            include_top=include_top,
            weights='imagenet'
        )

class PathConfig:
    """
    Path configuration - easy to modify for different directory structures
    """
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Dataset paths
    DATASET_DIR = os.path.join(BASE_DIR, 'dataset')
    TRAIN_DIR = os.path.join(DATASET_DIR, 'train')
    VALIDATION_DIR = os.path.join(DATASET_DIR, 'validation')
    TEST_DIR = os.path.join(DATASET_DIR, 'test')
    
    # Model paths
    MODEL_DIR = os.path.join(BASE_DIR, 'model')
    SAVED_MODEL_PATH = os.path.join(MODEL_DIR, 'skin_disease_model.h5')
    CLASS_NAMES_PATH = os.path.join(MODEL_DIR, 'class_names.json')
    HISTORY_PATH = os.path.join(MODEL_DIR, 'training_history.json')
    
    # Output paths
    PLOTS_DIR = os.path.join(MODEL_DIR, 'plots')
    LOGS_DIR = os.path.join(MODEL_DIR, 'logs')

class DiseaseInfo:
    """
    Disease information and metadata
    Can be extended to include treatment info, severity levels, etc.
    """
    
    # Common skin diseases information
    DISEASE_METADATA = {
        'acne': {
            'severity': 'mild-moderate',
            'common_age_group': '12-25',
            'description': 'Inflammatory skin condition causing pimples and spots'
        },
        'eczema': {
            'severity': 'mild-severe',
            'common_age_group': 'all',
            'description': 'Chronic condition causing itchy, inflamed skin'
        },
        'psoriasis': {
            'severity': 'moderate-severe',
            'common_age_group': 'adult',
            'description': 'Autoimmune condition causing scaly skin patches'
        },
        # Add more diseases as needed
    }
    
    @classmethod
    def get_info(cls, disease_name):
        """Get metadata for a specific disease"""
        disease_key = disease_name.lower()
        return cls.DISEASE_METADATA.get(disease_key, {
            'severity': 'unknown',
            'common_age_group': 'unknown',
            'description': 'No information available'
        })

def get_disease_search_query(disease_name, query_type='treatment'):
    """
    Generate search queries for different types of information
    
    Args:
        disease_name: Name of the disease
        query_type: Type of query ('treatment', 'symptoms', 'causes', 'prevention')
    
    Returns:
        Formatted search query string
    """
    
    query_templates = {
        'treatment': f'{disease_name} skin disease treatment and remedies',
        'symptoms': f'{disease_name} skin disease symptoms and signs',
        'causes': f'{disease_name} skin disease causes and risk factors',
        'prevention': f'{disease_name} skin disease prevention and care',
        'specialist': f'dermatologist for {disease_name} near me'
    }
    
    return query_templates.get(query_type, f'{disease_name} skin disease information')
