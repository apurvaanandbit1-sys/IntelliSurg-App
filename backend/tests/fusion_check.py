from tensorflow.keras.models import load_model

model = load_model(
    "models/fusion_model.h5",
    compile=False
)

print("INPUT SHAPE:")
print(model.input_shape)

print("\nOUTPUT SHAPE:")
print(model.output_shape)

print("\nSUMMARY:")
model.summary()