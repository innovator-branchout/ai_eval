#!/usr/bin/env python3
"""
AI Evaluation System - Backend API

This FastAPI application serves as the backend for our AI evaluation system,
providing endpoints to interact with models, datasets, and predictions.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
from typing import List, Optional
from pathlib import Path
from dataclasses import asdict

# Import backend modules
from backend.scripts.predict_utils import predict_prompt, predict_prompt_with_response, get_label_mapping
from backend.scripts.nn.layers import EmbeddingClassifier
from backend.scripts.database import connect, list_categories, list_models, list_labels, get_prompts, prompts_by_category, prompts_by_model, search_prompts
from backend.scripts.predict import predict, predict_with_response

app = FastAPI(
    title="AI Evaluation System API",
    description="API for the AI evaluation system with prediction capabilities",
    version="1.0.0"
)

# Add CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model instances for efficiency
prompt_model = None
response_model = None

def load_models():
    """Load prediction models once at startup"""
    global prompt_model, response_model

    if prompt_model is None:
        try:
            # Load prompt prediction model
            prompt_model = EmbeddingClassifier(
                input_size=1024,
                num_rubric_classes=19,
                dropout=0.2
            )

            checkpoint = torch.load('backend/models/prompt_predictor/best.pt', weights_only=True)
            prompt_model.load_state_dict(checkpoint['model_state'])
            prompt_model.eval()
            print("Prompt model loaded successfully")
        except Exception as e:
            print(f"Error loading prompt model: {e}")
            raise

    if response_model is None:
        try:
            # Load response prediction model
            response_model = EmbeddingClassifier(
                input_size=1024,
                num_rubric_classes=19,
                dropout=0.2
            )

            checkpoint = torch.load('backend/models/response_grader/best.pt', weights_only=True)
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
    model_type: str = "auto"  # "prompt", "response", or "auto"

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
@app.get("/")
async def root():
    return {
        "message": "AI Evaluation System API",
        "version": "1.0.0",
        "endpoints": [
            "/predict",
            "/prompts",
            "/categories",
            "/models",
            "/labels"
        ]
    }

@app.post("/predict")
async def predict_endpoint(request: PredictionRequest):
    """
    Make a prediction for a prompt and/or response
    """
    try:
        # Load models if not already loaded
        load_models()

        # Determine which model to use
        if request.model_type == "auto":
            # Auto-determine based on whether response is provided
            model_to_use = "response" if request.response else "prompt"
        else:
            model_to_use = request.model_type

        # Get prediction
        if model_to_use == "prompt":
            result = predict_prompt(prompt_model, request.prompt)
        elif model_to_use == "response":
            if not request.response:
                raise HTTPException(status_code=400, detail="Response is required for response prediction")
            result = predict_prompt_with_response(response_model, request.prompt, request.response)
        else:
            raise HTTPException(status_code=400, detail="Invalid model type. Use 'prompt', 'response', or 'auto'")

        return PredictionResponse(
            prediction=result['prediction'],
            confidence=result['confidence'],
            model_used=model_to_use
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/prompts")
async def get_prompts_endpoint():
    """
    Get all prompts from the database
    """
    try:
        prompts = get_prompts()
        return [PromptData(**asdict(prompt)) for prompt in prompts]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving prompts: {str(e)}")

@app.get("/prompts/category/{category_name}")
async def get_prompts_by_category_endpoint(category_name: str):
    """
    Get prompts by category name
    """
    try:
        prompts = prompts_by_category(category_name)
        return [PromptData(**asdict(prompt)) for prompt in prompts]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving prompts: {str(e)}")

@app.get("/prompts/model/{model_name}")
async def get_prompts_by_model_endpoint(model_name: str):
    """
    Get prompts by model name
    """
    try:
        prompts = prompts_by_model(model_name)
        return [PromptData(**asdict(prompt)) for prompt in prompts]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving prompts: {str(e)}")

@app.get("/prompts/search/{keyword}")
async def search_prompts_endpoint(keyword: str):
    """
    Search prompts by keyword
    """
    try:
        prompts = search_prompts(keyword)
        return [PromptData(**asdict(prompt)) for prompt in prompts]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching prompts: {str(e)}")

@app.get("/categories")
async def get_categories():
    """
    Get all categories
    """
    try:
        categories = list_categories()
        return [Category(**asdict(cat)) for cat in categories]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving categories: {str(e)}")

@app.get("/models")
async def get_models():
    """
    Get all models
    """
    try:
        models = list_models()
        return [Model(**asdict(model)) for model in models]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving models: {str(e)}")

@app.get("/labels")
async def get_labels():
    """
    Get all labels
    """
    try:
        labels = list_labels()
        return [Label(**asdict(label)) for label in labels]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving labels: {str(e)}")

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    try:
        # Test database connection
        with connect() as conn:
            conn.execute("SELECT 1")

        # Test model loading
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

if __name__ == "__main__":
    import uvicorn
    print("Starting AI Evaluation System API...")
    print("Loading models...")
    load_models()
    print("Models loaded successfully!")
    uvicorn.run(app, host="0.0.0.0", port=8000)
