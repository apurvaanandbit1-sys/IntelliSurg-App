import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers.health import router as health_router
from core.model_manager import model_manager

from routers.predict_ann import router as ann_router
from routers.predict_rnn import router as rnn_router
from routers.predict_cnn import router as cnn_router
from routers import predict_fusion

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Starting IntelliSurg Backend...")

    model_manager.load_all()

    logger.info("All assets loaded successfully.")

    yield

    logger.info("Shutting down IntelliSurg Backend...")


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