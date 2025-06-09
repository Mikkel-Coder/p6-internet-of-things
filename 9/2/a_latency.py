from utils import Compute


def main():
    W = 1  # GFLOP
    compute = Compute()

    # For x = 256 = xp bits
    x = xp = 256  # bits
    t_task_local = compute.compute_latency_ms(W, x, xp, "S", "S")
    t_task_edge = compute.compute_latency_ms(W, x, xp, "S", "E")
    t_task_cloud = compute.compute_latency_ms(W, x, xp, "S", "C")
    print(f"### For {x = } and {xp = } ###")
    print(f"{t_task_local = :.3f} ms")  # 3906.250 ms
    print(f"{t_task_edge = :.3f} ms")  # 0.831 ms
    print(f"{t_task_cloud = :.3f} ms")  # 0.391 ms

    # For x = 12304 and xp = 256 bits
    x = 12304  # bits
    xp = 256  # bits
    t_task_local = compute.compute_latency_ms(W, x, xp, "S", "S")
    t_task_edge = compute.compute_latency_ms(W, x, xp, "S", "E")
    t_task_cloud = compute.compute_latency_ms(W, x, xp, "S", "C")
    print(f"### For {x = } and {xp = } ###")
    print(f"{t_task_local = :.3f} ms")  # 3906.250 ms
    print(f"{t_task_edge = :.3f} ms")  # 2.170 ms
    print(f"{t_task_cloud = :.3f} ms")  # 5.344 ms


if __name__ == "__main__":
    main()
