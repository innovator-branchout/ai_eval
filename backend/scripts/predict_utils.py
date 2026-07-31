import torch
from functools import lru_cache
from pathlib import Path
from scripts.embeddings import Embedder
import numpy as np

# Initialize the embedder lazily for efficiency
@lru_cache(maxsize=1)
def get_embedder():
    return Embedder()

@lru_cache(maxsize=1)
def get_label_mapping():
    """Get mapping from label_id to label_name"""
    from scripts.database import connect

    with connect() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM labels
            ORDER BY severity DESC
            """
        ).fetchall()

    # Create a mapping from label_id to label_name
    label_map = {}
    for row in rows:
        label_map[row["label_id"]] = row["label_name"]

    return label_map

def predict_prompt(session, raw_prompt):
    embedding = get_embedder().encode([raw_prompt]).astype(np.float32)

    logits = session.run(
        None,
        {"embedding": embedding},
    )[0]

    probs = np.exp(logits - logits.max(axis=1, keepdims=True))
    probs /= probs.sum(axis=1, keepdims=True)

    prediction = int(np.argmax(probs))

    label_mapping = get_label_mapping()

    return {
        "prediction": label_mapping[prediction + 1],
        "confidence": float(probs[0, prediction]),
        "logits": logits[0],
    }

def predict_prompt_with_response(session, raw_prompt: str, raw_response: str):
    """Predict using prompt + response embeddings"""
    formatted_input = f"""
Prompt:
{raw_prompt}

Response:
{raw_response}
"""
    embedding = get_embedder().encode([formatted_input]).astype(np.float32)

    logits = session.run(
            None,
            {"embedding": embedding},
    )[0]

    probs = np.exp(logits - logits.max(axis=1, keepdims=True))
    probs /= probs.sum(axis=1, keepdims=True)

    prediction = int(np.argmax(probs))

    # Get label mapping
    label_mapping = get_label_mapping()

    return {
        'prediction': label_mapping[prediction + 1],
        'confidence': float(probs[0, prediction]),
        'logits': logits[0]
    }

def get_all_labels():
    """Return list of all labels ordered by severity"""
    from scripts.database import connect

    with connect() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM labels
            ORDER BY severity DESC
            """
        ).fetchall()

    return rows

if __name__ == "__main__":
    # Test the functions
    print("Label mapping test:")

    try:
        import onnxruntime as ort

        session = ort.InferenceSession(
            "models/prompt_predictor/model.onnx",
            providers=["CPUExecutionProvider"],
        )

        test_prompt = "What is the capital of France?"

        result = predict_prompt(session, test_prompt)
        print(result)

    except Exception as e:
        print(f"Error testing predictions: {e}")
