import torch
from tqdm.auto import tqdm
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

class Trainer:
    def __init__(
            self,
            model,
            optimizer,
            criterion,
            train_loader,
            val_loader,
            device,
            checkpoint_dir
    ):
        self.model = model.to(device)
        self.optimizer = optimizer
        self.criterion = criterion

        self.train_loader = train_loader
        self.val_loader = val_loader
        
        self.device = device

        self.checkpoint_dir = checkpoint_dir


    def train_epoch(self):
        self.model.train()

        total_loss = 0.0
        correct = 0
        total = 0

        progress = tqdm(
                self.train_loader,
                desc="Training",
                leave=False,
        )

        for x, y in progress:
            x = x.to(self.device)
            y = y.to(self.device)

            self.optimizer.zero_grad()

            logits = self.model(x)

            loss = self.criterion(logits, y)

            loss.backward()

            self.optimizer.step()

            total_loss += loss.item() * y.size(0)

            predictions = logits.argmax(dim=1)

            correct += (predictions == y).sum().item()
            total += y.size(0)

            progress.set_postfix(
                    loss=f"{loss.item():.4f}",
                    acc=f"{correct / total:.3f}",
            )

        return (
                total_loss / total,
                correct / total,
        )

    @torch.no_grad()
    def validate(self):
        self.model.eval()
        
        total_loss = 0.0
        correct = 0
        total = 0
         
        progress = tqdm(
                self.val_loader,
                desc="Validation",
                leave=False,
        )

        for x, y in progress:

            x = x.to(self.device)
            y = y.to(self.device)

            logits = self.model(x)

            loss = self.criterion(logits, y)

            total_loss += loss.item() * y.size(0)

            predictions = logits.argmax(dim=1)

            correct += (predictions == y).sum().item()
            total += y.size(0)

            progress.set_postfix(
                    loss=f"{loss.item():.4f}",
                    acc=f"{correct / total:.3f}",
            )

        return (
            total_loss / total,
            correct / total,
        )

    def fit(self, epochs, patience):
        best_acc = 0.0
        counter = 0

        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(self.optimizer, patience=patience)

        epoch_bar = tqdm(range(epochs), desc="Epochs")
        epochs_total=0

        for epoch in epoch_bar:
            epochs_total += 1
            train_loss, train_acc = self.train_epoch()
            val_loss, val_acc = self.validate()
            scheduler.step(val_loss)

            if val_acc > best_acc + 1e-3:
                best_acc = val_acc
                counter = 0
                self.save_checkpoint(epoch, best_acc, self.checkpoint_dir / "best.pt")
                tqdm.write(
                        f"Epoch {epoch+1}: new best validation accuracy {best_acc:.3f}"
                )
            else:
                counter += 1
                tqdm.write(
                        f"Epoch {epoch + 1}: no improvement "
                        f"({counter}/{patience})"
                    )

            if counter >= patience:
                break


            epoch_bar.set_postfix(
            train_loss=f"{train_loss:.4f}",
            train_acc=f"{train_acc:.3f}",
            val_loss=f"{val_loss:.4f}",
            val_acc=f"{val_acc:.3f}",
            best=f"{best_acc:.3f}",
            )

        self.save_checkpoint(
            epochs_total,
            best_acc,
            self.checkpoint_dir / "final.pt",
        )



    def save_checkpoint(self, epoch, best_acc, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        torch.save(
                {
                    "model_state": self.model.state_dict(),
                    "optimizer_state": self.optimizer.state_dict(),
                    "epoch": epoch,
                    "best_acc": best_acc,
                },
                path,
        )
