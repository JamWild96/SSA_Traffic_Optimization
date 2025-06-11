#include "graph.h"
#include <stdio.h>
#include <stdlib.h>

Graph* load_graph(const char *filename) {
    FILE *f = fopen(filename, "r");
    if (!f) { perror("fopen"); return NULL; }
    int n;
    if (fscanf(f, "%d", &n) != 1) { fclose(f); return NULL; }
    Graph *g = malloc(sizeof(*g));
    g->num_nodes = n;
    g->adj_matrix = malloc(n * sizeof(double*));
    for (int i = 0; i < n; i++) {
        g->adj_matrix[i] = malloc(n * sizeof(double));
        for (int j = 0; j < n; j++) {
            if (j == n - 1) {
                // Last column - no comma
                if (fscanf(f, "%lf", &g->adj_matrix[i][j]) != 1)
                    g->adj_matrix[i][j] = 0.0;
            } else {
                // Has comma
                if (fscanf(f, "%lf,", &g->adj_matrix[i][j]) != 1)
                    g->adj_matrix[i][j] = 0.0;
            }
        }
    }
    fclose(f);
    return g;
}

void free_graph(Graph *g) {
    for (int i = 0; i < g->num_nodes; i++)
        free(g->adj_matrix[i]);
    free(g->adj_matrix);
    free(g);
}
