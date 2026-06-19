# routers/predict_cnn.py




from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import tempfile
import os

from core.inference import predict_cnn
from core.model_manager import model_manager


router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)


@router.post("/cnn")
async def cnn_predict(file: UploadFile = File(...)):
    temp_path = None

    try:

        suffix = Path(file.filename).suffix
        if suffix.lower() not in {".jpg", ".jpeg", ".png", ".bmp", ".webp"}:
            raise HTTPException(
                status_code=400,
                detail="Unsupported image type. Upload JPG, JPEG, PNG, BMP, or WEBP."
            )

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:

            temp_file.write(await file.read())

            temp_path = temp_file.name

        result = predict_cnn(temp_path)

        return {
            "wound_class": result["class"],
            "wound_confidence": result["confidence"],
            "raw_probs": result["raw_probs"],
            "available_classes": list(model_manager.metadata["cnn_classes"].keys())
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


import time

start = time.time()

# existing prediction code

print("CNN inference took:", time.time() - start)