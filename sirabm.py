from mesa import Model, DataCollector
from mesa.discrete_space import CellAgent, OrthogonalVonNeumannGrid
import matplotlib.pyplot as plt
import numpy as np


MEAN_INFECTIOUS_DURATION = 13   # days


class Person(CellAgent):
    def __init__(self, model, cell):
        super().__init__(model)
        self.cell = cell
        self.status = "S"
        self.num_days_since_infected = 0

    def step(self):
        self.move()
        if self.status == "I":
            self.infect_others()
            self.check_recovery()
        
    def check_recovery(self):
        if self.num_days_since_infected >= MEAN_INFECTIOUS_DURATION:
            self.status = "R"
        else:
            self.num_days_since_infected += 1

    def infect_others(self):
        my_neighboring_populated_cells = [
            c for c in self.cell.neighborhood if not c.is_empty
        ]
        if not my_neighboring_populated_cells:
            return
        my_neighbors = [c.agents[0] for c in my_neighboring_populated_cells]
        for n in my_neighbors:
            if n.status == "S":
                n.status = "I"

    def move(self):
        avail_cells = [c for c in self.cell.neighborhood if c.is_empty]
        if avail_cells:
            self.cell = self.random.choice(avail_cells)

    def sayhi(self):
        print(f"Hi! I'm agent {self.unique_id}!")

    def color(self):
        if self.status == "S":
            return (0,0,1)
        elif self.status == "I":
            return (1,0,0)
        elif self.status == "R":
            return (0,1,0)
        else:
            print("PANIC!!!")

class Room(Model):
    def __init__(self, N, dim, seed=None, do_plot=False):
        super().__init__(rng=seed)
        self.N = N
        self.do_plot = do_plot
        self.dim = dim
        self.grid = OrthogonalVonNeumannGrid((dim, dim), torus=False,
            capacity=1, random=self.random)
        init_pos = self.random.sample(self.grid.all_cells.cells, N)
        Person.create_agents(self, N, init_pos)
        self.agents[0].status = "I"
        self.datacollector = DataCollector(
            model_reporters={
                's_pop':self.s_pop, 
                'i_pop':self.i_pop, 
                'r_pop':self.r_pop, 
            }
        )
    def s_pop(self):
        return sum([ a.status == "S" for a in self.agents ])
    def i_pop(self):
        return sum([ a.status == "I" for a in self.agents ])
    def r_pop(self):
        return sum([ a.status == "R" for a in self.agents ])

    def show_room(self):
        if self.do_plot:
            cells = np.zeros((self.dim, self.dim, 3))
            for a in self.agents:
                cells[a.cell.coordinate[0], a.cell.coordinate[1]] = a.color()
            plt.imshow(cells)
            plt.pause(.1)

    def step(self):
        print(f"Iteration {self.steps}...")
        self.agents.shuffle_do("step")
        self.show_room()
        self.datacollector.collect(self)


N = 5000
dim = 100
r = Room(N, dim, 123)
while any([ a.status == "I" for a in r.agents ]):
    r.step()

df = r.datacollector.get_model_vars_dataframe()
df.plot()

prct_got_sick = (df.r_pop.iloc[-1] / N) * 100.0
print(f"{prct_got_sick:.3f}% of the population got sick.")
