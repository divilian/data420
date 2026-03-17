from mesa import Model, DataCollector
from mesa.discrete_space import CellAgent, OrthogonalMooreGrid
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
import random

legend_elements = [
    Patch(facecolor=(0,0,1), label='S'),
    Patch(facecolor=(1,0,0), label='I'),
    Patch(facecolor=(0,1,0), label='R')
]

class Person(CellAgent):
    def __init__(self, model, cell):
        super().__init__(model)
        self.cell = cell
        self.state = "S"
        self.sick_timer = 0
    def sayhi(self):
        print(f"Hi, I'm agent {self.unique_id}! I live at {self.cell.coordinate}")
    def move(self):
        empties = [c for c in self.cell.neighborhood if c.is_empty]
        if empties:
            self.cell = self.model.random.choice(empties)
    def step(self):
        #self.sayhi()
        self.move()
        if self.state == "I":
            self.infect_others()
            self.progress_disease()
    def infect_others(self):
        if self.model.random.random() < self.model.transmissibility:
            victims = [c for c in self.cell.neighborhood if not c.is_empty]
            for v in victims:
                if v.agents[0].state == "S":
                    v.agents[0].state = "I"
    def progress_disease(self):
        if self.sick_timer == self.model.inf_dur:
            self.state = "R"
        self.sick_timer += 1
        
    def color(self):
        if self.state == "S":
            return (0,0,1)
        elif self.state == "I":
            return (1,0,0)
        elif self.state == "R":
            return (0,1,0)
        else:
            import sys; sys.exit("PANIC!!!")
    


class Env(Model):
    def __init__(self, N, dim, transmissibility=1.0, inf_dur=8, seed=None):
        super().__init__(rng=seed)
        self.N = N
        self.dim = dim
        self.transmissibility = transmissibility
        self.inf_dur = inf_dur
        self.grid = OrthogonalMooreGrid((dim, dim), torus=False,
            random=self.random)
        Person.create_agents(
            self,
            N,
            self.random.sample(self.grid.empties.cells, N)
        )
        self.agents[0].state = "I"
        fig, ax = plt.subplots(figsize=(8,8))
        ax.set_title(f"Transmissibility: {self.transmissibility:.3f}\nMean infectious duration: {self.inf_dur}")
        self.img = ax.imshow(np.zeros((self.dim, self.dim, 3)))
        ax.legend(
            handles=legend_elements,
            loc='center left',
            bbox_to_anchor=(1, 0.5)
        )
        self.datacollector = DataCollector(
            model_reporters={
                's_pop':self.s_pop,
                'i_pop':self.i_pop,
                'r_pop':self.r_pop,
            }
        )

    def s_pop(self):
        return sum([a.state == "S" for a in self.agents])
    def i_pop(self):
        return sum([a.state == "I" for a in self.agents])
    def r_pop(self):
        return sum([a.state == "R" for a in self.agents])
        
    def show_world(self):
        cells = np.zeros((self.dim, self.dim, 3))
        for a in self.agents:
            cells[a.cell.coordinate] = a.color()
        self.img.set_data(cells)
        plt.pause(.1)
        
    def step(self):
        print(f"Simulation step {self.steps}...")
        self.agents.do("step")
        self.show_world()
        self.datacollector.collect(self)
        

e = Env(1000,55,random.random(), random.randint(1,15))
while e.i_pop() > 0:
    e.step()

df = e.datacollector.get_model_vars_dataframe()
plt.clf()
fig, ax = plt.subplots(figsize=(10,8))
perc_ever_sick = e.r_pop() / len(e.agents) * 100
plt.suptitle(f"{perc_ever_sick:.1f}% of the population got sick.")
ax.set_title(f"Transmissibility: {e.transmissibility:.3f}\nMean infectious duration: {e.inf_dur}")
df.plot(ax=ax)
plt.pause(5)
plt.close()
