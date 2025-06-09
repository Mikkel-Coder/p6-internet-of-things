from utils import Compute


def main():
    W = 1  # GFLOP
    compute = Compute()

    # For x = 256 = xp bits
    x = xp = 256  # bits
    e_task_local = compute.compute_energy_mj(W, x, xp, "S", "S", wi=1)
    e_task_edge = compute.compute_energy_mj(W, x, xp, "S", "E", wi=1)
    e_task_cloud = compute.compute_energy_mj(W, x, xp, "S", "C", wi=1)
    print(f"### For {x = } and {xp = } ###")
    print(f"{e_task_local = :.3f} mj") # 6.094 mj
    print(f"{e_task_edge = :.3f} mj") # 12.574 mj
    print(f"{e_task_cloud = :.3f} mj") # 59.554 mj

    # For x = 256 = xp bits
    x = xp = 256  # bits
    e_task_local = compute.compute_energy_mj(W, x, xp, "S", "S", wi=0)
    e_task_edge = compute.compute_energy_mj(W, x, xp, "S", "E", wi=0)
    e_task_cloud = compute.compute_energy_mj(W, x, xp, "S", "C", wi=0)
    print(f"### For {x = } and {xp = } ###")
    print(f"{e_task_local = :.3f} mj") # 6.094 mj
    print(f"{e_task_edge = :.3f} mj") # 0.006 mj
    print(f"{e_task_cloud = :.3f} mj") # 0.006 mj



if __name__ == "__main__":
    main()
