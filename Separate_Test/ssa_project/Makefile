CC      := gcc
CFLAGS  := -std=c17 -O2 -Wall
PYTHON  := python3

.PHONY: all build generate_map optimize simulate clean

all: build generate_map optimize simulate

build:
	$(CC) $(CFLAGS) -o ssa_sim \
		c_src/main.c c_src/graph.c c_src/ssa.c

generate_map:
	$(PYTHON) python/map_generator.py \
		--nodes 30 --density 0.2 --output graph.csv

optimize: build
	./ssa_sim graph.csv best_route.txt

simulate:
	$(PYTHON) python/traffic_simulator.py \
		--graph graph.csv --route best_route.txt

clean:
	rm -f ssa_sim best_route.txt graph.csv
