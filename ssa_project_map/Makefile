CC      := gcc
CFLAGS  := -std=c17 -O2 -Wall
LDFLAGS := -lm
PYTHON  := venv/bin/python
NODES   := 30
DENSITY := 0.2

.PHONY: all build run visualize clean deep-clean check_venv rebuild help distclean

all: build run visualize

build:
	$(CC) $(CFLAGS) -o ssa_sim \
		c_src/main.c c_src/graph.c c_src/ssa.c $(LDFLAGS)

check_venv:
	@echo "Checking virtual environment..."
	@if [ ! -f "venv/bin/python" ]; then \
		echo "Virtual environment not found. Please run 'python3 -m venv venv && source venv/bin/activate && pip install -r python/requirements.txt'"; \
		exit 1; \
	fi

run: build
	./ssa_sim graph.csv best_route.txt $(NODES) $(DENSITY)

histogram: check_venv
	@if [ ! -f "visit_matrix.txt" ]; then \
		echo "Visit matrix not found. Please run 'make run' first"; \
		exit 1; \
	fi
	$(PYTHON) python/generate_histogram.py --print-stats

map: check_venv
	@if [ ! -f "best_route.txt" ]; then \
		echo "Route file not found. Please run 'make run' first"; \
		exit 1; \
	fi
	$(PYTHON) python/draw_map.py \
		--graph graph.csv \
		--coords coords.csv \
		--route best_route.txt \
		--places places.csv \
		--jams jams.csv

visualize: check_venv histogram map
	@echo "All visualizations complete."
	@echo "Output files:"
	@echo "  - map.png: Traffic simulation map"
	@echo "  - visit_histogram.png: Visit frequency chart"
	@echo "  - visit_heatmap.png: Visit matrix heatmap"

# Run with custom parameters
custom: clean build
	./ssa_sim graph.csv best_route.txt $(NODES) $(DENSITY)
	$(MAKE) visualize

clean:
	rm -f ssa_sim best_route.txt graph.csv coords.csv map.png results.txt
	rm -f visit_histogram.png visit_heatmap.png visit_matrix.txt ssa_result.png
	rm -f places.csv jams.csv node_visits.txt route_stats.txt
	rm -f python/*.png python/test_*.csv python/results.txt
	rm -f test_*.csv test_*_route.txt perf_test*.csv perf_test*.txt
	rm -f invalid*.csv invalid*_route.txt
	find . -type d -name "__pycache__" -exec rm -rf {} +  2>/dev/null || true
	find . -name "*.pyc" -delete
	@echo "Clean complete. Run 'make build' to rebuild the project."

deep-clean: clean
	rm -rf venv
	@echo "Virtual environment removed. Use 'make rebuild' to recreate everything, or run:"
	@echo "    python3 -m venv venv && source venv/bin/activate && pip install -r python/requirements.txt"

distclean: deep-clean
	rm -f .DS_Store */.DS_Store */*/.DS_Store
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -f *.log *.tmp

rebuild:
	@echo "===== Starting complete rebuild ====="
	@echo "1. Removing old files and environment..."
	$(MAKE) deep-clean
	@echo "2. Creating fresh Python virtual environment..."
	python3 -m venv venv
	@echo "3. Installing Python dependencies..."
	./venv/bin/pip install -r python/requirements.txt
	@echo "4. Building and running..."
	$(MAKE) all
	@echo "===== Rebuild complete ====="



help:
	@echo "SSA Project Map - Available commands:"
	@echo "  make all           - Build and run the complete workflow (default)"
	@echo "  make build         - Compile the C program"
	@echo "  make run           - Run the SSA simulation (NODES=$(NODES), DENSITY=$(DENSITY))"
	@echo "  make histogram     - Generate visit frequency histogram and heatmap"
	@echo "  make map           - Generate traffic map visualization"
	@echo "  make visualize     - Generate all visualizations"
	@echo "  make custom        - Run with custom parameters (example: make custom NODES=50 DENSITY=0.4)"
	@echo "  make clean         - Remove all generated files"
	@echo "  make deep-clean    - Remove all generated files and virtual environment"
	@echo "  make distclean     - Complete cleanup (deep-clean plus system files like .DS_Store)"
	@echo "  make rebuild       - Complete rebuild from scratch"
	@echo "  make help          - Display this help message"
