from math import log10
from numpy.random import normal
import numpy as np
import matplotlib.pyplot as plt

# Path loss function
def path_loss(d, pl_d0, d0, n, sigma):
    return pl_d0 + 10 * n * log10(d / d0) + normal(loc=0, scale=sigma)

def main():

    # Shared constant variable between each opgave
    pl_d0 = 40  # Path loss at d0 in dBm
    d0 = 1 # Reference distance meter
    distances = np.arange(10, 101, 1)
    sigma = 4 # Shadowing gaussian

    # Opgave 2 - Simulated path loss printout with shadowing
    n = 3 # Path loss exponent

    path_losses = [path_loss(d, pl_d0, d0, n, sigma) for d in distances]
    plt.plot(distances, path_losses)
    plt.xlabel("Distance (m)")
    plt.ylabel("Path loss (dBm)")
    plt.savefig("1/figures/2_path_loss.png")
    plt.close()

    # Opgave 3 - Plot RSS over distance
    tx_p = 30   # Transmit power in dBm

    # RSS (Received Signal Strength) = Tx power - Path loss
    rss_shadowed = [tx_p - path_loss(d, pl_d0, d0, n, sigma) for d in distances]

    plt.plot(distances, rss_shadowed)
    plt.xlabel("Distance (m)")
    plt.ylabel("Received Signal Strength (dBm)")
    plt.savefig("1/figures/3_signal_loss.png")

if __name__ == "__main__":
    main()
