import argparse, csv
import networkx as nx
import matplotlib.pyplot as plt

def load_coords(filename):
    coords = {}
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            coords[int(row['node'])] = (float(row['x']), float(row['y']))
    return coords

def load_graph(filename):
    with open(filename) as f:
        reader = csv.reader(f)
        n = int(next(reader)[0])
        G = nx.DiGraph()
        for i in range(n):
            row = list(map(float, next(reader)))
            for j, w in enumerate(row):
                if w > 0:
                    G.add_edge(i, j, weight=w)
    return G

def draw_map(G, coords, route):
    fig, ax = plt.subplots(figsize=(8, 8))
    # Draw all edges as light grey
    nx.draw_networkx_edges(G, coords, ax=ax, edge_color='lightgrey', width=1)
    # Draw nodes
    nx.draw_networkx_nodes(G, coords, ax=ax, node_size=30, node_color='black')
    # Highlight optimal route in blue
    route_edges = list(zip(route, route[1:]))
    nx.draw_networkx_edges(G, coords, edgelist=route_edges, ax=ax, edge_color='blue', width=3)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('map.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('--graph', type=str, required=True)
    p.add_argument('--coords', type=str, required=True)
    p.add_argument('--route', type=str, required=True)
    args = p.parse_args()

    coords = load_coords(args.coords)
    G = load_graph(args.graph)
    with open(args.route) as f:
        route = [int(line.strip()) for line in f if line.strip().isdigit()]

    print("Simulating traffic on route:", route)
    draw_map(G, coords, route)
