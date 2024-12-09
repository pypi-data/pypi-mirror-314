import torch
import time
import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping
from .utils.optimizer import create_optimizer
from .models.base_model import BaseModel

class LRABenchmark(pl.LightningModule):
    def __init__(self, model: BaseModel, num_classes: int, learning_rate: float, weight_decay: float):
        super().__init__()
        self.model = model
        self.num_classes = num_classes
        self.learning_rate = learning_rate
        self.weight_decay = weight_decay
        self.loss_fn = torch.nn.CrossEntropyLoss()
        
        for param in self.model.parameters():
            param.requires_grad = True

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        inputs, targets = batch
        logits = self(inputs)
        loss = self.loss_fn(logits, targets)
        self.log("train_loss", loss)
        return loss

    def validation_step(self, batch, batch_idx):
        inputs, targets = batch
        logits = self(inputs)
        loss = self.loss_fn(logits, targets)
        acc = (logits.argmax(dim=-1) == targets).float().mean()
        self.log("val_loss", loss, prog_bar=True)
        self.log("val_acc", acc, prog_bar=True)

    def test_step(self, batch, batch_idx):
        inputs, targets = batch
        logits = self(inputs)
        loss = self.loss_fn(logits, targets)
        acc = (logits.argmax(dim=-1) == targets).float().mean()
        self.log("test_loss", loss, prog_bar=True)
        self.log("test_acc", acc, prog_bar=True)

    def configure_optimizers(self):
        return torch.optim.Adam(self.model.parameters(), lr=self.learning_rate, weight_decay=self.weight_decay)

def compute_model_size(model: BaseModel) -> int:
    """Compute the total number of parameters (weights) in the model."""
    return sum(p.numel() for p in model.parameters())

def compute_inference_time(model: BaseModel, input_size: tuple) -> float:
    """Compute the average inference time of the model."""
    input_tensor = torch.randn(input_size)
    num_warmup_runs = 5
    num_inference_runs = 10

    # Warmup
    for _ in range(num_warmup_runs):
        _ = model(input_tensor)

    # Measure inference time
    inference_times = []
    for _ in range(num_inference_runs):
        start_time = time.time()
        _ = model(input_tensor)
        end_time = time.time()
        inference_times.append(end_time - start_time)

    return sum(inference_times) / num_inference_runs

def run_benchmark(config, model: BaseModel, train_dataloader, val_dataloader, test_dataloader):
    """Run a benchmark on the given model."""
    benchmark = LRABenchmark(
        model=model,
        num_classes=config.num_classes,
        learning_rate=config.learning_rate,
        weight_decay=config.weight_decay
    )

    trainer = pl.Trainer(
        max_epochs=config.max_epochs,
        callbacks=[
            ModelCheckpoint(monitor="val_acc", mode="max"),
            EarlyStopping(monitor="val_loss", patience=5)
        ]
    )

    trainer.fit(benchmark, train_dataloader, val_dataloader)

    # Load the best-performing model checkpoint
    best_model_path = trainer.checkpoint_callback.best_model_path
    best_model = benchmark.load_from_checkpoint(best_model_path)

    # Compute test metrics
    trainer.test(best_model, test_dataloader)
    test_acc = trainer.callback_metrics["test_acc"].item()
    test_loss = trainer.callback_metrics["test_loss"].item()
    model_size = compute_model_size(best_model.model)
    inference_time = compute_inference_time(best_model.model, (config.batch_size, 1, 32, 32))

    return {
        "test_accuracy": test_acc,
        "test_loss": test_loss,
        "model_size": model_size,
        "inference_time": inference_time
    }