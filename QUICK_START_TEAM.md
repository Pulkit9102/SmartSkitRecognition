# 🚀 Quick Start for Team Members

## First Time Setup (5 Minutes)

### 1. Install Requirements
```powershell
# Install Python dependencies
cd "skin disease\backend"
pip install -r requirements.txt
```

### 2. Get the Google Drive Link
Ask your team lead for the Google Drive dataset link. It looks like:
```
https://drive.google.com/file/d/1a2b3c4d5e6f7g8h9i0j/view?usp=sharing
```

### 3. Download Dataset
```powershell
cd ..\model
python gdrive_dataset_manager.py
```

├── sync_and_train.bat                ← One-click workflow
This quick-start file previously provided fast onboarding for a Google Drive
based team workflow. The team collaboration features have been removed.

Use `HOW_TO_RUN.md` for standard local setup instructions and place your
dataset under `model/dataset/`.

If you'd like a compact quick-start card recreated (without Google Drive),
I can generate one that covers only local dataset, training, and running
the app.
```powershell
