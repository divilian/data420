import csv

import seaborn as sns
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

g = nx.read_edgelist(
    "class_graph_less_dense.csv",
    delimiter=",",
#    create_using=nx.DiGraph()
)
ug = g.to_undirected()

pos = nx.spring_layout(g, seed=124)

fig,ax = plt.subplots(figsize=(12,8),constrained_layout=True)
nx.draw(
    ug,
    pos,
    with_labels=True,
    node_size=3200,
    node_color="navy",
    font_color="yellow",
    font_size=10,
    ax=ax,
)
fig.savefig("class_graph.png")

fig2,ax2 = plt.subplots(figsize=(12,8),constrained_layout=True)
sns.histplot([d for _, d in ug.degree()], ax=ax2, discrete=True)
ax2.xaxis.set_major_locator(MaxNLocator(integer=True))
ax2.set_xlim(left=0)
fig2.savefig("class_graph_degree_distro.png")
