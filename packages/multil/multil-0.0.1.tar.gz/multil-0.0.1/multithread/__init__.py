from multiprocessing import Process

def multi(target_func, thr, *args):
    processes = []
    for _ in range(thr):
        process = Process(target=target_func, args=args)
        processes.append(process)
        process.start()

    for process in processes:
        process.join()