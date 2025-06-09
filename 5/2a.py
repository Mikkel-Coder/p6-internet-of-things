import numpy as np
import matplotlib.pyplot as plt

def average_energy_consumption_per_slot(p_s):
    p_a = 10**-5  # Arrival rate [per slot time]
    delta_t = 1  # Time slot duration [ms]

    P_idle_comm = 5. # mW
    P_Tx_comm = 25. # mW
 
    # slide 20
    pi_idle = (p_s * (1 - p_a)) / (p_a + p_s * (1 - p_a))
    pi_Tx = 1 - pi_idle

    # slide 21
    e = delta_t * (pi_idle*P_idle_comm + pi_Tx * P_Tx_comm)
    
    # Convert from mW to mJ (per time slot)
    return e * (delta_t / 1000)

def main():
    y_vals = []
    x_vals = []
    for i in np.arange(0.01, 1+0.01, 0.01):
        y_vals.append(average_energy_consumption_per_slot(i))
        x_vals.append(i)

    plt.plot(x_vals, y_vals)
    
    plt.title("Average Energy Consumption per Slot")
    plt.xlabel("Success probability")
    plt.ylabel("Avg. energy consumption (mJ) [per 1 ms time slot]")
    plt.grid(True)

    plt.savefig("5/average_ee_per_slot.png")



if __name__ == "__main__":
    main()

