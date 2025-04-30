//SSA skeleton outline for traffic optimization

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <time.h>

#define POP_SIZE    50        // Number of sparrows
#define MAX_ITER    500       // Number of iterations
// Dimension = number of decision variables (timings + routing + detour flags)
#define DIMENSION   (num_intersections * PHASE_COUNT + MAX_ROUTES + num_intersections)

/// CONFIGURABLE PARAMETERS
enum {
    PHASE_COUNT = 4,         // e.g. 4 phases per intersection
    MAX_ROUTES  = 10,        // maximum alternative paths per origin–destination
    MAX_LINES   = 256,       // max CSV line length
};

/// DATA STRUCTURES
typedef struct {
    int    id;
    double x, y;
    int    in_deg, out_deg;
    double phase_durations[PHASE_COUNT];
    double capacity[PHASE_COUNT];
    double flow[PHASE_COUNT];
} Intersection;

typedef struct {
    double vars[DIMENSION];  // [ signal timings | routing indices | detour flags ]
    double fitness;
} Sparrow;

/// GLOBALS
static Intersection *intersections = NULL;
static int num_intersections    = 0;

// Decision-variable bounds
static double LOWER_BOUND[DIMENSION];
static double UPPER_BOUND[DIMENSION];

static Sparrow population[POP_SIZE];

/// FUNCTION PROTOTYPES
void    load_traffic_data(const char *filename);
double  evaluate_fitness(const Sparrow *s);
void    initialize_population(void);
void    update_positions(int iter);
double  rand_uniform(void);
double  rand_normal(void);
int     compare_sparrows(const void *a, const void *b);

/// MAIN
int main(void) {
    srand((unsigned)time(NULL));

    load_traffic_data("traffic_data.csv");
    initialize_population();

    for (int iter = 0; iter < MAX_ITER; ++iter) {
        update_positions(iter);
        // Optionally print best fitness:
        // printf("Iter %3d: Best fitness = %.6f\n", iter, population[0].fitness);
    }

    // Output best solution
    printf("Best fitness: %.6f\n", population[0].fitness);
    // TODO: decode and print vars as timings, routes, detours

    // Clean up
    free(intersections);
    return 0;
}

/// LOAD DATASET
void load_traffic_data(const char *filename) {
    FILE *fp = fopen(filename, "r");
    if (!fp) {
        perror("Error opening data file");
        exit(EXIT_FAILURE);
    }

    char line[MAX_LINES];
    // Read header
    fgets(line, MAX_LINES, fp);

    // Temporary storage (e.g., dynamic array) until we count lines…
    Intersection *temp = malloc(sizeof(Intersection) * 1000);
    int count = 0;

    while (fgets(line, MAX_LINES, fp)) {
        // Example CSV parse; adjust tokens to your format
        char *tok = strtok(line, ",");
        temp[count].id = atoi(tok);
        tok = strtok(NULL, ",");
        temp[count].x  = atof(tok);
        tok = strtok(NULL, ",");
        temp[count].y  = atof(tok);

        // TODO: parse in_deg, out_deg, phase_durations[], capacity[], flow[]
        // e.g.: for (int i = 0; i < PHASE_COUNT; ++i) { temp[count].phase_durations[i] = atof(strtok(NULL, ",")); }

        count++;
    }
    fclose(fp);

    num_intersections = count;
    intersections     = malloc(sizeof(Intersection) * num_intersections);
    memcpy(intersections, temp, sizeof(Intersection) * count);
    free(temp);

    // Initialize decision-variable bounds
    for (int d = 0; d < DIMENSION; ++d) {
        // Example: timings between 10s and 120s, routing indices [0, MAX_ROUTES), detour flags {0,1}
        LOWER_BOUND[d] = 0.0;
        UPPER_BOUND[d] = 1.0;
    }
}

/// FITNESS EVALUATION
double evaluate_fitness(const Sparrow *s) {
    // TODO:
    // 1. Decode s->vars into phase durations, routing decisions, detour flags
    // 2. Run traffic simulation (e.g., macroscopic queuing) for a time horizon
    // 3. Compute metrics: avg delay, max queue, throughput, bottleneck penalty
    // 4. Combine via weighted sum

    double fitness = 0.0;
    // ...
    return fitness;
}

/// INITIALIZATION
void initialize_population(void) {
    for (int i = 0; i < POP_SIZE; ++i) {
        for (int d = 0; d < DIMENSION; ++d) {
            population[i].vars[d] = LOWER_BOUND[d] +
                rand_uniform() * (UPPER_BOUND[d] - LOWER_BOUND[d]);
        }
        population[i].fitness = evaluate_fitness(&population[i]);
    }
}

/// POSITION UPDATES (SSA OPERATORS)
void update_positions(int iter) {
    // Sort by fitness ascending
    qsort(population, POP_SIZE, sizeof(Sparrow), compare_sparrows);

    int num_discover = (int)(0.2 * POP_SIZE);
    int num_scout   = POP_SIZE - (int)(0.9 * POP_SIZE);

    // Discoverers (best 20%)
    for (int i = 0; i < num_discover; ++i) {
        double alpha = 1.5;
        for (int d = 0; d < DIMENSION; ++d) {
            population[i].vars[d] *= exp(- (double)i / (alpha * MAX_ITER));
        }
    }

    // Joiners (next 70%)
    for (int i = num_discover; i < POP_SIZE - num_scout; ++i) {
        double beta = 0.5;
        int leader = rand() % num_discover;
        for (int d = 0; d < DIMENSION; ++d) {
            population[i].vars[d] += beta * rand_normal() *
                fabs(population[leader].vars[d] - population[i].vars[d]);
        }
    }

    // Scouters (worst 10%)
    for (int i = POP_SIZE - num_scout; i < POP_SIZE; ++i) {
        for (int d = 0; d < DIMENSION; ++d) {
            population[i].vars[d] = LOWER_BOUND[d] +
                rand_uniform() * (UPPER_BOUND[d] - LOWER_BOUND[d]);
        }
    }

    // Re-evaluate
    for (int i = 0; i < POP_SIZE; ++i) {
        population[i].fitness = evaluate_fitness(&population[i]);
    }
}

/// RANDOM UNIFORM [0,1)
double rand_uniform(void) {
    return (double)rand() / (RAND_MAX + 1.0);
}

/// RANDOM NORMAL (Box–Muller)
double rand_normal(void) {
    static int have_spare = 0;
    static double spare;
    if (have_spare) {
        have_spare = 0;
        return spare;
    }
    have_spare = 1;
    double u, v, s;
    do {
        u = rand_uniform() * 2.0 - 1.0;
        v = rand_uniform() * 2.0 - 1.0;
        s = u*u + v*v;
    } while (s >= 1.0 || s == 0.0);
    s = sqrt(-2.0 * log(s) / s);
    spare = v * s;
    return u * s;
}

/// COMPARATOR FOR QSORT
int compare_sparrows(const void *a, const void *b) {
    const Sparrow *sa = a;
    const Sparrow *sb = b;
    if (sa->fitness < sb->fitness) return -1;
    if (sa->fitness > sb->fitness) return  1;
    return 0;
}
