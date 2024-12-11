from math import tan, radians

WHITE_COEFFICIENT = 0.25
Y_SUB_PARTICLES = 16.5
KIN_VISCOSITY_WATER = 1.33e-6
GRAVITY = 9.81
D70_REF = 2.08e-4
ROLWEERSTANDSHOEK = 37
Y_WATER = 9.81


def stijghoogte_uittredepunt(
    sth_polder: float, river_level: float, dempingsfactor: float
) -> float:
    """Bereken de stijghoogte bij het uittredepunt

    Args:
        sth_polder (float): Stijghoogte in de polder bij het uittredepunt
        river_level (float): Waterstand in de rivier
        dempingsfactor (float): De toe te passen dempingsfactor (TR waterspanningen bij dijken)

    Returns:
        float: Stijghoogte bij het uittredepunt
    """
    return sth_polder + dempingsfactor * (river_level - sth_polder)


def opbarst_veiligheid(
    deklaag_dikte: float,
    y_sat: float,
    sth_uittredepunt: float,
    polderpeil: float,
    y_water: float = Y_WATER,
) -> float:
    """Bereken de opbarstveiligheid

    Args:
        deklaag_dikte (float): Dikte van de afdekkende laag
        y_sat (float): Nat volumieke massa van de afdekkende laag
        sth_uittredepunt (float): Stijghoogte ter plaatse van het uittredepunt
        polderpeil (float): Polderpeil ter hoogte van uittredepunt
        y_water (float, optional): Volumieke massa van water. Defaults to 9.81.

    Returns:
        float: De opbarst veiligheid
    """
    kritiek_sth_verschil = deklaag_dikte * (y_sat - y_water) / y_water
    return kritiek_sth_verschil - (sth_uittredepunt - polderpeil)


def heave(
    kritieke_heave_gradient: float,
    deklaag_dikte: float,
    sth_uittredepunt: float,
    polderpeil: float,
) -> float:
    """Bereken de veiligheid tegen heave

    Args:
        kritieke_heave_gradient (float): _description_
        deklaag_dikte (float): Dikte van de afdekkende laag
        sth_uittredepunt (float): Stijghoogte bij uittredepunt
        polderpeil (float): Polderpeil bij uittredepunt

    Returns:
        float: _description_
    """
    return kritieke_heave_gradient - (sth_uittredepunt - polderpeil) / deklaag_dikte


def sellmeijer(
    model_factor: float,
    river_level: float,
    polderpeil: float,
    deklaag_dikte: float,
    k: float,
    d70: float,
    kwelweglengte: float,
    dikte_zandlaag: float,
    reductie_factor: float = 0.3,
) -> float:
    F_res = (
        WHITE_COEFFICIENT
        * (Y_SUB_PARTICLES)
        / Y_WATER
        * tan(radians(ROLWEERSTANDSHOEK))
    )
    Kappa = KIN_VISCOSITY_WATER / GRAVITY * k
    F_scale = D70_REF / pow(Kappa * kwelweglengte, 1 / 3) * pow(d70 / D70_REF, 0.4)
    DdivL = dikte_zandlaag / kwelweglengte
    exponent = (0.28 / (pow(DdivL, 2.8) - 1)) + 0.04
    F_geometry = 0.91 * pow(DdivL, exponent)
    kritiek_verval = F_res * F_scale * F_geometry * kwelweglengte
    return model_factor * kritiek_verval - (
        river_level - polderpeil - reductie_factor * deklaag_dikte
    )


def sellmeijer_mc():
    pass
