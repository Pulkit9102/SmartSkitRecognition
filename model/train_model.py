"""
Skin Disease Recognition Model Training Script

This script trains a Convolutional Neural Network (CNN) to classify skin diseases
from images. It uses transfer learning with MobileNetV2 for efficient training.
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns

# Configuration
class Config:
    # Paths
    DATASET_PATH = os.path.join('..', 'dataset')
    TRAIN_PATH = os.path.join(DATASET_PATH, 'train')
    VALIDATION_PATH = os.path.join(DATASET_PATH, 'validation')
    TEST_PATH = os.path.join(DATASET_PATH, 'test')
    MODEL_SAVE_PATH = os.path.join('..', 'model', 'skin_disease_model.h5')
    CLASS_NAMES_PATH = os.path.join('..', 'model', 'class_names.json')
    HISTORY_PATH = os.path.join('..', 'model', 'training_history.json')
    
    # Model parameters
    IMAGE_SIZE = (224, 224)
    BATCH_SIZE = 32
    EPOCHS = 50
    LEARNING_RATE = 0.0001
    
    # Data augmentation
    ROTATION_RANGE = 20
    WIDTH_SHIFT_RANGE = 0.2
    HEIGHT_SHIFT_RANGE = 0.2
    HORIZONTAL_FLIP = True
    ZOOM_RANGE = 0.2
    SHEAR_RANGE = 0.2

def create_data_generators():
    """Create data generators with augmentation for training"""
    
    # Training data augmentation
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=Config.ROTATION_RANGE,
        width_shift_range=Config.WIDTH_SHIFT_RANGE,
        height_shift_range=Config.HEIGHT_SHIFT_RANGE,
        shear_range=Config.SHEAR_RANGE,
        zoom_range=Config.ZOOM_RANGE,
        horizontal_flip=Config.HORIZONTAL_FLIP,
        fill_mode='nearest'
    )
    
    # Validation and test data - only rescaling
    validation_datagen = ImageDataGenerator(rescale=1./255)
    test_datagen = ImageDataGenerator(rescale=1./255)
    
    # Create generators
    train_generator = train_datagen.flow_from_directory(
        Config.TRAIN_PATH,
        target_size=Config.IMAGE_SIZE,
        batch_size=Config.BATCH_SIZE,
        class_mode='categorical',
        shuffle=True
    )
    
    validation_generator = validation_datagen.flow_from_directory(
        Config.VALIDATION_PATH,
        target_size=Config.IMAGE_SIZE,
        batch_size=Config.BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
    )
    
    test_generator = None
    if os.path.exists(Config.TEST_PATH) and os.listdir(Config.TEST_PATH):
        test_generator = test_datagen.flow_from_directory(
            Config.TEST_PATH,
            target_size=Config.IMAGE_SIZE,
            batch_size=Config.BATCH_SIZE,
            class_mode='categorical',
            shuffle=False
        )
    
    return train_generator, validation_generator, test_generator

def create_model(num_classes):
    """
    Create a CNN model using transfer learning with MobileNetV2
    
    Args:
        num_classes: Number of disease classes
    
    Returns:
        Compiled Keras model
    """
    
    # Load pre-trained MobileNetV2 without top layers
    base_model = MobileNetV2(
        input_shape=(*Config.IMAGE_SIZE, 3),
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze base model layers
    base_model.trainable = False
    
    # Create custom top layers
    model = keras.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.BatchNormalization(),
        layers.Dense(512, activation='relu'),
        layers.Dropout(0.5),
        layers.BatchNormalization(),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    # Compile model
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=Config.LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=['accuracy', keras.metrics.TopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
    )
    
    return model

def create_callbacks():
    """Create training callbacks"""
    
    callbacks = [
        # Save best model
        ModelCheckpoint(
            Config.MODEL_SAVE_PATH,
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            verbose=1
        ),
        
        # Early stopping
        EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True,
            verbose=1
        ),
        
        # Reduce learning rate on plateau
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        )
    ]
    
    return callbacks

def plot_training_history(history):
    """Plot training history"""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Accuracy
    axes[0, 0].plot(history.history['accuracy'], label='Train Accuracy')
    axes[0, 0].plot(history.history['val_accuracy'], label='Validation Accuracy')
    axes[0, 0].set_title('Model Accuracy')
    axes[0, 0].set_xlabel('Epoch')
    axes[0, 0].set_ylabel('Accuracy')
    axes[0, 0].legend()
    axes[0, 0].grid(True)
    
    # Loss
    axes[0, 1].plot(history.history['loss'], label='Train Loss')
    axes[0, 1].plot(history.history['val_loss'], label='Validation Loss')
    axes[0, 1].set_title('Model Loss')
    axes[0, 1].set_xlabel('Epoch')
    axes[0, 1].set_ylabel('Loss')
    axes[0, 1].legend()
    axes[0, 1].grid(True)
    
    # Top-3 Accuracy
    if 'top_3_accuracy' in history.history:
        axes[1, 0].plot(history.history['top_3_accuracy'], label='Train Top-3 Accuracy')
        axes[1, 0].plot(history.history['val_top_3_accuracy'], label='Val Top-3 Accuracy')
        axes[1, 0].set_title('Model Top-3 Accuracy')
        axes[1, 0].set_xlabel('Epoch')
        axes[1, 0].set_ylabel('Top-3 Accuracy')
        axes[1, 0].legend()
        axes[1, 0].grid(True)
    
    # Learning Rate
    if 'lr' in history.history:
        axes[1, 1].plot(history.history['lr'])
        axes[1, 1].set_title('Learning Rate')
        axes[1, 1].set_xlabel('Epoch')
        axes[1, 1].set_ylabel('Learning Rate')
        axes[1, 1].set_yscale('log')
        axes[1, 1].grid(True)
    
    plt.tight_layout()
    plt.savefig(os.path.join('..', 'model', 'training_history.png'))
    print("Training history plot saved!")
    plt.close()

def evaluate_model(model, test_generator):
    """Evaluate model on test set"""
    
    if test_generator is None:
        print("No test data available for evaluation")
        return
    
    print("\n" + "="*50)
    print("Evaluating model on test set...")
    print("="*50)
    
    # Evaluate
    test_loss, test_accuracy, test_top3_accuracy = model.evaluate(test_generator, verbose=1)
    
    print(f"\nTest Loss: {test_loss:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f}")
    print(f"Test Top-3 Accuracy: {test_top3_accuracy:.4f}")
    
    # Predictions
    predictions = model.predict(test_generator, verbose=1)
    predicted_classes = np.argmax(predictions, axis=1)
    true_classes = test_generator.classes
    class_labels = list(test_generator.class_indices.keys())
    
    # Classification report
    print("\nClassification Report:")
    print(classification_report(true_classes, predicted_classes, target_names=class_labels))
    
    # Confusion matrix
    cm = confusion_matrix(true_classes, predicted_classes)
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_labels, yticklabels=class_labels)
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(os.path.join('..', 'model', 'confusion_matrix.png'))
    print("Confusion matrix saved!")
    plt.close()

def save_class_names(class_indices):
    """Save class names to JSON file"""
    
    # Convert {class_name: index} to [class_names] sorted by index
    class_names = [None] * len(class_indices)
    for class_name, index in class_indices.items():
        class_names[index] = class_name
    
    with open(Config.CLASS_NAMES_PATH, 'w') as f:
        json.dump(class_names, f, indent=2)
    
    print(f"\nClass names saved to {Config.CLASS_NAMES_PATH}")
    print(f"Classes: {class_names}")

def save_training_history(history):
    """Save training history to JSON file"""
    
    # Convert history to serializable format
    history_dict = {}
    for key, value in history.history.items():
        history_dict[key] = [float(v) for v in value]
    
    with open(Config.HISTORY_PATH, 'w') as f:
        json.dump(history_dict, f, indent=2)
    
    print(f"Training history saved to {Config.HISTORY_PATH}")

def main():
    """Main training function"""
    
    print("="*50)
    print("Skin Disease Recognition - Model Training")
    print("="*50)
    
    # Check if dataset exists
    if not os.path.exists(Config.TRAIN_PATH):
        print(f"\nError: Training data not found at {Config.TRAIN_PATH}")
        print("\nPlease organize your dataset as follows:")
        print("dataset/")
        print("  ├── train/")
        print("  │   ├── disease_1/")
        print("  │   │   ├── image1.jpg")
        print("  │   │   ├── image2.jpg")
        print("  │   ├── disease_2/")
        print("  │   │   ├── image1.jpg")
        print("  ├── validation/")
        print("  │   ├── disease_1/")
        print("  │   ├── disease_2/")
        print("  └── test/ (optional)")
        print("      ├── disease_1/")
        print("      ├── disease_2/")
        return
    
    # Create model directory if it doesn't exist
    os.makedirs(os.path.dirname(Config.MODEL_SAVE_PATH), exist_ok=True)
    
    # Create data generators
    print("\nLoading and preparing data...")
    train_generator, validation_generator, test_generator = create_data_generators()
    
    num_classes = train_generator.num_classes
    print(f"\nNumber of classes: {num_classes}")
    print(f"Training samples: {train_generator.samples}")
    print(f"Validation samples: {validation_generator.samples}")
    if test_generator:
        print(f"Test samples: {test_generator.samples}")
    
    # Save class names
    save_class_names(train_generator.class_indices)
    
    # Create model
    print("\nCreating model...")
    model = create_model(num_classes)
    model.summary()
    
    # Create callbacks
    callbacks = create_callbacks()
    
    # Train model
    print("\nStarting training...")
    print(f"Epochs: {Config.EPOCHS}")
    print(f"Batch size: {Config.BATCH_SIZE}")
    print(f"Learning rate: {Config.LEARNING_RATE}")
    
    history = model.fit(
        train_generator,
        epochs=Config.EPOCHS,
        validation_data=validation_generator,
        callbacks=callbacks,
        verbose=1
    )
    
    # Save training history
    save_training_history(history)
    
    # Plot training history
    plot_training_history(history)
    
    # Evaluate on test set
    if test_generator:
        evaluate_model(model, test_generator)
    
    print("\n" + "="*50)
    print("Training completed successfully!")
    print(f"Model saved to: {Config.MODEL_SAVE_PATH}")
    print("="*50)

if __name__ == '__main__':
    main()
