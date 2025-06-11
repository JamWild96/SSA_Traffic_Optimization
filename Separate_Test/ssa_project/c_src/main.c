#include "graph.h"
#include "ssa.h"
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <graph.csv> <output_route.txt>\n", argv[0]);
        return 1;
    }
    const char *graph_file = argv[1];
    const char *route_file = argv[2];

    Graph *g = load_graph(graph_file);
    if (!g) return 2;

    /* SSA parameters – tune as needed */
    int pop_size  = 50;
    int max_iter  = 200;

    /* Allocate buffer for best route */
    int *best_route = malloc(g->num_nodes * sizeof(int));
    int  best_len;

    run_ssa(g, pop_size, max_iter, best_route, &best_len);

    /* Write route to file */
    FILE *f = fopen(route_file, "w");
    for (int i = 0; i < best_len; i++)
        fprintf(f, "%d\n", best_route[i]);
    fclose(f);

    free(best_route);
    free_graph(g);
    return 0;
}
