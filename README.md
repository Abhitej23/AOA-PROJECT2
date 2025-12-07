# AOA Project 2: Marine Conservation Optimization

**Analysis of Algorithms - Project 2**
Due: December 11, 2025

## Overview

This project addresses two fundamental algorithmic problems in marine conservation:

1. **Marine Protected Area (MPA) Network Design** - Reducible to Network Flow (Polynomial Time)
2. **Marine Habitat Restoration Planning** - NP-Complete Problem requiring Greedy Approximation

## Project Structure

```
AOA-PROJECT2/
├── src/
│   ├── problem1_mpa_network_flow.py      # Problem 1: Network Flow solution
│   └── problem2_habitat_restoration.py    # Problem 2: NP-Complete with greedy
├── experiments/
│   └── runtime_analysis.py                # Experimental validation
├── latex/
│   └── main.tex                           # LaTeX report (ACM format)
├── results/
│   ├── problem1_runtime.png               # Problem 1 runtime graphs
│   ├── problem2_runtime.png               # Problem 2 runtime graphs
│   └── optimal_vs_greedy.png              # Comparison graphs
├── requirements.txt                       # Python dependencies
└── README.md                              # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- LaTeX distribution (for compiling the report)

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

Dependencies:
- `networkx>=3.0` - Network flow algorithms
- `numpy>=1.24.0` - Numerical computations
- `matplotlib>=3.7.0` - Visualization

## Usage

### Problem 1: Marine Protected Area Network Flow

Run the example MPA network:

```bash
python3 src/problem1_mpa_network_flow.py
```

**Output:**
```
Marine Protected Area Network Flow Problem
============================================================

Budget: $50

--- Greedy Solution ---
Protected Spawning Sites: ['S1', 'S2', 'S3']
Protected Settlement Sites: ['H1', 'H2', 'H3']
Total Cost: $64
Maximum Larval Flow: 330

--- Optimal Solution (Exhaustive Search) ---
Protected Spawning Sites: ['S1', 'S2', 'S3']
Protected Settlement Sites: ['H1', 'H2']
Total Cost: $47
Maximum Larval Flow: 280
```

### Problem 2: Marine Habitat Restoration

Run the habitat restoration example:

```bash
python3 src/problem2_habitat_restoration.py
```

**Output:**
```
Marine Habitat Restoration Planning Problem
(Reduces to Budgeted Maximum Coverage - NP-Complete)
======================================================================

Total species in ecosystem: 12
Budget: $60

GREEDY SOLUTION (Cost-Effectiveness Ratio)
======================================================================
Selected sites: ['Site_A', 'Site_C', 'Site_E']
Total cost: $63.00
Species covered: 10 / 12
Coverage percentage: 83.3%

OPTIMAL SOLUTION (Exhaustive Search)
======================================================================
Selected sites: ['Site_A', 'Site_C', 'Site_E']
Total cost: $63.00
Species covered: 10 / 12
Coverage percentage: 83.3%

Greedy approximation ratio: 1.000
```

### Experimental Runtime Analysis

Run all experiments and generate graphs:

```bash
python3 experiments/runtime_analysis.py
```

This will:
- Test Problem 1 with increasing network sizes (10-80 sites)
- Test Problem 2 with increasing restoration sites (10-80 sites)
- Compare optimal vs greedy for small instances (4-12 sites)
- Generate runtime graphs in `results/` directory

**Expected runtime:** ~30-60 seconds

## Compile LaTeX Report

Navigate to the `latex/` directory and compile:

```bash
cd latex
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Or use your preferred LaTeX editor (TeXShop, Overleaf, etc.)

The compiled PDF will be `latex/main.pdf`

## Key Results

### Problem 1: MPA Network Flow

- **Complexity:** O(n³) worst-case for max-flow computation
- **Observed:** O(n²) for sparse graphs (verified experimentally)
- **Runtime:** ~15ms for 80 sites
- **Solution Quality:** Optimal when all sites are protected; greedy approximation when budget-constrained

### Problem 2: Habitat Restoration (NP-Complete)

- **Complexity:** O(n²k) for greedy algorithm (n sites, k species)
- **Optimal:** O(2ⁿ) exhaustive search - intractable beyond ~15 sites
- **Greedy Approximation:** (1-1/e) ≈ 0.632 theoretical guarantee
- **Observed Quality:** 85-95% of optimal in practice
- **Runtime:** ~1ms for 80 sites (greedy) vs exponential for optimal

### Experimental Validation

All three generated graphs confirm theoretical complexity:

1. **problem1_runtime.png** - Quadratic growth for network flow
2. **problem2_runtime.png** - Quadratic growth for greedy coverage
3. **optimal_vs_greedy.png** - Exponential optimal vs polynomial greedy

## Algorithm Descriptions

### Problem 1: Network Flow Reduction

**Abstract Problem:**
- Given: Spawning sites S, settlement habitats H, ocean currents E, budget B
- Objective: Maximize larval flow within budget

**Reduction to Max-Flow:**
1. Create source node connected to protected spawning sites (capacity = spawning output)
2. Add current edges between spawning and settlement sites (capacity = transport rate)
3. Connect settlement sites to sink (capacity = carrying capacity)
4. Compute maximum flow using Ford-Fulkerson or similar algorithm

**Correctness:** Flow conservation models larval transport; capacities enforce biological constraints

### Problem 2: NP-Completeness Proof

**Reduction from Budgeted Maximum Coverage:**
- Restoration sites ↔ Sets in coverage problem
- Species ↔ Elements to cover
- Budget constraint ↔ Cardinality/cost constraint

**Greedy Algorithm:**
1. While budget remains:
   - Select site with maximum (marginal species coverage / cost)
   - Add to solution, update covered species
2. Return selected sites

**Approximation Guarantee:** (1-1/e) ≈ 63.2% of optimal coverage

## Testing

Both implementations include example instances:

```bash
# Test Problem 1
python3 -c "from src.problem1_mpa_network_flow import create_sample_instance; \
            mpa = create_sample_instance(); \
            print('MPA instance created with', len(mpa.spawning_sites), 'spawning sites')"

# Test Problem 2
python3 -c "from src.problem2_habitat_restoration import create_sample_instance; \
            prob = create_sample_instance(); \
            print('Restoration instance with', len(prob.all_species), 'species')"
```

## Report Contents

The LaTeX report (`latex/main.tex`) includes:

1. **Abstract** - Problem summary and key results
2. **Introduction** - Motivation and contributions
3. **Problem 1** - Real problem, abstraction, reduction, algorithm, proof
4. **Problem 2** - Real problem, abstraction, NP-completeness proof, greedy algorithm
5. **Experimental Validation** - Runtime analysis with graphs
6. **Discussion** - Practical implications and future work
7. **Conclusion** - Summary of findings
8. **Appendices:**
   - Implementation code listings
   - LLM usage documentation with prompts and verification

## LLM Usage Disclosure

This project used Claude 3.5 Sonnet (Anthropic) for:
- LaTeX formatting assistance
- Python debugging suggestions
- Algorithm verification

**All LLM-generated content was manually verified** against:
- Algorithm textbooks (Cormen et al.)
- Original research papers
- Experimental validation

See Appendix B in the report for complete LLM usage documentation.

## References

1. Khuller, S., Moss, A., and Naor, J.S. (1999). The budgeted maximum coverage problem. *Information Processing Letters*, 70(1), 39-45.

2. Hochbaum, D.S. and Pathria, A. (1998). Analysis of the greedy approach in problems of maximum k-coverage. *Naval Research Logistics*, 45(6), 615-627.

3. Ford, L.R. and Fulkerson, D.R. (1956). Maximal flow through a network. *Canadian Journal of Mathematics*, 8, 399-404.

4. Cormen, T.H., Leiserson, C.E., Rivest, R.L., and Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.

## Author

**Course:** Analysis of Algorithms
**Project:** Project 2 - Network Flow and NP-Completeness
**Date:** December 2025

## License

Educational project for academic purposes.
