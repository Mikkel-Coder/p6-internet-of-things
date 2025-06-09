from math import log2
import numpy as np


def R_sym(N_CS_RB, T_sym):
    return N_CS_RB / T_sym


def T_sym(T_sf, delta_f_0, N_slot_sym, delta_f):
    return (T_sf * delta_f_0) / (N_slot_sym * delta_f)


def bit_rate(
    delta_f,
    modulation,
    N_RB,
    N_CS_RB,
    T_sf,
    delta_f_0,
    N_slot_sym,
):
    return (
        N_RB
        * R_sym(
            N_CS_RB,
            T_sym(T_sf, delta_f_0, N_slot_sym, delta_f),
        )
        * log2(modulation)
    )


def main() -> None:
    N_slot_sym = 14  # symbols
    delta_f_0 = 15  # kHz
    T_sf = 1  # ms
    N_CS_RB = 12  # symbols
    N_RB = 1

    delta_f_vals = [15, 30, 60, 129, 240, 480, 960]  # kHz
    M_vals = [2**1, 2**2, 2**4, 2**6, 2**8, 2**10]  # Modulation

    res = np.zeros((len(delta_f_vals), len(M_vals)))

    for i, delta_f in enumerate(delta_f_vals):
        for j, M in enumerate(M_vals):
            res[i][j] = bit_rate(delta_f, M, N_RB, N_CS_RB, T_sf, delta_f_0, N_slot_sym)

    print(res)


if __name__ == "__main__":
    main()
