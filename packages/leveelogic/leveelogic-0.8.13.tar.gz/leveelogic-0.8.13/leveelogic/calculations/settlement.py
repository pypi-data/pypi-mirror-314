from typing import List, Tuple
from math import log, log10


def h_prim(Cp: float, Cap: float, s_ini: float, s_eff: float, s_pg: float) -> float:
    if s_eff <= s_pg:
        return 1 / Cp * log(s_eff / s_ini)
    else:
        return 1 / Cp * log(s_pg / s_ini) + 1 / Cap * (s_eff / s_pg)


def h_sec(
    Cs: float, Cas: float, s_ini: float, s_eff: float, s_pg: float, t: float, t_ref=1e4
) -> float:

    if s_eff <= s_pg:
        return 1 / Cs * log10(1 + t / t_ref) * log(s_eff / s_ini)
    else:
        return 1 / Cs * log10(1 + t / t_ref) * log(s_pg / s_ini) + 1 / Cas * log10(
            1 + t / t_ref
        ) * log(s_eff / s_pg)


def koppejan_t(
    h0: float,
    Cp: float,
    Cap: float,
    Cs: float,
    Cas: float,
    s_ini: float,
    s_eff: float,
    s_pg: float,
    t: float,
    t_ref: float = 1e4,
) -> float:
    return h0 * h_prim(Cp, Cap, s_ini, s_eff, s_pg) + h0 * h_sec(
        Cs, Cas, s_ini, s_eff, s_pg, t, t_ref
    )


def koppejan_10000(
    h0: float,
    Cp: float,
    Cap: float,
    Cs: float,
    Cas: float,
    s_ini: float,
    s_eff: float,
    s_pg: float,
    t_ref: float = 1e4,
) -> List[Tuple[float, float]]:
    ts = [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        20,
        30,
        40,
        50,
        60,
        70,
        80,
        90,
        100,
        200,
        300,
        400,
        500,
        600,
        700,
        800,
        900,
        1000,
        2000,
        3000,
        4000,
        5000,
        6000,
        7000,
        8000,
        9000,
        10000,
    ]
    return [
        (t, koppejan_t(h0, Cp, Cap, Cs, Cas, s_ini, s_eff, s_pg, t, t_ref)) for t in ts
    ]
