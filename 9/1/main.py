from dataclasses import dataclass, field
from abc import ABC
import numpy as np
import matplotlib.pyplot as plt


@dataclass
class Architecture(ABC):
    N_cores_c: int  # Number of CPU cores
    f_proc_c: float  # Processor clock frequency in GHz
    N_flops: int  # Number of FLOPs per Hz (Hz = cycle/sec)
    P_max_c: float  # Max Power consumption in Watts
    E_proc_c: list[float] = field(default_factory=list)
    frequencies: list[float] = field(default_factory=list)
    _freq_step_size: float = 0.01

    def energy_consumption_for_processing(self, W):
        step = self._freq_step_size
        for freq in np.arange(0, self.f_proc_c + step, step=step):
            self.frequencies.append(freq)
            self.E_proc_c.append(
                (
                    (self.P_max_c * W * (freq) ** 2)
                    / (self.f_proc_c**3 * self.N_cores_c * self.N_flops)
                )
                * 1_000
            )  # mJ

    def plot(self):
        arch = self.__class__.__name__
        fig, ax = plt.subplots()
        ax.plot(self.frequencies, self.E_proc_c)
        ax.set_title(f"Energy Consumption for {arch}")
        ax.set_xlabel("Frequency (GHz)")
        ax.set_ylabel("Energy consumption (mJ)")
        ax.grid()

        # Save the plot
        fig.savefig(f"9/1/{arch}.png")
        plt.close(fig)

    @staticmethod
    def plot_together(archs: list["Architecture"]):
        fig, ax = plt.subplots()

        for arch in archs:
            arch_name = arch.__class__.__name__
            ax.plot(arch.frequencies, arch.E_proc_c, label=arch_name)

        ax.set_title(f"Energy Consumption for multiple Architectures")
        ax.set_xlabel("Frequency (GHz)")
        ax.set_ylabel("Energy consumption (mJ)")
        ax.legend()
        ax.grid()
        fig.savefig(f"9/1/multiple_archs.png")
        plt.close(fig)


@dataclass
class AMD_EPYC_7H12(Architecture):
    N_cores_c: int = 64
    f_proc_c: float = 2.6
    N_flops: int = 32
    P_max_c: float = 280.0


@dataclass
class NVIDIA_Orin_Nano(Architecture):
    N_cores_c: int = 1024
    f_proc_c: float = 0.625
    N_flops: int = 2
    P_max_c: float = 15.0


@dataclass
class Nordic_Thingy_53(Architecture):
    N_cores_c: int = 1
    f_proc_c: float = 0.128
    N_flops: int = 2
    P_max_c: float = 0.00156


def main():
    W = 7  # GFLOPs
    architectures: list[Architecture] = [
        AMD_EPYC_7H12(),
        NVIDIA_Orin_Nano(),
        Nordic_Thingy_53(),
    ]

    for arch in architectures:
        arch.energy_consumption_for_processing(W)
        arch.plot()

    Architecture.plot_together(architectures)


if __name__ == "__main__":
    main()
