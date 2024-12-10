import pandas as pd
from datetime import datetime
import time
from tqdm import tqdm
import concurrent.futures
import multiprocessing
import itertools
import math

NUMBER_OF_CPU = math.floor(multiprocessing.cpu_count() - 3)
# NUMBER_OF_CPU = 3

# def multi_backtest(df, params, bt_method):
#     start = time.time()
#     stats = []
#     for param in tqdm(params):
#         bt = bt_method(param)
#         stats.append(bt.get_stats()["stats"])
#     end = time.time()

#     df = pd.DataFrame(stats, index=params)
#     print(f"Backtested {len(params)} combinations in {end - start} seconds")
#     print(df)
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = f"./data/simulation_result_{timestamp}.parquet"
#     df.to_parquet(filename)
#     df.to_parquet("./data/simulation.parquet")


def create_buckets(items):
    # Calculate the length of each part
    part_length = math.ceil(len(items) / NUMBER_OF_CPU)
    divided_list = [
        items[i : i + part_length] for i in range(0, len(items), part_length)
    ]
    return divided_list


def bt_wrapper(bt_method, st_params, iteration, df, ohlcvs, *args):
    pbar = tqdm(total=len(st_params), ncols=40)
    print("Start on iteraion", iteration)

    stats = []
    for param in st_params:
        bt = bt_method(param, df, ohlcvs, *args)
        stats.append(bt.get_stats()["stats"])

        if iteration == 0:
            pbar.update(1)

    df = pd.DataFrame(stats, index=st_params)

    if iteration == 0:
        pbar.close()
    return df


def worker(bt_method, params, iteration, df, ohlcvs, args, queue):
    result = bt_wrapper(bt_method, params, iteration, df, ohlcvs, *args)
    queue.put(result)


# def multi_backtest_parallel(df, params, bt_method):
def multi_backtest(df, ohlcvs, params, bt_method, *args):
    start = time.time()
    items = create_buckets(params)

    # Create a queue to store the results
    result_queue = multiprocessing.Queue()
    processes = []

    for i in range(NUMBER_OF_CPU):
        p = multiprocessing.Process(
            target=worker,
            args=(
                bt_method,
                items[i],
                i,
                df,
                ohlcvs,
                args,
                result_queue,
            ),
        )
        processes.append(p)
        p.start()

    # Collect the results from the queue
    results = pd.DataFrame()
    for _ in range(len(processes)):
        result = result_queue.get()
        results = pd.concat([results, result])

    # Wait for all processes to complete
    for p in processes:
        p.join()
    end = time.time()
    print(f"Backtested {len(params)} combinations in {end - start} seconds")

    results.to_parquet("./data/latest_simulation.parquet")
    return results
