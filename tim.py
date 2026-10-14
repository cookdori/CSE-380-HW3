#tim.py
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


def merge(left, not_left):
    done = []
    i = j=0
    while i < len(left) and j < len(not_left):
        if left[i] <= not_left[j]:
            done.append(left[i])
            i += 1
        else:
            done.append(not_left[j])
            j += 1
    done.extend(left[i:])
    done.extend(not_left[j:])
    return done

def tim_sort(arr,k):
    if len(arr) <= k:
        return insertion_sort(arr)
    beans = len(arr) // 2
    return merge(tim_sort(arr[:beans],k), tim_sort(arr[beans:],k))


def avg_time(sort_fn, datasets):
    something = time.perf_counter()
    for data in datasets:
        sort_fn(data)
    return (time.perf_counter() - something) / len(datasets)

#def run_experiment(sizes, total_work=200_000):
    #ins_times, mer_times = [], []
    #for n in sizes:
        #trials = max(5, total_work // n)
       # datasets = [[random.randint(0, 10**6) for _ in range(n)]
            #        for _ in range(trials)]
     #   ins_times.append(avg_time(insertion_sort, datasets))
#        mer_times.append(avg_time(merge_sort, datasets))
#    return ins_times, mer_times


#def find_crossover(sizes, ins, mer):
#    faster = [n for n, i, m in zip(sizes, ins, mer) if i < m]
#    return max(faster) if faster else None


def plot(sizes):
    for n in sizes:
        this = max(3, 20000//n)
        data = [[random.randint(0, 10**6) for _ in range(n)] for _ in range(this)]
        tick = [avg_time(lambda arr: tim_sort(arr, k), data) for k in range(1, 101)]
        yay = list(range(1, 101))[tick.index(min(tick))]
        flash = tick[0]/min(tick)
        print(f"n={n}: best k={yay}")
        plt.plot(list(range(1, 101)), [t/tick[0] for t in tick], label= f"n={n}, best k={yay}")
    plt.xlabel("k")
    plt.ylabel("Time relative to merge sort or k = 1")
    plt.title("tim_sort")
    plt.legend()
    plt.tight_layout()
    plt.savefig("tim_sort.png")
    plt.show()


if __name__ == "__main__":
    random.seed(87)
    hmm = [random.randint(0,1000) for _ in range(500)]
    assert all(tim_sort(hmm, k) == sorted(hmm) for k in (1,8,32,600))
    size = [1000,5000,20000]
    plot(size)


    plt.show()