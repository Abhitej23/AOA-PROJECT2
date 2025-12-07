# AOA Project 2: Marine Conservation Optimization

**Analysis of Algorithms - Project 2**
Due: December 11, 2025

## Overview

This project addresses two fundamental algorithmic problems in marine conservation:

1. **Marine Protected Area (MPA) Network Design** - Reducible to Network Flow (Polynomial Time)
2. **Marine Habitat Restoration Planning** - NP-Complete Problem requiring Greedy Approximation

**Implementation Language:** C++17

## Project Structure

```
AOA-PROJECT2/
├── src/
│   ├── problem1_mpa_network_flow.cpp     # Problem 1: Network Flow solution
│   ├── problem2_habitat_restoration.cpp   # Problem 2: NP-Complete with greedy
│   ├── mpa_network_flow_lib.h            # Problem 1 header (for experiments)
│   └── habitat_restoration_lib.h          # Problem 2 header (for experiments)
├── experiments/
│   ├── runtime_analysis.cpp               # C++ experimental validation
│   └── plot_results.py                    # Python plotting script
├── latex/
│   └── main.tex                           # LaTeX report (ACM format)
├── results/
│   ├── problem1_runtime.png               # Problem 1 runtime graphs
│   ├── problem2_runtime.png               # Problem 2 runtime graphs
│   ├── optimal_vs_greedy.png              # Comparison graphs
│   ├── problem1_data.txt                  # Raw data from C++ experiments
│   ├── problem2_data.txt                  # Raw data from C++ experiments
│   └── optimal_vs_greedy_data.txt         # Comparison data
├── bin/                                   # Compiled executables (generated)
│   ├── problem1
│   ├── problem2
│   └── runtime_analysis
├── Makefile                               # Build system
├── requirements.txt                       # Python dependencies (for plotting)
└── README.md                              # This file
```

## Installation

### Prerequisites

- **C++ Compiler**: g++ or clang++ with C++17 support
- **Make**: GNU Make for building
- **Python 3.8+** (optional, for plotting from C++ data)
- **LaTeX distribution** (for compiling the report)

### Install Python Dependencies (Optional - for plotting)

```bash
pip install -r requirements.txt
```

## Building the Project

### Build All Executables

```bash
make all
```

This compiles:
- `bin/problem1` - Problem 1 MPA Network Flow
- `bin/problem2` - Problem 2 Habitat Restoration
- `bin/runtime_analysis` - Experimental validation

### Build Individual Components

```bash
make bin/problem1          # Build only Problem 1
make bin/problem2          # Build only Problem 2
make bin/runtime_analysis  # Build only experiments
```

## Usage

### Problem 1: Marine Protected Area Network Flow

```bash
./bin/problem1
# OR
make run-problem1
```

### Problem 2: Marine Habitat Restoration

```bash
./bin/problem2
# OR
make run-problem2
```

### Experimental Runtime Analysis

```bash
./bin/runtime_analysis
# OR (also generates plots)
make run-experiments
```

### Generate Plots

```bash
python3 experiments/plot_results.py
```

### Run Everything

```bash
make test
```

## Key Results

### Problem 1: MPA Network Flow
- **Runtime:** ~2.8ms for 80 sites
- **Complexity:** O(n²) for sparse graphs
- **C++ is 5× faster than Python**

### Problem 2: Habitat Restoration (NP-Complete)
- **Runtime:** ~2.6ms for 80 sites (greedy)
- **Quality:** 95-100% of optimal
- **Approximation:** (1-1/e) ≈ 63.2% guarantee

## Author

**Course:** Analysis of Algorithms  
**Project:** Project 2 - Network Flow and NP-Completeness  
**Implementation:** C++17  
**Date:** December 2025
