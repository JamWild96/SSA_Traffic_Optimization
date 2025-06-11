import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random
import argparse
import csv
import math
from functools import reduce

# ---------------- Graph Generation ----------------
def generate_random_graph(n, density):
    # Generate random coordinates
    coords = []
    for _ in range(n):
        coords.append([random.random(), random.random()])
    coords = np.array(coords)

    # Create adjacency matrix
    adj_matrix = np.zeros((n, n))

    # Fill adjacency matrix based on distance
    for i in range(n):
        for j in range(n):
            if i != j:
                # Calculate Euclidean distance
                dx = coords[i][0] - coords[j][0]
                dy = coords[i][1] - coords[j][1]
                dist = math.sqrt(dx**2 + dy**2)

                if dist < density:
                    adj_matrix[i][j] = round(dist * 100, 2)

    return adj_matrix, coords

def save_graph_to_csv(adj_matrix, filename):
    """Save adjacency matrix to CSV format for C program"""
    n = len(adj_matrix)
    with open(filename, 'w') as f:
        f.write(f"{n}\n")
        for i in range(n):
            row = []
            for j in range(n):
                row.append(str(adj_matrix[i][j]))
            f.write(','.join(row) + '\n')

def save_coords_to_csv(coords, filename):
    """Save coordinates to CSV format"""
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['node', 'x', 'y'])
        for i, (x, y) in enumerate(coords):
            writer.writerow([i, x, y])

# ---------------- SSA Optimization ----------------
def evaluate_route(adj_matrix, route):
    return sum(adj_matrix[route[i-1], route[i]] for i in range(1, len(route)))

def ssa_optimize(adj_matrix, max_iter=100, population_size=30):
    n = len(adj_matrix)
    # Visit tracking
    visit_counts = np.array([0] * n)

    # Initial population: random permutations
    population = []
    for _ in range(population_size):
        perm = list(range(n))
        random.shuffle(perm)
        population.append(perm)

    fitness = [evaluate_route(adj_matrix, route) for route in population]

    # Find best route
    best_idx = fitness.index(min(fitness))
    best_route = population[best_idx]
    best_fitness = min(fitness)

    for iteration in range(max_iter):
        # Producer (top 20%) randomly swaps two nodes
        producers = population[:max(population_size // 5, 1)]
        for route in producers:
            a, b = random.sample(range(n), 2)
            route[a], route[b] = route[b], route[a]
        # Scrounger: rest copy/perturb best
        for i in range(len(producers), population_size):
            source = best_route[:]
            # Mutate: shuffle part of route
            random.shuffle(source[n//2:])
            population[i] = source
        # Danger-awareness: 10% random jumps
        for _ in range(max(1, population_size // 10)):
            idx = random.randint(0, population_size-1)
            perm = list(range(n))
            random.shuffle(perm)
            population[idx] = perm
        # Evaluate, update best, and visit tracking
        for route in population:
            for node in route:
                visit_counts[node] += 1
            fit = evaluate_route(adj_matrix, route)
            if fit < best_fitness:
                best_fitness = fit
                best_route = route[:]
    return best_route, visit_counts, adj_matrix

# ---------------- Visualization ----------------
def visualize(adj_matrix, coords, best_route, visit_counts, out_png="ssa_result.png"):
    n = len(adj_matrix)
    G = nx.DiGraph()
    for i in range(n):
        G.add_node(i, pos=coords[i])
    for i in range(n):
        for j in range(n):
            if adj_matrix[i, j] > 0:
                G.add_edge(i, j, weight=adj_matrix[i, j])

    pos = {i: coords[i] for i in range(n)}
    # Highlight most visited node
    most_visited = visit_counts.tolist().index(max(visit_counts))

    node_colors = ['orange' if i==most_visited else 'lightblue' for i in range(n)]

    plt.figure(figsize=(8,8))
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500, edgecolors='black')
    nx.draw_networkx_edges(G, pos, alpha=0.4)
    nx.draw_networkx_labels(G, pos, font_size=10, font_color='black')

    # Draw best route in red, thicker
    if best_route:
        path_edges = list(zip(best_route, best_route[1:]))
        nx.draw_networkx_edges(
            G, pos, edgelist=path_edges, edge_color='red', width=3,
            arrows=True, arrowstyle='-|>', arrowsize=24, alpha=0.7
        )

    plt.title(f"SSA Best Route (red), Most Visited Node: {most_visited} (orange)")
    plt.axis('off')
    plt.savefig(out_png, bbox_inches='tight')
    plt.close()
    print(f"Saved result image: {out_png}")

# ---------------- Main ----------------
def main():
    parser = argparse.ArgumentParser(description="Generate random graph for SSA optimization")
    parser.add_argument('--nodes', type=int, default=10, help='Number of nodes')
    parser.add_argument('--density', type=float, default=0.6, help='Connection density threshold')
    parser.add_argument('--graph', type=str, default='graph.csv', help='Output graph CSV file')
    parser.add_argument('--coords', type=str, default='coords.csv', help='Output coordinates CSV file')
    parser.add_argument('--run-optimization', action='store_true', help='Run Python SSA optimization')
    parser.add_argument('--max-iter', type=int, default=50, help='Maximum SSA iterations')
    parser.add_argument('--pop-size', type=int, default=20, help='Population size')

    args = parser.parse_args()

    # Parameter validation
    if args.nodes <= 0:
        print("Error: Number of nodes must be positive")
        return 1

    if args.nodes > 1000:
        print("Warning: Large number of nodes may cause performance issues")

    if args.density < 0:
        print("Error: Density cannot be negative")
        return 1

    if args.density > 2.0:
        print("Warning: Very high density may create overly connected graphs")

    if args.max_iter <= 0:
        print("Error: Maximum iterations must be positive")
        return 1

    if args.pop_size <= 0:
        print("Error: Population size must be positive")
        return 1

    # Generate graph
    print(f"Generating graph with {args.nodes} nodes and density {args.density}")
    adj_matrix, coords = generate_random_graph(args.nodes, args.density)

    # Save for C program
    save_graph_to_csv(adj_matrix, args.graph)
    save_coords_to_csv(coords, args.coords)
    print(f"Saved graph to {args.graph}")
    print(f"Saved coordinates to {args.coords}")

    # Optionally run Python optimization
    if args.run_optimization:
        print("Running Python SSA optimization...")
        best_route, visit_counts, adj_matrix = ssa_optimize(adj_matrix, args.max_iter, args.pop_size)
        visualize(adj_matrix, coords, best_route, visit_counts, out_png="ssa_result.png")

        # Print summary
        # Find most visited node
        visit_list = visit_counts.tolist()
        most_visited_count = max(visit_list)
        most_visited_idx = visit_list.index(most_visited_count)

        print("Best route:", best_route)
        print("Most visited node:", most_visited_idx, "with", most_visited_count, "visits")

        # Save results for external analysis
        with open("results.txt", "w") as f:
            f.write("Best route: {}\n".format(best_route))
            f.write("Most visited node: {} ({} visits)\n".format(most_visited_idx, most_visited_count))
            f.write("Node visit counts:\n")
            for i, count in enumerate(visit_counts):
                f.write(f"Node {i}: {count}\n")
        print("Results written to results.txt")

        # Plot node visit counts as a histogram
        plt.figure(figsize=(8, 4))
        plt.bar(range(args.nodes), visit_counts, color='skyblue', edgecolor='black')
        plt.xlabel("Node")
        plt.ylabel("Visit Count")
        plt.title("Node Visit Frequency (SSA Search)")
        plt.savefig("visit_histogram.png", bbox_inches='tight')
        plt.close()
        print("Saved histogram to visit_histogram.png")

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
