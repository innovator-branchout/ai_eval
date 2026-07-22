import argparse
import torch
from dataset import build_dataloaders
from nn.losses import get_loss
from nn.layers import EmbeddingClassifier
from tqdm.auto import tqdm

def get_test_loader(embedding_path, batch_size):
    _, _, test_loader = build_dataloaders(embedding_path, batch_size=batch_size)

    return test_loader

def evaluate(model, test_loader):
    model.eval()
    correct = 0
    total = 0
    total_loss = 0.0
    criterion = get_loss("cross_entropy")

    progress = tqdm(
        test_loader,
        desc="Evaluation",
        leave=False
    )
    with torch.no_grad():
        for input, label in progress:
            logits = model(input)

            loss = criterion(logits, label)
            total_loss += loss.item() * label.size(0) #in case the last_batch is less than 32 because drop_last=False by default

            predicted = logits.argmax(dim=1)
            total += label.size(0)
            correct += (predicted == label).sum().item()

            progress.set_postfix(
                loss=f"{loss.item():.4f}",
                acc=f"{correct / total:.3f}"
            )
    return (
        total_loss / total,
        correct / total
    )

if __name__=="__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("model", type=str, help="prompt or response")

    args = parser.parse_args()

    model = EmbeddingClassifier(
            input_size=1024,
            num_rubric_classes=19,
            dropout=0.2
    )

    checkpoint = torch.load('models/prompt_predictor/best.pt', weights_only=True) if args.model=="prompt" else torch.load('models/response_grader/best.pt')

    weights = checkpoint['model_state']

    model.load_state_dict(weights)


    embedding_path = "embeddings/prompts.npz" if args.model=="prompt" else "embeddings/responses.npz"
    print(evaluate(model, get_test_loader(embedding_path, 30)))
