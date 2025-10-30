"""
Dataset Helper - Utility script for dataset management
"""

import os
import shutil
from pathlib import Path
import random

def create_dataset_structure(base_path, diseases):
    """
    Create dataset folder structure for multiple diseases
    
    Args:
        base_path: Base directory for dataset
        diseases: List of disease names
    """
    splits = ['train', 'validation', 'test']
    
    for split in splits:
        for disease in diseases:
            path = os.path.join(base_path, split, disease)
            os.makedirs(path, exist_ok=True)
            print(f"Created: {path}")

def split_dataset(source_dir, dest_base_dir, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15):
    """
    Split images from source directory into train/val/test sets
    
    Args:
        source_dir: Directory containing disease subdirectories
        dest_base_dir: Destination base directory
        train_ratio: Ratio for training set (default 0.7)
        val_ratio: Ratio for validation set (default 0.15)
        test_ratio: Ratio for test set (default 0.15)
    """
    
    if abs(train_ratio + val_ratio + test_ratio - 1.0) > 0.01:
        raise ValueError("Ratios must sum to 1.0")
    
    # Get all disease directories
    disease_dirs = [d for d in os.listdir(source_dir) 
                   if os.path.isdir(os.path.join(source_dir, d))]
    
    for disease in disease_dirs:
        disease_path = os.path.join(source_dir, disease)
        
        # Get all images
        images = [f for f in os.listdir(disease_path) 
                 if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]
        
        # Shuffle images
        random.shuffle(images)
        
        # Calculate split sizes
        total = len(images)
        train_size = int(total * train_ratio)
        val_size = int(total * val_ratio)
        
        # Split images
        train_images = images[:train_size]
        val_images = images[train_size:train_size + val_size]
        test_images = images[train_size + val_size:]
        
        # Copy images to respective directories
        splits = {
            'train': train_images,
            'validation': val_images,
            'test': test_images
        }
        
        for split_name, split_images in splits.items():
            dest_dir = os.path.join(dest_base_dir, split_name, disease)
            os.makedirs(dest_dir, exist_ok=True)
            
            for img in split_images:
                src = os.path.join(disease_path, img)
                dst = os.path.join(dest_dir, img)
                shutil.copy2(src, dst)
            
            print(f"{disease} - {split_name}: {len(split_images)} images")

def count_images(dataset_path):
    """Count images in dataset"""
    
    splits = ['train', 'validation', 'test']
    total_count = 0
    
    print("\n" + "="*50)
    print("Dataset Statistics")
    print("="*50)
    
    for split in splits:
        split_path = os.path.join(dataset_path, split)
        if not os.path.exists(split_path):
            continue
            
        print(f"\n{split.upper()}:")
        split_total = 0
        
        diseases = [d for d in os.listdir(split_path) 
                   if os.path.isdir(os.path.join(split_path, d))]
        
        for disease in sorted(diseases):
            disease_path = os.path.join(split_path, disease)
            images = [f for f in os.listdir(disease_path) 
                     if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]
            count = len(images)
            split_total += count
            print(f"  {disease}: {count} images")
        
        print(f"  Total: {split_total} images")
        total_count += split_total
    
    print("\n" + "="*50)
    print(f"GRAND TOTAL: {total_count} images")
    print("="*50 + "\n")

def validate_dataset(dataset_path):
    """Validate dataset structure and provide recommendations"""
    
    print("\n" + "="*50)
    print("Dataset Validation")
    print("="*50 + "\n")
    
    issues = []
    warnings = []
    
    # Check if dataset directory exists
    if not os.path.exists(dataset_path):
        issues.append(f"Dataset directory not found: {dataset_path}")
        return issues, warnings
    
    # Check required splits
    train_path = os.path.join(dataset_path, 'train')
    val_path = os.path.join(dataset_path, 'validation')
    
    if not os.path.exists(train_path):
        issues.append("Training directory not found")
    
    if not os.path.exists(val_path):
        issues.append("Validation directory not found")
    
    # Check each split
    for split in ['train', 'validation', 'test']:
        split_path = os.path.join(dataset_path, split)
        
        if not os.path.exists(split_path):
            if split != 'test':  # test is optional
                continue
        
        diseases = [d for d in os.listdir(split_path) 
                   if os.path.isdir(os.path.join(split_path, d))]
        
        if len(diseases) < 2:
            warnings.append(f"{split}: Need at least 2 disease classes (found {len(diseases)})")
        
        for disease in diseases:
            disease_path = os.path.join(split_path, disease)
            images = [f for f in os.listdir(disease_path) 
                     if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]
            
            if len(images) < 10:
                warnings.append(f"{split}/{disease}: Only {len(images)} images (recommend 50+)")
            elif len(images) < 50:
                warnings.append(f"{split}/{disease}: {len(images)} images (recommend 100+ for better accuracy)")
    
    # Print results
    if issues:
        print("❌ ISSUES (must fix):")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("✅ No critical issues found")
    
    if warnings:
        print("\n⚠️ WARNINGS (recommended to address):")
        for warning in warnings:
            print(f"  - {warning}")
    else:
        print("\n✅ No warnings")
    
    print("\n" + "="*50 + "\n")
    
    return issues, warnings

if __name__ == '__main__':
    import sys
    
    # Get base directory (parent of model directory)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_path = os.path.join(base_dir, 'dataset')
    
    print("="*50)
    print("Skin Disease Dataset Helper")
    print("="*50)
    print("\nOptions:")
    print("1. Create dataset structure")
    print("2. Split existing dataset")
    print("3. Count images in dataset")
    print("4. Validate dataset")
    print("5. Exit")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == '1':
        print("\nEnter disease names (comma-separated):")
        print("Example: acne,eczema,melanoma,psoriasis")
        diseases_input = input("Diseases: ").strip()
        diseases = [d.strip() for d in diseases_input.split(',')]
        
        create_dataset_structure(dataset_path, diseases)
        print("\n✅ Dataset structure created!")
        
    elif choice == '2':
        source = input("\nEnter source directory path: ").strip()
        if os.path.exists(source):
            split_dataset(source, dataset_path)
            print("\n✅ Dataset split complete!")
        else:
            print(f"\n❌ Source directory not found: {source}")
    
    elif choice == '3':
        count_images(dataset_path)
    
    elif choice == '4':
        issues, warnings = validate_dataset(dataset_path)
        if not issues:
            count_images(dataset_path)
    
    elif choice == '5':
        print("\nGoodbye!")
    
    else:
        print("\n❌ Invalid choice")
