from dataclasses import dataclass
from abc import ABC
import networkx as nx


@dataclass
class Device(ABC):
    N_cores_c: int  # Number of CPU cores
    f_proc_c: float  # Processor clock frequency in GHz
    N_flops: int  # Number of FLOPs per Hz (Hz = cycle/sec)
    P_max_c: float  # Max Power consumption in Watts

    def latency(self, W: int) -> float:
        return (W) / (self.f_proc_c * self.N_flops * self.N_cores_c)  # sec

    def energy(self, W: int) -> float:
        return (self.P_max_c * W) / (
            self.f_proc_c * self.N_cores_c * self.N_flops
        )  # joule


def dbm_to_watts(dbm: float) -> float:
    # This does not seems right
    return 10 ** (dbm / 10) * 1e-3


@dataclass
class AMD_EPYC_7H12(Device):
    N_cores_c: int = 64
    f_proc_c: float = 2.6
    N_flops: int = 32
    P_max_c: float = 280.0


@dataclass
class NVIDIA_Orin_Nano(Device):
    N_cores_c: int = 1024
    f_proc_c: float = 0.625
    N_flops: int = 2
    P_max_c: float = 15.0


@dataclass
class Nordic_Thingy_53(Device):
    N_cores_c: int = 1
    f_proc_c: float = 0.128
    N_flops: int = 2
    P_max_c: float = 0.00156


@dataclass
class Compute:
    cloud = AMD_EPYC_7H12()
    edge = NVIDIA_Orin_Nano()
    iot = Nordic_Thingy_53()

    G_dist = nx.DiGraph()
    G_dist.add_node("S", device=iot)
    G_dist.add_node("E", device=edge)
    G_dist.add_node("C", device=cloud)
    G_dist.add_edge("S", "E", capacity=9, power=23)
    G_dist.add_edge("E", "R1", capacity=10, power=46)
    G_dist.add_edge("R1", "R2", capacity=7, power=46)
    G_dist.add_edge("R1", "R3", capacity=8, power=46)
    G_dist.add_edge("R1", "C", capacity=5, power=46)
    G_dist.add_edge("R2", "C", capacity=13, power=46)
    G_dist.add_edge("R3", "C", capacity=12, power=46)

    G_delivery = nx.DiGraph()
    G_delivery.add_node("C", device=cloud)
    G_delivery.add_node("E", device=edge)
    G_delivery.add_node("S", device=iot)
    G_delivery.add_edge("C", "R2", capacity=13, power=46)
    G_delivery.add_edge("C", "R1", capacity=5, power=46)
    G_delivery.add_edge("C", "R3", capacity=12, power=46)
    G_delivery.add_edge("R2", "R1", capacity=7, power=46)
    G_delivery.add_edge("R3", "R1", capacity=8, power=46)
    G_delivery.add_edge("R1", "E", capacity=10, power=46)
    G_delivery.add_edge("E", "S", capacity=12, power=46) # Note that only the S sends with less power

    def compute_latency_ms(self, W, x, xp, src, dist: str) -> float:

        ### Calculate t_dist ###
        # Find a route between the iot "S" and the destination
        route_dist = nx.dijkstra_path(self.G_dist, src, dist)
        edges_dist = [
            (route_dist[i], route_dist[i + 1]) for i in range(len(route_dist) - 1)
        ]

        # Calculate the running sum to the destination
        t_dist = 0
        for u, v in edges_dist:
            capacity = self.G_dist[u][v]["capacity"] * 1e6 # bps -> Mbps
            t_dist += x / capacity

        ### Calculate t_task ###
        t_task = 0.0
        device: Device = self.G_dist.nodes[dist].get("device")
        if device is not None:
            t_task = device.latency(W)

        ### Calculate t_delivery ###
        # Find a route back from the destination to the iot
        route_delivery = nx.dijkstra_path(self.G_delivery, dist, src)
        edges_delivery = [
            (route_delivery[i], route_delivery[i + 1])
            for i in range(len(route_delivery) - 1)
        ]

        t_delivery = 0
        for u, v in edges_delivery:
            capacity = self.G_delivery[u][v]["capacity"] * 1e6 # bps -> Mbps
            t_delivery += xp / capacity  # Note that we use compression: xp

        return (t_dist + t_task + t_delivery) * 1000  # ms

    def compute_energy_mj(self, W, x, xp, src, dist, wi) -> float:
        ### Calculate e_dist ###
        # Find a route between the iot "S" and the destination
        route_dist = nx.bellman_ford_path(self.G_dist, src, dist, weight="capacity")
        edges_dist = [
            (route_dist[i], route_dist[i + 1]) for i in range(len(route_dist) - 1)
        ]

        # If we only need to calculate from S -> E
        if not wi:
            # If we have any hoops
            # NOTE: That S -> S have 0 hoops
            if len(edges_dist) > 0:
                # Update edges dist to contain the 1 hop
                # from S --> E
                edges_dist = [edges_dist[0]]

        # Calculate the running sum to the destination
        e_dist = 0.0
        for u, v in edges_dist:
            capacity = self.G_dist[u][v]["capacity"] * 1e6
            transmission_time = x / capacity  # sec
            power_dbm = self.G_dist[u][v]["power"]
            watts = dbm_to_watts(power_dbm)
            e_dist += watts * transmission_time

        ### Calculate e_proc ###
        # Include only e_proc when the source is S OR wi=1 
        # (wi=1: include every hoop)
        e_proc = 0.0
        device: Device = self.G_dist.nodes[dist].get("device")
        if device is not None:
            e_proc = device.energy(W) if wi or dist == src else 0.0
    

        ### Calculate e_delivery ###
        # Find a route back from the destination to the iot
        route_delivery = nx.bellman_ford_path(
            self.G_delivery, dist, src, weight="capacity"
        )
        edges_delivery = [
            (route_delivery[i], route_delivery[i + 1])
            for i in range(len(route_delivery) - 1)
        ]

        e_delivery = 0.0
        # Include only e_delivery when wi = 1, else 0
        if wi:
            for u, v in edges_delivery:
                capacity = self.G_delivery[u][v]["capacity"] * 1e6
                transmission_time = xp / capacity  # Note that we use compression: xp
                power_dbm = self.G_delivery[u][v]["power"]
                watts = dbm_to_watts(power_dbm)
                e_delivery += watts * transmission_time

        return (e_dist + e_proc + e_delivery) * 1000  # mj
