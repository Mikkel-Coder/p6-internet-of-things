# python3 -m venv .venv
# source .venv/bin/activate
# pip install matplotlib

from math import log2
import matplotlib.pyplot as plt


def R_sym(N_CS_RB, T_sym):
    print(N_CS_RB, T_sym)
    print(f"rate: {N_CS_RB/T_sym}")

    return N_CS_RB / T_sym


def T_sym(T_sf, delta_f_0, N_slot_sym, delta_f):
    print(f" t_sym: {T_sf * delta_f_0 / N_slot_sym * delta_f}")
    print(f"{T_sf=}")
    print(f"{delta_f_0=}")
    print(f"{N_slot_sym=}")
    print(f"{delta_f=}")
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
    delta_f = 15  # kHz
    M = 2**1  # Modulation (binary)

    k = 100
    k_users = list(range(1, k + 1))
    throughput = []

    for k in k_users:
        throughput.append(
            bit_rate(delta_f, M, N_RB, N_CS_RB, T_sf, delta_f_0, N_slot_sym) / k
        )

    # 1.d
    # What is the maximum number of users supported by NB-IoT if they require
    # a throughput of 100 kbps?
    max_throughput = []
    for i, t in enumerate(throughput):
        if t > 100:
            max_throughput.append(i + 1)

    print(f"Max users for 100 kbps is {max(max_throughput)}")

    # Generate user range for plotting
    plt.plot(k_users, throughput)
    plt.xlabel("Number of Users K")
    plt.ylabel("Throughput per user [Kbps]")
    plt.savefig("3/datarate.png")


if __name__ == "__main__":
    main()
