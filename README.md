# ðŸ¥ AI-Powered Skin Disease Recognition System

A complete full-stack web application that uses machine learning to detect and classify skin diseases from uploaded images. Features a professional multi-page portal with educational content and instant AI-powered predictions.

![Project Status](https://img.shields.io/badge/status-ready-brightgreen)
![ML Model](https://img.shields.io/badge/model-sklearn-orange)
![Frontend](https://img.shields.io/badge/frontend-React-blue)
![Backend](https://img.shields.io/badge/backend-Flask-lightgrey)
![Python](https://img.shields.io/badge/Python-3.13.7-blue.svg)
![React](https://img.shields.io/badge/React-18.2.0-61DAFB.svg)

> **ðŸ“– For step-by-step running instructions, see [HOW_TO_RUN.md](HOW_TO_RUN.md)**
---

##  How to Run This Project

### Quick Start (30 Seconds!)

**Option 1: Double-Click (Easiest!)**
1. Double-click `start_backend.bat`
2. Double-click `start_frontend.bat`
3. Browser opens at http://localhost:3000

**Option 2: PowerShell Commands**

Terminal 1 - Backend:
``powershell
cd backend
.\venv\Scripts\Activate.ps1
python app_simple.py
``

Terminal 2 - Frontend:
``powershell
cd frontend
npm start
``

### First Time Setup

**Backend:**
``powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install flask flask-cors pillow scikit-learn numpy matplotlib seaborn pandas
``

**Frontend:**
``powershell
cd frontend
npm install
``

> ** See [HOW_TO_RUN.md](HOW_TO_RUN.md) for detailed instructions, troubleshooting, and training guide**

## ï¿½ SUPER QUICK START - 30 Seconds!

### Option 1: Double-Click Method (Easiest!)
1. Double-click **`start_backend.bat`**
2. Double-click **`start_frontend.bat`**
3. Browser opens at http://localhost:3000 automatically
4. **Done!** ðŸŽ‰

### Option 2: Command Line
**Terminal 1:** `cd backend` â†’ `.\venv\Scripts\Activate.ps1` â†’ `python app_simple.py`  
**Terminal 2:** `cd frontend` â†’ `npm start`

### ðŸ“– Detailed Guides
- **[QUICK_START.md](QUICK_START.md)** - 2-minute setup guide
- **[RUN_PROJECT.md](RUN_PROJECT.md)** - Complete instructions with troubleshooting
- **[SYSTEM_READY.md](SYSTEM_READY.md)** - Current status and what's working

---

## ï¿½ðŸ“‹ Table of Contents

- [Features](#features)
- [How to Run](#how-to-run)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Model Performance](#model-performance)
- [Training Your Model](#training-your-model)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)
- [Medical Disclaimer](#medical-disclaimer)

## âœ¨ Features

### ðŸ” AI Disease Detection (Working Now!)
- **Upload & Analyze**: Instant skin disease classification
- **Confidence Scores**: See prediction reliability
- **Top 5 Predictions**: View alternative diagnoses
- **6 Disease Classes**: Acne, Eczema, Melanoma, Psoriasis, Rosacea, Vitiligo

### ðŸ“š Educational Multi-Page Portal
- **Home Page**: Features showcase with modern glassmorphism design
- **Check Disease**: Interactive image upload and analysis
- **Common Diseases**: Learn about 6 skin conditions with symptoms and causes
- **Precautions**: 30+ preventive care tips across 6 categories
- **About**: Portal mission, technology, and how it works

### ðŸŽ¨ Professional UI/UX
- **Modern Design**: Glassmorphism effects with gradient animations
- **Fully Responsive**: Works on desktop, tablet, and mobile
- **Smooth Navigation**: Multi-page routing with React Router
- **Interactive Elements**: Hover effects and transitions
- **Clean Layout**: Organized information hierarchy

### ðŸ§  Machine Learning
- **Scikit-learn Based**: Simple and reliable (no TensorFlow issues!)
- **98.33% Accuracy**: On validation dataset
- **Fast Predictions**: Instant results
- **Optional PyTorch**: Upgrade for deep learning features
- **Easy Retraining**: Simple script to train with your data

### âš¡ Technical Features
- **REST API**: Flask backend with 4 endpoints
- **CORS Enabled**: Frontend-backend communication
- **Virtual Environment**: Isolated Python dependencies
- **Hot Reload**: Development mode with auto-refresh
- **Error Handling**: Graceful failure messages

## ðŸ› ï¸ Technology Stack

### Frontend
- **React** 18.2.0 - UI framework
- **React Router DOM** - Multi-page navigation
- **Axios** - HTTP client for API calls
- **CSS3** - Modern styling with glassmorphism

### Backend
- **Flask** 3.1.2 - Python web framework
- **Flask-CORS** - Cross-origin resource sharing
- **Python** 3.13.7 - Programming language

### Machine Learning
- **scikit-learn** - Machine learning library
- **Logistic Regression** - Classification algorithm
- **Pillow** - Image processing
- **NumPy** - Numerical computing
- **Matplotlib** - Visualization
- **Seaborn** - Statistical plots

### Optional Enhancements
- **PyTorch** - Deep learning (for better accuracy)
- **torchvision** - Pre-trained models (ResNet50)
- **SerpAPI** - Search recommendations (optional)

## ðŸ—ï¸ System Architecture

```
User â†’ Browser (Port 3000)
           â†“
    React Frontend
    (5 Pages + Navigation)
           â†“
    HTTP/REST API Calls
           â†“
    Flask Backend (Port 5000)
           â†“
    â”Œâ”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”
    â†“             â†“
sklearn Model   Optional:
(Logistic       - SerpAPI
Regression)     - PyTorch
    â†“
Prediction
    â†“
JSON Response
    â†“
Display Results
```

### Data Flow

1. User uploads image on **Check Disease** page
2. Frontend sends image via POST to `/api/predict`
3. Backend extracts features from image
4. Model predicts disease class
5. Backend returns prediction + confidence scores
6. Frontend displays results with top 5 predictions

## ðŸ“ Project Structure

```
skin disease/
â”‚
â”œâ”€â”€ ðŸ“„ README.md                   # This file - complete project guide
â”œâ”€â”€ ðŸ“„ QUICK_START.md              # Super fast 2-minute start guide
â”œâ”€â”€ ðŸ“„ RUN_PROJECT.md              # Detailed instructions + troubleshooting
â”œâ”€â”€ ðŸ“„ SYSTEM_READY.md             # Current status and next steps
â”œâ”€â”€ ðŸš€ start_backend.bat           # Click to start backend server
â”œâ”€â”€ ðŸš€ start_frontend.bat          # Click to start frontend server
â”‚
â”œâ”€â”€ backend/                       # Flask API Server
â”‚   â”œâ”€â”€ venv/                      # Python virtual environment âœ…
â”‚   â”œâ”€â”€ app_simple.py             # Main API (sklearn) â­ USE THIS
â”‚   â”œâ”€â”€ app.py                    # Legacy (TensorFlow) - optional
â”‚   â”œâ”€â”€ requirements.txt          # Python dependencies
â”‚   â””â”€â”€ .env                      # Optional: SerpAPI key
â”‚
â”œâ”€â”€ frontend/                      # React Web Application
â”‚   â”œâ”€â”€ src/
â”‚   â”‚   â”œâ”€â”€ App.js                # Main routing & pages
â”‚   â”‚   â”œâ”€â”€ App.css               # Global styles
â”‚   â”‚   â”œâ”€â”€ components/
â”‚   â”‚   â”‚   â”œâ”€â”€ Navigation.js     # 5-page menu bar
â”‚   â”‚   â”‚   â”œâ”€â”€ Navigation.css
â”‚   â”‚   â”‚   â”œâ”€â”€ ImageUpload.js    # Image picker component
â”‚   â”‚   â”‚   â””â”€â”€ ImageUpload.css
â”‚   â”‚   â”œâ”€â”€ pages/
â”‚   â”‚   â”‚   â”œâ”€â”€ HomePage.js       # Landing with features
â”‚   â”‚   â”‚   â”œâ”€â”€ CheckDiseasePage.js  # Disease detection
â”‚   â”‚   â”‚   â”œâ”€â”€ CommonDiseasesPage.js  # Educational content
â”‚   â”‚   â”‚   â”œâ”€â”€ PrecautionsPage.js     # Health tips
â”‚   â”‚   â”‚   â”œâ”€â”€ AboutPage.js      # About portal
â”‚   â”‚   â”‚   â””â”€â”€ *.css             # Page styles
â”‚   â”‚   â”œâ”€â”€ index.js              # React entry point
â”‚   â”‚   â””â”€â”€ index.css
â”‚   â”œâ”€â”€ package.json              # Node dependencies
â”‚   â””â”€â”€ node_modules/             # Installed packages
â”‚
â””â”€â”€ model/                         # ML Model & Training
    â”œâ”€â”€ trained_model/             # âœ… Saved model (ready!)
    â”‚   â”œâ”€â”€ model.pkl              # Trained classifier
    â”‚   â”œâ”€â”€ label_encoder.pkl      # Label encoder
    â”‚   â”œâ”€â”€ class_names.json       # Disease names
    â”‚   â”œâ”€â”€ config.json            # Model configuration
    â”‚   â””â”€â”€ confusion_matrix.png   # Performance visualization
    â”œâ”€â”€ dataset/                   # Training images âœ…
    â”‚   â”œâ”€â”€ train/                 # 180 training images
    â”‚   â”‚   â”œâ”€â”€ acne/             # 30 images
    â”‚   â”‚   â”œâ”€â”€ eczema/           # 30 images
    â”‚   â”‚   â”œâ”€â”€ melanoma/         # 30 images
    â”‚   â”‚   â”œâ”€â”€ psoriasis/        # 30 images
    â”‚   â”‚   â”œâ”€â”€ rosacea/          # 30 images
    â”‚   â”‚   â””â”€â”€ vitiligo/         # 30 images
    â”‚   â””â”€â”€ validation/            # 60 validation images
    â”‚       â”œâ”€â”€ acne/             # 10 images
    â”‚       â”œâ”€â”€ eczema/           # 10 images
    â”‚       â”œâ”€â”€ melanoma/         # 10 images
    â”‚       â”œâ”€â”€ psoriasis/        # 10 images
    â”‚       â”œâ”€â”€ rosacea/          # 10 images
    â”‚       â””â”€â”€ vitiligo/         # 10 images
    â”œâ”€â”€ train_model_simple.py      # Training script â­ USE THIS
    â”œâ”€â”€ train_model.py             # Legacy TensorFlow trainer
    â”œâ”€â”€ generate_sample_images.py  # Create test images
    â”œâ”€â”€ create_sample_dataset.py   # Setup folder structure
    â””â”€â”€ config.py                  # Model configuration
```

### Key Files

| File | Purpose | Status |
|------|---------|--------|
| `start_backend.bat` | Quick start backend | âœ… Ready |
| `start_frontend.bat` | Quick start frontend | âœ… Ready |
| `app_simple.py` | Flask API (sklearn) | âœ… Working |
| `train_model_simple.py` | Model training | âœ… Working |
| `trained_model/model.pkl` | Saved classifier | âœ… Trained |
| `dataset/` | Training images | âœ… Generated |

## ï¿½ Model Performance

### Current Model Stats

- **Algorithm**: Logistic Regression (sklearn)
- **Feature Extraction**: Color histograms + basic statistics
- **Training Accuracy**: 100.00%
- **Validation Accuracy**: 98.33%
- **Classes**: 6 skin diseases
- **Training Time**: ~10 seconds
- **Prediction Time**: <100ms

### Classification Report

```
              precision    recall  f1-score   support

        acne       1.00      0.90      0.95        10
      eczema       1.00      1.00      1.00        10
    melanoma       1.00      1.00      1.00        10
   psoriasis       1.00      1.00      1.00        10
     rosacea       0.91      1.00      0.95        10
    vitiligo       1.00      1.00      1.00        10

    accuracy                           0.98        60
   macro avg       0.98      0.98      0.98        60
weighted avg       0.98      0.98      0.98        60
```

### âš ï¸ Important Note

**Current model uses SAMPLE/DUMMY images for testing purposes.**

For real medical use, you MUST:
1. Download real skin disease images from medical datasets
2. Replace sample images in `model/dataset/`
3. Retrain the model
4. Validate on real test cases

### Upgrading to PyTorch (Better Accuracy)

Install PyTorch for deep learning features:
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install torch torchvision
```

Then retrain:
```powershell
cd ..\model
python train_model_simple.py
```

**Benefits:**
- Uses ResNet50 pre-trained features
- Much better accuracy on real medical images
- Better generalization

**Trade-offs:**
- Slower training (~2-5 minutes vs 10 seconds)
- Larger model size (~500MB vs 10KB)
- Requires more RAM

## ðŸŽ“ Training Your Own Model

### Current Dataset (Sample Images)

The model is currently trained on **computer-generated test images** (240 total):
- 30 training images per disease
- 10 validation images per disease
- Not suitable for real medical use!

### Training with Real Medical Images

#### Step 1: Get Real Dataset

Download from public medical datasets:
- **HAM10000** (Kaggle): https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000
- **ISIC Archive**: https://www.isic-archive.com/

#### Step 2: Organize Images

```
model/dataset/
â”œâ”€â”€ train/
â”‚   â”œâ”€â”€ acne/          (50-100 images)
â”‚   â”œâ”€â”€ eczema/        (50-100 images)
â”‚   â”œâ”€â”€ melanoma/      (50-100 images)
â”‚   â”œâ”€â”€ psoriasis/     (50-100 images)
â”‚   â”œâ”€â”€ rosacea/       (50-100 images)
â”‚   â””â”€â”€ vitiligo/      (50-100 images)
â””â”€â”€ validation/
    â”œâ”€â”€ acne/          (10-20 images)
    â”œâ”€â”€ eczema/        (10-20 images)
    â”œâ”€â”€ melanoma/      (10-20 images)
    â”œâ”€â”€ psoriasis/     (10-20 images)
    â”œâ”€â”€ rosacea/       (10-20 images)
    â””â”€â”€ vitiligo/      (10-20 images)
```

**Guidelines:**
- JPG or PNG format
- Clear, well-lit images
- Minimum 50 images per disease (more is better!)
- Balance classes (similar number of images per disease)
- Mix of different skin tones, ages, severities

#### Step 3: Train Model

```powershell
cd "C:\Users\pulkit\OneDrive\Desktop\skin disease\model"
& "C:/Users/pulkit/OneDrive/Desktop/skin disease/backend/venv/Scripts/python.exe" train_model_simple.py
```

**Training Process:**
1. Loads images from `dataset/train` and `dataset/validation`
2. Extracts features (color histograms or PyTorch ResNet50)
3. Trains Logistic Regression classifier
4. Evaluates on validation set
5. Saves model to `trained_model/`
6. Generates confusion matrix

**Output Files:**
- `model.pkl` - Trained classifier
- `label_encoder.pkl` - Label encoder
- `class_names.json` - Disease names
- `config.json` - Model configuration
- `confusion_matrix.png` - Performance visualization

#### Step 4: Restart Backend

The backend automatically loads the new model on startup!

```powershell
cd ..\backend
.\venv\Scripts\Activate.ps1
python app_simple.py
```

### Quick Training Commands

**Generate sample images (for testing only):**
```powershell
cd model
python generate_sample_images.py
```

**Create folder structure:**
```powershell
python create_sample_dataset.py
```

**Train model:**
```powershell
python train_model_simple.py
```

## ðŸƒâ€â™‚ï¸ How to Run

### âœ… System is Already Set Up!

Your project is **ready to run**. Just start the servers:

### Method 1: Batch Files (Recommended!)

1. **Start Backend**: Double-click `start_backend.bat`
2. **Start Frontend**: Double-click `start_frontend.bat`  
3. **Access App**: Browser opens at http://localhost:3000

### Method 2: PowerShell Commands

**Terminal 1 - Backend:**
```powershell
cd "C:\Users\pulkit\OneDrive\Desktop\skin disease\backend"
.\venv\Scripts\Activate.ps1
python app_simple.py
```

**Terminal 2 - Frontend:**
```powershell
cd "C:\Users\pulkit\OneDrive\Desktop\skin disease\frontend"
npm start
```

### What You Should See

**Backend Terminal:**
```
âœ… All components loaded successfully!
* Running on http://127.0.0.1:5000
```

**Frontend Terminal:**
```
Compiled successfully!
webpack compiled with 0 warnings
```

**Browser:** Automatically opens to http://localhost:3000

### First Time Setup (If Needed)

If you get errors, install dependencies:

**Backend:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install flask flask-cors pillow scikit-learn numpy matplotlib seaborn pandas
```

**Frontend:**
```powershell
cd frontend
npm install
```

### Testing the App

1. Click **"Check Disease"** in the navigation menu
2. Click **"Choose File"** button
3. Select any image (JPG or PNG)
4. See image preview
5. Click **"Analyze Image"**
6. View prediction results with confidence scores!

### Stopping the Servers

Press **Ctrl + C** in both terminal windows

## âš™ï¸ Configuration

### Backend Configuration (.env)

```env
# SerpAPI Configuration
SERP_API_KEY=your_api_key_here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=1
```

### Frontend Configuration

Create `frontend/.env`:

```env
# Backend API URL
REACT_APP_API_URL=http://localhost:5000/api
```

### SerpAPI Setup

1. Visit https://serpapi.com/
2. Sign up for free account
3. Get your API key
4. Add to `backend/.env`
5. Free tier: 100 searches/month

## ðŸ“¡ API Documentation

### Health Check
```
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "classes_loaded": true,
  "serpapi_configured": true
}
```

### Predict Disease
```
POST /api/predict
```

**Request:**
- Content-Type: multipart/form-data
- Body: 
  - `image`: Image file
  - `use_serpapi`: true/false (optional)

**Response:**
```json
{
  "prediction": "acne",
  "confidence": 0.92,
  "all_predictions": [
    {"disease": "acne", "confidence": 0.92},
    {"disease": "rosacea", "confidence": 0.05}
  ],
  "recommendations": {
    "search_query": "acne skin disease treatment",
    "recommendations": [...]
  },
  "similar_images": {
    "images": [...]
  }
}
```

### Get Classes
```
GET /api/classes
```

**Response:**
```json
{
  "classes": ["acne", "eczema", "melanoma", "psoriasis"],
  "total": 4
}
```

### Search Recommendations
```
POST /api/search-recommendations
```

**Request:**
```json
{
  "disease": "acne"
}
```

## ðŸ”® Future Improvements

### Planned Features
- [ ] User authentication and history
- [ ] Batch image processing
- [ ] Mobile app (React Native)
- [ ] Doctor consultation integration
- [ ] Multi-language support
- [ ] Severity assessment
- [ ] Treatment tracking
- [ ] Community features

### Model Improvements
- [ ] Ensemble models
- [ ] Attention mechanisms
- [ ] Larger datasets
- [ ] Active learning
- [ ] Model explainability (Grad-CAM)

### Technical Enhancements
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Cloud deployment
- [ ] API rate limiting
- [ ] Caching layer
- [ ] Database integration

## ðŸ”§ Troubleshooting

### Backend Issues

**Issue: Model not found**
```
Solution: Train the model first using train_model.py
```

**Issue: TensorFlow installation fails**
```
Solution: 
- Ensure Python 3.8-3.11
- Use: pip install tensorflow==2.15.0
- For GPU: Install CUDA and cuDNN
```

**Issue: SerpAPI not working**
```
Solution:
- Check API key in .env
- Verify API quota
- Check internet connection
```

### Frontend Issues

**Issue: Cannot connect to backend**
```
Solution:
- Ensure backend is running on port 5000
- Check REACT_APP_API_URL in .env
- Disable CORS blocking in browser
```

**Issue: npm install fails**
```
Solution:
- Clear npm cache: npm cache clean --force
- Delete node_modules and package-lock.json
- Run npm install again
```

### Training Issues

**Issue: Out of memory during training**
```
Solution:
- Reduce BATCH_SIZE in config.py
- Reduce IMAGE_SIZE
- Close other applications
```

**Issue: Low accuracy**
```
Solution:
- Collect more training data
- Increase EPOCHS
- Try different BASE_MODEL
- Check data quality
```

## ðŸ“ Important Notes

### Medical Disclaimer

âš ï¸ **This application is for educational and research purposes only.**

- Not a substitute for professional medical diagnosis
- Always consult qualified healthcare providers
- Do not use for critical medical decisions
- Results are probabilistic, not definitive
- Accuracy depends on training data quality

### Data Privacy

- Images are not stored on server
- Processing happens in-memory
- No personal data collected
- SerpAPI searches are anonymous

### Legal Compliance

- Ensure compliance with local healthcare regulations
- Follow data protection laws (GDPR, HIPAA, etc.)
- Obtain proper permissions for medical imaging
- Include appropriate disclaimers

## ðŸ¤ Contributing

Contributions are welcome! Areas for contribution:

1. **Dataset**: Share quality skin disease images
2. **Model**: Improve architecture or training
3. **Features**: Add new functionality
4. **Documentation**: Improve guides
5. **Testing**: Add unit/integration tests
6. **UI/UX**: Enhance user interface

## ðŸ“„ License

This project is licensed under the MIT License.

## ðŸ‘¨â€ðŸ’» Author

Created with â¤ï¸ for educational purposes

## ðŸ™ Acknowledgments

- TensorFlow team for the framework
- Keras for the high-level API
- MobileNetV2 creators for the architecture
- SerpAPI for search integration
- React team for the frontend framework
- Medical image dataset providers

## ðŸ“ž Support

For issues and questions:
1. Check [Troubleshooting](#troubleshooting) section
2. Review closed issues on GitHub
3. Create a new issue with:
   - Error messages
   - System information
   - Steps to reproduce

---

**Remember**: This is a learning tool. Always seek professional medical advice for health concerns.

**Happy Coding! ðŸš€**




