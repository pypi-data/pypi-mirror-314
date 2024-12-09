from __future__ import annotations

import warnings
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, cast

import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from numpy.typing import NDArray

from .grids import AbstractGrid

Array = NDArray[np.float64]


try:  # pragma: no cover
    from assimulo.problem import Explicit_Problem
    from assimulo.solvers import CVode

    def _simulate(
        fn: Callable[[float, Array], Array],
        y0: Array,
        t_end: float,
        t_points: int = 0,
        t_eval: Array | None = None,
    ) -> tuple[Array, Array]:
        problem = Explicit_Problem(fn, y0)
        integrator = CVode(problem)
        integrator.verbosity = 50
        t, y = integrator.simulate(t_end, t_points, t_eval)
        return np.array(t), np.array(y)

except (ImportError, ModuleNotFoundError):  # pragma: no cover
    import scipy.integrate

    warnings.warn("Assimulo not found, disabling sundials support.")

    def _simulate(
        fn: Callable[[float, Array], Array],
        y0: Array,
        t_end: float,
        t_points: int = 0,
        t_eval: Array | None = None,
    ) -> tuple[Array, Array]:
        if t_eval is None:
            if t_points > 0:
                t = np.linspace(0, t_end, t_points)
            else:
                t = np.linspace(0, t_end, 100)
        else:
            t = t_eval
        y = scipy.integrate.odeint(fn, y0, t, tfirst=True)
        return np.array(t), np.array(y)


try:  # pragma: no cover
    # from pde_perffuncs import diffusion_nonavg  # type: ignore
    raise ImportError
except ImportError:  # pragma: no cover

    def diffusion(
        y0: Array,
        is_celltype: list[bool],
        celltype_neighbors: NDArray[np.int64],  # list[list[int]]
        alpha: float,
        n_neighbors: float,
    ) -> Array:
        dydt = np.zeros_like(y0, dtype=float)
        for cell, cell_conc in enumerate(y0):
            if not is_celltype[cell]:
                continue
            diff = 0.0
            for neighbor in celltype_neighbors[cell]:
                if neighbor == -1:
                    continue
                diff += y0[neighbor] - cell_conc
            dydt[cell] += diff / n_neighbors * alpha
        return dydt

    def diffusion_nonavg(
        y0: Array,
        is_celltype: list[bool],
        celltype_neighbors: NDArray[np.int64],  # list[list[int]]
        alpha: float,
    ) -> Array:
        dydt = np.zeros_like(y0, dtype=float)
        for cell, cell_conc in enumerate(y0):
            if not is_celltype[cell]:
                continue
            diff = 0.0
            for neighbor in celltype_neighbors[cell]:
                if neighbor == -1:
                    continue
                diff += y0[neighbor] - cell_conc
            dydt[cell] += diff * alpha
        return dydt

    def diffusion_active(
        y0: Array,
        is_celltype: list[bool],
        celltype_neighbors: NDArray[np.int64],  # list[list[int]]
        alpha: float,
    ) -> Array:
        dydt = np.zeros_like(y0, dtype=float)
        for cell, cell_conc in enumerate(y0):
            if not is_celltype[cell]:
                continue
            for neighbor in celltype_neighbors[cell]:
                if neighbor == -1:
                    continue
                diff = (y0[neighbor] - cell_conc) * alpha
                if diff < 0:
                    dydt[cell] += diff  # mesophyll cell
                    dydt[neighbor] -= diff  # vein cell
        return dydt


def photosynthesis_saturating(sugar: Array, k: float, capacity: float) -> Array:
    return k * (1 - sugar / capacity)


def photosynthesis_saturating_co2(
    sugar: Array, co2: Array, k: float, capacity: float
) -> Array:
    return k * co2 * (1 - sugar / capacity)


def outflux(sugar: Array, alpha: float) -> Array:
    return -sugar * alpha


@dataclass
class AbstractModel(ABC):
    grid: AbstractGrid

    @abstractmethod
    def _get_right_hand_side(self, t: float, y0: Array) -> Array: ...

    def simulate(
        self,
        y0: Array,
        t_end: float | None = None,
        t_points: int = 0,
        t_eval: Array | None = None,
    ) -> tuple[Array, ...]:
        if t_end is None:
            if t_eval is None:
                raise ValueError("Either `t_end` or `t_eval` needs to be supplied")
            t_end = t_eval[-1]

        self.grid.initialize()

        # Do test run for better error messages
        self._get_right_hand_side(0, y0)

        t, y = _simulate(
            self._get_right_hand_side,
            y0,
            cast(float, t_end),
            t_points,
            t_eval,
        )
        n_vars = len(self.grid.variables)
        if n_vars < 2:
            return t, y
        else:
            return t, *np.split(y, n_vars, axis=1)


@dataclass
class MesophyllModel(AbstractModel):
    ps_k: float
    ps_capacity: float
    suc_meso_to_meso: float

    def __post_init__(self) -> None:
        self.grid.add_celltype("mesophyll", 1)
        self.grid.add_variable("sucrose")

    def _create_variables(self, y: Array) -> tuple[dict[str, Array], dict[str, Array]]:
        in_vars = dict(zip(self.grid.variables, np.hsplit(y, len(self.grid.variables))))
        out_vars = {
            i: np.zeros(self.grid.gridsize, dtype=float).flatten()
            for i in self.grid.variables
        }
        return in_vars, out_vars

    def _get_influxes(
        self, in_vars: dict[str, Array], out_vars: dict[str, Array]
    ) -> None:
        mesophyll_cells = self.grid.celltype_indices["mesophyll"]
        dydt = photosynthesis_saturating(
            in_vars["sucrose"][mesophyll_cells], self.ps_k, self.ps_capacity
        )
        out_vars["sucrose"][mesophyll_cells] += dydt

    def get_influxes_by_process(self, y: Array) -> dict[str, dict[str, Array]]:
        self.grid.initialize()
        mesophyll_cells = self.grid.celltype_indices["mesophyll"]
        in_vars, out_vars = self._create_variables(y)
        return {
            "sucrose": {
                "photosynthesis": photosynthesis_saturating(
                    in_vars["sucrose"][mesophyll_cells], self.ps_k, self.ps_capacity
                )
            }
        }

    def get_influxes(self, y: Array) -> dict[str, Array]:
        self.grid.initialize()
        in_vars, out_vars = self._create_variables(y)
        self._get_influxes(in_vars, out_vars)
        return out_vars

    def _get_diffusion_processes(
        self, in_vars: dict[str, Array], out_vars: dict[str, Array]
    ) -> None:
        mesophyll_cells = self.grid._is_celltype_array["mesophyll"]
        meso_to_meso = self.grid.neighbors["mesophyll", "mesophyll"]

        out_vars["sucrose"] += diffusion_nonavg(
            y0=in_vars["sucrose"],
            is_celltype=mesophyll_cells,
            celltype_neighbors=meso_to_meso,
            alpha=self.suc_meso_to_meso,
        )

    def get_diffusion_by_process(self, y: Array) -> dict[str, dict[str, Array]]:
        self.grid.initialize()
        in_vars, _ = self._create_variables(y)
        mesophyll_cells = self.grid._is_celltype_array["mesophyll"]
        meso_to_meso = self.grid.neighbors["mesophyll", "mesophyll"]
        return {
            "sucrose": {
                "meso_to_meso": diffusion_nonavg(
                    y0=in_vars["sucrose"],
                    is_celltype=mesophyll_cells,
                    celltype_neighbors=meso_to_meso,
                    alpha=self.suc_meso_to_meso,
                ),
            }
        }

    def get_diffusion(self, y: Array) -> dict[str, Array]:
        self.grid.initialize()
        in_vars, out_vars = self._create_variables(y)
        self._get_diffusion_processes(in_vars, out_vars)
        return out_vars

    def _get_right_hand_side(self, t: float, y: Array) -> Array:
        in_vars, out_vars = self._create_variables(y)
        self._get_influxes(in_vars, out_vars)
        self._get_diffusion_processes(in_vars, out_vars)
        return np.array(list(out_vars.values())).flatten()

    def get_right_hand_side(self, y: Array) -> Array:
        self.grid.initialize()
        return self._get_right_hand_side(0, y)

    def add_mesophyll_cell(self, coordinates: tuple[int, ...]) -> None:
        self.grid.add_cell(coordinates=coordinates, celltype="mesophyll")

    def _plot_all_celltypes(
        self, ax: Axes, normalized_concentrations: Array, alpha: float | None
    ) -> None:
        self._plot_mesophyll_cells(
            ax=ax,
            normalized_concentrations=normalized_concentrations,
            alpha=alpha,
        )

    def _plot_mesophyll_cells(
        self, ax: Axes, normalized_concentrations: Array, alpha: float | None
    ) -> None:
        for cr in zip(*np.where(self.grid.cells == 1)):
            if alpha is None:
                al = max(normalized_concentrations[cr], 0.05)  # type: ignore
            else:
                al = alpha
            self.grid.plot_cell(
                cr,
                facecolor=(0.00, 0.50, 0.00, al),
                edgecolor=(0, 0, 0, 1),
                ax=ax,
            )

    def plot_cells(
        self,
        ax: Axes,
        concentrations: Array | None = None,
        min_conc: float = 0.0,
        max_conc: float | None = None,
        alpha: float | None = None,
    ) -> Axes:
        if concentrations is None:
            concentrations = np.ones(self.grid.gridsize)
            min_conc = 0.0
            max_conc = 1.0

        if max_conc is None:
            max_conc = cast(float, np.max(concentrations))
        if min_conc == max_conc:
            max_conc += 0.1
        self._plot_all_celltypes(
            ax=ax,
            normalized_concentrations=(
                (concentrations - min_conc) / (max_conc - min_conc)
            ).reshape(self.grid.gridsize),
            alpha=alpha,
        )

        return ax

    def plot(
        self,
        concentrations: Array | None = None,
        min_conc: float = 0.0,
        max_conc: float | None = None,
        figsize: tuple[int, int] = (10, 10),
        ax: Axes | None = None,
        annotate: bool = False,
        alpha: float | None = None,
    ) -> tuple[Figure, Axes]:
        fig, ax = self.grid.plot_axes(figsize=figsize, ax=ax)
        ax = self.plot_cells(ax, concentrations, min_conc, max_conc, alpha)
        if annotate:
            if concentrations is None:
                raise ValueError("Supply concentrations when using annotate")
            self.grid.plot_cell_concentration(ax, concentrations)
        return fig, ax


@dataclass(kw_only=True)
class VeinModel(MesophyllModel):
    vein_base_coordinates: tuple[int, ...]
    suc_vein_to_vein: float
    suc_meso_to_vein: float
    _vein_base_idx: int = 0

    def __post_init__(self) -> None:
        super().__post_init__()

        self.grid.add_celltype("vein", 2)
        self._vein_base_idx = self.grid.get_index_of_coordinates(
            self.vein_base_coordinates
        )
        self.add_vein_cell(self.vein_base_coordinates)

    def _get_diffusion_processes(
        self, in_vars: dict[str, Array], out_vars: dict[str, Array]
    ) -> None:
        mesophyll_cells = self.grid._is_celltype_array["mesophyll"]
        vein_cells = self.grid._is_celltype_array["vein"]

        meso_to_meso = self.grid.neighbors["mesophyll", "mesophyll"]
        meso_to_vein = self.grid.neighbors["mesophyll", "vein"]
        vein_to_vein = self.grid.neighbors["vein", "vein"]

        out_vars["sucrose"] += diffusion_nonavg(
            y0=in_vars["sucrose"],
            is_celltype=mesophyll_cells,
            celltype_neighbors=meso_to_meso,
            alpha=self.suc_meso_to_meso,
        )
        out_vars["sucrose"] += diffusion_active(
            y0=in_vars["sucrose"],
            is_celltype=mesophyll_cells,
            celltype_neighbors=meso_to_vein,
            alpha=self.suc_meso_to_vein,
        )
        out_vars["sucrose"] += diffusion_nonavg(
            y0=in_vars["sucrose"],
            is_celltype=vein_cells,
            celltype_neighbors=vein_to_vein,
            alpha=self.suc_vein_to_vein,
        )

    def get_diffusion_by_process(self, y: Array) -> dict[str, dict[str, Array]]:
        self.grid.initialize()
        in_vars, _ = self._create_variables(y)
        mesophyll_cells = self.grid._is_celltype_array["mesophyll"]
        vein_cells = self.grid._is_celltype_array["vein"]

        meso_to_meso = self.grid.neighbors["mesophyll", "mesophyll"]
        meso_to_vein = self.grid.neighbors["mesophyll", "vein"]
        vein_to_vein = self.grid.neighbors["vein", "vein"]
        return {
            "sucrose": {
                "meso_to_meso": diffusion_nonavg(
                    y0=in_vars["sucrose"],
                    is_celltype=mesophyll_cells,
                    celltype_neighbors=meso_to_meso,
                    alpha=self.suc_meso_to_meso,
                ),
                "meso_to_vein": diffusion_active(
                    y0=in_vars["sucrose"],
                    is_celltype=mesophyll_cells,
                    celltype_neighbors=meso_to_vein,
                    alpha=self.suc_meso_to_vein,
                ),
                "vein_to_vein": diffusion_nonavg(
                    y0=in_vars["sucrose"],
                    is_celltype=vein_cells,
                    celltype_neighbors=vein_to_vein,
                    alpha=self.suc_vein_to_vein,
                ),
            }
        }

    def _get_outfluxes(
        self, in_vars: dict[str, Array], out_vars: dict[str, Array]
    ) -> None:
        out_vars["sucrose"][self._vein_base_idx] += outflux(
            in_vars["sucrose"][self._vein_base_idx],
            self.suc_vein_to_vein,
        )

    def get_outfluxes(self, y: Array) -> dict[str, Array]:
        self.grid.initialize()
        in_vars, out_vars = self._create_variables(y)
        self._get_outfluxes(in_vars, out_vars)
        return out_vars

    def _get_right_hand_side(self, t: float, y: Array) -> Array:
        in_vars, out_vars = self._create_variables(y)
        self._get_influxes(in_vars, out_vars)
        self._get_diffusion_processes(in_vars, out_vars)
        self._get_outfluxes(in_vars, out_vars)
        return np.array(list(out_vars.values())).flatten()

    def add_vein_cell(self, coordinates: tuple[int, ...]) -> None:
        self.grid.add_cell(coordinates=coordinates, celltype="vein")

    def get_vein_outflux(self, y: Array) -> Array:
        self.grid.initialize()
        """Get vein outflux for a single concentration array"""

        if y.ndim > 1:
            return -outflux(
                y[:, self._vein_base_idx],
                self.suc_vein_to_vein,
            )
        return -outflux(
            y[self._vein_base_idx],
            self.suc_vein_to_vein,
        )

    def _plot_vein_cells(
        self, ax: Axes, normalized_concentrations: Array, alpha: float | None
    ) -> None:
        for cr in zip(*np.where(self.grid.cells == 2)):
            if alpha is None:
                al = max(normalized_concentrations[cr], 0.05)  # type: ignore
            else:
                al = alpha
            self.grid.plot_cell(
                cr,
                facecolor=(0.30, 0.15, 0.03, al),
                edgecolor=(0, 0, 0, 1),
                ax=ax,
            )

    def _plot_all_celltypes(
        self, ax: Axes, normalized_concentrations: Array, alpha: float | None
    ) -> None:
        self._plot_mesophyll_cells(
            ax=ax,
            normalized_concentrations=normalized_concentrations,
            alpha=alpha,
        )
        self._plot_vein_cells(
            ax=ax,
            normalized_concentrations=normalized_concentrations,
            alpha=alpha,
        )


@dataclass(kw_only=True)
class StomataModel(VeinModel):
    co2_k: float
    co2_capacity: float
    co2_stoma_to_meso: float
    co2_meso_to_meso: float

    def __post_init__(self) -> None:
        super().__post_init__()

        self.grid.add_celltype("stoma", 3)
        self.grid.add_variable("co2")

    def _get_influxes(
        self, in_vars: dict[str, Array], out_vars: dict[str, Array]
    ) -> None:
        mesophyll_cells = self.grid.celltype_indices["mesophyll"]
        stoma_cells = self.grid.celltype_indices["stoma"]

        # Sucrose processes
        dydt = photosynthesis_saturating_co2(
            sugar=in_vars["sucrose"][mesophyll_cells],
            co2=in_vars["co2"][mesophyll_cells],
            k=self.ps_k,
            capacity=self.ps_capacity,
        )
        out_vars["sucrose"][mesophyll_cells] += dydt
        out_vars["co2"][mesophyll_cells] -= dydt

        # CO2 processes
        out_vars["co2"][stoma_cells] += photosynthesis_saturating(
            sugar=in_vars["co2"][stoma_cells],
            k=self.co2_k,
            capacity=self.co2_capacity,
        )

    def get_influxes_by_process(self, y: Array) -> dict[str, dict[str, Array]]:
        self.grid.initialize()
        mesophyll_cells = self.grid.celltype_indices["mesophyll"]
        in_vars, out_vars = self._create_variables(y)

        mesophyll_cells = self.grid.celltype_indices["mesophyll"]
        stoma_cells = self.grid.celltype_indices["stoma"]

        return {
            "sucrose": {
                "photosynthesis": photosynthesis_saturating_co2(
                    sugar=in_vars["sucrose"][mesophyll_cells],
                    co2=in_vars["co2"][mesophyll_cells],
                    k=self.ps_k,
                    capacity=self.ps_capacity,
                ),
            },
            "co2": {
                "stomata": photosynthesis_saturating(
                    sugar=in_vars["co2"][stoma_cells],
                    k=self.co2_k,
                    capacity=self.co2_capacity,
                ),
            },
        }

    def _get_diffusion_processes(
        self, in_vars: dict[str, Array], out_vars: dict[str, Array]
    ) -> None:
        mesophyll_cells = self.grid._is_celltype_array["mesophyll"]
        vein_cells = self.grid._is_celltype_array["vein"]
        stoma_cells = self.grid._is_celltype_array["stoma"]

        meso_to_meso = self.grid.neighbors["mesophyll", "mesophyll"]
        meso_to_vein = self.grid.neighbors["mesophyll", "vein"]
        vein_to_vein = self.grid.neighbors["vein", "vein"]
        stoma_to_meso = self.grid.neighbors["stoma", "mesophyll"]

        out_vars["sucrose"] += diffusion_nonavg(
            y0=in_vars["sucrose"],
            is_celltype=mesophyll_cells,
            celltype_neighbors=meso_to_meso,
            alpha=self.suc_meso_to_meso,
        )
        out_vars["sucrose"] += diffusion_active(
            y0=in_vars["sucrose"],
            is_celltype=mesophyll_cells,
            celltype_neighbors=meso_to_vein,
            alpha=self.suc_meso_to_vein,
        )
        out_vars["sucrose"] += diffusion_nonavg(
            y0=in_vars["sucrose"],
            is_celltype=vein_cells,
            celltype_neighbors=vein_to_vein,
            alpha=self.suc_vein_to_vein,
        )
        out_vars["co2"] += diffusion_active(
            y0=in_vars["co2"],
            is_celltype=stoma_cells,
            celltype_neighbors=stoma_to_meso,
            alpha=self.co2_stoma_to_meso,
        )
        out_vars["co2"] += diffusion_nonavg(
            y0=in_vars["co2"],
            is_celltype=mesophyll_cells,
            celltype_neighbors=meso_to_meso,
            alpha=self.co2_meso_to_meso,
        )

    def get_diffusion_by_process(self, y: Array) -> dict[str, dict[str, Array]]:
        self.grid.initialize()
        in_vars, _ = self._create_variables(y)

        mesophyll_cells = self.grid._is_celltype_array["mesophyll"]
        vein_cells = self.grid._is_celltype_array["vein"]
        stoma_cells = self.grid._is_celltype_array["stoma"]

        meso_to_meso = self.grid.neighbors["mesophyll", "mesophyll"]
        meso_to_vein = self.grid.neighbors["mesophyll", "vein"]
        vein_to_vein = self.grid.neighbors["vein", "vein"]
        stoma_to_meso = self.grid.neighbors["stoma", "mesophyll"]
        return {
            "sucrose": {
                "meso_to_meso": diffusion_nonavg(
                    y0=in_vars["sucrose"],
                    is_celltype=mesophyll_cells,
                    celltype_neighbors=meso_to_meso,
                    alpha=self.suc_meso_to_meso,
                ),
                "meso_to_vein": diffusion_active(
                    y0=in_vars["sucrose"],
                    is_celltype=mesophyll_cells,
                    celltype_neighbors=meso_to_vein,
                    alpha=self.suc_meso_to_vein,
                ),
                "vein_to_vein": diffusion_nonavg(
                    y0=in_vars["sucrose"],
                    is_celltype=vein_cells,
                    celltype_neighbors=vein_to_vein,
                    alpha=self.suc_vein_to_vein,
                ),
            },
            "co2": {
                "stoma_to_meso": diffusion_active(
                    y0=in_vars["co2"],
                    is_celltype=stoma_cells,
                    celltype_neighbors=stoma_to_meso,
                    alpha=self.co2_stoma_to_meso,
                ),
                "co2_meso_to_meso": diffusion_nonavg(
                    y0=in_vars["co2"],
                    is_celltype=mesophyll_cells,
                    celltype_neighbors=meso_to_meso,
                    alpha=self.co2_meso_to_meso,
                ),
            },
        }

    def add_stoma_cell(self, coordinates: tuple[int, ...]) -> None:
        self.grid.add_cell(coordinates=coordinates, celltype="stoma")

    def _plot_stomata_cells(
        self, ax: Axes, normalized_concentrations: Array, alpha: float | None
    ) -> None:
        for cr in zip(*np.where(self.grid.cells == 3)):
            if alpha is None:
                al = max(normalized_concentrations[cr], 0.05)  # type: ignore
            else:
                al = alpha
            self.grid.plot_cell(
                cr,
                facecolor=(0.80, 0.37, 0.04, al),
                edgecolor=(0, 0, 0, 1),
                ax=ax,
            )

    def _plot_all_celltypes(
        self, ax: Axes, normalized_concentrations: Array, alpha: float | None
    ) -> None:
        self._plot_mesophyll_cells(
            ax=ax,
            normalized_concentrations=normalized_concentrations,
            alpha=alpha,
        )
        self._plot_vein_cells(
            ax=ax,
            normalized_concentrations=normalized_concentrations,
            alpha=alpha,
        )
        self._plot_stomata_cells(
            ax=ax,
            normalized_concentrations=normalized_concentrations,
            alpha=alpha,
        )
