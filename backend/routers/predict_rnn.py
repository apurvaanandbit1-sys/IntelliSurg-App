from fastapi import APIRouter, HTTPException

from core.preprocessing import parse_signal_payload, validate_signal_187
from schemas.models import RNNRequest
from schemas.models import SignalTextRequest
from core.inference import predict_rnn

router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)


@router.post("/rnn")
def rnn_predict(request: RNNRequest):

    try:

        if len(request.signal) != 187:
            raise HTTPException(
                status_code=400,
                detail="RNN expects exactly 187 ECG values"
            )

        result = predict_rnn(request.signal)

        return result

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.post("/rnn-from-text")
def rnn_predict_from_text(request: SignalTextRequest):

    try:

        signal = parse_signal_payload(request.signal_text)
        signal = validate_signal_187(signal)

        return predict_rnn(signal)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
