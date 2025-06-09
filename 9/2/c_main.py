from utils import Compute


def main():
    W = 1  # GFLOP
    compute = Compute()

    x = xp = 12304  # bits
    e_task_r2 = compute.compute_energy_mj(W, x, xp, src="S", dist="R2", wi=1)
    t_task_r2 = compute.compute_latency_ms(W, x, xp, src="S", dist="R2")
    print(f"### For {x = } and {xp = } ###")
    print(f"{e_task_r2 = :.3f} mj")  # 290.729 mj
    print(f"{t_task_r2 = :.3f} ms")  # 9.150 ms

    x = 12304
    xp = 256
    e_task_r2 = compute.compute_energy_mj(W, x, xp, src="S", dist="R2", wi=1)
    t_task_r2 = compute.compute_latency_ms(W, x, xp, src="S", dist="R2")
    print(f"### For {x = } and {xp = } ###")
    print(f"{e_task_r2 = :.3f} mj") # 122.556 mj
    print(f"{t_task_r2 = :.3f} ms") # 4.439 ms


    x = xp = 256
    e_task_r2 = compute.compute_energy_mj(W, x, xp, src="S", dist="R2", wi=1)
    t_task_r2 = compute.compute_latency_ms(W, x, xp, src="S", dist="R2")
    print(f"### For {x = } and {xp = } ###")
    print(f"{e_task_r2 = :.3f} mj") # 5.805 mj
    print(f"{t_task_r2 = :.3f} ms") # 0.174 ms


if __name__ == "__main__":
    main()
