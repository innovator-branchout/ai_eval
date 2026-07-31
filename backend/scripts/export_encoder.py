from transformers import AutoModel, AutoTokenizer
import torch
from pathlib import Path


MODEL = "sentence-transformers/all-MiniLM-L6-v2"

OUT = Path("models/minilm")


OUT.mkdir(parents=True, exist_ok=True)


tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModel.from_pretrained(MODEL)

model.eval()


dummy = tokenizer(
    ["hello world"],
    padding=True,
    truncation=True,
    return_tensors="pt",
)


torch.onnx.export(
    model,
    (
        dummy["input_ids"],
        dummy["attention_mask"],
    ),
    OUT / "encoder.onnx",
    input_names=[
        "input_ids",
        "attention_mask",
    ],
    output_names=[
        "last_hidden_state"
    ],
    dynamic_axes={
        "input_ids": {
            0:"batch",
            1:"sequence"
        },
        "attention_mask":{
            0:"batch",
            1:"sequence"
        },
    },
    opset_version=17,
)


tokenizer.save_pretrained(OUT)

print("done")
