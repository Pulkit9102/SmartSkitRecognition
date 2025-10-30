"""
Generate sample colored images for testing the training pipeline
This creates dummy images so you can test training without real medical images
"""

from PIL import Image, ImageDraw, ImageFont
import os
import random
import numpy as np

# Dataset configuration
DATASET_DIR = "dataset"
DISEASES = ['acne', 'eczema', 'melanoma', 'psoriasis', 'rosacea', 'vitiligo']
IMAGE_SIZE = (224, 224)

# Number of images to generate
TRAIN_COUNT = 30
VAL_COUNT = 10

# Color schemes for each disease (to make them visually different)
COLOR_SCHEMES = {
    'acne': [(220, 100, 100), (200, 80, 80), (180, 60, 60)],  # Reddish
    'eczema': [(200, 150, 150), (180, 130, 130), (160, 110, 110)],  # Pink
    'melanoma': [(80, 60, 50), (100, 80, 70), (120, 100, 90)],  # Dark brown
    'psoriasis': [(220, 180, 180), (200, 160, 160), (180, 140, 140)],  # Light pink
    'rosacea': [(230, 120, 120), (210, 100, 100), (190, 80, 80)],  # Red
    'vitiligo': [(250, 245, 240), (240, 235, 230), (230, 225, 220)]  # Light/white
}

def create_sample_image(disease, index, split):
    """Create a sample colored image with random patterns"""
    # Create base image
    img = Image.new('RGB', IMAGE_SIZE, color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Get color scheme for this disease
    colors = COLOR_SCHEMES.get(disease, [(200, 200, 200)])
    
    # Add random circles/spots to simulate skin texture
    num_spots = random.randint(10, 30)
    for _ in range(num_spots):
        x = random.randint(0, IMAGE_SIZE[0])
        y = random.randint(0, IMAGE_SIZE[1])
        radius = random.randint(5, 30)
        color = random.choice(colors)
        
        # Add some variation to color
        varied_color = tuple(min(255, max(0, c + random.randint(-20, 20))) for c in color)
        
        draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                    fill=varied_color, outline=None)
    
    # Add some noise
    img_array = np.array(img)
    noise = np.random.randint(-10, 10, img_array.shape, dtype=np.int16)
    img_array = np.clip(img_array.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    img = Image.fromarray(img_array)
    
    # Add text label (optional, for identification)
    draw = ImageDraw.Draw(img)
    try:
        # Try to use a font, fallback to default if not available
        font = ImageFont.truetype("arial.ttf", 12)
    except:
        font = ImageFont.load_default()
    
    draw.text((5, 5), f"{disease}_{split}_{index}", fill=(0, 0, 0), font=font)
    
    return img

def generate_dataset():
    """Generate sample dataset"""
    print("=" * 60)
    print("  SAMPLE IMAGE GENERATOR FOR TESTING")
    print("=" * 60)
    print("\n⚠️  WARNING: These are NOT real medical images!")
    print("   This is only for testing the training pipeline.\n")
    print("   For actual use, you MUST collect real skin disease images")
    print("   from medical datasets like Kaggle HAM10000 or ISIC.\n")
    print("=" * 60)
    
    response = input("\nGenerate sample images for testing? (y/n): ").lower()
    if response != 'y':
        print("Cancelled.")
        return
    
    total_images = 0
    
    for disease in DISEASES:
        print(f"\n📸 Generating images for: {disease}")
        
        # Generate training images
        train_dir = os.path.join(DATASET_DIR, 'train', disease)
        os.makedirs(train_dir, exist_ok=True)
        
        for i in range(TRAIN_COUNT):
            img = create_sample_image(disease, i, 'train')
            img_path = os.path.join(train_dir, f'{disease}_{i:03d}.jpg')
            img.save(img_path, quality=85)
        
        print(f"  ✓ Created {TRAIN_COUNT} training images")
        total_images += TRAIN_COUNT
        
        # Generate validation images
        val_dir = os.path.join(DATASET_DIR, 'validation', disease)
        os.makedirs(val_dir, exist_ok=True)
        
        for i in range(VAL_COUNT):
            img = create_sample_image(disease, i, 'val')
            img_path = os.path.join(val_dir, f'{disease}_val_{i:03d}.jpg')
            img.save(img_path, quality=85)
        
        print(f"  ✓ Created {VAL_COUNT} validation images")
        total_images += VAL_COUNT
    
    print("\n" + "=" * 60)
    print(f"✅ Generated {total_images} sample images!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Run training: python train_model_simple.py")
    print("2. The model will train on these dummy images")
    print("3. Once you verify it works, replace with real images")
    print("4. Re-train with real images for actual use")
    print("\n⚠️  REMEMBER: Replace these dummy images with real medical")
    print("   images before using the system for actual predictions!\n")

if __name__ == "__main__":
    generate_dataset()
