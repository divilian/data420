from mesa import Model, DataCollector
from mesa.batchrunner import batch_run
from mesa.discrete_space import CellAgent, Network
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import seaborn as sns


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
    def __init__(self, N, edge_prob, prob_blue, do_plot=False, seed=None):
        super().__init__(rng=seed)
        self.N = N
        self.do_plot = do_plot
        self.edge_prob = edge_prob
        self.prob_blue = prob_blue
        graph = nx.watts_strogatz_graph(N, 4, edge_prob, seed=seed)
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
        if self.do_plot:
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
        #print(f" Iteration {self.steps}...")
        self.agents.shuffle_do("step")        
        if self.do_plot:
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
        if self.has_converged():
            self.running = False


def run_suite(num_runs: int):

    # Same parameters for every run
    params = {
        "N": 50,
        "edge_prob": np.arange(.01,0.2,.01),
        "prob_blue": np.arange(0.1,0.5,.02),
    }

    # 100 explicit seeds
    seeds = list(range(num_runs))

    results = batch_run(
        Society,
        parameters=params,
        rng=seeds,               # one replication per seed
        max_steps=500,
        data_collection_period=-1,
        number_processes=None,
    )

    return pd.DataFrame(results)

if __name__ == "__main__":
    res = run_suite(100)
    fig, ax = plt.subplots(figsize=(10,5))
    #res.groupby('edge_prob').Step.mean().plot(kind="line", ax=ax)
    heat = (
        res.groupby(["prob_blue", "edge_prob"])["Step"]
           .mean()
           .reset_index()
           .pivot(index="prob_blue", columns="edge_prob", values="Step")
    )
    sns.heatmap(heat, ax=ax)


#if __name__ == "__main__":
#    main()
#s = Society(N=100, edge_prob=.01, prob_blue=.5, seed=126)
#while not s.has_converged():
#    s.step()
#
#df = s.datacollector.get_model_vars_dataframe()
#fig, ax = plt.subplots(figsize=(10,6))
#df.plot(ax=ax)
#ax.set_title("Percentage of nodes which are blue")
#ax.set_ylim((0,100))
#fig.savefig("surgery.png")
