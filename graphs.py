
import networkx as nx
import matplotlib.pyplot as plt

fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18,6))

erg = nx.erdos_renyi_graph(50, .15)
nx.draw(erg, ax=axes[0], node_color='blue')
axes[0].set_title("Erdos-Renyi")

wsg = nx.watts_strogatz_graph(50, 7, .05)
nx.draw(wsg, ax=axes[1], node_color='green')
axes[1].set_title("Watts-Strogatz")

bag = nx.barabasi_albert_graph(50, 2)
nx.draw(bag, ax=axes[2], node_color='red')
axes[2].set_title("Barabasi-Albert")

def stat_string(g):
    diam = nx.diameter(g)
    aspl = nx.average_shortest_path_length(g)
    deghist = nx.degree_histogram(g)
    trans = nx.transitivity(g)
    return (
        f"diameter {diam}\n"
        f"ASPL {aspl:.2f}\n"
        f"Degrees: {deghist}\n"
        f"Transitivity: {trans:.2f}"
    )

axes[0].set_title(stat_string(erg))
axes[1].set_title(stat_string(wsg))
axes[2].set_title(stat_string(bag))

plt.tight_layout()
