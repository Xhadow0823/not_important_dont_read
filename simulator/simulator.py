# from simulator.logger import Logger
from common import types
from typing import Literal
import threading
from time import sleep
import tqdm
from dataclasses import dataclass

class Simulation:
    # progress info
    status: Literal["idle", "simulating", "done"] = "idle"
    progress_now: int =  0
    progress_max: int = -1

    def set_platform_config(self):
        pass
    def set_model_config(self):
        pass
    
    def work_thread(self):
        self.progress_max = 10
        for i in range(10):
            # print(i)
            self.progress_now = i
            sleep(1)
        self.progress_now = self.progress_max
    def start(self):
        t = threading.Thread(target=self.work_thread)
        t.start()
        pass


def simulate(env: type[types.Environment]) -> type[Simulation]:
    simulation = Simulation()
    simulation.start()
    return simulation



###############################################
def test():
    sim: Simulation = simulate(dict())

    with tqdm.tqdm(total = sim.progress_max) as p:
        p.set_description('progress: ')
        while(sim.progress_now < sim.progress_max):
            sleep(0.5)
            p.update(sim.progress_now - p.n)
            p.refresh()
        p.update(sim.progress_now - p.n)
        p.refresh()
        
if __name__ == '__main__':
    __test()