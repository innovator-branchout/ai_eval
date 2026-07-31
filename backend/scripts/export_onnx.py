import torch
from pathlib import Path

from scripts.nn.layers import EmbeddingClassifier

ROOT = Path(__file__).resolve().parents[1]


def export(checkpoint_path, output_path):
    model = EmbeddingClassifier(
        input_size=384,
        num_rubric_classes=19,
        dropout=0.0,          # dropout disabled for inference
    )

    checkpoint = torch.load(
        checkpoint_path,
        map_location="cpu",
        weights_only=True,
    )

    model.load_state_dict(checkpoint["model_state"])
    model.eval()

    dummy = torch.randn(1, 384)

    torch.onnx.export(
        model,
        dummy,
        output_path,
        input_names=["embedding"],
        output_names=["logits"],
        dynamic_axes={
            "embedding": {0: "batch"},
            "logits": {0: "batch"},
        },
        opset_version=17,
        do_constant_folding=True,
        external_data=False
    )

    print("Saved", output_path)


export(
    ROOT / "models/prompt_predictor/best.pt",
    ROOT / "models/prompt_predictor/model.onnx",
)

export(
    ROOT / "models/response_grader/best.pt",
    ROOT / "models/response_grader/model.onnx",
)
