from typing import List, Dict, Optional
from pydantic import BaseModel

class ProviderCost(BaseModel):
    name: str
    cost: float

class Metrics(BaseModel):
    latency: float
    throughput: float
    current_provider: str
    cost: float
    savings: float
    available_providers: List[ProviderCost]

class ChatRequest(BaseModel):
    model: str
    prompt: str
    history: List[Dict[str, str]] = []
    provider: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 1000

class ChatResponse(BaseModel):
    response: str
    metrics: Metrics

class ModelProvider(BaseModel):
    name: str
    cost: float
    quantisation: Optional[int] = None
    context: Optional[int] = None

class ModelInfo(BaseModel):
    name: str
    providers: List[ModelProvider]

class ModelsResponse(BaseModel):
    models: List[str]
    providers: Dict[str, List[str]]

class APIError(Exception):
    """Raised when the API request fails"""
    pass
