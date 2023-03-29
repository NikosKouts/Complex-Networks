import matplotlib.pyplot as plt
import networkx as nx


if __name__ == "__main__":
    damping_factor = [0.1, 0.3, 0.5, 0.85]

    G = nx.DiGraph()
    G.add_edge(1, 1)
    G.add_edge(1, 2)
    G.add_edge(2, 3)
    G.add_edge(3, 1)
    G.add_edge(3, 4)
    G.add_edge(3, 2)
    G.add_edge(4, 3)
    G.add_edge(4, 5)
    G.add_edge(5, 4)


    for d in damping_factor:
        print("\nPage Rank with damping factor: " + str(d))
        page_rank = nx.pagerank(G, d)
        for pr in page_rank:
            print('Node', pr, '->', page_rank[pr])
        

    nx.draw_networkx(G)
    plt.show()