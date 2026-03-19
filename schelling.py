from mesa import Model
from mesa.discrete_space import CellAgent, OrthogonalMooreGrid
import numpy as np
import matplotlib.pyplot as plt


class Resident(CellAgent):
    def __init__(self, model, cell, color):
        super().__init__(model)
        self.cell = cell
        self.color = color
    def step(self):
        if not self.is_happy():
            self.teleport()

    def is_happy(self):
        if self.get_happiness() > self.model.thresh:
            return True
        else:
            return False

    def get_happiness(self):
        my_nbr_cells = [c for c in self.cell.neighborhood if not c.is_empty]
        if len(my_nbr_cells) == 0:
            return 0
        num_same_neighbors = 0
        num_diff_neighbors = 0
        for cell in my_nbr_cells:
            if cell.agents[0].color == self.color:
                num_same_neighbors += 1
            else:
                num_diff_neighbors += 1
        return num_same_neighbors / (num_same_neighbors + num_diff_neighbors)

    def teleport(self):
        self.cell = self.random.sample(self.model.grid.empties.cells, 1)[0]


class District(Model):
    def __init__(self, N, dim, prob_blue, thresh, plot=True):
        super().__init__()
        self.N = N
        self.dim = dim
        self.plot = plot
        self.thresh = thresh
        self.prob_blue = prob_blue
        self.grid = OrthogonalMooreGrid((dim, dim), torus=False,
            random=self.random)
        init_locs = self.random.sample(self.grid.empties.cells, N)
        Resident.create_agents(
            self,
            N,
            init_locs,
            ['blue' if self.random.random() < prob_blue else 'red' for i in range(N)]
        )
        if self.plot:
            fig, ax = plt.subplots(figsize=(8,8))
            self.img = ax.imshow(np.zeros((dim, dim, 3)))

    def draw(self):
        cells = np.zeros((self.dim, self.dim, 3))
        for a in self.agents:
            if a.color == "blue":
                cells[a.cell.coordinate] = (0,0,1)
            else:
                cells[a.cell.coordinate] = (1,0,0)
        self.img.set_data(cells)
        plt.title(f"Iteration {self.steps}")
        plt.pause(.2)
        
    def step(self):
        self.agents.shuffle_do("step")
        if self.plot:
            self.draw()


d = District(800, 40, .5, .7, True)
while any([not a.is_happy() for a in d.agents]):
    d.step()

happinesses = np.array([a.get_happiness() for a in d.agents])
print(f"Average happiness {happinesses.mean():.3f}")

