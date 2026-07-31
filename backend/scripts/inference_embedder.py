from pathlib import Path
import numpy as np
import onnxruntime as ort
from transformers import AutoTokenizer


ROOT = Path(__file__).resolve().parent.parent

MODEL_DIR = ROOT / "models" / "minilm"


_session = None
_tokenizer = None


def load():

    global _session, _tokenizer

    if _session is None:

        _session = ort.InferenceSession(
            str(MODEL_DIR / "encoder.onnx"),
            providers=[
                "CPUExecutionProvider"
            ],
        )

        _tokenizer = AutoTokenizer.from_pretrained(
            MODEL_DIR
        )

    return _session, _tokenizer



def encode(texts):

    session, tokenizer = load()


    tokens = tokenizer(
        texts,
        padding=True,
        truncation=True,
        max_length=256,
        return_tensors="np",
    )


    output = session.run(
        None,
        {
            "input_ids":
                tokens["input_ids"].astype(np.int64),

            "attention_mask":
                tokens["attention_mask"].astype(np.int64),
        },
    )


    hidden = output[0]


    mask = tokens["attention_mask"]


    # mean pooling
    embeddings = (
        hidden * mask[:,:,None]
    ).sum(axis=1) / mask.sum(axis=1)[:,None]


    # normalize exactly like SentenceTransformer
    embeddings /= np.linalg.norm(
        embeddings,
        axis=1,
        keepdims=True,
    )


    return embeddings.astype(np.float32)
