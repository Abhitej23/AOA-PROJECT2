# Makefile for AOA Project 2 - Marine Conservation Optimization
# C++ Implementation

CXX = g++
CXXFLAGS = -std=c++17 -O2 -Wall -Wextra
SRC_DIR = src
EXP_DIR = experiments
BIN_DIR = bin
RESULTS_DIR = results

# Targets
all: $(BIN_DIR)/problem1 $(BIN_DIR)/problem2 $(BIN_DIR)/runtime_analysis

# Create directories
$(BIN_DIR):
	mkdir -p $(BIN_DIR)

$(RESULTS_DIR):
	mkdir -p $(RESULTS_DIR)

# Problem 1: MPA Network Flow
$(BIN_DIR)/problem1: $(SRC_DIR)/problem1_mpa_network_flow.cpp | $(BIN_DIR)
	$(CXX) $(CXXFLAGS) $< -o $@

# Problem 2: Habitat Restoration
$(BIN_DIR)/problem2: $(SRC_DIR)/problem2_habitat_restoration.cpp | $(BIN_DIR)
	$(CXX) $(CXXFLAGS) $< -o $@

# Runtime Analysis (needs both problem implementations)
$(BIN_DIR)/runtime_analysis: $(EXP_DIR)/runtime_analysis.cpp | $(BIN_DIR)
	$(CXX) $(CXXFLAGS) -I$(SRC_DIR) $< -o $@

# Run examples
run-problem1: $(BIN_DIR)/problem1
	@echo "Running Problem 1: Marine Protected Area Network Flow"
	@echo "======================================================="
	@./$(BIN_DIR)/problem1

run-problem2: $(BIN_DIR)/problem2
	@echo "Running Problem 2: Marine Habitat Restoration"
	@echo "=============================================="
	@./$(BIN_DIR)/problem2

# Run experiments and generate plots
run-experiments: $(BIN_DIR)/runtime_analysis | $(RESULTS_DIR)
	@echo "Running Experimental Analysis..."
	@./$(BIN_DIR)/runtime_analysis
	@echo ""
	@if command -v gnuplot >/dev/null 2>&1; then \
		echo "Generating plots with gnuplot..."; \
		gnuplot $(RESULTS_DIR)/plot.gnu; \
		echo "✓ Plots generated successfully!"; \
	else \
		echo "Warning: gnuplot not found. Install gnuplot to generate plots."; \
		echo "Data files are available in $(RESULTS_DIR)/"; \
	fi

# Run all examples and experiments
test: run-problem1 run-problem2 run-experiments

# Clean build artifacts
clean:
	rm -rf $(BIN_DIR)
	rm -f $(RESULTS_DIR)/*.txt
	rm -f $(RESULTS_DIR)/*.gnu

# Clean everything including results
clean-all: clean
	rm -f $(RESULTS_DIR)/*.png
	rm -rf $(BIN_DIR)

# Help
help:
	@echo "AOA Project 2 - Marine Conservation Optimization (C++)"
	@echo "======================================================"
	@echo ""
	@echo "Available targets:"
	@echo "  make all              - Build all executables"
	@echo "  make run-problem1     - Run Problem 1 example"
	@echo "  make run-problem2     - Run Problem 2 example"
	@echo "  make run-experiments  - Run experimental analysis"
	@echo "  make test             - Run all examples and experiments"
	@echo "  make clean            - Remove build artifacts"
	@echo "  make clean-all        - Remove all generated files"
	@echo "  make help             - Show this help message"
	@echo ""
	@echo "Requirements:"
	@echo "  - C++17 compatible compiler (g++ or clang++)"
	@echo "  - gnuplot (optional, for generating plots)"

.PHONY: all run-problem1 run-problem2 run-experiments test clean clean-all help
