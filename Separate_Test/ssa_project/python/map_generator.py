import argparse, csv, random

def generate_graph(n, density, filename):
    # First column: n, then n×n weights
    with open(filename, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow([n])
        for i in range(n):
            row = []
            for j in range(n):
                if i==j: row.append(0.0)
                else:
                    row.append(round(random.random()*100 if random.random()<density else 0.0,2))
            w.writerow(row)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('--nodes', type=int, required=True)
    p.add_argument('--density', type=float, required=True)
    p.add_argument('--output', type=str, required=True)
    args = p.parse_args()
    generate_graph(args.nodes, args.density, args.output)
