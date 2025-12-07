"""
Plot results from C++ experimental analysis
Uses matplotlib to read data files and generate plots
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def plot_problem1():
    """Plot Problem 1 runtime results"""
    # Read data
    data = np.loadtxt('../results/problem1_data.txt')
    sizes = data[:, 0]
    mean_times = data[:, 1]
    std_times = data[:, 2]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Plot 1: Runtime vs Problem Size
    ax1.errorbar(sizes, mean_times, yerr=std_times, marker='o',
                capsize=5, linewidth=2, markersize=8, label='Observed', color='blue')

    # Fit polynomial
    if len(sizes) >= 3:
        coeffs = np.polyfit(sizes, mean_times, 2)
        poly = np.poly1d(coeffs)
        x_smooth = np.linspace(min(sizes), max(sizes), 100)
        ax1.plot(x_smooth, poly(x_smooth), '--', linewidth=2,
                label='Quadratic fit', alpha=0.7, color='red')

    ax1.set_xlabel('Problem Size (Total Sites)', fontsize=12)
    ax1.set_ylabel('Runtime (ms)', fontsize=12)
    ax1.set_title('Problem 1: Greedy MPA Selection Runtime', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Plot 2: Log-log scale
    ax2.loglog(sizes, mean_times, 'o-', linewidth=2, markersize=8, label='Observed', color='blue')

    # Fit power law
    if len(sizes) >= 3:
        log_sizes = np.log(sizes)
        log_times = np.log(mean_times)
        slope, intercept = np.polyfit(log_sizes, log_times, 1)
        fitted = np.exp(intercept) * sizes ** slope
        ax2.loglog(sizes, fitted, '--', linewidth=2,
                  label=f'Power law: O(n^{slope:.2f})', alpha=0.7, color='red')

    ax2.set_xlabel('Problem Size (Total Sites)', fontsize=12)
    ax2.set_ylabel('Runtime (ms)', fontsize=12)
    ax2.set_title('Problem 1: Log-Log Scale Analysis', fontsize=14, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3, which='both')

    plt.tight_layout()
    plt.savefig('../results/problem1_runtime.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: ../results/problem1_runtime.png")
    plt.close()

def plot_problem2():
    """Plot Problem 2 runtime results"""
    data = np.loadtxt('../results/problem2_data.txt')
    sites = data[:, 0]
    mean_times = data[:, 2]
    std_times = data[:, 3]

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))

    ax.errorbar(sites, mean_times, yerr=std_times, marker='s',
               capsize=5, linewidth=2, markersize=8, label='Observed', color='green')

    # Fit quadratic
    if len(sites) >= 3:
        coeffs = np.polyfit(sites, mean_times, 2)
        poly = np.poly1d(coeffs)
        x_smooth = np.linspace(min(sites), max(sites), 100)
        ax.plot(x_smooth, poly(x_smooth), '--', linewidth=2,
               label='Quadratic fit: O(n²)', alpha=0.7, color='darkgreen')

    ax.set_xlabel('Number of Restoration Sites', fontsize=12)
    ax.set_ylabel('Runtime (ms)', fontsize=12)
    ax.set_title('Problem 2: Greedy Coverage Runtime', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('../results/problem2_runtime.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: ../results/problem2_runtime.png")
    plt.close()

def plot_optimal_vs_greedy():
    """Plot optimal vs greedy comparison"""
    data = np.loadtxt('../results/optimal_vs_greedy_data.txt')
    sites = data[:, 0]
    opt_times = data[:, 1]
    greedy_times = data[:, 2]
    approx_ratios = data[:, 5]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Plot 1: Runtime comparison
    ax1.semilogy(sites, opt_times, 'o-', linewidth=2, markersize=8,
                label='Optimal (Exponential)', color='red')
    ax1.semilogy(sites, greedy_times, 's-', linewidth=2, markersize=8,
                label='Greedy (Polynomial)', color='green')

    # Fit exponential to optimal
    if len(sites) >= 3 and np.all(opt_times > 0):
        log_opt = np.log(opt_times)
        coeffs = np.polyfit(sites, log_opt, 1)
        fitted_opt = np.exp(coeffs[1]) * np.exp(coeffs[0] * sites)
        ax1.semilogy(sites, fitted_opt, '--', linewidth=2,
                    label=f'Exponential fit: O({np.exp(coeffs[0]):.2f}ⁿ)',
                    alpha=0.7, color='darkred')

    ax1.set_xlabel('Number of Sites', fontsize=12)
    ax1.set_ylabel('Runtime (ms, log scale)', fontsize=12)
    ax1.set_title('Runtime: Optimal vs Greedy', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Plot 2: Approximation ratio
    ax2.plot(sites, approx_ratios, 'o-',
            linewidth=2, markersize=8, color='blue', label='Observed ratio')
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
    plt.savefig('../results/optimal_vs_greedy.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: ../results/optimal_vs_greedy.png")
    plt.close()

if __name__ == '__main__':
    print("\nGenerating plots from C++ experimental data...")
    print("=" * 60)

    plot_problem1()
    plot_problem2()
    plot_optimal_vs_greedy()

    print("\n" + "=" * 60)
    print("All plots generated successfully!")
    print("=" * 60)
