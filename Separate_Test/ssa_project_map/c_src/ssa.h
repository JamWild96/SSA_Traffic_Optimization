#ifndef SSA_H
#define SSA_H

#include "graph.h"

/* Run discrete SSA on graph g; write best route (node indices) to best_route,
 * route_len to *out_len, using population_size sparrows for max_iter iterations. */
void run_ssa(const Graph *g,
             int population_size,
             int max_iter,
             int *best_route,
             int *out_len);

#endif /* SSA_H */
