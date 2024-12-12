import torch


def chi_squared(
    estimate: torch.Tensor,
    target: torch.Tensor,
    uncertainty: torch.Tensor | float
) -> torch.Tensor:
    return torch.sum((estimate - target)**2 / uncertainty**2)