from dataclasses import dataclass
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt
import networkx as nx
from community import community_louvain
from matplotlib import cm
from networkx.algorithms.community import greedy_modularity_communities

FILE_PATH = 'dataset.html'


############################################ PARSER ######################################################


@dataclass
class Professor:
    index: int
    name: str
    collaborators: list

    def __eq__(self, other):
        return self.name == other.name


def parse_dataset():
    with open(FILE_PATH, 'r') as file:
        content = file.read()

        data = BeautifulSoup(content, 'html.parser')
        collaborators = []
        for outer_span in data.find_all('cite'):
            collaboration = []
            for inner_span in outer_span.find_all('span'):
                try:
                    if inner_span['class'] == ['this-person']:
                        collaboration.append(inner_span.contents[0])
                except:
                    pass
            for link in outer_span.find_all('a'):
                for inner_span in link.find_all('span'):
                    try:
                        collaboration.append(inner_span['title'])
                    except:
                        pass
                if collaboration:
                    collaborators.append(collaboration)

    return collaborators


def get_professor_index_by_name(name):
    for professor in graph:
        if professor.name != name:
            continue
        return professor.index
    return -1


def helper_graph_node_builder(collaborators):
    graph = []
    index = 0
    for collaboration in collaborators:
        for professor in collaboration:
            member = Professor(index, professor, [])
            if member not in graph:
                graph.append(member)
                index = index + 1
    return graph


def helper_graph_edge_builder(graph, collaborators):
    for collaboration in collaborators:
        for professor_outer in collaboration:
            for professor_inner in collaboration:
                if professor_outer != professor_inner:
                    inner_professor_index = get_professor_index_by_name(
                        professor_inner)
                    member = Professor(inner_professor_index, professor_inner, [])

                    if member not in graph[get_professor_index_by_name(professor_outer)].collaborators:
                        graph[get_professor_index_by_name(professor_outer)].collaborators.append(member)


def graph_builder(graph):
    nx_graph = nx.Graph()

    for professor in graph:
        for collaborator in professor.collaborators:
            nx_graph.add_edge(professor.index, collaborator.index)
    return nx_graph


############################################ EXERSICE 4 ######################################################


def modularity_optimization(graph):
    communities = list(greedy_modularity_communities(graph))

    community_color = {
        0 : 'blue',
        1 : 'orange',
        2 : 'green',
        3 : 'red',
        4 : 'yellow',
        5 : 'purple',
        6 : 'cyan',
        7 : 'magenta',
        8 : 'white'
    }

    for co in communities:
        print(list(co))

    color_map = []
    for node in graph:
        iter = 0
        for comm_id in communities:
            if node in comm_id:
                color_map.append(community_color[iter])
            iter += 1
                

    nx.draw(graph, node_color=color_map, with_labels=True)
    plt.show()

  

if __name__ == '__main__':
    # Parse Dataset
    collaborators = parse_dataset()

    # (Temporary) Create a Template Graph with the Collaborators as Nodes
    graph = helper_graph_node_builder(collaborators)
   
    # Add Edges the Template Graph
    helper_graph_edge_builder(graph, collaborators)

    # Graph for Computations
    GRAPH = graph_builder(graph)    
    
    modularity_optimization(GRAPH)