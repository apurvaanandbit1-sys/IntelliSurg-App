# 🏥 IntelliSurg

<div align="center">

### AI-Powered Post-operative Patient Monitoring System

*A multi-model healthcare AI prototype integrating ANN, RNN, CNN and Fusion AI into a unified clinical dashboard.*

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge\&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge\&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge\&logo=streamlit)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge\&logo=tensorflow)
![GitHub](https://img.shields.io/github/stars/apurvaanandbit1-sys/IntelliSurg-App?style=for-the-badge)

</div>

---

# 📖 Overview

IntelliSurg is an AI-powered clinical decision support prototype designed to demonstrate how multiple machine learning models can work together to assist in post-operative patient monitoring.

The system combines structured clinical data, ECG signals and wound images into a single dashboard capable of generating an overall patient assessment.

This project was developed as an educational demonstration of applied AI in healthcare.

---

# ✨ Features

### 🧠 ANN — Readmission Risk Prediction

* Predicts post-operative readmission risk
* Interactive probability visualization
* Clinical feature input form

---

### ❤️ RNN — ECG Beat Classification

* 187-point ECG signal classification
* Interactive ECG waveform visualization
* Beat probability distribution
* Confidence estimation

---

### 🩹 CNN — Wound Infection Detection

* Medical wound image classification
* Image upload interface
* Infection confidence prediction

---

### 📊 Fusion AI Dashboard

Combines outputs from all models to generate

* Overall patient criticality score
* Risk badge
* ANN summary
* ECG summary
* Wound assessment

---

# 📸 Screenshots

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

# 🏗 System Architecture

```text
               Patient Data
                     │
     ┌───────────────┼───────────────┐
     │               │               │
 Clinical Data     ECG Signal     Wound Image
     │               │               │
     ▼               ▼               ▼
    ANN             RNN             CNN
     │               │               │
     └───────────────┼───────────────┘
                     ▼
              Fusion AI Engine
                     ▼
          Clinical Dashboard (Streamlit)
```

---

# ⚙️ Tech Stack

## Frontend

* Streamlit
* Plotly

## Backend

* FastAPI
* Uvicorn

## Machine Learning

* TensorFlow / Keras
* Artificial Neural Networks (ANN)
* Recurrent Neural Networks (RNN)
* Convolutional Neural Networks (CNN)

## Languages

* Python

---

# 📂 Project Structure

```text
IntelliSurg-App
│
├── backend
│   ├── core
│   ├── metadata
│   ├── models
│   ├── routers
│   ├── scalers
│   ├── schemas
│   └── requirements.txt
│
├── frontend
│   ├── app.py
│   ├── theme.py
│   └── start_frontend.ps1
│
├── screenshots
│   ├── ann.png
│   ├── rnn.png
│   ├── cnn.png
│   └── fusion.png
│
└── README.md
```

---

# 🚀 Getting Started

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

Open

```
http://localhost:8501
```

---

# 🎯 Future Improvements

* User authentication
* Patient database integration
* Real-time ECG streaming
* Explainable AI visualizations
* Electronic Health Record integration
* PDF report generation
* Cloud deployment
* Docker support
* CI/CD pipeline

---

# ⚠️ Disclaimer

This project was developed for educational, research and portfolio purposes.

It is **not intended for clinical diagnosis or real-world medical decision-making.**

---

# 👨‍💻 Author

### Apurv Anand

B.Tech Computer Science Engineering

Birla Institute of Technology, Mesra

GitHub:

https://github.com/apurvaanandbit1-sys

---

<div align="center">

### ⭐ If you found this project interesting, consider giving it a star.

</div>
