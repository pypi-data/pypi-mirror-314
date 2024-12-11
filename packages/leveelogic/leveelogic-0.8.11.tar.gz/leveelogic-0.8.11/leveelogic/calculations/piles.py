from typing import Tuple, List
from enum import Enum

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Rectangle

from ..models.datamodel import DataModel
from ..objects.cpt import Cpt, CptInterpretationMethod
from ..objects.soilcollection import SoilCollection

QCMAX_PLOT = 25


class PileType(Enum):
    CONCRETE_PREFAB = {
        "alpha_p": 0.7,
        "alpha_s": 0.010,
        "alpha_t": 0.007,
        "lz": 1,
        "description": "Geprefabriceerd; met constante dwarsafmeting, Geheid",
    }
    CONCRETE_MANTELBUIS_VOETPLAAT_TERUGHEIEND = {
        "alpha_p": 0.7,
        "alpha_s": 0.014,
        "alpha_t": 0.012,
        "lz": 1,
        "description": "In de grond gevormd met een gladde mantelbuis op een voetplaat, waarbij het beton direct tegen de grond drukt, Geheid; de mantelbuis wordt terugheiend in combinatie met statisch trekken uit de grond verwijderd; de voetplaat blijft in de grond achter",
    }
    CONCRETE_MANTELBUIS_VOETPLAAT_TRILLEND = {
        "alpha_p": 0.7,
        "alpha_s": 0.012,
        "alpha_t": 0.010,
        "lz": 1,
        "description": "In de grond gevormd met een gladde mantelbuis op een voetplaat, waarbij het beton direct tegen drukt, Geheid; de mantelbuis wordt trillend in combinatie met statisch trekken uit degrond verwijderd; de voetplaat bijft in de grond achter",
    }
    CONCRETE_MANTELBUIS_SCHROEFPUNT = {
        "alpha_p": 0.63,
        "alpha_s": 0.009,
        "alpha_t": 0.009,
        "lz": 1,
        "description": "In de grond gevormd met een gladde mantelbuis op een schroefpunt, waarbij het beton direct tegen de grond drukt, Geschroefd; bij het trekken van de mantelbuis blijft de schroefpunt in de grond achter",
    }
    CONCRETE_AVEGAAR = {
        "alpha_p": 0.56,
        "alpha_s": 0.006,
        "alpha_t": 0.0045,
        "lz": 2,
        "description": "In de grond gevormd met behulp van een avegaar, Geschroefd",
    }
    CONCRETE_STEUNVLOEISTOF = {
        "alpha_p": 0.35,
        "alpha_s": 0.006,
        "alpha_t": 0.0045,
        "lz": 3,
        "description": "In de grond gevormd met behulp van een steunvloeistof, Gegraven of geboord",
    }
    STEEL_CONSTANT_D_CLOSED = {
        "alpha_p": 0.70,
        "alpha_s": 0.010,
        "alpha_t": 0.007,
        "lz": 1,
        "description": "Constante dwarsafmeting; buis met gesloten punt, geheid",
    }
    STEEL_CONSTANT_D_PROFIEL = {
        "alpha_p": 0.70,
        "alpha_s": 0.006,
        "alpha_t": 0.004,
        "lz": 1,
        "description": "Constante dwarsafmeting; profiel, Geheid",
    }
    STEEL_CONSTANT_D_OPEN = {
        "alpha_p": 0.70,
        "alpha_s": 0.006,
        "alpha_t": 0.004,
        "lz": 1,
        "description": "Constante dwarsafmeting; open buis, geheid",
    }
    STEEL_GROUTSCHIL_VOETPLAAT = {
        "alpha_p": 0.70,
        "alpha_s": 0.014,
        "alpha_t": 0.012,
        "lz": 1,
        "description": "In de grond gevormde groutschil rond profiel met voetplaat, Geheid; met groutinjectie",
    }
    STEEL_CONSTANT_D_GESCHROEFD = {
        "alpha_p": 0.56,
        "alpha_s": 0.006,
        "alpha_t": 0.0045,
        "lz": 1,
        "description": "Constante dwarsafmeting boven de schroefpunt, Geschroefd ",
    }
    STEEL_GROUTSCHIL_SCHROEFPUNT = {
        "alpha_p": 0.63,
        "alpha_s": 0.009,
        "alpha_t": 0.009,
        "lz": 1,
        "description": "In de grond gevormde groutschil rond buis met schroefpunt (schachtmiddellijn 300mm of groter), Geschroefd zonder de paal tijdens het aanbrengen op en neer te halen; menging van de grond met grout",
    }
    STEEL_CONSTANT_D_GEPULST = {
        "alpha_p": 0.35,
        "alpha_s": 0.005,
        "alpha_t": 0.0,
        "lz": 3,
        "description": "Constante dwarsafmeting, gepulst",
    }
    MICROPAAL_DUBBEL_NIET_AFGEPERST = {
        "alpha_p": 0.35,
        "alpha_s": 0.008,
        "alpha_t": 0.008,
        "lz": 1,
        "description": "In de grond gevormd met dubbele boorbuis, waarbij het grout direct tegen de grond drukt, spoelboren met groutinjectie, niet afgeperst",
    }
    MICROPAAL_DUBBEL_AFGEPERST = {
        "alpha_p": 0.35,
        "alpha_s": 0.011,
        "alpha_t": 0.011,
        "lz": 1,
        "description": "In de grond gevormd met dubbele boorbuis, waarbij het grout direct tegen de grond drukt, spoelboren met groutinjectie, wel afgeperst ",
    }
    MICROPAAL_ENKEL_NIET_AFGEPERST = {
        "alpha_p": 0.35,
        "alpha_s": 0.008,
        "alpha_t": 0.008,
        "lz": 2,
        "description": "In de grond gevormd met enkele boorbuis, waarbij het grout direct tegen de grond drukt, spoelboren buitenom met groutinjectie, niet afgeperst",
    }
    MICROPAAL_ENKEL_AFGEPERST = {
        "alpha_p": 0.35,
        "alpha_s": 0.011,
        "alpha_t": 0.011,
        "lz": 1,
        "description": "In de grond gevormd met enkele boorbuis, waarbij het grout direct tegen de grond drukt, spoelboren buitenom met groutinjectie, wel afgeperst",
    }
    MICROPAAL_ANKERBUIZEN_ZELFBOREND = {
        "alpha_p": 0.35,
        "alpha_s": 0.008,
        "alpha_t": 0.008,
        "lz": 2,
        "description": "In de grond gevormd met ankerbuizen en boorkop, waarbij het grout direct tegen de grond drukt, zelfborend met groutinjectie",
    }
    MICROPAAL_GESCHROEFD = {
        "alpha_p": 0.35,
        "alpha_s": 0.008,
        "alpha_t": 0.008,
        "lz": 2,
        "description": "In de grond gevormd met ankerbuizen en schroefbladen, waarbij het grout direct tegen de grond drukt, Geschroefd; menging van de grond met grout",
    }
    MICROPAAL_INGETRILD = {
        "alpha_p": 0.35,
        "alpha_s": 0.006,
        "alpha_t": 0.006,
        "lz": 2,
        "description": "In de grond gevormd met stalen hulpbuis, waarbij het grout direct tegen de grond drukt, ingetrild met groutinjectie",
    }
    HOUTEN_PAAL_CONSTANT_D = {
        "alpha_p": 0.7,
        "alpha_s": 0.010,
        "alpha_t": 0.007,
        "lz": 1,
        "description": "Constante dwarsafmeting, geheid",
    }
    HOUTEN_PAAL_TAPS = {
        "alpha_p": 0.7,
        "alpha_s": 0.012,
        "alpha_t": 0.007,
        "lz": 1,
        "description": "Taps toelopend, geheid",
    }


class PileCalculation(DataModel):
    cpt: Cpt
    cpt_phreatic_level: float
    Deq: float
    cpt_ocr: float = 1.0
    surface_load: float = 0.0

    pile_type: PileType = PileType.CONCRETE_PREFAB

    def calculate(
        self,
        pile_tip_levels: List[float],
        peat_friction_ratio: float = 5.0,
        debug_plot=False,
    ):
        sp = self.cpt.to_soilprofile(
            cpt_interpretation_method=CptInterpretationMethod.ROBERTSON,
            minimum_layerheight=0.1,
            peat_friction_ratio=peat_friction_ratio,
        )
        sc = SoilCollection()

        stresses = sp.stresses(
            soil_collection=sc,
            phreatic_level=self.cpt_phreatic_level,
            load=self.surface_load,
        )

        for pile_tip_level in pile_tip_levels:
            z_4d = pile_tip_level - 4 * self.Deq
            z_07d = pile_tip_level - 0.7 * self.Deq
            z_8d = pile_tip_level + 8 * self.Deq

            qc1 = self.cpt.qc_gem(pile_tip_level, z_4d)
            qc2 = self.cpt.qc_gem(pile_tip_level, z_07d)
            qc3 = self.cpt.qc_gem(z_8d, pile_tip_level)

            if debug_plot:
                fig = plt.figure(figsize=(10, 10))
                gs = gridspec.GridSpec(1, 2, width_ratios=[2, 1])
                ax1 = fig.add_subplot(gs[0, 0])
                ax2 = fig.add_subplot(gs[0, 1], sharey=ax1)

                ax1.plot(self.cpt.qc, self.cpt.z)
                ax1.plot(self.cpt.fr, self.cpt.z)
                ax1.plot([0, QCMAX_PLOT], [pile_tip_level, pile_tip_level], "k--")
                ax1.text(1, pile_tip_level, "pile tip level")

                ax1.plot([0, QCMAX_PLOT], [z_07d, z_07d], "k--")
                ax1.text(1, z_07d, "0.7D level")
                ax1.plot([qc2, qc2], [pile_tip_level, z_07d], "k--")
                ax1.text(qc2, (pile_tip_level + z_07d) / 2.0, "qc2")

                ax1.plot([0, QCMAX_PLOT], [z_4d, z_4d], "k--")
                ax1.text(1, z_4d, "4D level")
                ax1.plot([qc1, qc1], [pile_tip_level, z_4d], "k--")
                ax1.text(qc1, (pile_tip_level + z_4d) / 2.0, "qc1")

                ax1.plot([0, QCMAX_PLOT], [z_8d, z_8d], "k--")
                ax1.text(1, z_8d, "8D level")
                ax1.plot([qc3, qc3], [z_8d, pile_tip_level], "k--")
                ax1.text(qc3, (z_8d + pile_tip_level) / 2.0, "qc3")

                ax1.plot(
                    [0, QCMAX_PLOT],
                    [self.cpt_phreatic_level, self.cpt_phreatic_level],
                    "b--",
                )
                ax1.text(1, self.cpt_phreatic_level, "phreatic level")
                ax1.set_xlim(0, QCMAX_PLOT)

                ax1.grid(which="both")

                ax2.plot(stresses.s_eff, stresses.z, label="s_eff;v")
                ax2.plot(stresses.s_tot, stresses.z, label="s_tot;v")
                ax2.plot(stresses.u, stresses.z, "b", label="u")
                ax2.plot(
                    [0, max(stresses.s_tot)],
                    [self.cpt_phreatic_level, self.cpt_phreatic_level],
                    "b--",
                )
                ax2.plot(
                    [0, max(stresses.s_tot)], [pile_tip_level, pile_tip_level], "k--"
                )
                ax2.grid(which="both")
                ax2.legend()
                plt.tight_layout()
                plt.show()
                # plot piletip level
                # plot 07d, 4d, 8d
                # plot qc1, qc2, qc3
