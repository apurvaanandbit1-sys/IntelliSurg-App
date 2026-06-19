from fastapi import APIRouter

from core.model_manager import model_manager

router = APIRouter(tags=["Health"])


@router.get("/health")
def health():

    return {
        "ann_loaded": "ann" in model_manager.models,
        "cnn_loaded": "cnn" in model_manager.models,
        "rnn_loaded": "rnn" in model_manager.models,
        "fusion_loaded": "fusion" in model_manager.models,
    }


@router.get("/models")
def models():

    return {
        "loaded_models": list(
            model_manager.models.keys()
        )
    }


@router.get("/metadata/ann-fields")
def ann_fields():

    return {
        "expected_feature_count": len(model_manager.metadata.get("ann_features", [])),
        "feature_columns": model_manager.metadata.get("ann_features", [])
    }


@router.get("/metadata/cnn-classes")
def cnn_classes():

    return {
        "classes": list(model_manager.metadata.get("cnn_classes", {}).keys())
    }
