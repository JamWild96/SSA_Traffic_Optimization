// Psuedocode for SSA Traffic Simulation in C17
#ifndef TRAFFIC_SIM_H
#define TRAFFIC_SIM_H

// import statements
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

// Data structures for the different parameters: Sparrows, Traffic, Area of Focus, and Simulation Run
// Sparrows
typedef struct {
    int id;
    double x, y;
    double speed;
    double direction;
} Sparrow;

// Traffic/Vehicles
typedef struct {
    int id;
    double x, y;
    double speed;
    double direction;
} Traffic;

// Area of Focus
typedef struct {
    double x1, y1;
    double x2, y2;
} AreaOfFocus;

// Simulation Run
typedef struct {
    int id;
    double time;
    double speed;
    double direction;
} SimulationRun;

// Sparrow Initialization: Define the problem's objective function.
// Set population size (N), search space dimensions (D), maximum iterations (MaxIter), and other parameters.
void setParameters(int N, int D, int MaxIter, double minSpeed, double maxSpeed, double minDirection, double maxDirection);

// Initialize the sparrow population (X) randomly within the search space.
void initializePopulation(Sparrow* population, int N, double minX, double maxX, double minY, double maxY);

// Calculate the fitness value of each sparrow.
double calculateFitness(Sparrow* population, int N, Traffic* traffic, int numTraffic, AreaOfFocus* areaOfFocus);

// Initialize the traffic population (X) randomly within the search space.
void initializeTraffic(Traffic* traffic, int numTraffic, double minX, double maxX, double minY, double maxY);

// Calculate the fitness value of each traffic.
double calculateTrafficFitness(Traffic* traffic, int numTraffic, AreaOfFocus* areaOfFocus);

// Initialize the simulation run population (X) randomly within the search space.
void initializeSimulationRun(SimulationRun* simulationRun, int numSimulationRun, double minX, double maxX, double minY, double maxY);


// Calculate the fitness value of each simulation run.
double calculateSimulationRunFitness(SimulationRun* simulationRun, int numSimulationRun, AreaOfFocus* areaOfFocus);

#endif
