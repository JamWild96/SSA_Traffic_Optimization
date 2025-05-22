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
        /* TODO: initialize pop[i].route with a valid path */
        pop[i].len = 0;
        pop[i].fitness = 1e308;
    }

    double global_best = 1e308;
    int  *gb_route = malloc(g->num_nodes * sizeof(int));
    int   gb_len = 0;

    for (int iter = 0; iter < max_iter; iter++) {
        /* Producer stage: generate / update some sparrows */
        // top 20% (by fitness) explore new solutions
               int num_producers = population_size / 5;
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
                    int best_idx = 0;
                    double best_fit = pop[0].fitness;
                    for (int k = 1; k < num_producers; k++) {
                        if (pop[k].fitness < best_fit) {
                            best_fit = pop[k].fitness;
                            best_idx = k;
                        }
                    }
                    // Copy first half from best, rest random shuffle
                    memcpy(pop[i].route, pop[best_idx].route, (n/2)*sizeof(int));
                    for (int j = n/2; j < n; j++) {
                        pop[i].route[j] = randint(0, n - 1);
                    }
                }

        /* Danger-awareness stage: random jumps to avoid local optima */
        // Danger-awareness: 10% of population make random jumps
              int danger_count = population_size / 10;
              for (int i = 0; i < danger_count; i++) {
                  int idx = randint(0, population_size - 1);
                  random_route(pop[idx].route, n);
              }

        // Evaluate and track global best, update visit matrix
        for (int i = 0; i < population_size; i++) {
            pop[i].fitness = evaluate(g, &pop[i]);
            for (int j = 1; j < n; j++)
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

     // Output best route for later PNG visualization
     FILE *bf = fopen("best_route.txt", "w");
     fprintf(bf, "Best route length: %lf\n", global_best);
     for (int i = 0; i < gb_len; i++) {
         fprintf(bf, "%d ", gb_route[i]);
     }
     fprintf(bf, "\nROUTE_PNG: best_route.png\n");
     fclose(bf);

     // Cleanup
     free(gb_route);
     for (int i = 0; i < population_size; i++)
         free(pop[i].route);
     free(pop);

     for (int i = 0; i < n; i++)
         free(visit_matrix[i]);
     free(visit_matrix);
 }
