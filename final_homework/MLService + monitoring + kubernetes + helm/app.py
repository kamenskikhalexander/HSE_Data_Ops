from datetime import datetime
import json
import logging
import os

from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest
from sklearn.datasets import load_diabetes
from sklearn.ensemble import RandomForestRegressor
from sqlalchemy import JSON, Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from starlette.responses import Response


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "message": record.getMessage(),
        }
        if hasattr(record, "extra_data"):
            log_record.update(record.extra_data)
        return json.dumps(log_record, ensure_ascii=False)


logger = logging.getLogger("ml_service")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger.handlers.clear()
logger.addHandler(handler)


MODEL_VERSION = "1.0.0"
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/ml_service"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

REQUEST_COUNT = Counter(
    "ml_service_requests_total",
    "Total number of requests to prediction endpoint"
)


class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    inputs = Column(JSON, nullable=False)
    prediction = Column(Float, nullable=False)
    requested_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    model_version = Column(String, nullable=False)


Base.metadata.create_all(bind=engine)


app = FastAPI(title="Basic ML Service")


class PredictRequest(BaseModel):
    age: float
    sex: float
    bmi: float
    bp: float
    s1: float
    s2: float
    s3: float
    s4: float
    s5: float
    s6: float


class PredictResponse(BaseModel):
    predict: float


dataset = load_diabetes()
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(dataset.data, dataset.target)


@app.get("/health")
def health():
    logger.info(
        "health check",
        extra={"extra_data": {"endpoint": "/health", "method": "GET"}}
    )
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/api/v1/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    REQUEST_COUNT.inc()

    features = [[
        request.age,
        request.sex,
        request.bmi,
        request.bp,
        request.s1,
        request.s2,
        request.s3,
        request.s4,
        request.s5,
        request.s6,
    ]]
    prediction = round(float(model.predict(features)[0]), 2)
    request_time = datetime.utcnow()
    inputs = request.model_dump()

    db = SessionLocal()
    try:
        db_log = PredictionLog(
            inputs=inputs,
            prediction=prediction,
            requested_at=request_time,
            model_version=MODEL_VERSION,
        )
        db.add(db_log)
        db.commit()
    finally:
        db.close()

    logger.info(
        "prediction request processed",
        extra={
            "extra_data": {
                "endpoint": "/api/v1/predict",
                "method": "POST",
                "inputs": inputs,
                "predict": prediction,
                "requested_at": request_time.isoformat(),
                "model_version": MODEL_VERSION,
            }
        },
    )

    return PredictResponse(predict=prediction)