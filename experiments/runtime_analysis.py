"""
Experimental Runtime Analysis for AOA Project 2
Author: Analysis of Algorithms Project 2
Date: December 2025

This module conducts experimental analysis of running times for both problems.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import time
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for server environments
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict
import random

from problem1_mpa_network_flow import MPANetworkFlow
from problem2_habitat_restoration import HabitatRestorationProblem


class RuntimeAnalyzer:
    """Conducts runtime experiments and generates analysis graphs."""

    def __init__(self, output_dir: str = '../results'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_random_mpa_instance(self, n_spawning: int, n_settlement: int,
                                     edge_probability: float = 0.3) -> MPANetworkFlow:
        """
        Generate random MPA network instance.

        Args:
            n_spawning: Number of spawning sites
            n_settlement: Number of settlement sites
            edge_probability: Probability of ocean current connection

        Returns:
            MPANetworkFlow instance
        """
        mpa = MPANetworkFlow()

        # Add spawning sites
        for i in range(n_spawning):
            capacity = random.uniform(50, 200)
            cost = random.uniform(5, 20)
            mpa.add_spawning_site(f'S{i}', capacity, cost)

        # Add settlement sites
        for i in range(n_settlement):
            capacity = random.uniform(50, 200)
            cost = random.uniform(5, 20)
            mpa.add_settlement_site(f'H{i}', capacity, cost)

        # Add random current connections
        for i in range(n_spawning):
            for j in range(n_settlement):
                if random.random() < edge_probability:
                    transport = random.uniform(30, 100)
                    mpa.add_current_connection(f'S{i}', f'H{j}', transport)

        return mpa

    def generate_random_restoration_instance(self, n_sites: int,
                                            n_species: int) -> HabitatRestorationProblem:
        """
        Generate random habitat restoration instance.

        Args:
            n_sites: Number of restoration sites
            n_species: Number of species

        Returns:
            HabitatRestorationProblem instance
        """
        problem = HabitatRestorationProblem()
        species_names = [f'Species_{i}' for i in range(n_species)]

        for i in range(n_sites):
            # Each site covers random subset of species
            coverage_size = random.randint(max(1, n_species // 4), max(2, n_species // 2))
            covered = set(random.sample(species_names, coverage_size))
            cost = random.uniform(10, 50)
            problem.add_restoration_site(f'Site_{i}', covered, cost)

        return problem

    def experiment_problem1_greedy(self, sizes: List[int],
                                  trials: int = 5) -> Dict[str, List]:
        """
        Experiment with Problem 1 greedy algorithm runtime.

        Args:
            sizes: List of problem sizes (total number of sites)
            trials: Number of trials per size

        Returns:
            Dictionary with sizes and timing data
        """
        print("\n" + "=" * 70)
        print("Problem 1: MPA Network Flow - Greedy Runtime Analysis")
        print("=" * 70)

        results = {
            'sizes': [],
            'mean_times': [],
            'std_times': [],
            'min_times': [],
            'max_times': []
        }

        for size in sizes:
            n_spawning = size // 2
            n_settlement = size - n_spawning

            times = []
            for trial in range(trials):
                mpa = self.generate_random_mpa_instance(n_spawning, n_settlement)
                budget = sum(s['cost'] for s in mpa.spawning_sites[:n_spawning//2])

                start = time.perf_counter()
                mpa.greedy_site_selection(budget)
                end = time.perf_counter()

                times.append(end - start)

            results['sizes'].append(size)
            results['mean_times'].append(np.mean(times))
            results['std_times'].append(np.std(times))
            results['min_times'].append(np.min(times))
            results['max_times'].append(np.max(times))

            print(f"Size {size:3d}: {np.mean(times)*1000:8.3f} ms "
                  f"(±{np.std(times)*1000:6.3f} ms)")

        return results

    def experiment_problem1_maxflow(self, sizes: List[int],
                                   trials: int = 5) -> Dict[str, List]:
        """
        Experiment with Problem 1 max flow computation runtime.

        Args:
            sizes: List of problem sizes
            trials: Number of trials per size

        Returns:
            Dictionary with sizes and timing data
        """
        print("\n" + "=" * 70)
        print("Problem 1: Max Flow Computation Runtime Analysis")
        print("=" * 70)

        results = {
            'sizes': [],
            'mean_times': [],
            'std_times': []
        }

        for size in sizes:
            n_spawning = size // 2
            n_settlement = size - n_spawning

            times = []
            for trial in range(trials):
                mpa = self.generate_random_mpa_instance(n_spawning, n_settlement)

                # Select random subset of sites
                prot_spawn = set(random.sample([s['id'] for s in mpa.spawning_sites],
                                              n_spawning // 2))
                prot_settle = set(random.sample([s['id'] for s in mpa.settlement_sites],
                                               n_settlement // 2))

                start = time.perf_counter()
                mpa.solve_max_flow(prot_spawn, prot_settle)
                end = time.perf_counter()

                times.append(end - start)

            results['sizes'].append(size)
            results['mean_times'].append(np.mean(times))
            results['std_times'].append(np.std(times))

            print(f"Size {size:3d}: {np.mean(times)*1000:8.3f} ms "
                  f"(±{np.std(times)*1000:6.3f} ms)")

        return results

    def experiment_problem2_greedy(self, sizes: List[Tuple[int, int]],
                                  trials: int = 5) -> Dict[str, List]:
        """
        Experiment with Problem 2 greedy algorithm runtime.

        Args:
            sizes: List of (n_sites, n_species) tuples
            trials: Number of trials per size

        Returns:
            Dictionary with sizes and timing data
        """
        print("\n" + "=" * 70)
        print("Problem 2: Habitat Restoration - Greedy Runtime Analysis")
        print("=" * 70)

        results = {
            'sizes': [],
            'mean_times': [],
            'std_times': [],
            'min_times': [],
            'max_times': []
        }

        for n_sites, n_species in sizes:
            times = []
            for trial in range(trials):
                problem = self.generate_random_restoration_instance(n_sites, n_species)
                budget = sum(s['cost'] for s in problem.sites[:n_sites//2])

                start = time.perf_counter()
                problem.greedy_coverage(budget)
                end = time.perf_counter()

                times.append(end - start)

            results['sizes'].append(n_sites)
            results['mean_times'].append(np.mean(times))
            results['std_times'].append(np.std(times))
            results['min_times'].append(np.min(times))
            results['max_times'].append(np.max(times))

            print(f"Sites={n_sites:3d}, Species={n_species:3d}: "
                  f"{np.mean(times)*1000:8.3f} ms (±{np.std(times)*1000:6.3f} ms)")

        return results

    def experiment_problem2_optimal_vs_greedy(self, max_sites: int = 12) -> Dict:
        """
        Compare optimal exhaustive search vs greedy for small instances.

        Args:
            max_sites: Maximum number of sites to test

        Returns:
            Dictionary with comparison data
        """
        print("\n" + "=" * 70)
        print("Problem 2: Optimal vs Greedy Comparison")
        print("=" * 70)

        results = {
            'sizes': [],
            'optimal_times': [],
            'greedy_times': [],
            'optimal_coverage': [],
            'greedy_coverage': [],
            'approximation_ratios': []
        }

        for n_sites in range(4, max_sites + 1, 2):
            n_species = n_sites * 2
            problem = self.generate_random_restoration_instance(n_sites, n_species)
            budget = sum(s['cost'] for s in problem.sites[:n_sites//2])

            # Optimal solution
            start = time.perf_counter()
            opt_sel, opt_cov, opt_cost = problem.optimal_solution_small(budget)
            opt_time = time.perf_counter() - start

            # Greedy solution
            start = time.perf_counter()
            greedy_sel, greedy_cov, greedy_cost = problem.greedy_coverage(budget)
            greedy_time = time.perf_counter() - start

            approx_ratio = greedy_cov / opt_cov if opt_cov > 0 else 1.0

            results['sizes'].append(n_sites)
            results['optimal_times'].append(opt_time)
            results['greedy_times'].append(greedy_time)
            results['optimal_coverage'].append(opt_cov)
            results['greedy_coverage'].append(greedy_cov)
            results['approximation_ratios'].append(approx_ratio)

            print(f"Sites={n_sites:2d}: Optimal={opt_time*1000:7.2f}ms, "
                  f"Greedy={greedy_time*1000:6.3f}ms, "
                  f"Approx={approx_ratio:.3f}")

        return results

    def plot_problem1_results(self, results: Dict):
        """Generate plots for Problem 1 runtime analysis."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        # Plot 1: Runtime vs Problem Size
        sizes = results['sizes']
        mean_times = np.array(results['mean_times']) * 1000  # Convert to ms
        std_times = np.array(results['std_times']) * 1000

        ax1.errorbar(sizes, mean_times, yerr=std_times, marker='o',
                    capsize=5, linewidth=2, markersize=8, label='Observed')

        # Fit polynomial curve (expected O(n^2) or O(n^3) for flow algorithms)
        if len(sizes) >= 3:
            coeffs = np.polyfit(sizes, mean_times, 2)
            poly = np.poly1d(coeffs)
            x_smooth = np.linspace(min(sizes), max(sizes), 100)
            ax1.plot(x_smooth, poly(x_smooth), '--', linewidth=2,
                    label=f'Quadratic fit', alpha=0.7)

        ax1.set_xlabel('Problem Size (Total Sites)', fontsize=12)
        ax1.set_ylabel('Runtime (ms)', fontsize=12)
        ax1.set_title('Problem 1: Greedy MPA Selection Runtime', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Plot 2: Log-log scale
        ax2.loglog(sizes, mean_times, 'o-', linewidth=2, markersize=8, label='Observed')

        # Fit power law
        if len(sizes) >= 3:
            log_sizes = np.log(sizes)
            log_times = np.log(mean_times)
            slope, intercept = np.polyfit(log_sizes, log_times, 1)
            fitted = np.exp(intercept) * np.array(sizes) ** slope
            ax2.loglog(sizes, fitted, '--', linewidth=2,
                      label=f'Power law: O(n^{slope:.2f})', alpha=0.7)

        ax2.set_xlabel('Problem Size (Total Sites)', fontsize=12)
        ax2.set_ylabel('Runtime (ms)', fontsize=12)
        ax2.set_title('Problem 1: Log-Log Scale Analysis', fontsize=14, fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3, which='both')

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/problem1_runtime.png', dpi=300, bbox_inches='tight')
        print(f"\n✓ Saved plot: {self.output_dir}/problem1_runtime.png")
        plt.close()

    def plot_problem2_results(self, results: Dict):
        """Generate plots for Problem 2 runtime analysis."""
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))

        sizes = results['sizes']
        mean_times = np.array(results['mean_times']) * 1000
        std_times = np.array(results['std_times']) * 1000

        ax.errorbar(sizes, mean_times, yerr=std_times, marker='s',
                   capsize=5, linewidth=2, markersize=8, label='Observed')

        # Fit quadratic (expected O(n^2) for greedy)
        if len(sizes) >= 3:
            coeffs = np.polyfit(sizes, mean_times, 2)
            poly = np.poly1d(coeffs)
            x_smooth = np.linspace(min(sizes), max(sizes), 100)
            ax.plot(x_smooth, poly(x_smooth), '--', linewidth=2,
                   label='Quadratic fit: O(n²)', alpha=0.7)

        ax.set_xlabel('Number of Restoration Sites', fontsize=12)
        ax.set_ylabel('Runtime (ms)', fontsize=12)
        ax.set_title('Problem 2: Greedy Coverage Runtime', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/problem2_runtime.png', dpi=300, bbox_inches='tight')
        print(f"✓ Saved plot: {self.output_dir}/problem2_runtime.png")
        plt.close()

    def plot_optimal_vs_greedy(self, results: Dict):
        """Generate comparison plots for optimal vs greedy."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        sizes = results['sizes']
        opt_times = np.array(results['optimal_times']) * 1000
        greedy_times = np.array(results['greedy_times']) * 1000

        # Plot 1: Runtime comparison
        ax1.semilogy(sizes, opt_times, 'o-', linewidth=2, markersize=8,
                    label='Optimal (Exponential)', color='red')
        ax1.semilogy(sizes, greedy_times, 's-', linewidth=2, markersize=8,
                    label='Greedy (Polynomial)', color='green')

        # Fit exponential to optimal
        if len(sizes) >= 3:
            # Exponential fit for optimal: a * b^x
            log_opt = np.log(opt_times)
            coeffs = np.polyfit(sizes, log_opt, 1)
            fitted_opt = np.exp(coeffs[1]) * np.exp(coeffs[0] * np.array(sizes))
            ax1.semilogy(sizes, fitted_opt, '--', linewidth=2,
                        label=f'Exponential fit: O({np.exp(coeffs[0]):.2f}ⁿ)',
                        alpha=0.7, color='darkred')

        ax1.set_xlabel('Number of Sites', fontsize=12)
        ax1.set_ylabel('Runtime (ms, log scale)', fontsize=12)
        ax1.set_title('Runtime: Optimal vs Greedy', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Plot 2: Approximation ratio
        ax2.plot(sizes, results['approximation_ratios'], 'o-',
                linewidth=2, markersize=8, color='blue')
        ax2.axhline(y=1.0, color='green', linestyle='--', linewidth=2,
                   label='Optimal (ratio = 1.0)')
        ax2.axhline(y=1 - 1/np.e, color='orange', linestyle='--', linewidth=2,
                   label=f'Theoretical bound (1-1/e ≈ 0.632)')

        ax2.set_xlabel('Number of Sites', fontsize=12)
        ax2.set_ylabel('Approximation Ratio (Greedy/Optimal)', fontsize=12)
        ax2.set_title('Greedy Approximation Quality', fontsize=14, fontweight='bold')
        ax2.set_ylim([0.5, 1.05])
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/optimal_vs_greedy.png', dpi=300, bbox_inches='tight')
        print(f"✓ Saved plot: {self.output_dir}/optimal_vs_greedy.png")
        plt.close()


def main():
    """Run all experiments."""
    print("\n" + "=" * 70)
    print(" RUNTIME ANALYSIS FOR AOA PROJECT 2")
    print("=" * 70)

    analyzer = RuntimeAnalyzer()

    # Problem 1 experiments
    print("\n### PROBLEM 1: MARINE PROTECTED AREA NETWORK FLOW ###")
    p1_sizes = [10, 20, 30, 40, 50, 60, 70, 80]
    p1_results = analyzer.experiment_problem1_greedy(p1_sizes, trials=5)
    analyzer.plot_problem1_results(p1_results)

    # Problem 2 experiments
    print("\n### PROBLEM 2: HABITAT RESTORATION (NP-COMPLETE) ###")
    p2_sizes = [(10, 20), (20, 40), (30, 60), (40, 80), (50, 100),
                (60, 120), (70, 140), (80, 160)]
    p2_results = analyzer.experiment_problem2_greedy(p2_sizes, trials=5)
    analyzer.plot_problem2_results(p2_results)

    # Optimal vs Greedy comparison
    print("\n### OPTIMAL VS GREEDY COMPARISON ###")
    comparison = analyzer.experiment_problem2_optimal_vs_greedy(max_sites=12)
    analyzer.plot_optimal_vs_greedy(comparison)

    print("\n" + "=" * 70)
    print(" EXPERIMENTS COMPLETE")
    print("=" * 70)
    print(f"\nResults saved to: {analyzer.output_dir}/")
    print("  - problem1_runtime.png")
    print("  - problem2_runtime.png")
    print("  - optimal_vs_greedy.png")


if __name__ == '__main__':
    main()
