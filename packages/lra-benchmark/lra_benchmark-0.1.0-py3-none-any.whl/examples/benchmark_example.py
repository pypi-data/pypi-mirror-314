from lra_benchmark.models.tiny_vit import TinyViT
from lra_benchmark.config import LRABenchmarkConfig
from lra_benchmark.dataset import get_cifar10_datasets
from lra_benchmark.benchmark import run_benchmark

config = LRABenchmarkConfig(batch_size=128, max_epochs=5)
train_loader, val_loader, test_loader = get_cifar10_datasets(config.batch_size, config.num_workers)

model = TinyViT(img_size=32, num_classes=10)

metrics = run_benchmark(config, model, train_loader, val_loader, test_loader)

print(f"Test Accuracy: {metrics['test_accuracy']:.2%}")
print(f"Test Loss: {metrics['test_loss']:.4f}")
print(f"Model Size: {metrics['model_size']} parameters")
print(f"Inference Time: {metrics['inference_time']:.4f} seconds")


