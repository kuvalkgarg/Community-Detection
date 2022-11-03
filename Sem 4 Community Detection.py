import networkx as nx
import matplotlib.pyplot as plt

# load the graph
G = nx.karate_club_graph()

# visualize the graph
nx.draw(G, with_labels=True)


def edge_to_remove(graph):
    G_dict = nx.edge_betweenness_centrality(graph)
    edge = ()

    # extract the edge with highest edge betweenness centrality score
    for key, value in sorted(G_dict.items(), key=lambda item: item[1], reverse=True):
        edge = key
        break

    return edge


def leading_eigen(graph):
    # find number of connected components
    sg = nx.connected_components(graph)
    sg_count = nx.number_connected_components(graph)

    while(sg_count == 1):
        graph.remove_edge(edge_to_remove(graph)[0], edge_to_remove(graph)[1])
        sg = nx.connected_components(graph)
        sg_count = nx.number_connected_components(graph)

    return sg


def modularity(graph):
    i, j = 0
    # B is the modularity matrix, given by B = A - P
    b = nx.connected_components(graph)
    # A is the adjacency matrix of the undirected network
    a = graph.undirected()
    # P contains the probability that certain edges are present, eg, P[i][j] indicates probability of an edge between vertices i and j
    p = graph.prob(i, j)
    p.assign_lattice(graph)
    # The eigenvector for the largest positive eigen value is found and separated into 2 communities based on the sign of the corresponding elements
    while i > graph.edge:
        if p[i][j]:
            sep = graph(b).largest_positive_eigenvalue()
            j += 1
        i += 1
        if i == graph.edge and j == i:
            return False
    # if all elements have the same sign, the network has no underlying communities


# find communities in the graph
c = leading_eigen(G.copy())

# find the nodes forming the communities
node_groups = []

for i in c:
    node_groups.append(list(i))


# plot the communities
color_map = []
for node in G:
    if node in node_groups[0]:
        color_map.append('blue')
    else:
        color_map.append('green')

nx.draw(G, node_color=color_map, with_labels=True)
plt.show()

# 34 nodes 78 edges
