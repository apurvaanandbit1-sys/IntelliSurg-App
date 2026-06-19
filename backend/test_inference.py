from core.model_manager import model_manager
from core.preprocessing import build_ann_feature_vector

model_manager.load_all()

feature_vector = build_ann_feature_vector(
    {},
    model_manager.metadata["ann_features"]
)

print("Inference module imported successfully")
print("Demo ANN vector prepared:", len(feature_vector))
