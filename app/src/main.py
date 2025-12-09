from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict


# 1. Schema Definition (Minimal Strict Guideline Compliance)
# 本来は domain/health/schemas.py などに配置しますが、疎通確認用に定義します
class HealthResponse(BaseModel):
    model_config = ConfigDict(frozen=True)
    status: str
    message: str


# 2. Lifespan Management
# DB接続の確立などは将来的にここに記述します
@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup logic
    print("INFO:     Application startup sequence initiated.")

    yield

    # Shutdown logic
    print("INFO:     Application shutdown sequence initiated.")


# 3. App Definition
app = FastAPI(
    title="Serverless Mock API Generator",
    description="A serverless API to manage and simulate mock endpoints.",
    version="0.1.0",
    lifespan=lifespan,
    # Docs URLは本番では無効化することもありますが開発中は有効にします
    docs_url="/docs",
    redoc_url="/redoc",
)


# 4. Root Endpoint (Health Check)
# AWS Lambda Web Adapterのヘルスチェック用にも機能します
@app.get("/", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(
        status="ok",
        message="Server is running.",
    )
