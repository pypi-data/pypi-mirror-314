import torch.optim as optim

def create_optimizer(model, learning_rate, weight_decay):
    """
    Creates an Adam optimizer with specified hyperparameters.

    Args:
        model (torch.nn.Module): The model whose parameters will be optimized.
        learning_rate (float): The learning rate for the optimizer.
        weight_decay (float): The weight decay (L2 regularization).

    Returns:
        torch.optim.Optimizer: Configured Adam optimizer.
    """
    return optim.Adam(
        model.parameters(),
        lr=learning_rate,
        betas=(0.9, 0.98),
        eps=1e-9,
        weight_decay=weight_decay
    )


