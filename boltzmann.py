
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats
import seaborn as sns
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector

class MarchAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.cash = 1
    def step(self):
        self.move()
        if self.cash == 0:
            pass
        else:
            neighbors = self.model.grid.get_neighbors(self.pos, moore=True)
            if len(neighbors) > 0:
                other = self.random.choice(neighbors)
                other.cash += 1
                self.cash -= 1
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos,
            moore=True)
        place_to_go = self.random.choice(possible_steps)
        if self.model.grid.is_cell_empty(place_to_go):
            self.model.grid.move_agent(self, place_to_go)
    def am_broke(self):
        return not self.cash


class MarchModel(Model):
    def __init__(self, num_agents, dim):
        self.num_agents = num_agents
        self.dim = dim
        self.grid = SingleGrid(dim, dim, torus=True)
        self.schedule = RandomActivation(self)
        self.datacollector = DataCollector(
            model_reporters = { 'max_wealth': MarchModel.max_wealth },
            agent_reporters = { 'dun_broke': MarchAgent.am_broke }
        )
        for i in range(num_agents):
            a = MarchAgent(i, self)
            self.schedule.add(a)
            self.grid.move_to_empty(a)
    def max_wealth(self):
        cashes = [ a.cash for a in aprilmodel.schedule.agents ]
        return max(cashes)
    def step(self):
        self.schedule.step()
        self.display_grid()
        self.datacollector.collect(self)
    def display_grid(self):
        cells = np.zeros((self.dim, self.dim))
        for a in self.schedule.agents:
            cells[a.pos[0], a.pos[1]] = a.cash + 1
        plt.clf()
        sns.heatmap(cells, square=True, cmap="gray", vmin=0, vmax=8)
        plt.pause(.04)
        plt.show()
        

aprilmodel = MarchModel(100,25)
for i in range(80):
    aprilmodel.step()

cashes = [ a.cash for a in aprilmodel.schedule.agents ]
print(cashes)

plt.clf()
plt.plot(aprilmodel.datacollector.get_model_vars_dataframe().max_wealth)
plt.show()
