
# The Boltzmann wealth model -- using space, on a grid.

from mesa import Model, Agent
import numpy as np
from mesa.discrete_space import CellAgent, OrthogonalVonNeumannGrid
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class MoneyModel(Model):
    def __init__(self, N, dim=10, plothist=False, plotgrid=True):
        super().__init__()
        self.N = N
        self.plothist = plothist
        self.plotgrid = plotgrid
        self.dim = dim
        self.grid = OrthogonalVonNeumannGrid(
            (dim, dim),
            torus=False,
            random=self.random,
            capacity=1,
        )
        for i in range(N):
            self.agents.add(
                MoneyAgent(
                    self,
                    self.random.choice(self.grid.empties.cells),
                    4,
                )
            )
        self.fig, self.ax = plt.subplots()
    def step(self):
        if self.plothist:
            self.ax.clear()
            sns.histplot(self.agents.get("money"), ax=self.ax, discrete=True)
            self.ax.set_xlim(0,35)
            self.ax.set_ylim(0,20)
            plt.pause(0.3)
        if self.plotgrid:
            self.do_plotgrid()
            plt.pause(0.3)
        self.agents.shuffle_do("step")
    def max_dollars(self):
        return self.agents.agg("money", max)
    def do_plotgrid(self):
        agent_wealth = np.zeros((self.grid.width, self.grid.height))

        for cell in self.grid.all_cells:
            if cell.is_empty:
                agent_wealth[cell.coordinate] = -10
            else:
                agent_wealth[cell.coordinate] = cell.agents[0].money
        g = sns.heatmap(
            agent_wealth,
            cmap="inferno",
            annot=False,
            cbar=False,
            square=True,
            vmin=-10,
            vmax=10,
        )
        g.figure.set_size_inches(5, 5)
        g.set(title="Wealth of agent on each cell of the grid")
    


class MoneyAgent(CellAgent):
    def __init__(self, model, cell, money):
        super().__init__(model)
        self.cell = cell
        self.money = money
    def step(self):
        self.move()
        self.give_money()
        self.sayhi()
    def sayhi(self):
        print(f"Hi, I'm MoneyAgent {self.unique_id} and I have ${self.money}!")
    def give_money(self):
        neighbor_agents = []
        for cell in self.cell.neighborhood:
            if cell.agents:
                neighbor_agents += list(cell.agents)
        if neighbor_agents and self.money > 0:
            other_agent = self.random.choice(neighbor_agents)
            other_agent.money += 1
            self.money -= 1
    def move(self):
        neighoring_empties = [c for c in self.cell.neighborhood if c.is_empty]
        if neighoring_empties:
            self.cell = self.model.random.choice(neighoring_empties)

model = MoneyModel(100, dim=30)
model.run_for(50)
