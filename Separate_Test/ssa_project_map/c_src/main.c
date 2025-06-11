#include "graph.h"
#include "ssa.h"
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

/* Generate random coordinates for nodes */
void generate_coordinates(int n, double coords[][2]) {
    srand(time(NULL));
    for (int i = 0; i < n; i++) {
        coords[i][0] = (double)rand() / RAND_MAX;
        coords[i][1] = (double)rand() / RAND_MAX;
    }
}

/* Write coordinates to CSV file */
void save_coordinates(int n, double coords[][2], const char *filename) {
    FILE *f = fopen(filename, "w");
    if (!f) {
        perror("Error opening coordinates file");
        return;
    }
    
    fprintf(f, "node,x,y\n");
    for (int i = 0; i < n; i++) {
        fprintf(f, "%d,%f,%f\n", i, coords[i][0], coords[i][1]);
    }
    fclose(f);
    printf("Coordinates saved to %s\n", filename);
}

/* Generate test graph with given density */
void generate_test_graph(int n, double density, double **adj_matrix, double coords[][2]) {
    // Initialize with zeros
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            adj_matrix[i][j] = 0.0;
        }
    }
    
    // Connect nodes based on distance and density
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (i != j) {
                // Calculate Euclidean distance
                double dx = coords[i][0] - coords[j][0];
                double dy = coords[i][1] - coords[j][1];
                double dist = sqrt(dx*dx + dy*dy);
                
                if (dist < density) {
                    // Scale distance to make weights more meaningful
                    adj_matrix[i][j] = round(dist * 100.0) / 1.0;
                }
            }
        }
    }
}

/* Save graph to CSV file */
void save_graph(int n, double **adj_matrix, const char *filename) {
    FILE *f = fopen(filename, "w");
    if (!f) {
        perror("Error opening graph file");
        return;
    }
    
    fprintf(f, "%d\n", n);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            fprintf(f, "%g", adj_matrix[i][j]);
            if (j < n - 1) fprintf(f, ",");
        }
        fprintf(f, "\n");
    }
    fclose(f);
    printf("Graph saved to %s\n", filename);
}

/* Generate sample places (buildings) */
void generate_places(const char *filename) {
    FILE *f = fopen(filename, "w");
    if (!f) {
        perror("Error opening places file");
        return;
    }
    
    fprintf(f, "name,x1,y1,x2,y2\n");
    fprintf(f, "School,0.1,0.1,0.3,0.3\n");
    fprintf(f, "Hospital,0.65,0.7,0.95,0.95\n");
    fprintf(f, "Shopping Mall,0.2,0.6,0.5,0.8\n");
    fprintf(f, "Library,0.05,0.45,0.25,0.65\n");
    fprintf(f, "Park,0.75,0.1,0.95,0.4\n");
    fprintf(f, "Restaurant,0.4,0.3,0.6,0.5\n");
    fprintf(f, "Gas Station,0.8,0.6,0.9,0.7\n");
    fprintf(f, "Bank,0.3,0.8,0.5,0.95\n");
    
    fclose(f);
    printf("Sample places saved to %s\n", filename);
}

/* Generate sample traffic jams */
void generate_jams(int n, const char *filename) {
    FILE *f = fopen(filename, "w");
    if (!f) {
        perror("Error opening jams file");
        return;
    }
    
    // Generate a few random traffic jams
    int jam_count = n / 5; // 20% of nodes will have jams
    if (jam_count < 3) jam_count = 3;
    
    for (int i = 0; i < jam_count; i++) {
        int src = rand() % n;
        int dst = rand() % n;
        if (src != dst) {
            fprintf(f, "%d,%d\n", src, dst);
        }
    }
    
    fclose(f);
    printf("Sample traffic jams saved to %s\n", filename);
}

int main(int argc, char **argv) {
    if (argc < 3) {
        fprintf(stderr, "Usage: %s <graph.csv> <output_route.txt> [nodes] [density]\n", argv[0]);
        fprintf(stderr, "  nodes: number of nodes in the graph (default: 30)\n");
        fprintf(stderr, "  density: connection density 0.0-1.0 (default: 0.2)\n");
        return 1;
    }
    const char *graph_file = argv[1];
    const char *route_file = argv[2];
    
    // Optional parameters
    int n_nodes = (argc > 3) ? atoi(argv[3]) : 30;
    double density = (argc > 4) ? atof(argv[4]) : 0.2;
    
    if (n_nodes <= 0) {
        fprintf(stderr, "Error: Number of nodes must be positive\n");
        return 1;
    }
    
    if (density <= 0 || density > 1.0) {
        fprintf(stderr, "Warning: Density should be between 0.0 and 1.0\n");
        // Don't exit, just warn
    }
    
    printf("Generating graph with %d nodes and density %g\n", n_nodes, density);
    
    // Generate or load graph
    Graph *g = NULL;
    double coords[n_nodes][2];
    
    // Check if both graph and coordinates files exist
    FILE *test_graph = fopen(graph_file, "r");
    FILE *test_coords = fopen("coords.csv", "r");
    
    if (test_graph && test_coords) {
        // Both files exist - load them
        fclose(test_graph);
        fclose(test_coords);
        printf("Loading existing graph and coordinates\n");
        g = load_graph(graph_file);
        
        // We still need to populate the coords array for other functions
        printf("Loading coordinates from coords.csv\n");
        FILE *coord_file = fopen("coords.csv", "r");
        char line[256];
        // Skip header line
        fgets(line, sizeof(line), coord_file);
        
        int i = 0;
        while (i < n_nodes && fgets(line, sizeof(line), coord_file)) {
            // Parse CSV format: node,x,y
            int node;
            if (sscanf(line, "%d,%lf,%lf", &node, &coords[i][0], &coords[i][1]) != 3) {
                // Skip malformed lines
                continue;
            }
            i++;
        }
        fclose(coord_file);
        
    } else {
        // Clean up any opened file
        if (test_graph) fclose(test_graph);
        if (test_coords) fclose(test_coords);
        
        // Generate new graph and coordinates
        printf("Generating new graph and coordinates\n");
        g = malloc(sizeof(Graph));
        g->num_nodes = n_nodes;
        g->adj_matrix = malloc(n_nodes * sizeof(double*));
        for (int i = 0; i < n_nodes; i++) {
            g->adj_matrix[i] = malloc(n_nodes * sizeof(double));
        }
        
        // Generate random coordinates
        generate_coordinates(n_nodes, coords);
        save_coordinates(n_nodes, coords, "coords.csv");
        
        // Generate graph based on coordinates
        generate_test_graph(n_nodes, density, g->adj_matrix, coords);
        save_graph(n_nodes, g->adj_matrix, graph_file);
    }
    
    if (!g) {
        fprintf(stderr, "Error: Failed to create or load graph\n");
        return 2;
    }
    
    // Generate sample files for visualization
    generate_places("places.csv");
    generate_jams(g->num_nodes, "jams.csv");

    /* SSA parameters – tune as needed */
    int pop_size  = 50;
    int max_iter  = 200;

    /* Allocate buffer for best route */
    int *best_route = malloc(g->num_nodes * sizeof(int));
    int  best_len;

    printf("Running SSA optimization with pop_size=%d, max_iter=%d\n", pop_size, max_iter);
    run_ssa(g, pop_size, max_iter, best_route, &best_len);

    /* Write route to file */
    FILE *f = fopen(route_file, "w");
    for (int i = 0; i < best_len; i++)
        fprintf(f, "%d\n", best_route[i]);
    fclose(f);
    printf("Route saved to %s\n", route_file);

    free(best_route);
    free_graph(g);
    return 0;
}
