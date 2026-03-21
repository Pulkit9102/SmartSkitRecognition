This document previously described an extended Google Drive team collaboration
workflow (dataset sharing, sync, and automated downloads). Those features
were removed from this repository. Please use the local dataset workflow
described in `HOW_TO_RUN.md` and place your images under `model/dataset/`.

If you need a new team workflow later, we can re-introduce a lightweight
downloader (e.g. using `gdown`) or integrate a proper data versioning
tool (DVC) — tell me which you'd prefer and I'll add it.

## 🎯 Overview

**Goal:** Allow all team members to:
1. Upload medical images to a shared Google Drive
2. Download the latest dataset automatically
3. Train the model on their local machines
4. Share trained models with the team

---

## 📋 Quick Start (3 Steps)

### For Dataset Creator (First-Time Setup)

```powershell
# 1. Organize your images locally
dataset/
├── train/
│   ├── acne/
│   ├── eczema/
│   ├── melanoma/
│   ├── psoriasis/
│   ├── rosacea/
│   └── vitiligo/
└── validation/
    ├── acne/
    ├── eczema/
    └── ...

# 2. Compress the dataset folder
Compress-Archive -Path dataset -DestinationPath dataset.zip -Force

# 3. Upload to Google Drive and share
# - Go to drive.google.com
# - Upload dataset.zip
# - Right-click → Share → "Anyone with the link can view"
# - Copy the link and share with team
```

### For Team Members (First-Time Setup)

```powershell
# 1. Clone the repository (if not already done)
cd "C:\Users\<YourName>\OneDrive\Desktop"
git clone <repository-url> skin-disease

# 2. Install backend dependencies
cd "skin disease\backend"
pip install -r requirements.txt

# 3. Download dataset from Google Drive
cd ..\model
python gdrive_dataset_manager.py
# Choose option 1, paste the Google Drive link

# 4. Train the model
python train_model_simple.py
```

---

## 📁 Folder Structure for Team Collaboration

```
skin disease/
├── model/
│   ├── dataset/                    # Downloaded from Google Drive
│   │   ├── train/
│   │   │   ├── acne/              # At least 30 images per disease
│   │   │   ├── eczema/
│   │   │   └── ...
│   │   └── validation/
│   │       ├── acne/              # At least 10 images per disease
│   │       └── ...
│   ├── trained_model/              # Generated after training
│   │   ├── model.pkl
│   │   ├── label_encoder.pkl
│   │   └── class_names.json
│   ├── gdrive_config.json          # Auto-created (stores Google Drive link)
│   ├── gdrive_dataset_manager.py   # Dataset download tool
│   └── train_model_simple.py       # Training script
└── backend/
    └── app_simple.py               # Flask API server
```

---

## 🔄 Complete Workflow

### Phase 1: Initial Dataset Preparation (Dataset Owner)

#### Step 1: Collect Images
- Gather medical images of skin diseases
- Minimum recommended: **30 training + 10 validation per disease**
- Supported formats: `.jpg`, `.jpeg`, `.png`, `.bmp`
- Image requirements:
  - Clear, well-lit photos
  - Focus on affected area
  - Minimum 224x224 pixels
  - No watermarks

#### Step 2: Organize Locally

Create this exact structure:
```
dataset/
├── train/
│   ├── acne/
│   │   ├── image_001.jpg
│   │   ├── image_002.jpg
│   │   └── ... (30+ images)
│   ├── eczema/
│   ├── melanoma/
│   ├── psoriasis/
│   ├── rosacea/
│   └── vitiligo/
└── validation/
    ├── acne/
    │   ├── val_001.jpg
    │   └── ... (10+ images)
    ├── eczema/
    └── ...
```

#### Step 3: Compress Dataset

**PowerShell:**
```powershell
Compress-Archive -Path dataset -DestinationPath dataset.zip -Force
```

**Command Prompt:**
```cmd
powershell -Command "Compress-Archive -Path dataset -DestinationPath dataset.zip -Force"
```

**File Explorer:**
- Right-click `dataset` folder → Send to → Compressed (zipped) folder

#### Step 4: Upload to Google Drive

1. Go to [drive.google.com](https://drive.google.com)
2. Click "New" → "File upload"
3. Select `dataset.zip`
4. Wait for upload to complete

#### Step 5: Share the Link

1. Right-click `dataset.zip` in Google Drive
2. Click "Share"
3. Change to "Anyone with the link can view"
4. Click "Copy link"
5. Share link with team members via:
   - Email
   - Slack
   - Teams
   - WhatsApp
   - README.md

Example link:
```
https://drive.google.com/file/d/1a2b3c4d5e6f7g8h9i0j/view?usp=sharing
```

---

### Phase 2: Team Members Download Dataset

#### Method 1: Interactive (Recommended for First Time)

```powershell
cd "skin disease\model"
python gdrive_dataset_manager.py
```

Then:
1. Choose option **1** (Download dataset from Google Drive)
2. Paste the Google Drive link
3. Press Enter
4. Wait for download and extraction

#### Method 2: Command Line (Quick)

```powershell
cd "skin disease\model"
python gdrive_dataset_manager.py "YOUR_GOOGLE_DRIVE_LINK"
```

#### Method 3: Python Script

```python
from gdrive_dataset_manager import GDriveDatasetManager

manager = GDriveDatasetManager()
manager.download_dataset('YOUR_GOOGLE_DRIVE_LINK')
```

**Expected Output:**
```
======================================================================
  📥 DOWNLOADING DATASET FROM GOOGLE DRIVE
======================================================================

📥 Downloading from Google Drive...
Source: https://drive.google.com/file/d/1a2b3c4d5...

✅ Downloaded: 45.23 MB

📂 Extracting to: dataset
✅ Extracted successfully!

📊 Dataset Statistics:
----------------------------------------------------------------------
  Training Images:
    acne           :   30 images
    eczema         :   30 images
    melanoma       :   30 images
    psoriasis      :   30 images
    rosacea        :   30 images
    vitiligo       :   30 images

  Validation Images:
    acne           :   10 images
    eczema         :   10 images
    melanoma       :   10 images
    psoriasis      :   10 images
    rosacea        :   10 images
    vitiligo       :   10 images

----------------------------------------------------------------------
  Total Training:    180 images
  Total Validation:   60 images
  Total Dataset:     240 images
  Disease Classes:     6
----------------------------------------------------------------------

✅ Dataset size looks good!

======================================================================
  ✅ DATASET READY FOR TRAINING!
======================================================================
```

---

### Phase 3: Train the Model

After downloading the dataset, each team member can train:

```powershell
cd "skin disease\model"
python train_model_simple.py
```

**Training Output:**
```
======================================================================
  🧠 SIMPLE ML MODEL TRAINING
======================================================================

📊 Loading dataset from: dataset

📁 Training Data:
   • acne: 30 images
   • eczema: 30 images
   ...
   Total: 180 images

📁 Validation Data:
   ...
   Total: 60 images

🔄 Extracting features from images...
Processing training images: 100%|████████████| 180/180

⚙️ Training Logistic Regression model...

✅ Training completed!

📈 Model Performance:
   Training Accuracy:   100.00%
   Validation Accuracy:  98.33%

💾 Saving model to trained_model/
   ✅ model.pkl
   ✅ label_encoder.pkl
   ✅ class_names.json

======================================================================
  🎉 MODEL TRAINING COMPLETE!
======================================================================
```

---

### Phase 4: Test the Model

#### Option 1: Run Backend API

```powershell
# Terminal 1: Start Backend
cd "skin disease\backend"
python app_simple.py

# Terminal 2: Start Frontend
cd "skin disease\frontend"
npm start
```

Then visit: http://localhost:3000

#### Option 2: Python Test Script

```python
import pickle
import numpy as np
from PIL import Image

# Load model
with open('trained_model/model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('trained_model/label_encoder.pkl', 'rb') as f:
    encoder = pickle.load(f)

# Test on image
img = Image.open('test_image.jpg').resize((64, 64))
features = np.array(img).flatten().reshape(1, -1)
prediction = model.predict(features)
disease = encoder.inverse_transform(prediction)[0]

print(f"Predicted disease: {disease}")
```

---

## 🔄 Updating the Dataset (When New Images Are Added)

### For Dataset Owner

```powershell
# 1. Add new images to local dataset folder
# dataset/train/acne/new_image_001.jpg
# dataset/train/eczema/new_image_002.jpg

# 2. Re-compress
Compress-Archive -Path dataset -DestinationPath dataset_v2.zip -Force

# 3. Upload new version to Google Drive
# - Upload dataset_v2.zip
# - Share the new link OR replace old file

# 4. Notify team members
```

### For Team Members

```powershell
cd "skin disease\model"
python gdrive_dataset_manager.py

# Choose option 2 (Sync dataset)
# Or option 1 with new link
```

This will:
- Backup old dataset → `dataset_backup_20240115_143022`
- Download new dataset
- Extract to `dataset/`

Then re-train:
```powershell
python train_model_simple.py
```

---

## 🛠️ Troubleshooting

### Issue: "No Google Drive URL configured"

**Solution:**
```powershell
# Run interactive setup
python gdrive_dataset_manager.py
# Choose option 1, paste the link
```

### Issue: "Download failed - file not found"

**Causes:**
1. Link not set to "Anyone with the link can view"
2. Wrong link format
3. File deleted from Google Drive

**Solution:**
1. Re-share the file in Google Drive
2. Set permissions to "Anyone with the link"
3. Copy the new link
4. Try downloading again

### Issue: "Dataset structure may be incorrect"

**Solution:**
Check that zip contains:
```
dataset.zip
└── dataset/
    ├── train/
    │   ├── acne/
    │   └── ...
    └── validation/
        └── ...
```

NOT:
```
dataset.zip
├── image1.jpg
├── image2.jpg  ❌ Wrong!
```

### Issue: "Very small dataset" warning

**Solution:**
- Add more images (minimum 30 per disease)
- Use data augmentation in training
- Collect real medical images

### Issue: Training accuracy 100%, validation 60%

**Cause:** Overfitting (too few images)

**Solutions:**
1. Add more training images
2. Add more validation images
3. Use data augmentation
4. Try different model (KNN, Random Forest)

---

## 📊 Dataset Quality Guidelines

### Image Requirements

| Aspect | Requirement |
|--------|-------------|
| **Format** | JPG, PNG, BMP |
| **Size** | Minimum 224x224 pixels |
| **Quality** | Clear, well-lit, in-focus |
| **Content** | Close-up of affected area |
| **Background** | Minimal, non-distracting |
| **Quantity** | Min 30 train + 10 val per class |

### Good Examples ✅
- Clear view of skin condition
- Proper lighting (not too dark/bright)
- Focus on affected area
- Minimal background
- Consistent angle/distance

### Bad Examples ❌
- Blurry images
- Poor lighting (too dark/bright)
- Too far away (condition not visible)
- Heavy filters/editing
- Watermarks covering condition

---

## 🔐 Security & Privacy

### Important Notes

⚠️ **Medical Data Privacy:**
- Remove patient identifiable information
- Get proper consent for medical images
- Follow HIPAA/GDPR guidelines
- Use encryption for sensitive data

### Google Drive Security

1. **Link Sharing:**
   - Use "Anyone with the link" (not "Public")
   - Don't share link publicly (GitHub, forums)
   - Revoke link if compromised

2. **Access Control:**
   - Only share with authorized team members
   - Use Google Workspace for better control
   - Monitor access logs

3. **Data Protection:**
   - Encrypt sensitive images before upload
   - Use password-protected zips for extra security
   - Regularly audit who has access

---

## 🚀 Advanced: Automated Workflow

### Auto-Download Before Training

Update `train_model_simple.py`:

```python
# At the top of train_model_simple.py
from gdrive_dataset_manager import GDriveDatasetManager

# Before training
manager = GDriveDatasetManager()
if not manager.check_dataset_exists():
    print("Dataset not found. Downloading from Google Drive...")
    manager.sync_dataset()
```

### Batch Script for One-Click Workflow

Create `sync_and_train.bat`:

```batch
@echo off
echo ========================================
echo  Sync Dataset and Train Model
echo ========================================

cd model
echo Checking for dataset updates...
python gdrive_dataset_manager.py sync

echo.
echo Training model...
python train_model_simple.py

echo.
echo ========================================
echo  Complete!
echo ========================================
pause
```

Usage:
```powershell
.\sync_and_train.bat
```

---

## 📞 Support

### Common Questions

**Q: How often should I sync the dataset?**
A: Check weekly or when notified of updates.

**Q: Can multiple people train at the same time?**
A: Yes! Each person trains on their local machine independently.

**Q: How do I share my trained model?**
A: Upload the `trained_model/` folder to Google Drive and share.

**Q: What if Google Drive link changes?**
A: Just paste the new link when downloading. It auto-updates `gdrive_config.json`.

**Q: Can I use this with Dropbox/OneDrive?**
A: Currently only Google Drive. For others, manually download and extract.

### Getting Help

1. Check this guide first
2. Check `HOW_TO_RUN.md` for setup issues
3. Check error messages carefully
4. Contact team lead
5. Create GitHub issue (if using Git)

---

## ✅ Checklist for New Team Members

- [ ] Clone/download project
- [ ] Install Python 3.13+ and Node.js
- [ ] Install backend dependencies: `pip install -r backend/requirements.txt`
- [ ] Install frontend dependencies: `npm install` in `frontend/`
- [ ] Get Google Drive link from team
- [ ] Download dataset: `python gdrive_dataset_manager.py`
- [ ] Train model: `python train_model_simple.py`
- [ ] Test backend: `python app_simple.py`
- [ ] Test frontend: `npm start`
- [ ] Verify prediction works at http://localhost:3000

---

## 📚 Additional Resources

- **Main README:** `README.md` - Complete project documentation
- **Setup Guide:** `HOW_TO_RUN.md` - Step-by-step installation
- **Google Drive Setup:** `gdrive_config.json` - Auto-generated config
- **Training Script:** `train_model_simple.py` - Model training code
- **Dataset Manager:** `gdrive_dataset_manager.py` - Download/sync tool

---

**Happy Collaborating! 🎉**

Last Updated: 2024-01-15
