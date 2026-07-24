import torch
import torch.nn as nn

class EmbeddingClassifier(nn.Module):
    def __init__(self, input_size, num_rubric_classes, dropout):
        super().__init__()
        self.mySeq = nn.Sequential(
            nn.Linear(input_size, 512),
            nn.LayerNorm(512),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(512, 256),
            nn.LayerNorm(256),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(256, 128),
            nn.LayerNorm(128),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(128, num_rubric_classes)
        )

    def forward(self, x):
        return self.mySeq(x)
