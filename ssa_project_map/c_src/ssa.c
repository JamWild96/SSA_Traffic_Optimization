#include "ssa.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

/* Representation of a single sparrow (solution) */
typedef struct {
    int   *route;    /* sequence of node indices */
    int    len;
    double fitness;
} Sparrow;
static int randint(int min, int max) {
    return min + rand() % (max - min + 1);
}

// Simple random permutation of [0..n-1], used for initial population
static void random_route(int *route, int n) {
    for (int i = 0; i < n; i++)
        route[i] = i;
    for (int i = n - 1; i > 0; i--) {
        int j = randint(0, i);
        int tmp = route[i];
        route[i] = route[j];
        route[j] = tmp;
    }
}

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
    srand((unsigned int)time(NULL));

    int n = g->num_nodes;
    // Adjacency matrix for visit frequency
    int **visit_matrix = malloc(n * sizeof(int *));
    for (int i = 0; i < n; i++) {
        visit_matrix[i] = calloc(n, sizeof(int));
    }

    /* Allocate population */
    Sparrow *pop = calloc(population_size, sizeof(*pop));
    for (int i = 0; i < population_size; i++) {
        pop[i].route = malloc(n * sizeof(int));
        pop[i].len = n;
        random_route(pop[i].route, n);
        pop[i].fitness = evaluate(g, &pop[i]);
    }

    double global_best = 1e308;
    int  *gb_route = malloc(g->num_nodes * sizeof(int));
    int   gb_len = 0;

    for (int iter = 0; iter < max_iter; iter++) {
        /* Sort population by fitness for producer selection */
        for (int i = 0; i < population_size - 1; i++) {
            for (int j = i + 1; j < population_size; j++) {
                if (pop[j].fitness < pop[i].fitness) {
                    Sparrow temp = pop[i];
                    pop[i] = pop[j];
                    pop[j] = temp;
                }
            }
        }

        /* Producer stage: generate / update some sparrows */
        // top 20% (by fitness) explore new solutions
        int num_producers = population_size / 5;
        if (num_producers < 1) num_producers = 1;
        for (int i = 0; i < num_producers; i++) {
            // Randomly perturb route (swap two nodes)
            int a = randint(0, n - 1);
            int b = randint(0, n - 1);
            int tmp = pop[i].route[a];
            pop[i].route[a] = pop[i].route[b];
            pop[i].route[b] = tmp;
        }

        // Scrounger stage: rest copy parts from best producers
        for (int i = num_producers; i < population_size; i++) {
            // Copy from best producer (index 0 after sorting)
            memcpy(pop[i].route, pop[0].route, n * sizeof(int));
            // Mutate by shuffling a portion
            for (int j = n/2; j < n; j++) {
                int k = randint(0, n - 1);
                int tmp = pop[i].route[j];
                pop[i].route[j] = pop[i].route[k];
                pop[i].route[k] = tmp;
            }
        }

        /* Danger-awareness stage: random jumps to avoid local optima */
        // Danger-awareness: 10% of population make random jumps
        int danger_count = population_size / 10;
        if (danger_count < 1) danger_count = 1;
        for (int i = 0; i < danger_count; i++) {
            int idx = randint(0, population_size - 1);
            random_route(pop[idx].route, n);
            pop[idx].len = n;
        }

        // Evaluate and track global best, update visit matrix
        for (int i = 0; i < population_size; i++) {
            pop[i].fitness = evaluate(g, &pop[i]);
            for (int j = 1; j < pop[i].len; j++)
                visit_matrix[pop[i].route[j-1]][pop[i].route[j]]++;
            if (pop[i].fitness < global_best) {
                global_best = pop[i].fitness;
                gb_len = pop[i].len;
                for (int k = 0; k < gb_len; k++)
                    gb_route[k] = pop[i].route[k];
            }
        }
    }

    // Output best route
     *out_len = gb_len;
     for (int i = 0; i < gb_len; i++)
         best_route[i] = gb_route[i];

     // Output the visit matrix for visualization
     FILE *vf = fopen("visit_matrix.txt", "w");
     for (int i = 0; i < n; i++) {
         for (int j = 0; j < n; j++)
             fprintf(vf, "%d%c", visit_matrix[i][j], (j==n-1)?'\n':' ');
     }
     fclose(vf);

     // Calculate node visit frequencies (for histogram)
     int *node_visits = calloc(n, sizeof(int));
     for (int i = 0; i < n; i++) {
         for (int j = 0; j < n; j++) {
             // Count both outgoing and incoming visits
             if (i != j) {
                 node_visits[i] += visit_matrix[i][j]; // outgoing
                 node_visits[j] += visit_matrix[i][j]; // incoming
             }
         }
     }

     // Output node visit frequencies for histogram
     FILE *nf = fopen("node_visits.txt", "w");
     for (int i = 0; i < n; i++) {
         fprintf(nf, "%d %d\n", i, node_visits[i]);
     }
     fclose(nf);
     free(node_visits);

     // Output route statistics
     FILE *sf = fopen("route_stats.txt", "w");
     fprintf(sf, "nodes: %d\n", n);
     fprintf(sf, "route_length: %lf\n", global_best);
     fprintf(sf, "iterations: %d\n", max_iter);
     fprintf(sf, "population: %d\n", population_size);
     fclose(sf);

     // We don't write best_route.txt here as that's done in main.c

     // Cleanup
     free(gb_route);
     for (int i = 0; i < population_size; i++)
         free(pop[i].route);
     free(pop);

     for (int i = 0; i < n; i++)
         free(visit_matrix[i]);
     free(visit_matrix);
 }
