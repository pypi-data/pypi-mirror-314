"""
Contains methods for generating structures as torch tensors.
"""

import torch


def get_cubic_supercell_vectors(
    particle_count: int,
    number_density: float,
    device: torch.device | str | None = None,
) -> torch.Tensor:
    """Finds the ideal cubic supercell vectors for a given particle count and density.

    Args:
    - `particle_count`: Number of particles.
    - `number_density`: The number density of the given particles.
    - `device`: The device on which to create the tensor. Will use the default device of your
    system if not specified.

    Returns: Tensor of supercell vectors, e.g., [[ a1 ], [ a2 ], [ a3 ]].
    """
    volume = particle_count / number_density
    length = volume**(1/3)

    supercell_vectors = length * torch.eye(3, device=device)
    return supercell_vectors


def generate_random(
    particle_count: int,
    supercell_vectors: torch.Tensor,
) -> torch.Tensor:
    """Uniformly places a given number of points in a supercell.

    Args:
    - `particle_count`: Number of particles, N.
    - `supercell_vectors`: 3 x 3 tensor of supercell vectors, e.g., [[ a1 ], [ a2 ], [ a3 ]].
    
    Returns: N x 3 tensor of particle positions.
    """
    fractional_positions = torch.rand(
        (particle_count, 3),
        device=supercell_vectors.device
    )

    positions = fractional_positions @ supercell_vectors

    return positions


def generate_lattice(
    supercell_scaling: tuple[int, int, int],
    lattice_vectors: torch.Tensor,
    basis: torch.Tensor | None = None,
    noise: float = 0.2
) -> tuple[torch.Tensor, torch.Tensor]:
    """Places points on a lattice, with random displacement.

    Args:
    - `supercell_scaling`: Specifies the dimensions of the supercell. (n1, n2, n3).
    - `lattice_vectors`: 3 x 3 tensor of lattice vectors, e.g., [[ a1 ], [ a2 ], [ a3 ]].
    - `basis` (optional): A K x 3 tensor, that acts as list of basis vectors for the structure. If None,
    applies a basis of just the origin point.
    - `noise` (optional): The standard deviation of Normal noise applied to positions.

    Returns:
    - N x 3 tensor of point positions.
    - 3 x 3 tensor of supercell vectors, e.g., [[ n1 a1 ], [ n2 a2 ], [ n3 a3 ]].
    """
    # Get origins of each subcell
    ranges = (torch.arange(n, device=lattice_vectors.device) for n in supercell_scaling)
    lattice_scales = torch.cartesian_prod(*ranges)

    subcell_origins = lattice_scales.float() @ lattice_vectors

    # Get positions of each basis atom
    if basis is None:
        basis = torch.zeros((1, 3), device=lattice_vectors.device)

    positions = subcell_origins[:, None, :] + basis[None, :, :]
    positions = positions.flatten(end_dim=-2)

    # Add noise
    positions = torch.normal(positions, noise)

    # Get supercell vectors
    scaling_factors_tensor = torch.diag(
        torch.tensor(supercell_scaling, device=lattice_vectors.device)
    )
    supercell_vectors = scaling_factors_tensor.float() @ lattice_vectors

    return positions, supercell_vectors


def get_cell_volume(cell_vectors: torch.Tensor) -> torch.Tensor:
    """Calculates the volume of a super- or unit cell by its vectors.

    Note: As of July 3, 2024, the determinent is not implemented on MPS, so the
    computation is briefly moved to the CPU.

    Args:
    - `cell_vectors`: A D x D tensor of cell vectors, e.g., [[ a1 ], [ a2 ], [ a3 ]].

    Returns: The volume of the cell as a tensor.
    """
    try:
        return cell_vectors.det().abs()
    except NotImplementedError:
        # For MPS
        return cell_vectors.cpu().det().abs().to(cell_vectors.device)
