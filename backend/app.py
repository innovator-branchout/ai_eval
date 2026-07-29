#!/usr/bin/env python3
"""
AI Evaluation System - Backend API

This FastAPI application serves as the backend for our AI evaluation system,
providing endpoints to interact with models, datasets, and predictions.
"""

import os
from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
from typing import Optional
from dataclasses import asdict

# Import backend modules
from scripts.predict_utils import predict_prompt, predict_prompt_with_response
from scripts.nn.layers import EmbeddingClassifier
from scripts.database import (
    connect,
    list_categories,
    list_models,
    list_labels,
    get_prompts,
    prompts_by_category,
    prompts_by_model,
    search_prompts,
)

app = FastAPI(
    title="AI Evaluation System API",
    description="API for the AI evaluation system with prediction capabilities",
    version="1.0.0"
)

# Add CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,  
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model instances for efficiency
prompt_model = None
response_model = None

# API router - FIXED: Added the required /api prefix back
api = APIRouter(prefix="/api")

def resolve_path(relative_path: str) -> str:
    """Helper to handle pathing variations between local machines and Render's root directory"""
    # If already running inside backend directory, strip the leading 'backend/' component
    if os.path.basename(os.getcwd()) == "backend" and relative_path.startswith("backend/"):
        return relative_path.replace("backend/", "", 1)
    return relative_path

def load_models():
    """Load prediction models once at startup"""
    global prompt_model, response_model

    if prompt_model is None:
        try:
            prompt_model = EmbeddingClassifier(
                input_size=1024,
                num_rubric_classes=19,
                dropout=0.2
            )
            # FIXED: Dynamically resolved path
            model_path = resolve_path('backend/models/prompt_predictor/best.pt')
            checkpoint = torch.load(model_path, map_location=torch.device('cpu'), weights_only=True)
            prompt_model.load_state_dict(checkpoint['model_state'])
            prompt_model.eval()
            print("Prompt model loaded successfully")
        except Exception as e:
            print(f"Error loading prompt model: {e}")
            raise

    if response_model is None:
        try:
            response_model = EmbeddingClassifier(
                input_size=1024,
                num_rubric_classes=19,
                dropout=0.2
            )
            # FIXED: Dynamically resolved path
            model_path = resolve_path('backend/models/response_grader/best.pt')
            checkpoint = torch.load(model_path, map_location=torch.device('cpu'), weights_only=True)
            response_model.load_state_dict(checkpoint['model_state'])
            response_model.eval()
            print("Response model loaded successfully")
        except Exception as e:
            print(f"Error loading response model: {e}")
            raise

# Data models for API requests and responses
class PredictionRequest(BaseModel):
    prompt: str
    response: Optional[str] = None
    model_type: str = "auto"

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    model_used: str

class PromptData(BaseModel):
    prompt_id: int
    category_id: int
    model_id: int
    conversation_id: int
    prompt_number: int
    prompt_text: str
    raw_output: Optional[str] = None
    label_id: Optional[int] = None
    source: Optional[str] = None
    notes: Optional[str] = None

class Category(BaseModel):
    category_id: int
    category_name: str
    description: Optional[str] = None

class Model(BaseModel):
    model_id: int
    model_name: str
    provider: Optional[str] = None
    model_version: Optional[str] = None
    notes: Optional[str] = None

class Label(BaseModel):
    label_id: int
    label_name: str
    status: bool
    severity: int
    description: Optional[str] = None

# API Routes
@api.get("/")
async def root():
    return {
        "message": "AI Evaluation System API",
        "version": "1.0.0",
        "endpoints": [
            "/api/predict",
            "/api/prompts",
            "/api/categories",
            "/api/models",
            "/api/labels",
            "/api/health"
        ]
    }

@api.post("/predict")
async def predict_endpoint(request: PredictionRequest):
    """Make a prediction for a prompt and/or response"""
    try:
        load_models()

        if request.model_type == "auto":
            model_to_use = "response" if request.response else "prompt"
        else:
            model_to_use = request.model_type

        if model_to_use == "prompt":
            result = predict_prompt(prompt_model, request.prompt)
        elif model_to_use == "response":
            if not request.response:
                raise HTTPException(status_code=400, detail="Response is required for response prediction")
            result = predict_prompt_with_response(response_model, request.prompt, request.response)
        else:
            raise HTTPException(status_code=400, detail="Invalid model type. Use 'prompt', 'response', or 'auto'")

        return PredictionResponse(
            prediction=str(result['prediction']),
            confidence=float(result['confidence']),
            model_used=model_to_use
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@api.get("/prompts")
async def get_prompts_endpoint():
    try:
        prompts = get_prompts()
        return [PromptData(**asdict(prompt)) for prompt in prompts]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving prompts: {str(e)}")

@api.get("/prompts/category/{category_name}")
async def get_prompts_by_category_endpoint(category_name: str):
    try:
        prompts = prompts_by_category(category_name)
        return [PromptData(**asdict(prompt)) for prompt in prompts]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving prompts: {str(e)}")

@api.get("/prompts/model/{model_name}")
async def get_prompts_by_model_endpoint(model_name: str):
    try:
        prompts = prompts_by_model(model_name)
        return [PromptData(**asdict(prompt)) for prompt in prompts]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving prompts: {str(e)}")

@api.get("/prompts/search/{keyword}")
async def search_prompts_endpoint(keyword: str):
    try:
        prompts = search_prompts(keyword)
        return [PromptData(**asdict(prompt)) for prompt in prompts]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching prompts: {str(e)}")

@api.get("/categories")
async def get_categories():
    try:
        categories = list_categories()
        return [Category(**asdict(cat)) for cat in categories]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving categories: {str(e)}")

@api.get("/models")
async def get_models():
    try:
        models = list_models()
        return [Model(**asdict(model)) for model in models]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving models: {str(e)}")

@api.get("/labels")
async def get_labels():
    try:
        labels = list_labels()
        return [Label(**asdict(label)) for label in labels]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving labels: {str(e)}")

@api.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        with connect() as conn:
            conn.execute("SELECT 1")
        load_models()
        return {
            "status": "healthy",
            "models_loaded": True,
            "database_connection": True
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

# Include router AFTER all endpoints are registered to it
app.include_router(api)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

