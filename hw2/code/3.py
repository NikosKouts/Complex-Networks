from cgi import print_arguments
import matplotlib.pyplot as plt
import networkx as nx

if __name__ == "__main__":
    # Create Graph
    G = nx.Graph()
    G.add_edge(1, 2)
    G.add_edge(1, 3)
    G.add_edge(1, 4)
    G.add_edge(2, 5)
    G.add_edge(3, 4)
    G.add_edge(3, 5)
    G.add_edge(4, 5)

    # Calculate betweenness_centrality
    print("Calculating betweenness_centrality")
    edge_betweenness_centrality = nx.edge_betweenness_centrality(G)

    for ebc in edge_betweenness_centrality:
        print(ebc, '->', edge_betweenness_centrality[ebc])


    # Find the sortest paths
    print("\nSortest paths")
    shortest_paths = nx.shortest_path(G)

    for sp in shortest_paths:
        print(sp, '->', shortest_paths[sp])


    # Display the graph
    nx.draw_networkx(G)
    plt.show()