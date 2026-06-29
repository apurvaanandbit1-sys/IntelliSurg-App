import logging
from fastapi import APIRouter, HTTPException

from core.model_manager import model_manager
from core.preprocessing import build_ann_feature_vector
from core.inference import predict_ann as run_ann_inference
from schemas.models import ANNRequest, PatientProfileRequest

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)


@router.post("/ann")
def predict_ann(request: ANNRequest):

    try:

        expected_features = len(model_manager.metadata["ann_features"])

        if len(request.features) != expected_features:
            raise HTTPException(
                status_code=400,
                detail=f"Expected {expected_features} features but got {len(request.features)}"
            )

        risk = run_ann_inference(request.features)

        label = "High Readmission Risk" if risk >= 0.5 else "Low Readmission Risk"

        return {
            "readmission_risk": round(risk, 4),
            "risk_label": label
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"ANN Prediction failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred during ANN prediction."
        )


@router.post("/ann-from-form")
def predict_ann_from_form(request: PatientProfileRequest):

    try:

        expected_features = model_manager.metadata["ann_features"]

        feature_vector = build_ann_feature_vector(
            request.model_dump(),
            expected_features
        )

        risk = run_ann_inference(feature_vector)

        label = "High Readmission Risk" if risk >= 0.5 else "Low Readmission Risk"

        return {
            "readmission_risk": round(risk, 4),
            "risk_label": label,
            "feature_count": len(feature_vector),
            "model_input_ready": True
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"ANN form prediction failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred during ANN form prediction."
        )
