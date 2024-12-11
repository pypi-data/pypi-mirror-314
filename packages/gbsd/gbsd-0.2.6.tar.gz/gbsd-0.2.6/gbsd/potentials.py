import torch


def get_coulomb_potential(
    observed_distances: torch.Tensor,
    charge_1: int,
    charge_2: int,
    relative_permittivity: float = 1.0,
) -> torch.Tensor:
    """Calculates the Coulomb potential between two pairs of particles.

    Args:
    - `observed_distances`: Tensor of observed distances, in Angstroms.
    - `charge_1`, `charge_2`: Charges of each pair of particles (in units of electron-charges)
    - `relative_permittivity` (Optional): The dieletric constant. The default value is 1.0.

    Returns: The Coulomb potential in units of eV, as a tensor.
    """
    # Prefactor is e^2 / (4 pi epsilon)
    prefactor = 14.39 / relative_permittivity # eV Angstrom

    contributions = prefactor * (charge_1 * charge_2) / observed_distances
    return torch.sum(contributions)


def get_lennard_jones_potential(
    observed_distances: torch.Tensor,
    sigma: float,
    epsilon: float,
) -> torch.Tensor:
    """Calculates the Lennard-Jones potential between two pairs of particles.

    V = 4 * epsilon * [(sigma / r)^12 - (sigma / r)^6].

    Note: r_min = 2^(1/6) sigma.

    Args:
    - `observed_distances`: Tensor of observed distances, in Angstroms.
    - `sigma`: The Lennard-Jones sigma parameter, in Angstroms.
    - `epsilon`: The Lennard-Jones epsilon parameter, in eV.

    Returns: The Lennard-Jones potential in units of eV, as a tensor.
    """
    term_6 = (sigma / observed_distances)**6
    term_12 = term_6**2

    contributions = 4 * epsilon * (term_12 - term_6)
    return torch.sum(contributions)
