from dataclasses import dataclass


@dataclass
class System:
    users: list["User"]

    @property
    def total_bits(self) -> int:
        # bits
        return sum(u.transmitted_data for u in self.users)

    @property
    def total_energy(self) -> float:
        # joule
        return sum(u.energy_consumption for u in self.users)

    def gee(self):
        # bits/joule
        return self.total_bits / self.total_energy


@dataclass
class User:
    transmission_power: int  # watt
    data_rate: int  # bits per second
    n_packets: int  # Number of packets
    prob_error: float  # Error probability
    packet_size: int  # bits

    @property
    def transmitted_data(self) -> int:
        # bits
        return self.packet_size * self.n_packets

    @property
    def energy_consumption(self) -> float:
        # joule
        return self.n_packets * (
            (self.transmission_power * self.packet_size)
            / (self.data_rate * (1 - self.prob_error))
        )

    def ee(self) -> float:
        # bits/Joule
        return self.transmitted_data / self.energy_consumption


def main():
    user_1 = User(
        transmission_power=200 * 1e-3,  # mW -> W
        data_rate=256 * 1e3,  # kbps -> bps
        n_packets=100,
        prob_error=0.1,
        packet_size=32 * 8,  # byte -> bit
    )
    user_2 = User(
        transmission_power=25 * 1e-3,  # mW -> W
        data_rate=20 * 1e3,  # kbps -> bps
        n_packets=20,
        prob_error=0.15,
        packet_size=64,  # bit
    )
    system = System(users=[user_1, user_2])

    # A
    print(f"User 1 EE: {system.users[0].ee()*1e-3:.0f} kb/J")  # 1152 kb/J
    print(f"User 2 EE: {system.users[1].ee()*1e-3:.0f} kb/J")  # 680 kb/J

    # B
    print(f"System GEE: {system.gee()*1e-3:.0f} kb/J")  # 1115 kb/J

    # C
    res = (system.users[0].ee() + system.users[1].ee()) / 2
    print(f"{res*1e-3:.0f} kb/J")  # 916 kb/J
    # NOT the same!
    print("The same.") if res == system.gee() else print("NOT the same!")


if __name__ == "__main__":
    main()
