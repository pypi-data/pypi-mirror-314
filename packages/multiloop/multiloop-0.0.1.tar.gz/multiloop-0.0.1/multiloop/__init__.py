from multiprocessing import Process

def multiloop(tar,thr):
    processes = []
    for _ in range(thr):
        process = Process(target=tar)
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
