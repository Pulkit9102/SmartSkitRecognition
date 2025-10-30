"""
Sample Dataset Creator

This script helps you create a sample dataset structure for testing.
It creates placeholder folders that you can populate with your images.
"""

import os
import json

# Sample disease information
SAMPLE_DISEASES = {
    'acne': {
        'description': 'Common skin condition causing pimples and spots',
        'severity': 'mild-moderate',
        'common_locations': ['face', 'back', 'chest']
    },
    'eczema': {
        'description': 'Chronic condition causing itchy, inflamed skin',
        'severity': 'mild-severe',
        'common_locations': ['hands', 'face', 'elbows', 'knees']
    },
    'melanoma': {
        'description': 'Serious skin cancer requiring immediate attention',
        'severity': 'severe',
        'common_locations': ['any body part']
    },
    'psoriasis': {
        'description': 'Autoimmune condition causing scaly skin patches',
        'severity': 'moderate-severe',
        'common_locations': ['elbows', 'knees', 'scalp', 'lower back']
    },
    'rosacea': {
        'description': 'Facial redness and visible blood vessels',
        'severity': 'mild-moderate',
        'common_locations': ['face', 'nose', 'cheeks']
    },
    'vitiligo': {
        'description': 'Loss of skin pigmentation in patches',
        'severity': 'mild-moderate',
        'common_locations': ['face', 'hands', 'around body openings']
    }
}

def create_sample_structure(base_path):
    """Create sample dataset structure"""
    
    print("\n" + "="*60)
    print("Creating Sample Dataset Structure")
    print("="*60 + "\n")
    
    splits = ['train', 'validation', 'test']
    
    for split in splits:
        for disease in SAMPLE_DISEASES.keys():
            path = os.path.join(base_path, split, disease)
            os.makedirs(path, exist_ok=True)
            
            # Create README in each disease folder
            readme_path = os.path.join(path, 'README.txt')
            info = SAMPLE_DISEASES[disease]
            
            with open(readme_path, 'w') as f:
                f.write(f"Disease: {disease.upper()}\n")
                f.write("="*40 + "\n\n")
                f.write(f"Description: {info['description']}\n")
                f.write(f"Severity: {info['severity']}\n")
                f.write(f"Common locations: {', '.join(info['common_locations'])}\n\n")
                f.write(f"Instructions:\n")
                f.write(f"- Place your {disease} images in this folder\n")
                f.write(f"- Supported formats: JPG, PNG, GIF, BMP\n")
                f.write(f"- Recommended: 100+ images for {split} set\n")
                f.write(f"- Minimum: 50 images for {split} set\n")
            
            print(f"✅ Created: {split}/{disease}/")
    
    # Create disease info JSON
    info_path = os.path.join(base_path, 'disease_info.json')
    with open(info_path, 'w') as f:
        json.dump(SAMPLE_DISEASES, f, indent=2)
    
    print(f"\n✅ Created disease info: disease_info.json")
    
    # Create data collection guide
    guide_path = os.path.join(base_path, 'DATA_COLLECTION_GUIDE.txt')
    with open(guide_path, 'w') as f:
        f.write("SKIN DISEASE DATASET - DATA COLLECTION GUIDE\n")
        f.write("="*60 + "\n\n")
        
        f.write("RECOMMENDED DATASETS:\n")
        f.write("-" * 60 + "\n")
        f.write("1. HAM10000 (Skin Cancer)\n")
        f.write("   https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000\n\n")
        
        f.write("2. ISIC Archive (Melanoma)\n")
        f.write("   https://www.isic-archive.com/\n\n")
        
        f.write("3. DermNet (Various Conditions)\n")
        f.write("   https://dermnetnz.org/\n\n")
        
        f.write("4. SD-198 (Skin Diseases)\n")
        f.write("   Search: 'SD-198 skin disease dataset'\n\n")
        
        f.write("\nDATA COLLECTION GUIDELINES:\n")
        f.write("-" * 60 + "\n")
        f.write("1. Image Quality:\n")
        f.write("   - Clear, well-lit images\n")
        f.write("   - Focused on affected area\n")
        f.write("   - Minimal blur or obstruction\n\n")
        
        f.write("2. Quantity:\n")
        f.write("   - Minimum: 50 images per disease\n")
        f.write("   - Recommended: 100-500 images per disease\n")
        f.write("   - Professional: 500+ images per disease\n\n")
        
        f.write("3. Diversity:\n")
        f.write("   - Different skin tones\n")
        f.write("   - Various disease stages\n")
        f.write("   - Different body locations\n")
        f.write("   - Multiple age groups\n\n")
        
        f.write("4. Data Split:\n")
        f.write("   - Training: 70-80% of images\n")
        f.write("   - Validation: 10-15% of images\n")
        f.write("   - Test: 10-15% of images\n\n")
        
        f.write("5. Ethics & Privacy:\n")
        f.write("   - Use only publicly available or consented data\n")
        f.write("   - Remove any personal identifiers\n")
        f.write("   - Follow data usage agreements\n")
        f.write("   - Comply with medical data regulations\n\n")
        
        f.write("DISEASES INCLUDED:\n")
        f.write("-" * 60 + "\n")
        for disease, info in SAMPLE_DISEASES.items():
            f.write(f"\n{disease.upper()}:\n")
            f.write(f"  Description: {info['description']}\n")
            f.write(f"  Severity: {info['severity']}\n")
            f.write(f"  Locations: {', '.join(info['common_locations'])}\n")
        
        f.write("\n" + "="*60 + "\n")
        f.write("After collecting images, run: python dataset_helper.py\n")
        f.write("="*60 + "\n")
    
    print(f"✅ Created data collection guide: DATA_COLLECTION_GUIDE.txt\n")

def print_next_steps():
    """Print next steps after structure creation"""
    
    print("\n" + "="*60)
    print("Next Steps")
    print("="*60 + "\n")
    
    print("1. Download/collect skin disease images from:")
    print("   - Kaggle (HAM10000, ISIC datasets)")
    print("   - Medical image databases")
    print("   - Public research datasets")
    print("")
    print("2. Organize images into the created folders:")
    print("   - dataset/train/[disease]/")
    print("   - dataset/validation/[disease]/")
    print("   - dataset/test/[disease]/")
    print("")
    print("3. Validate your dataset:")
    print("   python dataset_helper.py")
    print("   (Choose option 4 to validate)")
    print("")
    print("4. Train your model:")
    print("   python train_model.py")
    print("")
    print("5. Test the backend:")
    print("   python test_api.py")
    print("")
    
    print("="*60 + "\n")

if __name__ == '__main__':
    # Get base directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_path = os.path.join(base_dir, 'dataset')
    
    print("\n" + "="*60)
    print("🔬 Skin Disease Dataset Setup")
    print("="*60)
    
    print("\nThis will create a sample dataset structure with the following diseases:")
    for disease in SAMPLE_DISEASES.keys():
        print(f"  - {disease}")
    
    print("\nYou'll need to populate these folders with actual images.")
    
    choice = input("\nCreate sample structure? (y/n): ").strip().lower()
    
    if choice == 'y':
        create_sample_structure(dataset_path)
        print_next_steps()
        
        print("✅ Sample dataset structure created successfully!")
        print("\n📖 Check DATA_COLLECTION_GUIDE.txt for detailed instructions.")
    else:
        print("\n❌ Setup cancelled.")
