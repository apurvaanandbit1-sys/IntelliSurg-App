from fastapi import APIRouter, HTTPException

from core.model_manager import model_manager
from core.preprocessing import build_ann_feature_vector
from schemas.models import ANNRequest, PatientProfileRequest

router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)


@router.post("/ann")
def predict_ann(request: ANNRequest):

    try:

        model = model_manager.models["ann"]
        scaler = model_manager.scalers["ann"]

        expected_features = len(
            model_manager.metadata["ann_features"]
        )

        if len(request.features) != expected_features:
            raise HTTPException(
                status_code=400,
                detail=f"Expected {expected_features} features but got {len(request.features)}"
            )

        X = scaler.transform(
            [request.features]
        )

        risk = float(
            model.predict(
                X,
                verbose=0
            )[0][0]
        )

        label = (
            "High Readmission Risk"
            if risk >= 0.5
            else "Low Readmission Risk"
        )

        return {
            "readmission_risk": round(risk, 4),
            "risk_label": label
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.post("/ann-from-form")
def predict_ann_from_form(request: PatientProfileRequest):

    try:

        model = model_manager.models["ann"]
        scaler = model_manager.scalers["ann"]
        expected_features = model_manager.metadata["ann_features"]

        feature_vector = build_ann_feature_vector(
            request.model_dump(),
            expected_features
        )

        X = scaler.transform([feature_vector])

        risk = float(
            model.predict(
                X,
                verbose=0
            )[0][0]
        )

        label = (
            "High Readmission Risk"
            if risk >= 0.5
            else "Low Readmission Risk"
        )

        return {
            "readmission_risk": round(risk, 4),
            "risk_label": label,
            "feature_count": len(feature_vector),
            "model_input_ready": True
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
