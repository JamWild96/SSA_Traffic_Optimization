#include "ssa.h"
#include <stdlib.h>

/* Representation of a single sparrow (solution) */
typedef struct {
    int   *route;    /* sequence of node indices */
    int    len;
    double fitness;
} Sparrow;

/* Compute fitness of a sparrow’s route on graph g (e.g., total travel time) */
static double evaluate(const Graph *g, const Sparrow *sp) {
    double sum = 0.0;
    for (int i = 1; i < sp->len; i++) {
        int u = sp->route[i-1], v = sp->route[i];
        sum += g->adj_matrix[u][v];
    }
    return sum;
}

void run_ssa(const Graph *g,
             int population_size,
             int max_iter,
             int *best_route,
             int *out_len)
{
    /* Allocate population */
    Sparrow *pop = calloc(population_size, sizeof(*pop));
    for (int i = 0; i < population_size; i++) {
        /* TODO: initialize pop[i].route with a valid path */
        pop[i].len = 0;
        pop[i].fitness = 1e308;
    }

    double global_best = 1e308;
    int  *gb_route = malloc(g->num_nodes * sizeof(int));
    int   gb_len = 0;

    for (int iter = 0; iter < max_iter; iter++) {
        /* Producer stage: generate / update some sparrows */
        // TODO

        /* Scrounger stage: followers update based on best producers */
        // TODO

        /* Danger-awareness stage: random jumps to avoid local optima */
        // TODO

        /* Evaluate and track global best */
        for (int i = 0; i < population_size; i++) {
            pop[i].fitness = evaluate(g, &pop[i]);
            if (pop[i].fitness < global_best) {
                global_best = pop[i].fitness;
                gb_len = pop[i].len;
                for (int k = 0; k < gb_len; k++)
                    gb_route[k] = pop[i].route[k];
            }
        }
    }

    /* Copy best back to caller */
    *out_len = gb_len;
    for (int i = 0; i < gb_len; i++)
        best_route[i] = gb_route[i];

    /* Cleanup */
    free(gb_route);
    for (int i = 0; i < population_size; i++)
        free(pop[i].route);
    free(pop);
}
