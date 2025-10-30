# 🚀 How to Run - Step by Step Instructions

Complete guide to run the AI Skin Disease Recognition System.

---

## ⚡ Quick Start (Recommended)

### Option 1: Using Batch Files (Easiest!)

1. **Start Backend**: Double-click `start_backend.bat`
2. **Start Frontend**: Double-click `start_frontend.bat`
3. **Open Browser**: Automatically opens at http://localhost:3000

### Option 2: Using PowerShell

**Terminal 1 - Start Backend:**
```powershell
cd "C:\Users\pulkit\OneDrive\Desktop\skin disease\backend"
.\venv\Scripts\Activate.ps1
python app_simple.py
```

**Terminal 2 - Start Frontend (New Terminal):**
```powershell
cd "C:\Users\pulkit\OneDrive\Desktop\skin disease\frontend"
npm start
```

---

## 📋 First Time Setup

### Backend Setup (One-Time Only)

```powershell
# Navigate to backend
cd "C:\Users\pulkit\OneDrive\Desktop\skin disease\backend"

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install flask flask-cors pillow scikit-learn numpy matplotlib seaborn pandas
```

### Frontend Setup (One-Time Only)

```powershell
# Navigate to frontend
cd "C:\Users\pulkit\OneDrive\Desktop\skin disease\frontend"

# Install dependencies
npm install
```

---

## ✅ Verification

### Check Backend is Running

You should see in Terminal 1:
```
============================================================
  SIMPLE SKIN DISEASE CLASSIFICATION API
============================================================

🔄 Loading model components...
✓ Loaded config: simple feature extractor
✓ Model loaded successfully!
✓ Label encoder loaded!
✓ Class names loaded: acne, eczema, melanoma, psoriasis, rosacea, vitiligo
✓ Using simple feature extractor
✅ All components loaded successfully!

Starting Flask server on http://localhost:5000
============================================================
 * Serving Flask app 'app_simple'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

**Test Backend:**
Open http://localhost:5000/api/health in browser

Should show:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "classes_loaded": true,
  "num_classes": 6
}
```

### Check Frontend is Running

You should see in Terminal 2:
```
Compiled successfully!

You can now view frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://172.16.17.137:3000
```

**Browser automatically opens to http://localhost:3000**

---

## 🎨 Using the Application

### 1. Navigation
The app has 5 pages accessible from the top menu:
- **Home** - Landing page with features
- **Check Disease** - Upload and analyze images
- **Common Diseases** - Educational content about 6 skin diseases
- **Precautions** - Health tips and preventive care
- **About** - Information about the portal

### 2. Testing Disease Detection

1. Click **"Check Disease"** in the navigation menu
2. Click the **"Choose File"** button
3. Select any image file (JPG, PNG, BMP)
4. You'll see an image preview
5. Click **"Analyze Image"** button
6. Wait 1-2 seconds for results

**Results Display:**
- Disease name (e.g., "Acne", "Melanoma")
- Confidence percentage (e.g., 92%)
- Top 5 predictions with confidence scores

---

## 🛑 Stopping the Application

1. Go to **Terminal 1** (Backend)
   - Press **Ctrl + C**

2. Go to **Terminal 2** (Frontend)
   - Press **Ctrl + C**
   - Type **Y** and press Enter if asked

---

## 🔧 Troubleshooting

### Backend Issues

#### Error: "Model not found"
**Solution:**
```powershell
cd "C:\Users\pulkit\OneDrive\Desktop\skin disease\model"
& "C:/Users/pulkit/OneDrive/Desktop/skin disease/backend/venv/Scripts/python.exe" train_model_simple.py
```

#### Error: "No module named 'flask'"
**Solution:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install flask flask-cors pillow scikit-learn numpy matplotlib seaborn pandas
```

#### Error: "Port 5000 already in use"
**Solution:** Kill the existing process or change port in `backend/app_simple.py`:
```python
# At the bottom of app_simple.py, change:
app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5000 to 5001
```

### Frontend Issues

#### Error: "npm not found"
**Solution:** Install Node.js from https://nodejs.org/

#### Error: Missing dependencies
**Solution:**
```powershell
cd frontend
npm install
```

#### Error: "Port 3000 already in use"
**Solution:** When prompted, press **Y** to use a different port (usually 3001)

#### Error: Blank page or build errors
**Solution:**
```powershell
cd frontend
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
npm install
npm start
```

### Connection Issues

#### Image upload not working
**Check:**
1. Backend is running (http://localhost:5000/api/health should work)
2. No CORS errors in browser console (Press F12 → Console tab)
3. Both backend and frontend are running

#### Prediction returns error
**Check:**
1. Model files exist in `model/trained_model/`
   - model.pkl
   - label_encoder.pkl
   - class_names.json
   - config.json

2. If missing, retrain:
```powershell
cd model
python train_model_simple.py
```

---

## 🎓 Training Your Own Model

### Current Model Status
- ⚠️ Trained on **computer-generated sample images** (for testing only)
- ✅ Works for demonstration
- ❌ **NOT suitable for real medical diagnosis**

### To Train with Real Medical Images

#### Step 1: Download Real Dataset
Get medical images from:
- **Kaggle HAM10000**: https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000
- **ISIC Archive**: https://www.isic-archive.com/

#### Step 2: Organize Images
Place images in this structure:
```
model/dataset/
├── train/
│   ├── acne/          (50-100 images)
│   ├── eczema/        (50-100 images)
│   ├── melanoma/      (50-100 images)
│   ├── psoriasis/     (50-100 images)
│   ├── rosacea/       (50-100 images)
│   └── vitiligo/      (50-100 images)
└── validation/
    ├── acne/          (10-20 images)
    ├── eczema/        (10-20 images)
    ├── melanoma/      (10-20 images)
    ├── psoriasis/     (10-20 images)
    ├── rosacea/       (10-20 images)
    └── vitiligo/      (10-20 images)
```

**Image Requirements:**
- Format: JPG or PNG
- Minimum: 50 images per disease for training, 10 for validation
- Quality: Clear, well-lit images
- Balance: Similar number of images per disease

#### Step 3: Train Model
```powershell
cd "C:\Users\pulkit\OneDrive\Desktop\skin disease\model"
& "C:/Users/pulkit/OneDrive/Desktop/skin disease/backend/venv/Scripts/python.exe" train_model_simple.py
```

**Training takes about 10-30 seconds**

Output files saved to `model/trained_model/`:
- `model.pkl` - Trained classifier
- `label_encoder.pkl` - Label encoder
- `class_names.json` - Disease names
- `config.json` - Model configuration
- `confusion_matrix.png` - Performance chart

#### Step 4: Restart Backend
The backend automatically loads the new model on startup.

```powershell
# Stop current backend (Ctrl+C in backend terminal)
# Then restart:
cd backend
.\venv\Scripts\Activate.ps1
python app_simple.py
```

---

## 💡 Upgrade to PyTorch (Better Accuracy)

For improved accuracy using deep learning features:

### Install PyTorch
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install torch torchvision
```

### Retrain Model
```powershell
cd ..\model
python train_model_simple.py
```

The script automatically detects PyTorch and uses ResNet50 features!

**Benefits:**
- 🎯 Much better accuracy on real medical images
- 🧠 Deep learning features instead of simple color histograms
- 📈 Better generalization

**Trade-offs:**
- ⏱️ Slower training (2-5 minutes vs 10 seconds)
- 💾 Larger download (~500MB for ResNet50)
- 🔋 More RAM required

---

## 📊 API Endpoints Reference

### 1. Health Check
```http
GET http://localhost:5000/api/health
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "classes_loaded": true,
  "num_classes": 6,
  "feature_extractor": "simple"
}
```

### 2. Predict Disease
```http
POST http://localhost:5000/api/predict
Content-Type: multipart/form-data
Body: image=<file>
```

**Response:**
```json
{
  "prediction": "melanoma",
  "confidence": 0.85,
  "all_predictions": [
    {"disease": "melanoma", "confidence": 0.85},
    {"disease": "acne", "confidence": 0.08},
    {"disease": "eczema", "confidence": 0.04},
    {"disease": "psoriasis", "confidence": 0.02},
    {"disease": "rosacea", "confidence": 0.01}
  ],
  "model_type": "simple"
}
```

### 3. Get Disease Classes
```http
GET http://localhost:5000/api/classes
```

**Response:**
```json
{
  "classes": ["acne", "eczema", "melanoma", "psoriasis", "rosacea", "vitiligo"],
  "total": 6
}
```

---

## 🔄 Restarting the Application

Every time you want to use the app:

### Using Batch Files (Easiest)
1. Double-click `start_backend.bat`
2. Double-click `start_frontend.bat`

### Using PowerShell
```powershell
# Terminal 1
cd "C:\Users\pulkit\OneDrive\Desktop\skin disease\backend"
.\venv\Scripts\Activate.ps1
python app_simple.py

# Terminal 2
cd "C:\Users\pulkit\OneDrive\Desktop\skin disease\frontend"
npm start
```

---

## ⚠️ Important Notes

### Medical Disclaimer
- ❌ This is NOT a medical diagnostic tool
- ❌ NOT approved for clinical use
- ❌ NOT a substitute for professional medical advice
- ✅ For educational and demonstration purposes only
- ✅ Always consult qualified healthcare providers

### Current Model Status
- Currently trained on **sample/dummy images** for testing
- For real medical use, MUST retrain with actual medical images
- Accuracy depends entirely on training data quality

### Data Privacy
- Images are processed in-memory only
- No images are stored on the server
- No personal data is collected
- Processing is local to your machine

---

## 📞 Quick Reference

| Action | Command |
|--------|---------|
| Start Backend | Double-click `start_backend.bat` OR `cd backend; .\venv\Scripts\Activate.ps1; python app_simple.py` |
| Start Frontend | Double-click `start_frontend.bat` OR `cd frontend; npm start` |
| Stop Servers | Press **Ctrl + C** in both terminals |
| Check Backend Health | Open http://localhost:5000/api/health |
| Train Model | `cd model; python train_model_simple.py` |
| Install Backend Deps | `cd backend; .\venv\Scripts\Activate.ps1; pip install flask flask-cors scikit-learn pillow numpy matplotlib seaborn` |
| Install Frontend Deps | `cd frontend; npm install` |

---

## ✅ Success Checklist

Before using the app, verify:

- [ ] Backend terminal shows "✅ All components loaded successfully!"
- [ ] Backend running on http://localhost:5000
- [ ] Frontend terminal shows "Compiled successfully!"
- [ ] Frontend running on http://localhost:3000
- [ ] Browser opens automatically
- [ ] Can navigate between all 5 pages
- [ ] Can upload an image on Check Disease page
- [ ] Can see prediction results

---

## 🎯 Next Steps

1. **Test the app** - Upload some images and see predictions
2. **Download real medical images** - From Kaggle HAM10000 or ISIC
3. **Organize images** - Into the dataset folder structure
4. **Retrain model** - With real medical data
5. **Optional: Install PyTorch** - For better accuracy

---

**Everything is ready to use! Start the servers and enjoy! 🚀**

*For complete project information, see [README.md](README.md)*
