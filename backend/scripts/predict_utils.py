import torch
from backend.scripts.embeddings import Embedder
from pathlib import Path
import numpy as np

# Initialize the embedder once for efficiency
_EMBEDDER = Embedder()

def get_label_mapping():
    """Get mapping from label_id to label_name"""
    from backend.scripts.database import connect

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

def predict_prompt(model, raw_prompt: str):
    """Predict using prompt embeddings"""
    model.eval()

    prompt_embedding = _EMBEDDER.encode([raw_prompt])
    prompt_tensor = torch.tensor(prompt_embedding[0], dtype=torch.float32).unsqueeze(0)

    with torch.no_grad():
        output = model(prompt_tensor)

    # Get label mapping
    label_mapping = get_label_mapping()

    # Convert logits to human-readable prediction
    predicted_class = torch.argmax(output).item()
    actual_label_id = predicted_class + 1  # Adjust for 0-based indexing

    predicted_label = label_mapping.get(actual_label_id, f"Unknown Label {actual_label_id}")

    return {
        'prediction': predicted_label,
        'logits': output.cpu().numpy()[0],
        'confidence': torch.softmax(output, dim=1).max().item()
    }

def predict_prompt_with_response(model, raw_prompt: str, raw_response: str):
    """Predict using prompt + response embeddings"""
    model.eval()

    formatted_input = f"""
Prompt:
{raw_prompt}

Response:
{raw_response}
"""
    embedded_input = _EMBEDDER.encode([formatted_input])
    input_tensor = torch.tensor(embedded_input[0], dtype=torch.float32).unsqueeze(0)

    with torch.no_grad():
        output = model(input_tensor)

    # Get label mapping
    label_mapping = get_label_mapping()

    # Convert logits to human-readable prediction
    predicted_class = torch.argmax(output).item()
    actual_label_id = predicted_class + 1  # Adjust for 0-based indexing

    predicted_label = label_mapping.get(actual_label_id, f"Unknown Label {actual_label_id}")

    return {
        'prediction': predicted_label,
        'logits': output.cpu().numpy()[0],
        'confidence': torch.softmax(output, dim=1).max().item()
    }

def get_all_labels():
    """Return list of all labels ordered by severity"""
    from database import connect

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
        from backend.scripts.nn.layers import EmbeddingClassifier

        model = EmbeddingClassifier(
            input_size=1024,
            num_rubric_classes=19,
            dropout=0.2
        )

        checkpoint = torch.load('models/prompt_predictor/best.pt', weights_only=True)
        model.load_state_dict(checkpoint['model_state'])

        # Test with a simple prompt
        test_prompt = "What is the capital of France?"
        result = predict_prompt(model, test_prompt)
        print(f"Prompt prediction: {result}")

    except Exception as e:
        print(f"Error testing predictions: {e}")
