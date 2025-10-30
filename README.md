# 🏥 AI-Powered Skin Disease Recognition System

A complete full-stack web application that uses machine learning to detect and classify skin diseases from uploaded images. Features a professional multi-page portal with educational content and instant AI-powered predictions.

![Project Status](https://img.shields.io/badge/status-ready-brightgreen)
![ML Model](https://img.shields.io/badge/model-sklearn-orange)
![Frontend](https://img.shields.io/badge/frontend-React-blue)
![Backend](https://img.shields.io/badge/backend-Flask-lightgrey)
![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![React](https://img.shields.io/badge/React-18.2-61DAFB.svg)

> 📖 **For step-by-step running instructions, see [HOW_TO_RUN.md](HOW_TO_RUN.md)**

---

## 🚀 How to Run This Project

### Quick Start (30 Seconds!)

**Option 1: Double-Click (Easiest!)**
1. Double-click `start_backend.bat`
2. Double-click `start_frontend.bat`
3. Browser opens at http://localhost:3000

**Option 2: PowerShell Commands**

Terminal 1 - Backend:
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python app_simple.py
```

Terminal 2 - Frontend:
```powershell
cd frontend
npm start
```

### First Time Setup

**Backend:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Frontend:**
```powershell
cd frontend
npm install
```

> 📖 **See [HOW_TO_RUN.md](HOW_TO_RUN.md) for detailed instructions, troubleshooting, and training guide**

---

## 📋 Table of Contents

- [Features](#features)
- [Google Drive Dataset Management](#google-drive-dataset-management)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Model Performance](#model-performance)
- [Training Your Model](#training-your-model)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)
- [Medical Disclaimer](#medical-disclaimer)

---

## ✨ Features

### 🔍 AI Disease Detection
- **Upload & Analyze**: Instant skin disease classification
- **Confidence Scores**: See prediction reliability
- **Top 5 Predictions**: View alternative diagnoses
- **6 Disease Classes**: Acne, Eczema, Melanoma, Psoriasis, Rosacea, Vitiligo

### 📚 Educational Multi-Page Portal
- **Home Page**: Features showcase with modern glassmorphism design
- **Check Disease**: Interactive image upload and analysis
- **Common Diseases**: Learn about 6 skin conditions
- **Precautions**: 30+ preventive care tips
- **About**: Portal mission and technology

### 🎨 Professional UI/UX
- **Modern Design**: Glassmorphism with gradient animations
- **Fully Responsive**: Desktop, tablet, and mobile
- **Smooth Navigation**: Multi-page routing
- **Interactive Elements**: Hover effects and transitions

### 🧠 Machine Learning
- **Scikit-learn Based**: Simple and reliable
- **98.33% Accuracy**: On validation dataset
- **Fast Predictions**: Instant results
- **Optional PyTorch**: Upgrade for deep learning
- **Easy Retraining**: Simple training script

---

## 📁 Google Drive Dataset Management

### Why Use Google Drive?

✅ **Easy Sharing**: Share datasets with team  
✅ **Cloud Backup**: Never lose training data  
✅ **Deployment Ready**: Download on any server  
✅ **Free Storage**: 15GB free space  

### Quick Setup (3 Steps)

**1. Prepare Dataset:**
```powershell
# Zip your dataset folder
Compress-Archive -Path model\dataset -DestinationPath skin_disease_dataset.zip
```

**2. Upload to Google Drive:**
- Go to https://drive.google.com
- Upload `skin_disease_dataset.zip`
- Right-click → Share → "Anyone with the link"
- Copy the sharing link

**3. Download & Use:**
```powershell
# Double-click this file:
download_dataset.bat

# Or run manually:
cd model
pip install gdown
python gdrive_dataset_manager.py
# Paste your Google Drive link
```

### For Deployment

```bash
# On your server
pip install gdown
python model/gdrive_dataset_manager.py "$GDRIVE_DATASET_URL"
python model/train_model_simple.py
```

📖 **See [GDRIVE_SETUP.md](GDRIVE_SETUP.md) for complete Google Drive guide**  
📊 **See [DATASET_WORKFLOW.md](DATASET_WORKFLOW.md) for workflow diagrams**

---

## 🛠️ Technology Stack

### Frontend
- **React** 18.2.0 - UI framework
- **React Router DOM** - Multi-page navigation
- **Axios** - HTTP client
- **CSS3** - Modern styling

### Backend
- **Flask** 3.1.2 - Web framework
- **Flask-CORS** - Cross-origin support
- **Python** 3.13 - Programming language

### Machine Learning
- **scikit-learn** - ML library
- **Logistic Regression** - Classification
- **Pillow** - Image processing
- **NumPy** - Numerical computing
- **Matplotlib** - Visualization

### Cloud Integration
- **gdown** - Google Drive downloads
- **Google Drive** - Dataset storage

### Optional Enhancements
- **PyTorch** - Deep learning
- **torchvision** - Pre-trained models
- **SerpAPI** - Search recommendations

---

## 🗂️ Project Structure

```
skin disease/
│
├── 📄 README.md                   # Complete project guide
├── 📄 HOW_TO_RUN.md              # Step-by-step instructions
├── 📄 GDRIVE_SETUP.md            # Google Drive setup guide
├── 📄 DATASET_WORKFLOW.md        # Dataset workflow diagrams
├── 🚀 start_backend.bat          # Start backend server
├── 🚀 start_frontend.bat         # Start frontend server
├── 🚀 download_dataset.bat       # Download from Google Drive
│
├── backend/                      # Flask API Server
│   ├── venv/                     # Virtual environment ✅
│   ├── app_simple.py            # Main API (sklearn) ⭐
│   ├── app.py                   # Legacy (TensorFlow)
│   ├── requirements.txt         # Dependencies
│   └── .env                     # API keys
│
├── frontend/                     # React Application
│   ├── src/
│   │   ├── App.js               # Main routing
│   │   ├── components/
│   │   │   ├── Navigation.js    # Menu bar
│   │   │   └── ImageUpload.js   # Image picker
│   │   ├── pages/
│   │   │   ├── HomePage.js      # Landing page
│   │   │   ├── CheckDiseasePage.js  # AI detection
│   │   │   ├── CommonDiseasesPage.js
│   │   │   ├── PrecautionsPage.js
│   │   │   └── AboutPage.js
│   │   └── services/
│   │       └── apiService.js    # API calls
│   └── package.json
│
└── model/                        # ML Training
    ├── trained_model/           # Saved model ✅
    │   ├── model.pkl           # Classifier
    │   ├── class_names.json    # Disease names
    │   └── confusion_matrix.png
    ├── dataset/                 # Training images
    │   ├── train/              # 180 images
    │   └── validation/         # 60 images
    ├── gdrive_dataset_manager.py  # Google Drive integration
    ├── train_model_simple.py   # Training script
    └── generate_sample_images.py
```

---

## 📊 Model Performance

### Current Stats

- **Algorithm**: Logistic Regression (sklearn)
- **Training Accuracy**: 100.00%
- **Validation Accuracy**: 98.33%
- **Classes**: 6 skin diseases
- **Training Time**: ~10 seconds
- **Prediction Time**: <100ms

### Classification Report

```
              precision    recall  f1-score

        acne       1.00      0.90      0.95
      eczema       1.00      1.00      1.00
    melanoma       1.00      1.00      1.00
   psoriasis       1.00      1.00      1.00
     rosacea       0.91      1.00      0.95
    vitiligo       1.00      1.00      1.00

    accuracy                           0.98
```

### ⚠️ Important Note

Current model uses **sample/dummy images** for testing.

For real medical use:
1. Download real medical images
2. Replace sample images in `model/dataset/`
3. Retrain the model
4. Validate on real test cases

---

## 🎓 Training Your Own Model

### Step 1: Get Real Dataset

Download from medical datasets:
- **HAM10000** (Kaggle): https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000
- **ISIC Archive**: https://www.isic-archive.com/

Or use Google Drive:
```powershell
.\download_dataset.bat
# Paste your Google Drive link
```

### Step 2: Organize Images

```
model/dataset/
├── train/
│   ├── acne/          (50-100 images)
│   ├── eczema/        (50-100 images)
│   └── ...
└── validation/
    ├── acne/          (10-20 images)
    └── ...
```

### Step 3: Train Model

```powershell
cd model
python train_model_simple.py
```

### Step 4: Restart Backend

```powershell
cd backend
python app_simple.py
```

---

## 📡 API Documentation

### Health Check
```
GET /api/health
```

Response:
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### Predict Disease
```
POST /api/predict
```

Request: `multipart/form-data` with `image` file

Response:
```json
{
  "prediction": "acne",
  "confidence": 0.92,
  "all_predictions": [
    {"disease": "acne", "confidence": 0.92}
  ]
}
```

### Get Classes
```
GET /api/classes
```

Response:
```json
{
  "classes": ["acne", "eczema", "melanoma"],
  "total": 6
}
```

---

## 🔧 Troubleshooting

### Backend Issues

**Model not found:**
```powershell
cd model
python train_model_simple.py
```

**Dependencies missing:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Frontend Issues

**Cannot connect to backend:**
- Ensure backend is running on port 5000
- Check firewall settings

**npm install fails:**
```powershell
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Training Issues

**Out of memory:**
- Reduce image count
- Close other applications
- Use smaller batch size

**Low accuracy:**
- Collect more training data
- Increase training epochs
- Use PyTorch for better features

---

## ⚠️ Medical Disclaimer

**This application is for educational purposes only.**

- Not a substitute for professional medical diagnosis
- Always consult qualified healthcare providers
- Do not use for critical medical decisions
- Results are probabilistic, not definitive
- Accuracy depends on training data quality

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- TensorFlow and Keras teams
- Scikit-learn developers
- React team
- Medical image dataset providers
- SerpAPI for search integration

---

**Remember**: This is a learning tool. Always seek professional medical advice for health concerns.

**Happy Coding! 🚀**




