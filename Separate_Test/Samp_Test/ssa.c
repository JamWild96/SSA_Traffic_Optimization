// ssa.c
// Sparrow Search Algorithm (SSA) implementation in C17.
// Compile with: gcc -std=c17 -O2 -Wall -o ssa ssa.c -lm

#include <stdio.h>   // printf, fprintf
#include <stdlib.h>  // rand, srand, EXIT_SUCCESS
#include <math.h>    // sqrt, exp
#include <time.h>    // time

#define POP_SIZE   20     // Number of sparrows in the population
#define DIM        2      // Problem dimensionality (e.g., x and y coordinates)
#define MAX_ITER   100    // Total number of iterations to perform
#define LOWER      0.0    // Lower bound of search space
#define UPPER     100.0   // Upper bound of search space

typedef struct {
    double pos[DIM];    // Position vector of dimensionality DIM
    double fitness;     // Fitness value at this position
} Sparrow;

static double evaluate(double pos[]) {
    double dx = pos[0] - 50.0;
    double dy = pos[1] - 50.0;
    return sqrt(dx*dx + dy*dy);
}

static void initialize(Sparrow pop[]) {
    for (int i = 0; i < POP_SIZE; i++) {
        for (int d = 0; d < DIM; d++) {
            pop[i].pos[d] = LOWER + (double)rand() / RAND_MAX * (UPPER - LOWER);
        }
        pop[i].fitness = evaluate(pop[i].pos);
    }
}

static void update_positions(Sparrow pop[], int iter) {
    int best = 0, worst = 0;
    for (int i = 1; i < POP_SIZE; i++) {
        if (pop[i].fitness < pop[best].fitness)   best = i;
        if (pop[i].fitness > pop[worst].fitness)  worst = i;
    }
    for (int i = 0; i < POP_SIZE/2; i++) {
        for (int d = 0; d < DIM; d++) {
            double r = (double)rand() / RAND_MAX;
            if (r < 0.8) {
                pop[i].pos[d] *= exp(- (double)i / (iter + 1));
            } else {
                pop[i].pos[d] = LOWER + (double)rand() / RAND_MAX * (UPPER - LOWER);
            }
        }
        pop[i].fitness = evaluate(pop[i].pos);
    }
    for (int i = POP_SIZE/2; i < POP_SIZE; i++) {
        for (int d = 0; d < DIM; d++) {
            double r = (double)rand() / RAND_MAX;
            pop[i].pos[d] += r * (pop[best].pos[d] - pop[i].pos[d]);
            if (pop[i].pos[d] < LOWER) pop[i].pos[d] = LOWER;
            if (pop[i].pos[d] > UPPER) pop[i].pos[d] = UPPER;
        }
        pop[i].fitness = evaluate(pop[i].pos);
    }
    for (int d = 0; d < DIM; d++) {
        double r = (double)rand() / RAND_MAX;
        pop[worst].pos[d] += r * (pop[worst].pos[d] - pop[best].pos[d]);
        if (pop[worst].pos[d] < LOWER) pop[worst].pos[d] = LOWER;
        if (pop[worst].pos[d] > UPPER) pop[worst].pos[d] = UPPER;
    }
    pop[worst].fitness = evaluate(pop[worst].pos);
}

int main(void) {
    srand((unsigned)time(NULL));
    Sparrow population[POP_SIZE];
    initialize(population);

    int  best_idx  = 0;
    double best_fit = population[0].fitness;
    for (int iter = 0; iter < MAX_ITER; iter++) {
        update_positions(population, iter);
        for (int i = 0; i < POP_SIZE; i++) {
            if (population[i].fitness < best_fit) {
                best_fit = population[i].fitness;
                best_idx = i;
            }
        }
        printf("Iter %3d: best fitness = %8.4f at (%6.2f, %6.2f)",
               iter,
               best_fit,
               population[best_idx].pos[0],
               population[best_idx].pos[1]);
    }
    printf("Optimal solution: fitness = %8.4f at (%6.2f, %6.2f)",
           best_fit,
           population[best_idx].pos[0],
           population[best_idx].pos[1]);
    return EXIT_SUCCESS;
}
