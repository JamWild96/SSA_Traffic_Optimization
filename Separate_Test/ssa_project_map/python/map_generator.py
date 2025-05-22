import argparse, csv, random, math

def generate_graph(n, density, graph_file, coords_file):
    # Generate random node positions
    coords = [(random.random(), random.random()) for _ in range(n)]
    # Write coordinates
    with open(coords_file, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['node', 'x', 'y'])
        for i, (x, y) in enumerate(coords):
            w.writerow([i, x, y])
    # Write adjacency matrix with weights based on distance threshold
    with open(graph_file, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow([n])
        for i in range(n):
            row = []
            for j in range(n):
                if i == j:
                    row.append(0.0)
                else:
                    dx = coords[i][0] - coords[j][0]
                    dy = coords[i][1] - coords[j][1]
                    dist = math.hypot(dx, dy)
                    if dist < density:
                        weight = round(dist * 100, 2)
                        row.append(weight)
                    else:
                        row.append(0.0)
                # end if
            w.writerow(row)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('--nodes', type=int, required=True)
    p.add_argument('--density', type=float, required=True)
    p.add_argument('--graph', type=str, required=True)
    p.add_argument('--coords', type=str, required=True)
    args = p.parse_args()
    generate_graph(args.nodes, args.density, args.graph, args.coords)

#Save the result of the adjacency matrix to a variable


#Mark the node most visited by the sparrows from the adjacency matrix
