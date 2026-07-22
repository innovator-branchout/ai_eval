from sentence_transformers import SentenceTransformer
from pathlib import Path
import numpy as np
import torch

ROOT = Path(__file__).resolve().parent.parent
EMBEDDINGS_DIR = ROOT / "embeddings"
MODEL = "BAAI/bge-large-en-v1.5"

class Embedder:
    def __init__(self):
        self.model = SentenceTransformer(
                MODEL,
                device="cuda" if torch.cuda.is_available() else "cpu"
                )

    def encode(self, texts): # encode a list
        return self.model.encode(
                texts,
                batch_size=32,
                normalize_embeddings=True,
                show_progress_bar=True
                )

def generate_prompt_embeddings(prompts):
    texts = [p.prompt_text for p in prompts] # get text of prompt
   
    ids = [p.prompt_id for p in prompts] # get prompt ids
    embeddings = Embedder().encode(texts) # encode prompts
    save_embeddings("prompts.npz", ids, embeddings) # save to embeddings directory

def generate_response_embeddings(prompts):
    texts = [
            f"""
            Prompt: 
            {p.prompt_text}
            
            Response:
            {p.raw_output}
            """
            for p in prompts
            ] # get text of prompt and response out of prompts (i'm sure that having multi-line strings will have no impact whatsoever

    ids = [p.prompt_id for p in prompts]
    embeddings = Embedder().encode(texts) # encode responses
    save_embeddings("responses.npz", ids, embeddings)

def save_embeddings(filename, ids, embeddings):
    EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)

    np.savez(
        EMBEDDINGS_DIR / filename,
        ids=np.asarray(ids),
        embeddings=embeddings,
    )

if __name__ == "__main__":
    from database import get_prompts

    prompts = get_prompts()

    generate_prompt_embeddings(prompts)
    generate_response_embeddings(prompts)
