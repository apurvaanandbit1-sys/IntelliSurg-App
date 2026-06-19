from pathlib import Path
import tensorflow as tf
import joblib
import json


class ModelManager:
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.metadata = {}

    def load_all(self):

        base_dir = Path(__file__).resolve().parent.parent

        # ======================
        # MODELS
        # ======================

        self.models["ann"] = tf.keras.models.load_model(
            base_dir / "models" / "ann_tabular.h5",
            compile=False
        )

        self.models["cnn"] = tf.keras.models.load_model(
            base_dir / "models" / "cnn_wound.h5",
            compile=False
        )

        self.models["rnn"] = tf.keras.models.load_model(
            base_dir / "models" / "rnn_best.h5",
            compile=False
        )

        self.models["fusion"] = tf.keras.models.load_model(
            base_dir / "models" / "fusion_model.h5",
            compile=False
        )

        # ======================
        # SCALERS
        # ======================

        self.scalers["ann"] = joblib.load(
            base_dir / "scalers" / "ann_scaler.pkl"
        )

        self.scalers["rnn"] = joblib.load(
            base_dir / "scalers" / "rnn_scaler.pkl"
        )

        # ======================
        # METADATA
        # ======================

        with open(
            base_dir / "metadata" / "ann_feature_columns.json",
            "r"
        ) as f:
            self.metadata["ann_features"] = json.load(f)

        with open(
            base_dir / "metadata" / "cnn_class_indices.json",
            "r"
        ) as f:
            self.metadata["cnn_classes"] = json.load(f)

    def status(self):
        return {
            "ann_loaded": "ann" in self.models,
            "cnn_loaded": "cnn" in self.models,
            "rnn_loaded": "rnn" in self.models,
            "fusion_loaded": "fusion" in self.models,
        }


model_manager = ModelManager()