from dataclasses import dataclass
from bs4 import BeautifulSoup
import networkx as nx


FILE_PATH = 'dataset.html'


############################################ PARSER ######################################################

graph = None

class Node:
    def __init__(self,key):
        self.left = None
        self.right = None
        self.val = key


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
    

############################################ EXERSICE 2 ######################################################


def height(root):
 
    # Check if the binary tree is empty
    if root is None:
        # If TRUE return 0
        return 0 
    # Recursively call height of each node
    leftAns = height(root.left)
    rightAns = height(root.right)
 
    # Return max(leftHeight, rightHeight) at each iteration
    return max(leftAns, rightAns) + 1


def Girvan_Newman(root, Graph):
    # Preorder Print
    print(Graph.nodes)

    while nx.is_connected(Graph):
        if Graph.number_of_edges() == 0:
            return

        # Calculate edge edge_betweenness_centrality
        edges = nx.edge_betweenness_centrality(Graph)

        #Remove edge with the biggest betweenneesss centrality
        sorted_edges = dict(sorted(edges.items(), key=lambda item: item[1]))
        remove_edge = sorted_edges.popitem()
        Graph.remove_edge(remove_edge[0][0], remove_edge[0][1])

    #Create subgraphs
    sub_graphs = list((Graph.subgraph(c) for c in nx.connected_components(Graph)))

    left_subgraph = nx.Graph(sub_graphs[0])
    right_subgraph = nx.Graph(sub_graphs[1])
   
    # left child
    root.left = Node(left_subgraph)
    Girvan_Newman(root.left, left_subgraph)

    # right child
    root.right = Node(right_subgraph)
    Girvan_Newman(root.right, right_subgraph)


def main():
    global graph

     # Parse Dataset
    collaborators = parse_dataset()

    # (Temporary) Create a Template Graph with the Collaborators as Nodes
    graph = helper_graph_node_builder(collaborators)
   
    # Add Edges the Template Graph
    helper_graph_edge_builder(graph, collaborators)

    # Graph for Computations
    GRAPH = graph_builder(graph)    

    root = Node(GRAPH)
    Girvan_Newman(root, GRAPH)

    print("Height of the tree:",height(root), "with 256 Nodes")


if __name__ == '__main__':
   main()