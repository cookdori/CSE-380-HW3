import random
import time
import matplotlib.pyplot as plt
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def insertion_sort(arr):
    beans = arr[:]             
    for i in range(1, len(beans)):
        key = beans[i]
        j = i - 1
        while j >= 0 and beans[j] > key:
            beans[j + 1] = beans[j]
            j -= 1
        beans[j + 1] = key
    return beans


def merge_sort(arr):
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    boots = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            boots.append(left[i])
            i += 1
        else:
            boots.append(right[j])
            j += 1
    boots.extend(left[i:])
    boots.extend(right[j:])
    return boots


def avg_time(sort_fn, datasets):
    something = time.perf_counter()
    for data in datasets:
        sort_fn(data)
    return (time.perf_counter() - something) / len(datasets)

def run_experiment(sizes, total_work=200_000):
    ins_times, mer_times = [], []
    for n in sizes:
        trials = max(5, total_work // n)
        datasets = [[random.randint(0, 10**6) for _ in range(n)]
                    for _ in range(trials)]
        ins_times.append(avg_time(insertion_sort, datasets))
        mer_times.append(avg_time(merge_sort, datasets))
    return ins_times, mer_times


def find_crossover(sizes, ins, mer):
    faster = [n for n, i, m in zip(sizes, ins, mer) if i < m]
    return max(faster) if faster else None


def plot(sizes, ins, mer, title, filename, logscale=False):
    cross = find_crossover(sizes, ins, mer)
    plt.figure(figsize=(9, 5))
    plt.plot(sizes, ins, label="Insertion")
    plt.plot(sizes, mer, label="Merge")
    if cross is not None:
        plt.axvline(cross, color="blue", linestyle="--",label=f"Crossover near n ≈ {cross}")
    if logscale:
        plt.xscale("log")
        plt.yscale("log")
    plt.xlabel("Input size n")
    plt.ylabel("Average time per sort (s)")
    plt.title(title)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    print(f"{title}: crossover near n = {cross}")


if __name__ == "__main__":
    random.seed(87)
    small = list(range(2, 151, 2))
    ins, mer = run_experiment(small)
    plot(small, ins, mer, "Zoomed view (n = 2 to 150)", "small_range.png")
    wide = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000]
    ins, mer = run_experiment(wide, total_work=50_000)
    plot(wide, ins, mer, "Wide view (log-log)", "wide_range.png", logscale=True)

    plt.show()

        