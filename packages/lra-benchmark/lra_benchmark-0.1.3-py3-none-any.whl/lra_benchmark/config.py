class LRABenchmarkConfig:
    def __init__(
        self,
        batch_size=256,
        learning_rate=3e-4,
        weight_decay=1e-4,
        num_workers=4,
        max_epochs=10,
        gpus=1,
        num_classes=10,
    ):
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.weight_decay = weight_decay
        self.num_workers = num_workers
        self.max_epochs = max_epochs
        self.gpus = gpus
        self.num_classes = num_classes
