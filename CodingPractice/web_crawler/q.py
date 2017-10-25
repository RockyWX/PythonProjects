import Queue
import threading
import time
import random

q = Queue.Queue()  # thread-safe FIFO queue

counter = 0  # race condition
lock = threading.RLock()  # safe lock to avoid race condition


def worker(i, q):
    while True:
        task = q.get()
        print('%d working on task %d' % (i, task))
        time.sleep(1)
        count_new_tasks = random.randrange(0, 10)
        print('putting %d new tasks in queue' % count_new_tasks)
        for new_task in range(count_new_tasks):
            q.put(new_task)
        q.task_done()
        global counter  # mark counter as global variable
        with lock:  # safe lock
            counter += 1
            print('processed %d tasks so far' % counter)


for i in range(2):
    t = threading.Thread(target=worker, args=(i, q, ))

    t.start()

q.put(1)
q.join()

# for i in range(100):
#     q.put(i)
#
# while not q.empty():
#     print(q.get())
