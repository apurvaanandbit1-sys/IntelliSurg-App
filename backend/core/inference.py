import numpy as np
from PIL import Image

from core.model_manager import model_manager


# ==================================================
# ANN
# ==================================================

def predict_ann(features_array):

    scaler = model_manager.scalers["ann"]
    model = model_manager.models["ann"]

    x = scaler.transform([features_array])

    pred = model.predict(x, verbose=0)

    return float(pred[0][0])


# ==================================================
# CNN
# ==================================================

def predict_cnn(image_path):

    model = model_manager.models["cnn"]

    img = Image.open(image_path).convert("RGB")
    img = img.resize((224, 224))

    arr = np.array(img) / 255.0
    arr = np.expand_dims(arr, axis=0)

    probs = model.predict(arr, verbose=0)[0]

    idx = int(np.argmax(probs))

    class_map = model_manager.metadata["cnn_classes"]

    idx_to_class = {
        v: k for k, v in class_map.items()
    }

    return {
        "class": idx_to_class[idx],
        "confidence": float(probs[idx]),
        "raw_probs": probs.tolist()
    }


# ==================================================
# RNN
# ==================================================

def predict_rnn(signal_187):

    scaler = model_manager.scalers["rnn"]
    model = model_manager.models["rnn"]

    signal = np.array(signal_187)

    signal = signal.reshape(1, 187)

    signal = scaler.transform(signal)

    signal = signal.reshape(1, 187, 1)

    probs = model.predict(signal, verbose=0)[0]

    ecg_classes = {
    0: "Normal",
    1: "Supraventricular",
    2: "Ventricular",
    3: "Fusion Beat",
    4: "Unknown"
    }

    idx = int(np.argmax(probs))

    return {
        "class_index": idx,
        "class_name": ecg_classes.get(idx, "Unknown"),
        "confidence": float(np.max(probs)),
        "raw_probs": probs.tolist()
    }


# ==================================================
# FUSION
# ==================================================

def predict_fusion(
    ann_score,
    cnn_score,
    rnn_score
):

    fusion_model = model_manager.models["fusion"]

    x = np.array([
        [
            ann_score,
            cnn_score,
            rnn_score
        ]
    ])

    result = fusion_model.predict(
        x,
        verbose=0
    )

    return float(result[0][0])