#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import argparse
import sys
import os

def load_visit_matrix(filename):
    """Load the visit matrix from the C program output"""
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()

        matrix = []
        for line in lines:
            row = list(map(int, line.strip().split()))
            matrix.append(row)

        # Convert to numpy array if possible, otherwise return list
        try:
            return np.array(matrix)
        except (AttributeError, ValueError):
            return matrix
    except FileNotFoundError:
        print(f"Error: {filename} not found. Make sure to run the C optimization first.")
        return None
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return None

def load_node_visits(filename):
    """Load node visit counts directly from C program output"""
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()

        node_visits = {}
        for line in lines:
            node_id, visits = map(int, line.strip().split())
            node_visits[node_id] = visits

        # Convert to ordered array
        n = max(node_visits.keys()) + 1
        # Create array of zeros and fill with visit counts
        visits_array = [0] * n
        for node, visits in node_visits.items():
            visits_array[node] = visits
        # Convert to numpy array if possible
        try:
            visits_array = np.array(visits_array)
        except (AttributeError, ValueError):
            pass

        return visits_array
    except FileNotFoundError:
        print(f"Error: {filename} not found. Make sure to run the C optimization first.")
        return None
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return None

def load_route_stats(filename):
    """Load route statistics from C program output"""
    stats = {}
    try:
        with open(filename, 'r') as f:
            for line in f:
                key, value = line.strip().split(': ')
                stats[key] = value
        return stats
    except FileNotFoundError:
        print(f"Error: {filename} not found. Make sure to run the C optimization first.")
        return None
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return None

def calculate_node_visit_counts(visit_matrix):
    """Calculate total visits per node from the visit matrix"""
    n = len(visit_matrix)
    # Initialize array with zeros
    node_visits = [0] * n

    # Sum all visits to and from each node
    for i in range(n):
        for j in range(n):
            if i != j:  # Don't count self-loops
                node_visits[i] += visit_matrix[i][j]  # Outgoing visits
                node_visits[j] += visit_matrix[i][j]  # Incoming visits

    # Convert to numpy array if possible
    try:
        node_visits = np.array(node_visits)
    except (AttributeError, ValueError):
        pass

    return node_visits

def generate_histogram(visit_counts, output_file="visit_histogram.png", title="Node Visit Frequency"):
    """Generate and save histogram of node visit frequencies"""
    n = len(visit_counts)

    plt.figure(figsize=(12, 6))

    # Create histogram
    bars = plt.bar(range(n), visit_counts, color='skyblue', edgecolor='navy', alpha=0.7)

    # Highlight the most visited node
    # Convert to list if it's a numpy array
    visit_list = visit_counts.tolist() if hasattr(visit_counts, 'tolist') else list(visit_counts)
    max_visits = max(visit_list)
    most_visited = visit_list.index(max_visits)

    bars[most_visited].set_color('orange')
    bars[most_visited].set_edgecolor('red')

    # Customize the plot
    plt.xlabel("Node ID", fontsize=12)
    plt.ylabel("Total Visit Count", fontsize=12)
    plt.title(f"{title} - Most Visited: Node {most_visited} ({max_visits} visits)", fontsize=14)
    plt.grid(axis='y', alpha=0.3)

    # Add value labels on top of bars for high-visited nodes
    threshold = max_visits * 0.8
    for i, v in enumerate(visit_counts):
        if v >= threshold:
            plt.text(i, v + max_visits * 0.01, str(v), ha='center', va='bottom', fontweight='bold')

    # Set x-axis ticks to show all nodes
    plt.xticks(range(n))

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Histogram saved to {output_file}")
    return most_visited, max_visits

def generate_heatmap(visit_matrix, output_file="visit_heatmap.png"):
    """Generate heatmap of the visit matrix"""
    plt.figure(figsize=(10, 8))

    # Create heatmap
    im = plt.imshow(visit_matrix, cmap='YlOrRd', interpolation='nearest')

    # Add colorbar
    plt.colorbar(im, label='Visit Count')

    # Customize the plot
    plt.xlabel("Destination Node", fontsize=12)
    plt.ylabel("Source Node", fontsize=12)
    plt.title("SSA Search Visit Matrix Heatmap", fontsize=14)

    # Add grid
    n = len(visit_matrix)
    plt.xticks(range(n))
    plt.yticks(range(n))

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Heatmap saved to {output_file}")

def print_statistics(visit_counts, visit_matrix=None):
    """Print detailed statistics about the visit patterns"""
    n = len(visit_counts)
    # Convert to list for consistent handling
    visit_list = visit_counts.tolist() if hasattr(visit_counts, 'tolist') else list(visit_counts)

    # Calculate total visits (divide by 2 because we count each edge twice)
    total_visits = sum(visit_list) // 2

    print("\n=== SSA Search Statistics ===")
    print(f"Total nodes: {n}")
    print(f"Total edge visits: {total_visits}")

    # Calculate average visits
    avg_visits = sum(visit_list) / len(visit_list) if visit_list else 0
    print(f"Average visits per node: {avg_visits:.2f}")

    # Find most visited node
    most_visited_count = max(visit_list) if visit_list else 0
    most_visited_idx = visit_list.index(most_visited_count) if visit_list else 0
    print(f"Most visited node: {most_visited_idx} ({most_visited_count} visits)")

    # Find least visited node
    least_visited_count = min(visit_list) if visit_list else 0
    least_visited_idx = visit_list.index(least_visited_count) if visit_list else 0
    print(f"Least visited node: {least_visited_idx} ({least_visited_count} visits)")

    # Calculate standard deviation
    mean = sum(visit_list) / len(visit_list) if visit_list else 0
    variance = sum((x - mean) ** 2 for x in visit_list) / len(visit_list) if visit_list else 0
    std_dev = variance ** 0.5
    print(f"Visit standard deviation: {std_dev:.2f}")

    # Show top 5 most visited nodes
    # Manual sorting for top 5
    indexed_visits = [(i, v) for i, v in enumerate(visit_list)]
    indexed_visits.sort(key=lambda x: x[1], reverse=True)
    top_indices = [idx for idx, _ in indexed_visits[:5]]

    print("\nTop 5 most visited nodes:")
    for i, idx in enumerate(top_indices):
        print(f"  {i+1}. Node {idx}: {visit_counts[idx]} visits")

    # Show distribution
    print("\nVisit distribution:")

    # Simple statistics calculations
    sorted_visits = sorted(visit_list)

    # Min value
    min_visits = min(visit_list) if visit_list else 0
    print(f"  Min: {min_visits}")

    # 25th percentile
    idx25 = int(len(sorted_visits) * 0.25)
    percentile25 = sorted_visits[idx25] if sorted_visits else 0
    print(f"  25th percentile: {percentile25}")

    # Median (50th percentile)
    mid = len(sorted_visits) // 2
    median_val = sorted_visits[mid] if sorted_visits else 0
    print(f"  Median: {int(median_val)}")

    # 75th percentile
    idx75 = int(len(sorted_visits) * 0.75)
    percentile75 = sorted_visits[idx75] if sorted_visits else 0
    print(f"  75th percentile: {percentile75}")

    # Max value
    max_visits = max(visit_list) if visit_list else 0
    print(f"  Max: {max_visits}")

def main():
    parser = argparse.ArgumentParser(description="Generate histogram from SSA visit matrix")
    parser.add_argument('--matrix', type=str, default='visit_matrix.txt',
                       help='Input visit matrix file (default: visit_matrix.txt)')
    parser.add_argument('--visits', type=str, default='node_visits.txt',
                       help='Input node visits file (default: node_visits.txt)')
    parser.add_argument('--stats', type=str, default='route_stats.txt',
                       help='Input route stats file (default: route_stats.txt)')
    parser.add_argument('--histogram', type=str, default='visit_histogram.png',
                       help='Output histogram file (default: visit_histogram.png)')
    parser.add_argument('--heatmap', type=str, default='visit_heatmap.png',
                       help='Output heatmap file (default: visit_heatmap.png)')
    parser.add_argument('--print-stats', action='store_true',
                       help='Print detailed statistics')
    parser.add_argument('--no-heatmap', action='store_true',
                       help='Skip heatmap generation')

    args = parser.parse_args()

    # Check if files exist
    matrix_exists = os.path.exists(args.matrix)
    visits_exists = os.path.exists(args.visits)

    if not matrix_exists or not visits_exists:
        print("Error: Required input files not found:")
        if not matrix_exists:
            print(f"  - {args.matrix} (visit matrix)")
        if not visits_exists:
            print(f"  - {args.visits} (node visits)")
        print("Make sure to run the C optimization program first (./ssa_sim graph.csv best_route.txt)")
        sys.exit(1)

    # Load visit counts directly if available
    print(f"Loading node visit counts from {args.visits}...")
    visit_counts = load_node_visits(args.visits)

    if visit_counts is None:
        # Fall back to calculating from matrix if direct file not available
        print(f"Falling back to visit matrix ({args.matrix}) for counts...")
        visit_matrix = load_visit_matrix(args.matrix)
        if visit_matrix is None:
            sys.exit(1)
        visit_counts = calculate_node_visit_counts(visit_matrix)

    # Load route statistics if available
    route_stats = None
    if os.path.exists(args.stats):
        print(f"Loading route statistics from {args.stats}...")
        route_stats = load_route_stats(args.stats)

    # Load visit matrix for heatmap (if needed)
    visit_matrix = None
    if not args.no_heatmap:
        print(f"Loading visit matrix from {args.matrix}...")
        visit_matrix = load_visit_matrix(args.matrix)
        if visit_matrix is None and not args.no_heatmap:
            print("Warning: Could not load visit matrix, heatmap will be skipped")
            args.no_heatmap = True

    # Generate histogram
    most_visited, max_visits = generate_histogram(visit_counts, args.histogram)

    # Generate heatmap unless disabled
    if not args.no_heatmap and visit_matrix is not None:
        generate_heatmap(visit_matrix, args.heatmap)

    # Print statistics if requested
    if args.print_stats:
        if visit_matrix is not None:
            print_statistics(visit_counts, visit_matrix)
        else:
            print_statistics(visit_counts, None)

    print(f"\nSummary:")
    print(f"  Most visited node: {most_visited} ({max_visits} visits)")
    print(f"  Total nodes analyzed: {len(visit_counts)}")

    # Print route statistics if available
    if route_stats:
        print(f"  Nodes in graph: {route_stats.get('nodes', 'unknown')}")
        print(f"  Best route length: {route_stats.get('route_length', 'unknown')}")
        print(f"  SSA iterations: {route_stats.get('iterations', 'unknown')}")
        print(f"  Population size: {route_stats.get('population', 'unknown')}")

    output_files = f"  Output files: {args.histogram}"
    if not args.no_heatmap:
        output_files += f", {args.heatmap}"
    print(output_files)

if __name__ == "__main__":
    main()
