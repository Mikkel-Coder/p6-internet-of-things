import numpy as np
import matplotlib.pyplot as plt


def average_energy_consumption_per_slot(p_a, RT: bool):
    p_s = 0.9  # Probability of success
    delta_t = 1  # Time slot duration [ms]

    P_idle_comm = 5.0  # mW
    P_Tx_comm = 15.0  # mW

    # slide 20
    if RT:
        pi_idle = (p_s * (1 - p_a)) / (p_a + p_s * (1 - p_a))
    else:
        pi_idle = 1 - p_a

    pi_Tx = 1 - pi_idle

    # slide 21
    e = delta_t * (pi_idle * P_idle_comm + pi_Tx * P_Tx_comm)

    # Convert from mW to mJ (per time slot)
    return e * (delta_t / 1000)


def lifetime(p_a, RT):
    C = 32_600  # Joule [two AA batteries]
    delta_t = 1  # Time per slot [ms]

    res = C * delta_t / average_energy_consumption_per_slot(p_a, RT)

    return res / 60 / 60 / 24 / 365 # Convert to years


def main():
    x_vals = np.logspace(-5, -1, 100)
    y_vals_rt = [lifetime(x, True) for x in x_vals]
    y_vals_no_rt = [lifetime(x, False) for x in x_vals]

    plt.plot(x_vals, y_vals_rt, label="With retransmissions")
    plt.plot(x_vals, y_vals_no_rt, label="Without retransmissions", linestyle="--")
    plt.xscale("log")
    plt.xlabel("Packet arrival rate")
    plt.ylabel("Battery lifetime [years]")
    plt.legend()

    plt.savefig("5/battery_lifetime.png")


if __name__ == "__main__":
    main()
