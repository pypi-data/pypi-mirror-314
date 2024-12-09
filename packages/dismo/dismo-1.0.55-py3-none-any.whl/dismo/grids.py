from __future__ import annotations

__all__ = [
    "AbstractGrid",
    "HexGrid",
    "RodGrid",
    "SquareGrid",
    "SquareGrid",
    "SquareGrid",
]

import copy
import itertools
import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Self, Type, cast

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from numpy.typing import NDArray

from .coordinates import Cube3D, Oddq, Rod, Square, Triangle, _RegularPolygon


@dataclass
class AbstractGrid(ABC):
    """General grid model representation"""

    gridsize: tuple[int, ...]
    cells: NDArray = field(default_factory=lambda: np.empty(0))
    variables: list[str] = field(default_factory=list)
    neighbors: dict[tuple[str, str], NDArray] = field(default_factory=dict)
    celltype_indices: dict[str, NDArray] = field(default_factory=dict)
    celltypes: dict[str, int] = field(default_factory=dict)
    initialized: bool = True
    _is_celltype_array: dict[str, list[bool]] = field(default_factory=dict)
    _base_shape: Type[_RegularPolygon] = _RegularPolygon  # type: ignore
    _n_neighbors: int = field(default=0)

    def __post_init__(self) -> None:
        self.initialized = True
        if self.cells.shape == (0,):
            self.cells = np.zeros(self.gridsize, dtype="int")

    @abstractmethod
    def plot_axes(
        self,
        figsize: tuple[int, int] | None = None,
        ax: Axes | None = None,
    ) -> tuple[Figure, Axes]:
        ...

    def copy(self) -> Self:
        return copy.deepcopy(self)

    def add_celltype(self, name: str, value: int) -> None:
        self.celltypes[name] = value
        self.celltype_indices[name] = np.empty(0)
        self._is_celltype_array[name] = []
        self.initialized = False

    def add_cell(self, coordinates: tuple[int, ...], celltype: str) -> None:
        self.cells[coordinates] = self.celltypes[celltype]
        self.initialized = False

    def remove_cell(self, coordinates: tuple[int, ...]) -> None:
        self.cells[coordinates] = 0
        self.initialized = False

    def add_variable(self, variable_name: str) -> None:
        if variable_name not in self.variables:
            self.variables.append(variable_name)
            self.initialized = False

    def get_celltypes(self) -> dict[str, int]:
        return self.celltypes

    def get_index_of_coordinates(self, coordinates: tuple[int, ...]) -> Any:
        return np.ravel_multi_index(coordinates, self.gridsize)

    def get_coordinates_of_index(self, index: int) -> tuple[int, ...]:
        return np.unravel_index(index, self.gridsize)  # type: ignore

    def get_indices_of_celltype(self, celltype: str) -> list[int]:
        type_value = self.celltypes[celltype]
        return [
            self.get_index_of_coordinates(i)  # type: ignore
            for i in zip(*np.where(self.cells == type_value))
        ]

    def get_celltype_of_index(self, index: int) -> NDArray:
        return self.cells[self.get_coordinates_of_index(index)]  # type: ignore

    def get_cell_neighbors(self, idx: int) -> NDArray:
        """Fills empty positions with -1"""
        upper_borders = self.cells.shape
        neighbors = np.full(self._n_neighbors, -1)
        for idx, neighbor in enumerate(
            self._base_shape(*self.get_coordinates_of_index(idx)).neighbors()
        ):
            neighbor_coordinates = neighbor.grid_coordinates
            if any((i < 0 for i in neighbor_coordinates)):
                pass
            elif any((i >= j for i, j in zip(neighbor_coordinates, upper_borders))):
                pass
            elif self.cells[neighbor_coordinates] != 0:
                neighbors[idx] = self.get_index_of_coordinates(neighbor_coordinates)
        return neighbors

    def get_cell_neighbors_of_celltype(self, idx: int, celltype: str) -> NDArray:
        ct = self.celltypes[celltype]
        neighbors = np.full(self._n_neighbors, -1)
        for idx, i in enumerate(self.get_cell_neighbors(idx)):
            if i != -1:
                if self.cells[self.get_coordinates_of_index(i)] == ct:
                    neighbors[idx] = i
        return neighbors

    def get_all_neighbors_of_celltype(
        self, celltype: str, neighbor_celltype: str
    ) -> NDArray:
        arr = np.full((np.prod(self.gridsize), self._n_neighbors), -1)
        for idx in self.get_indices_of_celltype(celltype):
            arr[idx] = self.get_cell_neighbors_of_celltype(idx, neighbor_celltype)
        return arr

    def nearest_neighbor_of_celltype(
        self, cell: tuple[int, ...], neighbor_celltype: str
    ) -> float:
        start = self._base_shape(*cell)
        return min(
            [
                start.distance(self._base_shape(*cr))
                for cr in zip(
                    *np.where((self.cells == self.celltypes[neighbor_celltype]))
                )
            ]
        )

    def nearest_distances_of_celltypes(
        self, celltype1: str, celltype2: str
    ) -> list[float]:
        return [
            self.nearest_neighbor_of_celltype(cr, celltype2)
            for cr in zip(*np.where((self.cells == self.celltypes[celltype1])))
        ]

    def initialize(self) -> None:
        """
        All functions need boolean arrays of cells
        Diffusion and active transport further need neighbor arrays
        """
        # Generate celltype indices
        for celltype in self.celltypes:
            self.celltype_indices[celltype] = np.array(
                self.get_indices_of_celltype(celltype)
            )
            # FIXME: pyo3 doesn't like the boolean array
            self._is_celltype_array[celltype] = [
                bool(i) for i in (self.cells.flatten() == self.celltypes[celltype])
            ]

        # Generate neighbor arrays
        for in_celltype in self.celltypes:
            for out_celltype in self.celltypes:
                self.neighbors[
                    in_celltype, out_celltype
                ] = self.get_all_neighbors_of_celltype(in_celltype, out_celltype)
        self.initialized = True

    def generate_initial_values(self) -> NDArray:
        # Let's start with a simple: Everything is zero ;)
        return np.zeros((*self.gridsize, len(self.variables))).flatten()

    def plot_cell(
        self,
        coordinates: tuple[int, ...],
        ax: Axes,
        facecolor: str | tuple[float, float, float, float] = "C1",
        edgecolor: str | tuple[float, float, float, float] = (0, 0, 0, 1),
    ) -> None:
        self._base_shape(*coordinates).plot(
            ax=ax, facecolor=facecolor, edgecolor=edgecolor
        )

    def plot_grid(self, ax: Axes) -> None:
        cols, rows = self.cells.shape
        for cr in itertools.product(range(cols), range(rows)):
            self.plot_cell(cr, facecolor=(0.50, 0.50, 0.50, 1 / 16), ax=ax)

    def plot_cell_coordinates(self, ax: Axes, fontsize: int = 14) -> None:
        for coordinates in itertools.product(*(range(var) for var in self.cells.shape)):
            ax.text(
                *self._base_shape(*coordinates).to_plot_coordinates(),  # type: ignore
                s=f"{coordinates}",
                fontsize=fontsize,
                ha="center",
                va="center",
            )

    def plot_cell_concentration(
        self,
        ax: Axes,
        concentrations: NDArray,
        **kwargs: dict[str, Any],
    ) -> None:
        coordinates: tuple[int, int]
        concentrations = concentrations.reshape(self.gridsize)
        for coordinates in zip(*np.where(self.cells != 0)):  # type: ignore
            ax.text(
                *self._base_shape(*coordinates).to_plot_coordinates(),  # type: ignore
                s=f"{concentrations[coordinates]:.2g}",
                **{"ha": "center", "fontsize": 12} | kwargs,  # type: ignore
            )


@dataclass
class RodGrid(AbstractGrid):
    _base_shape: Type[Rod] = Rod
    _n_neighbors: int = 2

    def plot_axes(
        self,
        figsize: tuple[int, int] | None = None,
        ax: Axes | None = None,
    ) -> tuple[Figure, Axes]:
        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=figsize)
            ax = cast(Axes, ax)
        else:
            fig = cast(Figure, ax.get_figure())
        ax.set_aspect("equal")

        def pad(x: float) -> float:
            return x * 1.04

        ax.set_xlim(pad(-0.5), (self.cells.shape[0] + 0.5))
        ax.set_ylim(pad(-0.5), 0.5)
        ax.axis("off")
        return fig, ax

    def plot_grid(self, ax: Axes) -> None:
        cols = self.cells.shape[0]
        for col in range(cols):
            self.plot_cell((col,), facecolor=(0.50, 0.50, 0.50, 1 / 16), ax=ax)

    def plot_cell_coordinates(self, ax: Axes, fontsize: int = 14) -> None:
        for coordinates in range(self.cells.shape[0]):
            ax.text(
                *self._base_shape(coordinates).to_plot_coordinates(),  # type: ignore
                s=f"{coordinates}",
                fontsize=fontsize,
                ha="center",
                va="center",
            )


@dataclass
class TriGrid(AbstractGrid):
    _base_shape: Type[Triangle] = Triangle
    _n_neighbors: int = 3

    def plot_axes(
        self,
        figsize: tuple[int, int] | None = None,
        ax: Axes | None = None,
    ) -> tuple[Figure, Axes]:
        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=figsize)
            ax = cast(Axes, ax)
        else:
            fig = cast(Figure, ax.get_figure())
        ax.set_aspect("equal")

        c, r = self.cells.shape
        base_shape = cast(Triangle, self._base_shape(0, 0))
        x_offset = base_shape.x_offset
        y_offset = base_shape.y_offset
        x_lower = -x_offset
        x_upper = 0.5 * c
        y_lower = -y_offset
        y_upper = r * base_shape.h - y_offset
        ax.set_xlim(x_lower, x_upper)
        ax.set_ylim(y_lower, y_upper)
        ax.axis("off")
        return fig, ax


@dataclass
class SquareGrid(AbstractGrid):
    _base_shape: Type[Square] = Square
    _n_neighbors: int = 4

    def plot_axes(
        self,
        figsize: tuple[int, int] | None = None,
        ax: Axes | None = None,
    ) -> tuple[Figure, Axes]:
        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=figsize)
            ax = cast(Axes, ax)
        else:
            fig = cast(Figure, ax.get_figure())
        ax.set_aspect("equal")

        c, r = self.cells.shape
        x_offset = self._base_shape(0, 0).x_offset
        y_offset = self._base_shape(0, 0).y_offset

        x_lower = -x_offset - 0.1
        x_upper = c - x_offset + 0.1
        y_lower = -y_offset - 0.1
        y_upper = r - y_offset + 0.1
        ax.set_xlim(x_lower, x_upper)
        ax.set_ylim(y_lower, y_upper)
        ax.axis("off")
        return fig, ax


@dataclass
class HexGrid(AbstractGrid):
    _base_shape: Type[Oddq] = Oddq
    _n_neighbors: int = 6

    def plot_axes(
        self,
        figsize: tuple[int, int] | None = None,
        ax: Axes | None = None,
    ) -> tuple[Figure, Axes]:
        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=figsize)
            ax = cast(Axes, ax)
        else:
            fig = cast(Figure, ax.get_figure())
        ax.set_aspect("equal")

        c, r = self.cells.shape
        x_lower = -1
        x_upper = 1 + 3 / 2 * (c - 1)
        y_lower = -math.sqrt(3) * 0.5
        y_upper = math.sqrt(3) * r
        ax.set_xlim(x_lower, x_upper)
        ax.set_ylim(y_lower, y_upper)
        ax.axis("off")
        return fig, ax


@dataclass
class CubeGrid(AbstractGrid):
    _base_shape: Type[Cube3D] = Cube3D
    _n_neighbors: int = 6

    def plot_axes(
        self,
        figsize: tuple[int, int] | None = None,
        ax: Axes | None = None,
    ) -> tuple[Figure, Axes]:
        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=figsize, subplot_kw={"projection": "3d"})
            ax = cast(Axes, ax)
        else:
            fig = cast(Figure, ax.get_figure())

        a, b, c = self.cells.shape
        ax.set_xlim(0, a)
        ax.set_ylim(0, b)
        ax.set_zlim(0, c)  # type: ignore
        ax.axis("off")
        return fig, ax

    def plot_grid(
        self,
        ax: Axes,
        facecolor: str | tuple[float, float, float, float] = (0.50, 0.50, 0.50, 1 / 16),
        edgecolor: str | tuple[float, float, float, float] = (0, 0, 0, 1 / 16),
    ) -> None:
        x, y, z = self.cells.shape
        for xyz in itertools.product(range(x), range(y), range(z)):
            self.plot_cell(xyz, facecolor=facecolor, edgecolor=edgecolor, ax=ax)
