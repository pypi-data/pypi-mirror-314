"""
Contains methods for calculating various spectra from a structure, and converting between
different types of spectra.
"""

from itertools import combinations_with_replacement

import torch
from ._data import NEUTRON_SCATTERING_LENGTHS, XRAY_FORM_FACTOR_PARAMS

_DEFAULT_KERNEL_WIDTH = 0.035

def get_distance_matrix(
    points_1: torch.Tensor,
    points_2: torch.Tensor,
    cell: torch.Tensor
) -> torch.Tensor:
    """Gets distance matrix while accounting for minimal image convention.

    Args:
    - `points_1`: Tensor with shape M x D.
    - `points_2`: Tensor with shape N x D.
    - `cell`: D x D tensor of supercell vectors, e.g., [[ a1... ], [ a2... ], [ a3... ]].

    Returns: M x N tensor of distances.
    """
    pair_differences = points_2[None, :, :] - points_1[:, None, :]

    pair_differences_shifts = torch.round(pair_differences @ cell.inverse()) @ cell
    image_pair_differences = pair_differences - pair_differences_shifts

    distance_matrix = torch.linalg.norm(image_pair_differences, dim=-1)

    return distance_matrix


def get_observed_distances(
    points_1: torch.Tensor,
    points_2: torch.Tensor,
    cell: torch.Tensor
) -> torch.Tensor:
    """Gets the list of observed distances between two sets of points in D dimensions.
    
    If the points are identical, symmetry and zeros are ignored.

    Args:
    - `points_1`: Tensor with shape M x D
    - `points_2`: Tensor with shape N x D
    - `cell`: D x D tensor of supercell vectors, e.g., [[ a1... ], [ a2... ], [ a3... ]].
    
    Returns: 1D tensor of observed distances.
    """
    distance_matrix = get_distance_matrix(points_1, points_2, cell)

    if points_1 is points_2:
        # Ignore diagonal and symmetry-equivalent points
        mask = torch.triu(
            torch.ones_like(distance_matrix, dtype=torch.bool),
            diagonal=1
        )
        observed_distances = distance_matrix[mask]
    else:
        observed_distances = torch.flatten(distance_matrix)

    return observed_distances


def get_cell_volume(cell: torch.Tensor) -> torch.Tensor:
    """Calculates the volume of a super- or unit cell by its vectors.

    Note: The determinent may not be implemented on MPS, so the computation may briefly be moved
    to the CPU.

    Args:
    - `cell`: A D x D tensor of supercell vectors, e.g., [[ a1... ], [ a2... ], [ a3... ]].

    Returns: The volume of the cell as a tensor.
    """
    try:
        return cell.det().abs()
    except NotImplementedError:
        # For MPS
        return cell.cpu().det().abs().to(cell.device)


def get_partial_rdf(
    points_1: torch.Tensor,
    points_2: torch.Tensor,
    cell: torch.Tensor,
    bins: torch.Tensor,
    kernel_width: float = _DEFAULT_KERNEL_WIDTH,
) -> torch.Tensor:
    """Gets the partial radial distribution function (RDF) between two sets of points.

    Note: Uses kernel density estimation (KDE) with Gaussians so that the output is differentiable.

    Args:
    - `points_1`: Tensor with shape M x D.
    - `points_2`: Tensor with shape N x D.
    - `cell`: D x D tensor of supercell vectors, e.g., [[ a1... ], [ a2... ], [ a3... ]].
    - `bins`: The values of $r$ on which to evaluate the partial RDF.
    - `kernel_width`: Width of Gaussians for KDE. You should use a value less than half the width
    of the smallest expected peak. Using a good value may require trial and error.
    
    Returns: 1D tensor of estimated partial RDF values evaluated on `bins`.
    """
    observed_distances = get_observed_distances(points_1, points_2, cell)

    try:
        gaussians: torch.Tensor = torch.exp(
            -0.5 * ((bins - observed_distances.view(-1, 1)) / kernel_width)**2
        ) / (kernel_width * (2 * torch.pi)**0.5)

        summed_gaussians = gaussians.sum(dim=0)

    except (torch.cuda.OutOfMemoryError, MemoryError):
        summed_gaussians = torch.zeros_like(bins)

        for distance in observed_distances:
            summed_gaussians += torch.exp(
                -0.5 * ((bins - distance) / kernel_width)**2
            ) / (kernel_width * (2 * torch.pi)**0.5)

    volume = get_cell_volume(cell)
    partial_rdf = (volume / (observed_distances).size(0)) * (1 / (4 * torch.pi * bins**2)) * summed_gaussians

    return partial_rdf


def get_neutron_total_rdf(
    chemical_symbols: list[str],
    positions: torch.Tensor,
    cell: torch.Tensor,
    bins: torch.Tensor,
    kernel_width: float = _DEFAULT_KERNEL_WIDTH,
    scattering_lengths: dict[str, float] = NEUTRON_SCATTERING_LENGTHS,
) -> torch.Tensor:
    """Calculates the total radial distribution function (RDF), G(r), for a structure.
    
    G(r) is defined as in "Keen. J. Appl. Crystallogr. (2001). 34, 172-177."

    Outputs in units of barns when scattering_lengths are in femtometers.

    Note: Uses kernel density estimation (KDE) with Gaussians so that the output is differentiable.

    Args:
    - `chemical_symbols`: List of atom symbols.
    - `positions: N x D tensor of atom positions in your system.
    - `cell`: D x D tensor of supercell vectors, e.g., [[ a1... ], [ a2... ], [ a3... ]].
    - `bins`: The values of $r$ on which to evaluate the total RDF.
    - `kernel_width`: Width of Gaussians for KDE. You should use a value less than half the width
    of the smallest expected peak in each partial RDF. Using a good value may require trial and
    error. Defaults to 0.05.
    - `scattering_lengths`: Dictionary that maps element labels to the element's average coherent
    bound neutron scattering length. Use units of femtometers. Defaults to values from _data.py file.

    Returns: 1D tensor of estimated total RDF values evaluated on `bins`.
    """
    total_particle_count = len(chemical_symbols)
    unique_elements = set(chemical_symbols)

    element_fractions = {
        element: chemical_symbols.count(element) / total_particle_count for element in unique_elements
    }
    element_masks = {
        element: [symbol == element for symbol in chemical_symbols] for element in unique_elements
    }    

    total_rdf = torch.zeros_like(bins)
    #for (element_1, element_2) in product(unique_elements, repeat=2):
    for element_1, element_2 in combinations_with_replacement(unique_elements, 2):
        positions_1 = positions[element_masks[element_1]]
        fraction_1 = element_fractions[element_1]
        scattering_length_1 = scattering_lengths[element_1]

        if element_1 != element_2:
            positions_2 = positions[element_masks[element_2]]
            fraction_2 = element_fractions[element_2]
            scattering_length_2 = scattering_lengths[element_2] 
        else:
            positions_2 = positions_1
            fraction_2 = fraction_1
            scattering_length_2 = scattering_length_1

        coefficient = fraction_1 * fraction_2 * scattering_length_1 * scattering_length_2 * 0.01

        if element_1 != element_2:
            coefficient *= 2

        partial_rdf = get_partial_rdf(
            positions_1,
            positions_2,
            cell,
            bins,
            kernel_width
        )

        total_rdf += coefficient * (partial_rdf - 1)

    return total_rdf


def get_neutron_total_correlation_function(
    total_rdf: torch.Tensor,
    r_bins: torch.Tensor,
    chemical_symbols: list[str],
    cell: torch.Tensor,
    scattering_lengths: dict[str, float] = NEUTRON_SCATTERING_LENGTHS,
):
    """Calculates the total correlation function, T(r), from the total RDF.

    T(r) is defined as in "Keen. J. Appl. Crystallogr. (2001). 34, 172-177."

    You can get the `total_rdf` from `get_neutron_total_rdf(...)`.

    Args:
    - `total_rdf`: 1D tensor of total radial distribution function values evaluated on `r_bins`.
    - `r_bins`: The values of $r$ on which the total_rdf is evaluated.
    - `chemical_symbols`: List of atom symbols.
    - `cell`: D x D tensor of supercell vectors, e.g., [[ a1... ], [ a2... ], [ a3... ]].
    - `scattering_lengths`: Dictionary that maps element labels to the element's average coherent
    bound neutron scattering length. Use units of femtometers. Defaults to values from _data.py file.

    Returns: 1D tensor of the total correlation function, T(r), evaluated on r_bins.
    """
    total_particle_count = len(chemical_symbols)
    unique_elements = set(chemical_symbols)

    element_fractions = {
        element: chemical_symbols.count(element) / total_particle_count for element in unique_elements
    }

    volume = get_cell_volume(cell)
    total_density = total_particle_count / volume

    rdf_offset = 0.01 * (sum(fraction * scattering_lengths[element] for element, fraction in element_fractions.items()))**2

    return 4 * torch.pi * r_bins * total_density * (total_rdf + rdf_offset)
    

def get_neutron_total_scattering_sf(
    total_rdf: torch.Tensor,
    r_bins: torch.Tensor,
    q_bins: torch.Tensor,
    chemical_symbols: list[str],
    cell: torch.Tensor,
) -> torch.Tensor:
    """Calculates the total scattering structure factor (SF), F(Q) = i(Q), from the total RDF.

    F(Q) = i(Q) is defined as in "Keen. J. Appl. Crystallogr. (2001). 34, 172-177."

    You can get the `total_rdf` from `get_neutron_total_rdf(...)`.

    Note: It is important for the accuracy of this calculation that `r_bins` is large enough that
    the `total_rdf` becomes close to zero.

    Args:
    - `total_rdf`: 1D tensor of total radial distribution function values evaluated on `r_bins`.
    - `r_bins`: The values of $r$ on which the total_rdf is evaluated.
    - `q_bins`: The values of $Q$ on which to evaluate the total scattering SF.
    - `chemical_symbols`: List of atom symbols.
    - `cell`: D x D tensor of supercell vectors, e.g., [[ a1... ], [ a2... ], [ a3... ]].

    Returns: 1D tensor of estimated total-scattering SF values, evaluated on q_bins.
    """
    total_particle_count = len(chemical_symbols)
    volume = get_cell_volume(cell)
    total_density = total_particle_count / volume

    integrand = r_bins[None, :] * total_rdf[None, :] * torch.sin(q_bins[:, None] * r_bins[None, :]) / q_bins[:, None]

    total_scattering_sf = 4 * torch.pi * total_density * torch.trapz(integrand, r_bins)
    return total_scattering_sf

def get_xray_total_scattering_sf(
    chemical_symbols: list[str],
    positions: torch.Tensor,
    cell: torch.Tensor,
    q_bins: torch.Tensor,
    r_bins: torch.Tensor,
    kernel_width: float = _DEFAULT_KERNEL_WIDTH,
    form_factor_params: dict[str, dict[str, list[float]]] = XRAY_FORM_FACTOR_PARAMS,
) -> torch.Tensor:
    """Calculates the total X-ray scattering factor (SF), F^X(r), for a structure.
    
    F^X(r) is defined as in "Keen. J. Appl. Crystallogr. (2001). 34, 172-177."

    Outputs in units of barns when scattering_lengths are in femtometers.

    Note: Uses kernel density estimation (KDE) with Gaussians so that the output is differentiable.

    Args:
    - `chemical_symbols`: List of atom symbols.
    - `positions: N x D tensor of atom positions in your system.
    - `cell`: D x D tensor of supercell vectors, e.g., [[ a1... ], [ a2... ], [ a3... ]].
    - `bins`: The values of $r$ on which to evaluate the total RDF.
    - `kernel_width`: Width of Gaussians for KDE. You should use a value less than half the width
    of the smallest expected peak in each partial RDF. Using a good value may require trial and
    error. Defaults to 0.05.
    - `scattering_lengths`: Dictionary that maps element labels to the element's average coherent
    bound neutron scattering length. Use units of femtometers. Defaults to values from _data.py file.

    Returns: 1D tensor of estimated total RDF values evaluated on `bins`.
    """
    total_particle_count = len(chemical_symbols)
    volume = get_cell_volume(cell)
    total_density = total_particle_count / volume

    unique_elements = set(chemical_symbols)

    element_fractions = {
        element: chemical_symbols.count(element) / total_particle_count for element in unique_elements
    }

    element_masks = {
        element: [symbol == element for symbol in chemical_symbols] for element in unique_elements
    }

    # Form factors
    element_form_factors: dict[str, torch.Tensor] = {}
    for element in unique_elements:
        a = torch.tensor(form_factor_params[element]["a"], device=q_bins.device)
        b = torch.tensor(form_factor_params[element]["b"], device=q_bins.device)
        c = form_factor_params[element]["c"][0]

        element_form_factors[element] = c + torch.sum(a[:, None] * torch.exp(-b[:, None] * (q_bins[None, :] / (4 * torch.pi))**2), dim=0)

    sum_of_form_factors = sum(element_fractions[element] * element_form_factors[element] for element in unique_elements)

    scaled_form_factors = {
        element: element_fractions[element] * element_form_factors[element] / sum_of_form_factors for element in unique_elements
    }

    qr_product = r_bins[:, None] * q_bins[None, :]
    total_sf = torch.zeros_like(q_bins)
    for element_1, element_2 in combinations_with_replacement(unique_elements, 2):
        positions_1 = positions[element_masks[element_1]]
        scaled_form_factor_1 = scaled_form_factors[element_1]

        if element_1 != element_2:
            positions_2 = positions[element_masks[element_2]]
            scaled_form_factor_2 = scaled_form_factors[element_2] 
        else:
            positions_2 = positions_1
            scaled_form_factor_2 = scaled_form_factor_1

        coefficient = total_density * scaled_form_factor_1 * scaled_form_factor_2

        if element_1 != element_2:
            coefficient *= 2

        partial_rdf = get_partial_rdf(
            positions_1,
            positions_2,
            cell,
            r_bins,
            kernel_width
        )

        integrand = 4 * torch.pi * r_bins[:, None]**2 * (partial_rdf[:, None] - 1) * torch.sin(qr_product) / qr_product

        total_sf += coefficient * torch.trapz(integrand, r_bins, dim=0)

    return total_sf


def get_xray_total_rdf(
    total_sf: torch.Tensor,
    r_bins: torch.Tensor,
    q_bins: torch.Tensor,
    chemical_symbols: list[str],
    cell: torch.Tensor,
) -> torch.Tensor:
    total_particle_count = len(chemical_symbols)
    volume = get_cell_volume(cell)
    total_density = total_particle_count / volume
    
    qr_product = q_bins[None, :] * r_bins[:, None]
    integrand = 4 * torch.pi * q_bins[None, :]**2 * total_sf[None, :] * torch.sin(qr_product) / qr_product

    total_rdf = torch.trapz(integrand, q_bins) / ((2 * torch.pi)**3 * total_density)

    return total_rdf