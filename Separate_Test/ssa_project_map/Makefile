CC      := gcc
CFLAGS  := -std=c17 -O2 -Wall
PYTHON  := python3

.PHONY: all build generate_map optimize visualize clean

all: build generate_map optimize visualize

build:
	$(CC) $(CFLAGS) -o ssa_sim \
		c_src/main.c c_src/graph.c c_src/ssa.c

generate_map:
	$(PYTHON) python/map_generator.py \
		--nodes 30 --density 0.2 \
		--graph graph.csv --coords coords.csv

optimize: build
	./ssa_sim graph.csv best_route.txt

visualize:
	$(PYTHON) python/draw_map.py \
		--graph graph.csv \
		--coords coords.csv \
		--route best_route.txt \
		--places places.csv \
		--jams jams.csv

clean:
	rm -f ssa_sim best_route.txt graph.csv coords.csv map.png results.txt visit_histogram.png
