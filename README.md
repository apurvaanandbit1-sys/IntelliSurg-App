# 🏥 IntelliSurg

> **AI-powered Post-operative Patient Monitoring System**

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 📖 Overview

IntelliSurg is an AI-powered clinical decision support prototype that assists in post-operative patient monitoring by combining multiple deep learning models into a single dashboard.

The application predicts:

- 🧠 Readmission Risk (ANN)
- ❤️ ECG Beat Classification (RNN)
- 🩹 Wound Infection Detection (CNN)
- 📊 Overall Criticality Score (Fusion Model)

The project demonstrates how multiple AI models can be integrated into a unified healthcare monitoring system.

---

# Screenshots

## ANN Readmission Prediction

![ANN](screenshots/ann.png)

---

## ECG Beat Classification

![RNN](screenshots/rnn.png)

---

## Wound Classification

![CNN](screenshots/cnn.png)

---

## Fusion Dashboard

![Fusion](screenshots/fusion.png)

---

# Features

- Modern Streamlit dashboard
- FastAPI backend
- Interactive ECG waveform visualization
- Readmission risk estimation
- ECG beat classification
- Wound infection classification
- Fusion-based patient criticality scoring
- Dark clinical UI

---

# Tech Stack

### Frontend

- Streamlit
- Plotly

### Backend

- FastAPI
- Uvicorn

### AI Models

- Artificial Neural Network (ANN)
- Recurrent Neural Network (RNN)
- Convolutional Neural Network (CNN)

### Languages

- Python

---

# Project Structure

```
IntelliSurg-App
│
├── backend
│   ├── core
│   ├── metadata
│   ├── models
│   ├── routers
│   ├── scalers
│   └── schemas
│
├── frontend
│   ├── app.py
│   └── theme.py
│
├── screenshots
│
└── README.md
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/apurvaanandbit1-sys/IntelliSurg-App.git
```

Install backend dependencies

```bash
pip install -r backend/requirements.txt
```

Start backend

```bash
cd backend
.\start_backend.ps1
```

Start frontend

```bash
cd frontend
.\start_frontend.ps1
```

---

# Future Improvements

- Patient authentication
- Database integration
- Real-time ECG streaming
- Explainable AI visualizations
- Electronic Health Record integration
- Cloud deployment
- Doctor dashboard
- PDF report generation

---

# Disclaimer

This project is intended for educational and research purposes only.

It is **not** intended for clinical diagnosis or real-world medical decision making.

---

# Author

**Apurv Anand**

B.Tech Computer Science Engineering

BIT Mesra

GitHub:
https://github.com/apurvaanandbit1-sys

---

⭐ If you found this project interesting, consider giving it a star.
