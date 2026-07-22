import torch.nn as nn

def get_loss(name="cross_entropy", **kwargs):
    name = name.lower()

    if name == "cross_entropy":
        return nn.CrossEntropyLoss(**kwargs)
    
    if name == "bce":
        return nn.BCEWithLogitsLoss(**kwargs)

    if name == "mse":
        return nn.MSELoss(**kwargs)

    raise ValueError(f"Unkown loss function: {name}")
