import torch
from functools import lru_cache

from backend.scripts.embeddings import Embedder


@lru_cache(maxsize=1)
def _get_embedder() -> Embedder:
    return Embedder()


def predict(model, raw_prompt: str):
    model.eval()
    prompt_embedding = _get_embedder().encode([raw_prompt])
    prompt_tensor = torch.tensor(prompt_embedding[0], dtype=torch.float32).unsqueeze(0)
    with torch.no_grad():
        output = model(prompt_tensor)
    return output


def predict_with_response(model, raw_prompt: str, raw_response: str):
    model.eval()
    formatted_input = f"""
    Prompt:
    {raw_prompt}

    Response:
    {raw_response}
    """
    embedded_input = _get_embedder().encode([formatted_input])
    input_tensor = torch.tensor(embedded_input[0], dtype=torch.float32).unsqueeze(0)
    with torch.no_grad():
        output = model(input_tensor)
    return output
