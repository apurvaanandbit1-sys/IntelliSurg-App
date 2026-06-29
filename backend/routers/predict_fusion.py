import json
import os
import tempfile
import logging
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import ValidationError

from core.inference import predict_ann, predict_cnn, predict_fusion, predict_rnn
from core.model_manager import model_manager
from core.preprocessing import build_ann_feature_vector, parse_signal_payload, validate_signal_187
from schemas.models import PatientProfileRequest

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/predict",
    tags=["Prediction"],
)


@router.post("/fusion")
async def fusion_predict(
    patient_profile: str = Form(...),
    signal: str = Form(...),
    file: UploadFile = File(...),
):
    temp_path = None

    try:
        profile_data = json.loads(patient_profile)
        if not isinstance(profile_data, dict):
            raise HTTPException(
                status_code=400,
                detail="patient_profile must be a JSON object.",
            )

        try:
            validated_profile = PatientProfileRequest(**profile_data)
            profile_dict = validated_profile.model_dump()
        except ValidationError as e:
            raise HTTPException(
                status_code=422,
                detail=e.errors(),
            )

        feature_vector = build_ann_feature_vector(
            profile_dict,
            model_manager.metadata["ann_features"],
        )

        parsed_signal = parse_signal_payload(signal)
        parsed_signal = validate_signal_187(parsed_signal)

        suffix = Path(file.filename).suffix
        if suffix.lower() not in {".jpg", ".jpeg", ".png", ".bmp", ".webp"}:
            raise HTTPException(
                status_code=400,
                detail="Unsupported image type. Upload JPG, JPEG, PNG, BMP, or WEBP.",
            )

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(await file.read())
            temp_path = temp_file.name

        ann_score = predict_ann(feature_vector)
        rnn_result = predict_rnn(parsed_signal)
        cnn_result = predict_cnn(temp_path)

        criticality = predict_fusion(
            ann_score,
            cnn_result["confidence"],
            rnn_result["confidence"],
        )

        if criticality >= 0.75:
            triage = "HIGH"
        elif criticality >= 0.40:
            triage = "MEDIUM"
        else:
            triage = "LOW"

        return {
            "readmission_risk": ann_score,
            "wound_class": cnn_result["class"],
            "wound_confidence": cnn_result["confidence"],
            "ecg_class": rnn_result["class_name"],
            "ecg_confidence": rnn_result["confidence"],
            "criticality_index": criticality,
            "triage_level": triage,
            "feature_count": len(feature_vector),
            "signal_length": len(parsed_signal),
            "fusion_note": "Experimental combined score for demo purposes only.",
            "clinical_use": False,
        }

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400,
            detail="patient_profile must be valid JSON.",
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Fusion prediction failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred during fusion prediction.",
        )

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
