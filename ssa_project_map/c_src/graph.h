#ifndef GRAPH_H
#define GRAPH_H

typedef struct {
    int  num_nodes;
    double **adj_matrix;
} Graph;

/* Load a CSV adjacency matrix of size n×n */
Graph* load_graph(const char *filename);
/* Free all allocated memory for the graph */
void   free_graph(Graph *g);

#endif /* GRAPH_H */
