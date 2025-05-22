import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random, math

# ---------------- Graph Generation ----------------
def generate_random_graph(n, density):
    coords = np.random.rand(n, 2)
    adj_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                dist = np.linalg.norm(coords[i] - coords[j])
                if dist < density:
                    adj_matrix[i][j] = round(dist * 100, 2)
    return adj_matrix, coords

# ---------------- SSA Optimization ----------------
def evaluate_route(adj_matrix, route):
    return sum(adj_matrix[route[i-1], route[i]] for i in range(1, len(route)))

def ssa_optimize(adj_matrix, max_iter=100, population_size=30):
    n = len(adj_matrix)
    # Visit tracking
    visit_counts = np.zeros(n, dtype=int)
    # Initial population: random permutations
    population = [np.random.permutation(n).tolist() for _ in range(population_size)]
    fitness = [evaluate_route(adj_matrix, route) for route in population]
    best_route = population[np.argmin(fitness)]
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
            population[idx] = np.random.permutation(n).tolist()
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
    most_visited = np.argmax(visit_counts)
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
if __name__ == "__main__":
    # Parameters (edit as needed)
    N_NODES = 10
    DENSITY = 0.6  # Lower for sparser, higher for denser graphs
    MAX_ITER = 50
    POP_SIZE = 20

    adj_matrix, coords = generate_random_graph(N_NODES, DENSITY)
    best_route, visit_counts, adj_matrix = ssa_optimize(adj_matrix, MAX_ITER, POP_SIZE)
    visualize(adj_matrix, coords, best_route, visit_counts, out_png="ssa_result.png")

    # Print summary
    print("Best route:", best_route)
    print("Most visited node:", np.argmax(visit_counts), "with", np.max(visit_counts), "visits")

    # Save results for external analysis
    with open("results.txt", "w") as f:
        f.write("Best route: {}\n".format(best_route))
        f.write("Most visited node: {} ({} visits)\n".format(np.argmax(visit_counts), np.max(visit_counts)))
        f.write("Node visit counts:\n")
        for i, count in enumerate(visit_counts):
            f.write(f"Node {i}: {count}\n")
    print("Results written to results.txt")

    # Plot node visit counts as a histogram
    plt.figure(figsize=(8, 4))
    plt.bar(range(N_NODES), visit_counts, color='skyblue', edgecolor='black')
    plt.xlabel("Node")
    plt.ylabel("Visit Count")
    plt.title("Node Visit Frequency (SSA Search)")
    plt.savefig("visit_histogram.png", bbox_inches='tight')
    plt.close()
    print("Saved histogram to visit_histogram.png")
