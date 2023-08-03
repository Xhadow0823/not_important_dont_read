import threading
import time
import tqdm

sleep = time.sleep

progress = 0

MAX_PROGRESS = 100

def backend():
    global progress, MAX_PROGRESS
    while(progress < MAX_PROGRESS):
        sleep(1)
        progress += 10
    progress = min(progress, MAX_PROGRESS)
    # progress = MAX_PROGRESS

t = threading.Thread(target = backend)

t.start()

with tqdm.tqdm(total = MAX_PROGRESS) as p:
    p.set_description('progress: ')
    while(progress < MAX_PROGRESS):
        sleep(0.5)
        p.update(progress - p.n)
        p.refresh()
    p.update(progress - p.n)
    p.refresh()


print(f"out");

print(f"multi-thread");