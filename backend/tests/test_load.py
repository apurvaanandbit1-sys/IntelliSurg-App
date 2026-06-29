from core.model_manager import model_manager
from core.preprocessing import build_ann_feature_vector, parse_signal_payload, validate_signal_187

model_manager.load_all()

print(model_manager.status())

feature_vector = build_ann_feature_vector(
    {},
    model_manager.metadata["ann_features"]
)

print("ANN feature count:", len(feature_vector))
print("ANN expected count:", len(model_manager.metadata["ann_features"]))

signal = validate_signal_187(
    parse_signal_payload(",".join(["0"] * 187))
)
print("Validated ECG signal length:", len(signal))
