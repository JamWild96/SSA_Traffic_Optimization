import argparse, csv
import networkx as nx
import matplotlib.pyplot as plt

def load_graph(filename):
    with open(filename) as f:
        reader = csv.reader(f)
        n = int(next(reader)[0])
        G = nx.DiGraph()
        for i in range(n):
            row = list(map(float, next(reader)))
            for j, w in enumerate(row):
                if w>0:
                    G.add_edge(i,j,weight=w)
    return G

def draw_route(G, route):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=300)
    edges = list(zip(route, route[1:]))
    nx.draw_networkx_edges(G, pos,
                           edgelist=edges,
                           width=3.0,
                           edge_color='r')
    plt.show()

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('--graph', type=str, required=True)
    p.add_argument('--route', type=str, required=True)
    args = p.parse_args()

    G = load_graph(args.graph)
    with open(args.route) as f:
        route = [int(line.strip()) for line in f if line.strip().isdigit()]

    print("Simulating traffic on route:", route)
    draw_route(G, route)
