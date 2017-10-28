# --- Functionality --- #
# Crawl web page 'https://jsonplaceholder.typicode.com' content and output a JSON file
# Crawl web page 'https://en.wikipedia.org/wiki/Leonard_Cohen':
#   Get page title
#   Get hyperlinks: numbers and urls
# Implement multi-thread workers with FIFO safe queue, safe counter and safe lock

import requests
from bs4 import BeautifulSoup  # bs4 (beautiful soup library)
import datetime  # time-consuming
import threading
import time  # sleep time
import Queue
import random

queue = Queue.Queue()  # thread-safe FIFO queue

safe_counter = 0  # safe_counter to avoid "race condition" for multi-thread
lock = threading.RLock()  # safe lock


def worker(thread_id, safe_queue):
    while not safe_queue.empty():
        task = safe_queue.get()
        print('Thread %d is working on task %d' % (thread_id, task))

        # assign random work_num to run
        new_task_num = random.randrange(0, 5)
        print('putting %d new tasks in queue' % new_task_num)

        # enqueue new tasks
        for new_task in range(new_task_num):
            safe_queue.put(new_task)

        start = datetime.datetime.now()

        for i in range(new_task_num):
            time.sleep(1)  # slow down crawling: sleep 1s before every fetching data action

            resp = requests.get('https://jsonplaceholder.typicode.com')
            print('status code is %d' % resp.status_code)
            print(resp.text)

            # BeautifulSoup block
            resp2 = requests.get('https://en.wikipedia.org/wiki/Leonard_Cohen')

            # parse html file with html.parser
            soup = BeautifulSoup(resp2.text, 'html.parser')

            # get page tile
            print('Title is %s.' % soup.title.string)

            # get all hyperlinks and in HTML a refers to hyperlink
            links = soup.find_all('a')
            print('There are %d hyperlinks on this page.' % len(links))

            # get all urls
            urls = [link.get('href') for link in links]
            print('Here are all urls:')
            for url in urls:
                print(url)

        safe_queue.task_done()

        # assign lock to counter
        global safe_counter  # mark counter as global variable
        with lock:  # safe lock
            safe_counter += 1
            print('processed %d tasks so far' % safe_counter)

        end = datetime.datetime.now()
        print('Done in %ss' % (end - start))


threads = []  # multi-threads container for adding or killing threads in runtime

for i in range(3):  # 3 threads
    t = threading.Thread(target=worker, args=(i, queue))  # each thread will run random(0,10) times
    t.setDaemon(False)  # able to stop/quit in runtime
    threads.append(t)
    t.start()

queue.put(1)  # initialize queue
queue.join()

