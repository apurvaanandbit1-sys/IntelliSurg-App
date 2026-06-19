# IntelliSurg Demo Run Guide

This project is now structured as a functional demo:

- `backend/` serves the ANN, CNN, RNN, and fusion inference APIs
- `frontend/` contains the Streamlit demo UI
- the UI talks to the backend at `http://127.0.0.1:8000`

## 1. Fix Python First

The backend depends on `tensorflow==2.16.1`, which should be run with Python 3.11.

Expected Python path used by the launcher:

```powershell
C:\Users\apurv\AppData\Local\Programs\Python\Python311\python.exe
```

If that path is missing or not executable, reinstall Python 3.11 first.

Recommended installer settings:

1. Install Python 3.11.x
2. Enable `Add python.exe to PATH`
3. Keep `pip` enabled
4. Install for your user

## 2. Start The Backend

From PowerShell:

```powershell
cd C:\Users\apurv\OneDrive\Desktop\IntelliSurg\IntelliSurg-App\backend
.\start_backend.ps1
```

What this script does:

1. checks for Python 3.11
2. creates a fresh virtual environment in `backend\.venv311`
3. installs all requirements
4. starts FastAPI with Uvicorn on port `8000`

Backend test URLs:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/docs`

## 3. Start The Frontend

Open a second PowerShell window:

```powershell
cd C:\Users\apurv\OneDrive\Desktop\IntelliSurg\IntelliSurg-App\frontend
.\start_frontend.ps1
```

What this script does:

1. reuses the backend virtual environment
2. launches Streamlit
3. opens the demo at `http://localhost:8501`

## 4. Demo Workflow

Use the frontend tabs in this order:

1. `ANN Risk`
   - Enter structured patient fields
   - Click `Run ANN Prediction`

2. `ECG RNN`
   - Paste one preprocessed `187`-value ECG beat
   - Click `Run RNN Prediction`

3. `Wound CNN`
   - Upload a wound image
   - Click `Run CNN Prediction`

4. `Fusion Demo`
   - Enter patient profile
   - Paste the ECG beat
   - Upload the wound image
   - Click `Run Fusion Demo`

## 5. Important Demo Note

This is a demo project for resume/interview use.

- ANN is trained on tabular diabetes readmission data
- RNN expects a preprocessed 187-point ECG beat
- CNN predicts wound severity classes
- fusion output is experimental and should be described as demo-only

## 6. If Something Breaks

Common checks:

1. Make sure backend is running before frontend
2. Open `http://127.0.0.1:8000/docs`
3. Confirm the frontend sidebar backend URL is `http://127.0.0.1:8000`
4. If installs fail, delete `backend\.venv311` and rerun `start_backend.ps1`

## 7. Good Interview Framing

Describe it like this:

`A multimodal healthcare AI demo integrating ANN, CNN, and BiLSTM/RNN models with a FastAPI backend, Streamlit frontend, preprocessing pipeline, model orchestration, and an experimental fusion-based triage view.`
