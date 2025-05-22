import argparse
import csv
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

def load_places(filename):
    places = []
    if filename is None:
        return places
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Supports both rectangles (x1,y1,x2,y2) and polygons (list of x/y pairs, if you want to extend)
            place = {
                'name': row['name'],
                'x1': float(row['x1']),
                'y1': float(row['y1']),
                'x2': float(row['x2']),
                'y2': float(row['y2'])
            }
            places.append(place)
    return places

def load_jams(filename):
    jammed_edges = []
    if filename is None:
        return jammed_edges
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                jammed_edges.append((int(row[0]), int(row[1])))
    return jammed_edges

def draw_map(G, coords, route, places=None, jammed_edges=None):
    fig, ax = plt.subplots(figsize=(8, 8))

    # Draw buildings/places as rectangles
    if places:
        for p in places:
            rect = plt.Rectangle((p['x1'], p['y1']),
                                 p['x2'] - p['x1'],
                                 p['y2'] - p['y1'],
                                 linewidth=1.5, edgecolor='brown', facecolor='tan', alpha=0.35)
            ax.add_patch(rect)
            # Label the building in the center
            cx = (p['x1'] + p['x2']) / 2
            cy = (p['y1'] + p['y2']) / 2
            ax.text(cx, cy, p['name'], fontsize=10, ha='center', va='center', color='brown', alpha=0.8)

    # Draw all edges as light grey
    nx.draw_networkx_edges(G, coords, ax=ax, edge_color='lightgrey', width=1, alpha=0.6)

    # Draw jammed edges as red
    if jammed_edges:
        nx.draw_networkx_edges(G, coords, edgelist=jammed_edges, ax=ax,
                               edge_color='red', width=3, alpha=0.8, label="Traffic Jam")

    # Draw nodes
    nx.draw_networkx_nodes(G, coords, ax=ax, node_size=30, node_color='black')

    # Highlight optimal route in green
    route_edges = list(zip(route, route[1:]))
    nx.draw_networkx_edges(G, coords, edgelist=route_edges, ax=ax,
                           edge_color='green', width=4, alpha=0.95, label="Optimal Route")

    # Add a legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='lightgrey', lw=2, label='Regular Traffic'),
        Line2D([0], [0], color='red', lw=3, label='Traffic Jam'),
        Line2D([0], [0], color='green', lw=4, label='Optimal Route'),
        Line2D([0], [0], marker='s', color='w', label='Building', markerfacecolor='tan', alpha=0.5, markersize=15)
    ]
    ax.legend(handles=legend_elements, loc='upper left')

    plt.axis('off')
    plt.tight_layout()
    plt.savefig('map.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Draw road network with buildings, jams, and optimal route.")
    p.add_argument('--graph', type=str, required=True, help="Adjacency matrix .csv")
    p.add_argument('--coords', type=str, required=True, help="Node coordinates .csv")
    p.add_argument('--route', type=str, required=True, help="File with optimal route (list of node indices)")
    p.add_argument('--places', type=str, required=False, help="CSV with building outlines")
    p.add_argument('--jams', type=str, required=False, help="CSV with jammed edges (src,dst per line)")
    args = p.parse_args()

    coords = load_coords(args.coords)
    G = load_graph(args.graph)
    with open(args.route) as f:
        route = [int(line.strip()) for line in f if line.strip().isdigit()]

    # Optional: Load buildings/places and jammed edges
    places = load_places(args.places) if args.places else None
    jammed_edges = load_jams(args.jams) if args.jams else None

    print("Simulating traffic on route:", route)
    draw_map(G, coords, route, places, jammed_edges)
