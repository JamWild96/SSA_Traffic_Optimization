import argparse
import csv
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os
import sys

def load_coords(filename):
    coords = {}
    try:
        with open(filename) as f:
            reader = csv.DictReader(f)
            for row in reader:
                coords[int(row['node'])] = (float(row['x']), float(row['y']))
        return coords
    except FileNotFoundError:
        print(f"Error: Coordinates file '{filename}' not found")
        print("Make sure to run the C program first: ./ssa_sim graph.csv best_route.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading coordinates: {e}")
        sys.exit(1)

def load_graph(filename):
    try:
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
    except FileNotFoundError:
        print(f"Error: Graph file '{filename}' not found")
        print("Make sure to run the C program first: ./ssa_sim graph.csv best_route.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading graph: {e}")
        sys.exit(1)

def load_places(filename):
    places = []
    if filename is None:
        return places
    try:
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
    except FileNotFoundError:
        print(f"Warning: Places file '{filename}' not found, continuing without buildings")
        return []
    except Exception as e:
        print(f"Warning: Error loading places: {e}, continuing without buildings")
        return []

def load_jams(filename):
    jammed_edges = []
    if filename is None:
        return jammed_edges
    try:
        with open(filename) as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2:
                    jammed_edges.append((int(row[0]), int(row[1])))
        return jammed_edges
    except FileNotFoundError:
        print(f"Warning: Jams file '{filename}' not found, continuing without traffic jams")
        return []
    except Exception as e:
        print(f"Warning: Error loading traffic jams: {e}, continuing without jams")
        return []

def draw_map(G, coords, route, places=None, jammed_edges=None, output_file="map.png", show_plot=False):
    fig, ax = plt.subplots(figsize=(8, 8))

    # Draw buildings/places as rectangles
    if places:
        for p in places:
            rect = Rectangle((p['x1'], p['y1']),
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
    route_edges = []
    if route and len(route) > 1:
        route_edges = list(zip(route, route[1:]))
        nx.draw_networkx_edges(G, coords, edgelist=route_edges, ax=ax,
                            edge_color='green', width=4, alpha=0.95, label="Optimal Route")

        # Add start and end markers
        start_node = route[0]
        end_node = route[-1]
        ax.scatter([coords[start_node][0]], [coords[start_node][1]],
                s=200, c='blue', marker='o', edgecolors='white', zorder=10, label='Start')
        ax.scatter([coords[end_node][0]], [coords[end_node][1]],
                s=200, c='red', marker='*', edgecolors='white', zorder=10, label='End')

    # Add a legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='lightgrey', lw=2, label='Regular Traffic'),
        Line2D([0], [0], color='red', lw=3, label='Traffic Jam'),
        Line2D([0], [0], color='green', lw=4, label='Optimal Route'),
        Line2D([0], [0], marker='s', color='w', label='Building', markerfacecolor='tan', alpha=0.5, markersize=15),
        Line2D([0], [0], marker='o', color='blue', label='Start', markersize=10),
        Line2D([0], [0], marker='*', color='red', label='End', markersize=10)
    ]
    ax.legend(handles=legend_elements, loc='upper left')

    # Add title with route information
    if route:
        plt.title(f"Optimized Route - {len(route)} nodes, {len(route_edges)} edges", fontsize=12)
    else:
        plt.title("Traffic Map (No Route)", fontsize=12)

    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    print(f"Map saved to {output_file}")

    if show_plot:
        plt.show()
    else:
        plt.close()

def load_route(filename):
    route = []
    try:
        with open(filename) as f:
            for line in f:
                line = line.strip()
                if line.isdigit():
                    route.append(int(line))
        if not route:
            print(f"Warning: No valid route found in {filename}")
        return route
    except FileNotFoundError:
        print(f"Error: Route file '{filename}' not found")
        print("Make sure to run the C program first: ./ssa_sim graph.csv best_route.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading route: {e}")
        sys.exit(1)

def load_stats(filename="route_stats.txt"):
    """Load statistics from the C program output"""
    stats = {}
    if os.path.exists(filename):
        try:
            with open(filename) as f:
                for line in f:
                    if ':' in line:
                        key, value = line.strip().split(':')
                        stats[key.strip()] = value.strip()
            return stats
        except Exception as e:
            print(f"Warning: Couldn't load stats from {filename}: {e}")
    return stats

def print_route_summary(route, stats):
    """Print a summary of the route and optimization"""
    print("\n=== Route Summary ===")
    print(f"Nodes in route: {len(route)}")

    if 'route_length' in stats:
        print(f"Route length: {stats['route_length']}")
    if 'nodes' in stats:
        print(f"Total nodes in graph: {stats['nodes']}")
    if 'iterations' in stats:
        print(f"SSA iterations: {stats['iterations']}")
    if 'population' in stats:
        print(f"Population size: {stats['population']}")

    if len(route) > 6:
        start_nodes = ', '.join(map(str, route[:3]))
        end_nodes = ', '.join(map(str, route[-3:]))
        print(f"Route: [{start_nodes}, ..., {end_nodes}]")
    else:
        print(f"Route: {route}")
    print("======================")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Draw road network with buildings, jams, and optimal route.")
    p.add_argument('--graph', type=str, default="graph.csv", help="Adjacency matrix .csv (default: graph.csv)")
    p.add_argument('--coords', type=str, default="coords.csv", help="Node coordinates .csv (default: coords.csv)")
    p.add_argument('--route', type=str, default="best_route.txt", help="File with optimal route (default: best_route.txt)")
    p.add_argument('--places', type=str, default="places.csv", help="CSV with building outlines (default: places.csv)")
    p.add_argument('--jams', type=str, default="jams.csv", help="CSV with jammed edges (default: jams.csv)")
    p.add_argument('--output', type=str, default="map.png", help="Output filename (default: map.png)")
    p.add_argument('--no-buildings', action='store_true', help="Don't include buildings")
    p.add_argument('--no-jams', action='store_true', help="Don't include traffic jams")
    p.add_argument('--show', action='store_true', help="Show map using matplotlib window")
    args = p.parse_args()

    # Check if required files exist
    for filename in [args.graph, args.coords, args.route]:
        if not os.path.exists(filename):
            print(f"Error: Required file '{filename}' doesn't exist")
            print("Make sure to run the C program first: ./ssa_sim graph.csv best_route.txt")
            sys.exit(1)

    # Load graph data from C program output files
    coords = load_coords(args.coords)
    G = load_graph(args.graph)
    route = load_route(args.route)

    # Load optimization statistics if available
    stats = load_stats()

    # Print route summary
    print_route_summary(route, stats)

    # Optional: Load buildings/places and jammed edges
    places = None if args.no_buildings else load_places(args.places)
    jammed_edges = None if args.no_jams else load_jams(args.jams)

    print(f"Generating traffic map with {len(route)} nodes...")
    draw_map(G, coords, route, places, jammed_edges, args.output, args.show)
