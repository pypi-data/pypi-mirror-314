import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Rectangle
from typing import List, Optional, Tuple

from ..models.datamodel import DataModel
from .soillayer import SoilLayer
from .soilcollection import SoilCollection


class Stresses(DataModel):
    z: List[float] = []
    s_tot: List[float] = []
    u: List[float] = []
    s_eff: List[float] = []

    @property
    def phreatic_level(self) -> Optional[float]:
        for i in range(1, len(self.u)):
            u1 = self.u[i - 1]
            u2 = self.u[i]
            if u1 != u2:
                return self.z[i - 1]
        return None

    def add(self, z: float, s_tot: float, u: float):
        self.z.append(z)
        self.s_tot.append(s_tot)
        self.u.append(u)
        self.s_eff.append(max(0, s_tot - u))

    def at(self, z: float) -> Tuple[float, float, float, float]:  # z, s_tot, u, s_eff
        for i in range(1, len(self.z)):
            z1 = self.z[i - 1]
            z2 = self.z[i]

            if z1 >= z and z2 <= z:
                s_tot1 = self.s_tot[i - 1]
                s_tot2 = self.s_tot[i]
                u1 = self.u[i - 1]
                u2 = self.u[i]
                stot = s_tot1 + (z1 - z) / (z1 - z2) * (s_tot2 - s_tot1)
                u = u1 + (z1 - z) / (z1 - z2) * (u2 - u1)
                return (z, stot, u, max(0, stot - u))

        raise ValueError(
            f"No stresses found at z={z:.2f}, z;max={self.z[0]:.2f}, z;min={self.z[-1]:.2f}"
        )

    def plot(
        self, soillayers: List[SoilLayer] = [], soilcollection: SoilCollection = None
    ):
        fig = plt.figure(figsize=(10, 5))

        if len(soillayers) > 0:
            gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
        else:
            gs = gridspec.GridSpec(1, 1, width_ratios=[1])

        ax1 = fig.add_subplot(gs[0, 0])

        ax1.plot(self.s_tot, self.z, "k", label="totaalspanning [kPa]")
        ax1.plot(self.u, self.z, "b", label="waterspanning [kPa]")
        ax1.plot(self.s_eff, self.z, "k--", label="effectieve spanning [kPa]")

        pl = self.phreatic_level
        if pl is not None:
            ax1.plot([0, max(self.s_tot)], [pl, pl], "b--", label="freatisch niveau")

        if len(soillayers) > 0 and soilcollection is not None:
            ax2 = fig.add_subplot(gs[0, 1], sharey=ax1)

            soilcolors = soilcollection.get_color_dict()
            for layer in soillayers:
                soil = soilcollection.get(layer.soilcode)
                color = soilcolors[soil.code.lower()]
                p = Rectangle(
                    xy=(0, layer.bottom),
                    width=1,
                    height=layer.height,
                    facecolor=color,
                    edgecolor="k",
                )
                ax2.add_patch(p)
                ax2.text(0.1, layer.mid, f"yd={soil.yd:.2f}, ys={soil.ys:.2f}")
            if pl is not None:
                ax2.plot([0, 1], [pl, pl], "b--")
            ax2.grid(axis="y")

        ax1.grid(which="both")
        ax1.legend()
        plt.tight_layout()
        plt.show()
