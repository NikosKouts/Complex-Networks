from dataclasses import dataclass
from bs4 import BeautifulSoup
import random
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import csv
from ast import literal_eval as make_tuple

FILE_PATH = 'dataset.html'
OUTPUT_FILE = 'output.cnt'


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
    nx_graph = nx.DiGraph()

    for professor in graph:
        for collaborator in professor.collaborators:
            nx_graph.add_edge(professor.index, collaborator.index)
    return nx_graph


def visual_representation(GRAPH):
    position = nx.spring_layout(GRAPH, seed=225)
    options = {
        "font_size": 7,
        "node_size": 200,
        "node_color": "yellow",
        "edgecolors": "black",
        "linewidths": 1,
        "width": 1,
    }
    nx.draw_networkx(GRAPH, position, **options)

    # Set margins for the axes so that nodes aren't clipped
    ax = plt.gca()
    plt.axis("off")
    plt.show()


def page_rank(GRAPH):
    page_rank = nx.pagerank(GRAPH)
    for pr in page_rank:
        #print('Node', pr, '->', page_rank[pr])
        print(page_rank[pr])
        

if __name__ == '__main__':
    # Parse Dataset
    collaborators = parse_dataset()

    # (Temporary) Create a Template Graph with the Collaborators as Nodes
    graph = helper_graph_node_builder(collaborators)

    # Add Edges the Template Graph
    helper_graph_edge_builder(graph, collaborators)

    # Graph for Computations
    GRAPH = graph_builder(graph)

    # Show Nearest Neighbor Edge Centrality for each Edge
    page_rank(GRAPH)

    # Visually Display Graph
    visual_representation(GRAPH)