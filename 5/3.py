import numpy as np
import matplotlib.pyplot as plt


def average_energy_consumption_per_slot(p_a):
    p_s = 0.9  # Probability of success
    delta_t = 1  # Time slot duration [ms]

    P_sleep_comm = 9.5 / 1000  # mW
    P_Tx_comm = 200.0  # mW

    # Including retransmission
    pi_sleep = (p_s * (1 - p_a)) / (p_a + p_s * (1 - p_a))
    pi_Tx = 1 - pi_sleep

    # slide 21
    e = delta_t * (pi_sleep * P_sleep_comm + pi_Tx * P_Tx_comm)

    # Convert from mW to mJ (per time slot)
    return e * (delta_t / 1000)


def lifetime(p_a):
    C = 32_600  # Joule [two AA batteries]
    delta_t = 1  # Time per slot [ms]

    res = C * delta_t / average_energy_consumption_per_slot(p_a)

    return res / 60 / 60 / 24 / 365 # Convert to years


def main():
    x_vals = np.logspace(-5, -3, 100)
    y_vals_rt = [lifetime(x) for x in x_vals]

    plt.plot(x_vals, y_vals_rt)
    plt.xscale("log")
    plt.xlabel("Packet arrival rate")
    plt.ylabel("Battery lifetime [years]")

    plt.savefig("5/battery_lifetime_different_devices.png")


if __name__ == "__main__":
    main()
