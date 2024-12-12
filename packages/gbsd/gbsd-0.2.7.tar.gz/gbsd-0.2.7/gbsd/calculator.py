from typing import Callable
import time

from ase import Atoms
from ase.calculators.calculator import Calculator, all_properties
import torch
import numpy as np

from .spectra import get_cell_volume


class GBSDCalculator(Calculator):
    implemented_properties = ['energy', 'free_energy', 'forces', 'stress']

    def __init__(
        self,
        energy_method: Callable[[torch.Tensor, list[str], torch.Tensor], torch.Tensor],
        device: torch.device | str | None = None,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.energy_method = energy_method
        self.device = device

        self._time_spent_converting = 0.

    # def _move_to_device_and_time(self, array: np.ndarray) -> torch.Tensor:
    #     start_time = time.perf_counter()
    #     tensor = torch.from_numpy(array).to(self.device)
    #     self._time_spent_converting += time.perf_counter() - start_time

    #     return tensor
    
    # def _move_to_cpu_and_time(self, tensor: torch.Tensor) -> np.ndarray:
    #     start_time = time.perf_counter()
    #     array = tensor.numpy(force=True)
    #     self._time_spent_converting += time.perf_counter() - start_time

    #     return array

    def calculate(
        self,
        atoms: Atoms | None = None,
        properties: list[str] | None = None,
        system_changes: list[str] | None = None,
    ) -> None:
        super().calculate(atoms, properties, system_changes)

        properties = properties or all_properties

        if atoms is None:
            raise ValueError("No atoms.")
        
        fractional_positions = torch.from_numpy(atoms.get_scaled_positions()).to(self.device)
        species = atoms.get_chemical_symbols()
        cell = torch.from_numpy(atoms.get_cell().array).to(self.device)
        
        strain = torch.zeros_like(cell, requires_grad=True)
        cell = cell @ (torch.eye(3, device=self.device) + strain)

        positions = fractional_positions @ cell

        energy = self.energy_method(positions, species, cell)
        if "energy" in properties:
            self.results.update(energy=float(energy))

        if "free_energy" in properties:
            self.results.update(free_energy=float(energy))

        if "forces" in properties:
            forces = - torch.autograd.grad(energy, positions)[0]
            self.results.update(forces=forces.numpy(force=True))

        if "stress" in properties:
            stress = (1 / get_cell_volume(cell)) * torch.autograd.grad(energy, strain)[0]
            self.results.update(stress=stress.numpy(force=True).flat[[0, 4, 8, 5, 2, 1]])  # voigt stress
