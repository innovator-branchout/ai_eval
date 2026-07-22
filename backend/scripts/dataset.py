import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import torch
from torch.utils.data import Dataset, DataLoader

from database import connect


class EmbeddingDataset(Dataset):
    def __init__(self, embeddings, labels):
        self.embeddings = embeddings
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return (
                torch.tensor(self.embeddings[idx], dtype=torch.float32),
                torch.tensor(self.labels[idx], dtype=torch.long)
        )


def load_prompts():
    with connect() as conn:
        df = pd.read_sql("SELECT * FROM prompts", conn)

    return df


def load_embeddings(path):
    data = np.load(path)

    return data["ids"], data["embeddings"]


def build_datasets(embedding_path):
    df = load_prompts()
    ids, embeddings = load_embeddings(embedding_path)
    df = df.set_index("prompt_id").loc[ids]

    assert len(df) == len(ids)
    assert np.all(df.index.to_numpy() == ids)

    labels = df["label_id"].to_numpy() - 1

    train_x, test_x, train_y, test_y = train_test_split(
        embeddings,
        labels,
        test_size=0.2,
        random_state=42,
        #stratify=labels, # not possible with small dataset
    )

    train_x, val_x, train_y, val_y = train_test_split(
        train_x,
        train_y,
        test_size=0.25,
        random_state=42,
        # stratify=train_y, # not possible with small dataset
    )

    return (
        EmbeddingDataset(train_x, train_y),
        EmbeddingDataset(val_x, val_y),
        EmbeddingDataset(test_x, test_y),
    )


def build_dataloaders(embedding_path, batch_size=32):
    train, val, test = build_datasets(embedding_path)

    return (
            DataLoader(train, batch_size=batch_size, shuffle=True),
            DataLoader(val, batch_size=batch_size),
            DataLoader(test, batch_size=batch_size)
    )

if __name__ == "__main__":
    train_loader, val_loader, test_loader = build_dataloaders(Path(__file__).parent.parent / "embeddings" / "prompts.npz")

    print(f"Train batches: {len(train_loader)}")
    print(f"Validation batches: {len(val_loader)}")
    print(f"Test batches: {len(test_loader)}")
