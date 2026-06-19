from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers.health import router as health_router
from core.model_manager import model_manager

from routers.predict_ann import router as ann_router
from routers.predict_rnn import router as rnn_router
from routers.predict_cnn import router as cnn_router
from routers import predict_fusion


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("\n===================================")
    print("Starting IntelliSurg Backend...")
    print("===================================\n")

    model_manager.load_all()

    print("\n===================================")
    print("All assets loaded successfully.")
    print("===================================\n")

    yield

    print("\nShutting down IntelliSurg Backend...\n")


app = FastAPI(
    title="IntelliSurg API",
    version="1.0.0",
    lifespan=lifespan
)
app.include_router(
    health_router
)
app.include_router(
    ann_router
)
app.include_router(
    rnn_router
)
app.include_router(
    cnn_router
)
app.include_router(
    predict_fusion.router
)
@app.get("/")
def root():

    return {
        "message": "IntelliSurg API Running",
        "version": "1.0.0"
    }