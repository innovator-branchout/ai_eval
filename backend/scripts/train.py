import argparse

import torch
from torch.optim import Adam

from backend.scripts.dataset import build_dataloaders
from backend.scripts.nn.layers import EmbeddingClassifier
from backend.scripts.nn.trainer import Trainer
from backend.scripts.nn.losses import get_loss

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("model", type=str, help="prompt or response")

    args = parser.parse_args()

    train_loader, val_loader, _ = build_dataloaders(ROOT / "embeddings" / "prompts.npz") if args.model=="prompt" else build_dataloaders(ROOT / "embeddings" / "responses.npz")

    model = EmbeddingClassifier(
            input_size=1024,
            num_rubric_classes=19,
            dropout=0.2
    )

    criterion = get_loss("cross_entropy")

    optimizer = Adam(
            model.parameters(),
            lr=3e-4,
    )

    trainer = Trainer(
        model=model,
        optimizer=optimizer,
        criterion=criterion,
        train_loader=train_loader,
        val_loader=val_loader,
        device="cuda" if torch.cuda.is_available() else "cpu",
        checkpoint_dir=ROOT / "models" / "prompt_predictor" if args.model=="prompt" else ROOT / "models" / "response_grader"
    )

    trainer.fit(epochs=30, patience=5)
