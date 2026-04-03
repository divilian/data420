from mesa import Model, DataCollector
from mesa.discrete_space import CellAgent, Network
import networkx as nx
import matplotlib.pyplot as plt
import math


class Citizen(CellAgent):
    def __init__(self, model, cell, color):
        super().__init__(model)
        self.cell = cell
        self.color = color
    def step(self):
        neighboring_agents = [c.agents[0] for c in self.cell.neighborhood.cells]
        if len(neighboring_agents) == 0:
            return
        influencer = self.model.random.choice(neighboring_agents)
        self.color = influencer.color


class Society(Model):
    def __init__(self, N, edge_prob, prob_blue, seed=None):
        super().__init__(rng=seed)
        self.N = N
        self.edge_prob = edge_prob
        self.prob_blue = prob_blue
        graph = nx.barabasi_albert_graph(N, 1, seed=seed)
        self.datacollector = DataCollector(
            model_reporters={
                'perc_blue':self.perc_blue
            }
        )
        self.network = Network(graph, random=self.random)
        Citizen.create_agents(
            self,
            N,
            self.network.all_cells.cells,
            self.random.choices(
                ["red","blue"],
                weights=[1-prob_blue,prob_blue],
                k=N,
            )
        )
        self.fig, self.ax = plt.subplots(figsize=(8,8))
        self.pos = nx.spring_layout(self.network.G)

    def perc_blue(self):
        blueness = [a.color=="blue" for a in self.agents]
        return sum(blueness) / self.N * 100

    def has_converged(self):
        if (
            math.isclose(self.perc_blue(), 100) or
            math.isclose(self.perc_blue(), 0)
        ):
            return True
        return False

    def step(self):
        print(f" Iteration {self.steps}...")
        self.agents.shuffle_do("step")        
        self.ax.clear()
        # Recompute the node layout, using the existing layout as a starting
        # point. (This way, if the graph changes, the next frame will pretty
        # smoothly shift to indicate that change, rather than randomly
        # redrawing from scratch.)
        self.pos = nx.spring_layout(self.network.G, pos=self.pos)

        nx.draw_networkx_nodes(
            self.network.G,
            node_color=[a.color for a in self.agents],
            edgecolors="black",
            pos=self.pos,
            ax=self.ax,
        )
        nx.draw_networkx_edges(
            self.network.G,
            pos=self.pos,
            ax=self.ax,
        )
        plt.pause(.2)
        self.datacollector.collect(self)


s = Society(N=100, edge_prob=.01, prob_blue=.5, seed=126)
while not s.has_converged():
    s.step()

df = s.datacollector.get_model_vars_dataframe()
fig, ax = plt.subplots(figsize=(10,6))
df.plot(ax=ax)
ax.set_title("Percentage of nodes which are blue")
ax.set_ylim((0,100))
fig.savefig("surgery.png")
