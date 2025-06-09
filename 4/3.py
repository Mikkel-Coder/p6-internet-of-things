from dataclasses import dataclass
import numpy as np
import matplotlib.pylab as plt


@dataclass
class LoRaModulation:
    transmission_power: float  # dBm
    carrier_frequency: int  # Hz
    bandwidth: int  # Hz
    spreading_factor: int  # [6-12]
    coding_rate: int  # [0-4] where 0 = 4/5 1= 4/6 etc.

    @property
    def rate_symbol(self) -> float:
        return self.bandwidth / 2**self.spreading_factor  # symbol/sec

    @property
    def rate_payload(self) -> float:
        return (self.spreading_factor * (4 / (4 + self.coding_rate))) / (
            (2**self.spreading_factor) / self.bandwidth
        )  # bits/sec


@dataclass
class LoRaFrame(LoRaModulation):
    n_preamble: int  # [6-65535]
    n_payload: int  # [1-255] Bytes inclusive header and CRC

    @property
    def time_preamble(self) -> float:
        return self.n_preamble / self.rate_symbol  # sec

    @property
    def time_payload(self) -> float:
        return self.n_payload * 8 / self.rate_payload  # sec

    @property
    def air_time(self) -> float:
        return self.time_preamble + self.time_payload  # sec


class LoRaNode:
    def __init__(
        self,
        lora_frame: LoRaFrame,
        allowed_duty_cycle: float,  # in %
        simulation_time: int,  # sec
    ):
        self.lora_frame = lora_frame
        self.allowed_duty_cycle = allowed_duty_cycle
        self.simulation_time = simulation_time
        self.idle_time: float = 0
        self.bytes_transmitted: int = 0

    def simulate(self) -> None:
        air_time = self.lora_frame.air_time
        off_time = air_time / self.allowed_duty_cycle - air_time

        if air_time > self.simulation_time:
            raise ValueError("Not enough time to send one frame")

        for sec in range(self.simulation_time):
            if self.idle_time <= 0:
                # Send a packet
                self.bytes_transmitted += self.lora_frame.n_payload
                self.idle_time = off_time
                continue

            self.idle_time -= 1

    @property
    def throughput(self) -> float:
        return self.bytes_transmitted  # Bytes per simulation time (1 day)


def main():
    frame = LoRaFrame(
        transmission_power=14.0,  # Not needed for the simulation
        carrier_frequency=868_000_000,  # Not needed for the simulation
        bandwidth=125_000,  # 125 kHz bandwidth
        spreading_factor=12,  # spreading factors 7-12 (use air-time calculator)
        coding_rate=4,  # [0-4]
        n_preamble=8 + 4.25,  # 4.25 comes from radio, 8 is fine (symbols)
        n_payload=12,  # Assume a fixed 12-byte payload
    )

    duty_cycles = np.linspace(0.001, 0.01, 100)  # in percentage
    simulation_time: int = 3_600 * 24  # One day in sec
    throughputs = []
    found_good_dc: bool = False

    for duty_cycle in duty_cycles:
        node = LoRaNode(
            lora_frame=frame,
            allowed_duty_cycle=duty_cycle,
            simulation_time=simulation_time,
        )
        node.simulate()
        throughput = node.throughput  # in bytes
        throughputs.append(throughput)

        if not found_good_dc:
            if throughput > 1680:
                print(
                    f"A duty cycle of less than: {duty_cycle*100:.2f}% is good for the throughout: {throughput} Bytes/day"
                )
                found_good_dc = True

    # Plot throughput vs duty cycle
    plt.plot(duty_cycles, throughputs, label="LoRaWAN")
    plt.title("Throughput vs Duty Cycle for 1 day")
    plt.xlabel("Duty Cycle (%)")
    plt.ylabel("Throughput (bytes)")
    plt.grid(True)

    plt.axhline(y=1680, color="red", label="SigFox")
    plt.legend()

    plt.savefig("4/lora_vs_sigfox.png")


if __name__ == "__main__":
    main()
