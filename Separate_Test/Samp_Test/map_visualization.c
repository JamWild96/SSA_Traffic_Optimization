// map_visualization.c
// OpenGL grid visualizer for the JSON map.
// Compile with: gcc -std=c17 -O2 -Wall map_visualization.c -lGL -lGLU -lglut -o map_vis

#include <stdio.h>    // fopen, fgetc, fprintf, stderr
#include <stdlib.h>   // exit, EXIT_FAILURE

#if defined(__APPLE__)
#  include <OpenGL/gl.h>
#  include <OpenGL/glu.h>
#  include <GLUT/glut.h>
#else
#  include <GL/gl.h>
#  include <GL/glu.h>
#  include <GL/glut.h>
#endif

#define GRID_SIZE 20  // Must match map_gen.py's GRID_SIZE

// Grid representation: 0 = free cell, 1 = blocked cell
static int grid[GRID_SIZE][GRID_SIZE];

/**
 * Loads map data from a file.
 * @param filename The filename to load from
 */
void load_map(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        fprintf(stderr, "Error: cannot open %s\n", filename);
        exit(EXIT_FAILURE);
    }

    int cell_count = 0;
    int ch;
    while ((ch = fgetc(file)) != EOF && cell_count < GRID_SIZE * GRID_SIZE) {
        if (ch == '0' || ch == '1') {
            grid[cell_count / GRID_SIZE][cell_count % GRID_SIZE] = ch - '0';
            cell_count++;
        }
    }

    fclose(file);

    if (cell_count < GRID_SIZE * GRID_SIZE) {
        fprintf(stderr, "Error: map data incomplete (read %d entries)\n", cell_count);
        exit(EXIT_FAILURE);
    }
}

/**
 * Displays the grid using OpenGL.
 */
void display(void) {
    glClear(GL_COLOR_BUFFER_BIT);

    double cell_size = 2.0 / GRID_SIZE;
    for (int row = 0; row < GRID_SIZE; row++) {
        for (int col = 0; col < GRID_SIZE; col++) {
            // Set color based on cell type (blocked or free)
            if (grid[row][col]) {
                glColor3f(0.2f, 0.2f, 0.2f);  // Dark gray for blocked cells
            } else {
                glColor3f(0.9f, 0.9f, 0.9f);  // Light gray for free cells
            }

            // Calculate cell position
            double x = -1.0 + col * cell_size;
            double y = -1.0 + row * cell_size;

            // Draw the cell as a quad
            glBegin(GL_QUADS);
            glVertex2f(x, y);
            glVertex2f(x + cell_size, y);
            glVertex2f(x + cell_size, y + cell_size);
            glVertex2f(x, y + cell_size);
            glEnd();
        }
    }

    glutSwapBuffers();
}

/**
 * Main program entry point.
 */
int main(int argc, char **argv) {
    // Load the map data
    load_map("map.json");

    // Initialize GLUT
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB);
    glutInitWindowSize(600, 600);
    glutCreateWindow("Map Visualization");

    // Set the display callback
    glutDisplayFunc(display);

    // Enter the main loop
    glutMainLoop();

    return EXIT_SUCCESS;
}
