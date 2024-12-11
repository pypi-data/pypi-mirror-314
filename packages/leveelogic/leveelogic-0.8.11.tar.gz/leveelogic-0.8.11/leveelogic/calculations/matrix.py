import numpy as np
from enum import IntEnum
from typing import Tuple

import matplotlib.pyplot as plt


class PlotValueEnum(IntEnum):
    C = 1
    PHI = 2
    SIGMA_V = 10
    SIGMA_V_EFF = 11
    U = 12
    TAU = 20


PLOTVALUE_TITLES = {
    PlotValueEnum.C: "Cohesion [kPa]",
    PlotValueEnum.PHI: "Friction angle [deg]",
    PlotValueEnum.SIGMA_V: "Total stress [kPa]",
    PlotValueEnum.SIGMA_V_EFF: "Effective stress [kPa]",
    PlotValueEnum.U: "Waterpressure [kPa]",
    PlotValueEnum.TAU: "Schuifspanning [kPa]",
}


class Matrix:
    def __init__(self, left: float, top: float, numx: int, numz: int, gridsize: float):
        self.left = left
        self.top = top
        self.gridsize = gridsize
        # self.x = np.empty((numx, numz), np.float64)
        # self.z = np.empty((numx, numz), np.float64)
        self.c = np.zeros((numz, numx), np.float64)
        self.phi = np.zeros((numz, numx), np.float64)
        self.below_pl = np.empty((numz, numx), np.bool)
        self.sigma_v = np.zeros((numz, numx), np.float64)
        self.sigma_eff_v = np.zeros((numz, numx), np.float64)
        self.u = np.zeros((numz, numx), np.float64)
        self.tau = np.zeros((numz, numx), np.float64)

        self.num_columns = numz
        self.num_rows = numx

        # for x in range(numx):
        #     for z in range(numz):
        #         self.x[x, z] = left + (x + 0.5) * gridsize
        #         self.z[x, z] = top - (z - 0.5) * gridsize

    def post_process(self) -> None:
        self.tau = self.c + self.sigma_eff_v * np.tan(np.radians(self.phi))

    def x_at(self, x: int) -> float:
        return self.left + (x + 0.5) * self.gridsize

    def z_at(self, z: int) -> float:
        return self.top - (z + 0.5) * self.gridsize

    def c_at(self, x: float) -> int:
        return int((x - self.left) / self.gridsize)

    def r_at(self, z: float) -> int:
        return int((self.top - z) / self.gridsize)

    # debug
    def plot_below_pl(self):
        masked_matrix = np.ma.masked_where(self.below_pl == 0, self.below_pl)
        plt.imshow(masked_matrix)
        plt.colorbar()
        plt.title("Onder water")
        plt.show()

    def plot(self, plot_value: PlotValueEnum = PlotValueEnum.SIGMA_V_EFF):
        if plot_value == PlotValueEnum.C:
            m = self.c
        elif plot_value == PlotValueEnum.PHI:
            m = self.phi
        elif plot_value == PlotValueEnum.PHI:
            m = self.phi
        elif plot_value == PlotValueEnum.SIGMA_V:
            m = self.sigma_v
        elif plot_value == PlotValueEnum.SIGMA_V_EFF:
            m = self.sigma_eff_v
        elif plot_value == PlotValueEnum.TAU:
            m = self.tau

        masked_matrix = np.ma.masked_where(m == 0, m)
        plt.imshow(masked_matrix, cmap="rainbow")
        plt.colorbar()
        plt.title(PLOTVALUE_TITLES[plot_value])
        plt.show()

    def plot_stresses(self, x):
        c = self.c_at(x)
        z = [self.top - (i + 0.5) * self.gridsize for i in range(self.num_columns)]
        s_v = self.sigma_v[:, c]
        s_v_eff = self.sigma_eff_v[:, c]
        u = self.u[:, c]
        plt.plot(s_v, z, "k", label="totaalspanning [kPa]")
        plt.plot(u, z, "b", label="waterspanning [kPa]")
        plt.plot(s_v_eff, z, "k--", label="effectieve spanning [kPa]")
        plt.grid(which="both")
        plt.legend()
        plt.show()

    def bishop(self, M: Tuple[float, float], r: float):
        xc = M[0]
        zc = M[1]
