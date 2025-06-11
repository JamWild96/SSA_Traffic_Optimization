FRAMEWORK_FLAGS := -framework OpenGL -framework GLUT
# Makefile
#  - Builds the SSA executable (ssa)
#  - Builds the OpenGL visualizer (map_vis)
#  - "make run" executes the full pipeline (ssa + Python scripts)

CC       := gcc
CFLAGS   := -std=c17 -O2 -Wall
PYTHON   := python3

.PHONY: all run clean

all: ssa map_vis

ssa: ssa.c
	$(CC) $(CFLAGS) -o ssa ssa.c -lm

map_vis: map_visualization.c
	$(CC) $(CFLAGS) map_visualization.c -o map_vis $(FRAMEWORK_FLAGS)

run: ssa map_vis
	@echo "=== Running SSA ==="
	./ssa
	@echo
	@echo "=== Generating Map ==="
	$(PYTHON) map_gen.py
	@echo
	@echo "=== Simulating Traffic ==="
	$(PYTHON) simulate.py
	@echo
	@echo "=== Launching Map GUI ==="
	./map_vis

clean:
	 rm -f ssa map_vis map.json
