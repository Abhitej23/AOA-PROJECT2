/**
 * Experimental Runtime Analysis for AOA Project 2
 * Author: Analysis of Algorithms Project 2
 * Date: December 2025
 *
 * This module conducts experimental analysis of running times for both problems.
 * Outputs data files that can be plotted using gnuplot.
 */

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <set>
#include <map>
#include <random>
#include <chrono>
#include <iomanip>
#include <cmath>
#include <algorithm>

using namespace std;
using namespace chrono;

// Forward declarations - we'll compile with problem implementations separately
// For now, we'll redefine the minimal classes needed for experiments

// Copy of MPANetworkFlow class (without main function)
#include "../src/mpa_network_flow_lib.h"
// Copy of HabitatRestorationProblem class (without main function)
#include "../src/habitat_restoration_lib.h"

class RuntimeAnalyzer {
private:
    string output_dir;
    mt19937 rng;

public:
    RuntimeAnalyzer(const string& dir = "../results")
        : output_dir(dir), rng(random_device{}()) {}

    /**
     * Generate random MPA instance
     */
    MPANetworkFlow generateRandomMPAInstance(int n_spawning, int n_settlement,
                                            double edge_probability = 0.3) {
        MPANetworkFlow mpa;
        uniform_real_distribution<double> cap_dist(50.0, 200.0);
        uniform_real_distribution<double> cost_dist(5.0, 20.0);
        uniform_real_distribution<double> prob_dist(0.0, 1.0);
        uniform_real_distribution<double> transport_dist(30.0, 100.0);

        // Add spawning sites
        for (int i = 0; i < n_spawning; i++) {
            mpa.addSpawningSite("S" + to_string(i),
                               cap_dist(rng), cost_dist(rng));
        }

        // Add settlement sites
        for (int i = 0; i < n_settlement; i++) {
            mpa.addSettlementSite("H" + to_string(i),
                                 cap_dist(rng), cost_dist(rng));
        }

        // Add random current connections
        for (int i = 0; i < n_spawning; i++) {
            for (int j = 0; j < n_settlement; j++) {
                if (prob_dist(rng) < edge_probability) {
                    mpa.addCurrentConnection("S" + to_string(i),
                                           "H" + to_string(j),
                                           transport_dist(rng));
                }
            }
        }

        return mpa;
    }

    /**
     * Generate random restoration instance
     */
    HabitatRestorationProblem generateRandomRestorationInstance(int n_sites,
                                                                int n_species) {
        HabitatRestorationProblem problem;
        uniform_real_distribution<double> cost_dist(10.0, 50.0);
        uniform_int_distribution<int> coverage_size_dist(
            max(1, n_species / 4), max(2, n_species / 2));

        // Generate species names
        vector<string> species_names;
        for (int i = 0; i < n_species; i++) {
            species_names.push_back("Species_" + to_string(i));
        }

        // Add sites
        for (int i = 0; i < n_sites; i++) {
            int coverage_size = coverage_size_dist(rng);
            set<string> covered;

            // Random sample
            vector<int> indices(n_species);
            iota(indices.begin(), indices.end(), 0);
            shuffle(indices.begin(), indices.end(), rng);

            for (int j = 0; j < coverage_size && j < n_species; j++) {
                covered.insert(species_names[indices[j]]);
            }

            problem.addRestorationSite("Site_" + to_string(i),
                                      covered, cost_dist(rng));
        }

        return problem;
    }

    /**
     * Experiment with Problem 1 greedy algorithm
     */
    void experimentProblem1Greedy(const vector<int>& sizes, int trials = 5) {
        cout << "\n" << string(70, '=') << endl;
        cout << "Problem 1: MPA Network Flow - Greedy Runtime Analysis" << endl;
        cout << string(70, '=') << endl;

        ofstream data_file(output_dir + "/problem1_data.txt");
        data_file << "# Size MeanTime(ms) StdDev(ms) MinTime(ms) MaxTime(ms)" << endl;

        for (int size : sizes) {
            int n_spawning = size / 2;
            int n_settlement = size - n_spawning;

            vector<double> times;
            for (int trial = 0; trial < trials; trial++) {
                auto mpa = generateRandomMPAInstance(n_spawning, n_settlement);

                // Calculate budget
                double budget = 0.0;
                for (int i = 0; i < n_spawning / 2; i++) {
                    budget += 12.5; // Average cost
                }

                auto start = high_resolution_clock::now();
                mpa.greedySiteSelection(budget);
                auto end = high_resolution_clock::now();

                double time_ms = duration<double, milli>(end - start).count();
                times.push_back(time_ms);
            }

            double mean = 0.0, std_dev = 0.0;
            double min_time = *min_element(times.begin(), times.end());
            double max_time = *max_element(times.begin(), times.end());

            for (double t : times) mean += t;
            mean /= times.size();

            for (double t : times) std_dev += (t - mean) * (t - mean);
            std_dev = sqrt(std_dev / times.size());

            data_file << size << " " << mean << " " << std_dev << " "
                     << min_time << " " << max_time << endl;

            cout << "Size " << setw(3) << size << ": "
                 << setw(8) << fixed << setprecision(3) << mean << " ms "
                 << "(±" << setw(6) << std_dev << " ms)" << endl;
        }

        data_file.close();
        cout << "\n✓ Saved data: " << output_dir << "/problem1_data.txt" << endl;
    }

    /**
     * Experiment with Problem 2 greedy algorithm
     */
    void experimentProblem2Greedy(const vector<pair<int, int>>& sizes,
                                  int trials = 5) {
        cout << "\n" << string(70, '=') << endl;
        cout << "Problem 2: Habitat Restoration - Greedy Runtime Analysis" << endl;
        cout << string(70, '=') << endl;

        ofstream data_file(output_dir + "/problem2_data.txt");
        data_file << "# Sites Species MeanTime(ms) StdDev(ms)" << endl;

        for (const auto& [n_sites, n_species] : sizes) {
            vector<double> times;

            for (int trial = 0; trial < trials; trial++) {
                auto problem = generateRandomRestorationInstance(n_sites, n_species);
                double budget = n_sites * 30.0 / 2; // Approximate budget

                auto start = high_resolution_clock::now();
                problem.greedyCoverage(budget);
                auto end = high_resolution_clock::now();

                double time_ms = duration<double, milli>(end - start).count();
                times.push_back(time_ms);
            }

            double mean = 0.0, std_dev = 0.0;
            for (double t : times) mean += t;
            mean /= times.size();

            for (double t : times) std_dev += (t - mean) * (t - mean);
            std_dev = sqrt(std_dev / times.size());

            data_file << n_sites << " " << n_species << " "
                     << mean << " " << std_dev << endl;

            cout << "Sites=" << setw(3) << n_sites
                 << ", Species=" << setw(3) << n_species << ": "
                 << setw(8) << fixed << setprecision(3) << mean << " ms "
                 << "(±" << setw(6) << std_dev << " ms)" << endl;
        }

        data_file.close();
        cout << "\n✓ Saved data: " << output_dir << "/problem2_data.txt" << endl;
    }

    /**
     * Compare optimal vs greedy for small instances
     */
    void experimentOptimalVsGreedy(int max_sites = 12) {
        cout << "\n" << string(70, '=') << endl;
        cout << "Problem 2: Optimal vs Greedy Comparison" << endl;
        cout << string(70, '=') << endl;

        ofstream data_file(output_dir + "/optimal_vs_greedy_data.txt");
        data_file << "# Sites OptimalTime(ms) GreedyTime(ms) "
                  << "OptCoverage GreedyCoverage ApproxRatio" << endl;

        for (int n_sites = 4; n_sites <= max_sites; n_sites += 2) {
            int n_species = n_sites * 2;
            auto problem = generateRandomRestorationInstance(n_sites, n_species);
            double budget = n_sites * 30.0 / 2;

            // Optimal solution
            auto start = high_resolution_clock::now();
            auto [opt_sel, opt_cov, opt_cost] = problem.optimalSolutionSmall(budget);
            auto end = high_resolution_clock::now();
            double opt_time = duration<double, milli>(end - start).count();

            // Greedy solution
            start = high_resolution_clock::now();
            auto [greedy_sel, greedy_cov, greedy_cost] = problem.greedyCoverage(budget);
            end = high_resolution_clock::now();
            double greedy_time = duration<double, milli>(end - start).count();

            double approx_ratio = (opt_cov > 0) ? (double)greedy_cov / opt_cov : 1.0;

            data_file << n_sites << " " << opt_time << " " << greedy_time << " "
                     << opt_cov << " " << greedy_cov << " "
                     << approx_ratio << endl;

            cout << "Sites=" << setw(2) << n_sites << ": "
                 << "Optimal=" << setw(7) << fixed << setprecision(2) << opt_time << "ms, "
                 << "Greedy=" << setw(6) << setprecision(3) << greedy_time << "ms, "
                 << "Approx=" << fixed << setprecision(3) << approx_ratio << endl;
        }

        data_file.close();
        cout << "\n✓ Saved data: " << output_dir << "/optimal_vs_greedy_data.txt" << endl;
    }

    /**
     * Generate gnuplot script for plotting
     */
    void generateGnuplotScript() {
        ofstream script(output_dir + "/plot.gnu");

        script << "set terminal pngcairo enhanced font 'Arial,12' size 1400,500" << endl;
        script << "set output '" << output_dir << "/problem1_runtime.png'" << endl;
        script << "set multiplot layout 1,2" << endl;
        script << "set grid" << endl;
        script << "set xlabel 'Problem Size (Total Sites)'" << endl;
        script << "set ylabel 'Runtime (ms)'" << endl;
        script << "set title 'Problem 1: Greedy MPA Selection Runtime' font 'Arial,14'" << endl;
        script << "plot '" << output_dir << "/problem1_data.txt' using 1:2:3 with errorbars "
               << "title 'Observed' lc rgb 'blue', \\\n"
               << "     '" << output_dir << "/problem1_data.txt' using 1:2 with lines "
               << "title 'Mean' lc rgb 'red' lw 2" << endl;

        script << "set xlabel 'Problem Size (Total Sites)'" << endl;
        script << "set ylabel 'Runtime (ms)'" << endl;
        script << "set logscale xy" << endl;
        script << "set title 'Problem 1: Log-Log Scale Analysis' font 'Arial,14'" << endl;
        script << "plot '" << output_dir << "/problem1_data.txt' using 1:2 with linespoints "
               << "title 'Observed' lc rgb 'blue' lw 2 pt 7" << endl;
        script << "unset multiplot" << endl;
        script << endl;

        // Problem 2 plot
        script << "set terminal pngcairo enhanced font 'Arial,12' size 1000,600" << endl;
        script << "set output '" << output_dir << "/problem2_runtime.png'" << endl;
        script << "unset logscale xy" << endl;
        script << "set xlabel 'Number of Restoration Sites'" << endl;
        script << "set ylabel 'Runtime (ms)'" << endl;
        script << "set title 'Problem 2: Greedy Coverage Runtime' font 'Arial,14'" << endl;
        script << "plot '" << output_dir << "/problem2_data.txt' using 1:3:4 with errorbars "
               << "title 'Observed' lc rgb 'green', \\\n"
               << "     '" << output_dir << "/problem2_data.txt' using 1:3 with lines "
               << "title 'Mean' lc rgb 'darkgreen' lw 2" << endl;
        script << endl;

        // Optimal vs Greedy plot
        script << "set terminal pngcairo enhanced font 'Arial,12' size 1400,500" << endl;
        script << "set output '" << output_dir << "/optimal_vs_greedy.png'" << endl;
        script << "set multiplot layout 1,2" << endl;
        script << "set logscale y" << endl;
        script << "set xlabel 'Number of Sites'" << endl;
        script << "set ylabel 'Runtime (ms, log scale)'" << endl;
        script << "set title 'Runtime: Optimal vs Greedy' font 'Arial,14'" << endl;
        script << "plot '" << output_dir << "/optimal_vs_greedy_data.txt' using 1:2 "
               << "with linespoints title 'Optimal (Exponential)' lc rgb 'red' lw 2 pt 7, \\\n"
               << "     '" << output_dir << "/optimal_vs_greedy_data.txt' using 1:3 "
               << "with linespoints title 'Greedy (Polynomial)' lc rgb 'green' lw 2 pt 9" << endl;

        script << "unset logscale y" << endl;
        script << "set xlabel 'Number of Sites'" << endl;
        script << "set ylabel 'Approximation Ratio (Greedy/Optimal)'" << endl;
        script << "set yrange [0.5:1.05]" << endl;
        script << "set title 'Greedy Approximation Quality' font 'Arial,14'" << endl;
        script << "plot '" << output_dir << "/optimal_vs_greedy_data.txt' using 1:6 "
               << "with linespoints title 'Observed' lc rgb 'blue' lw 2 pt 7, \\\n"
               << "     1.0 with lines title 'Optimal (ratio = 1.0)' lc rgb 'green' lw 2 dt 2, \\\n"
               << "     " << (1.0 - 1.0/M_E) << " with lines title 'Theoretical bound (1-1/e)' "
               << "lc rgb 'orange' lw 2 dt 2" << endl;
        script << "unset multiplot" << endl;

        script.close();
        cout << "\n✓ Generated gnuplot script: " << output_dir << "/plot.gnu" << endl;
        cout << "  Run: gnuplot " << output_dir << "/plot.gnu" << endl;
    }
};

int main() {
    cout << "\n" << string(70, '=') << endl;
    cout << " RUNTIME ANALYSIS FOR AOA PROJECT 2" << endl;
    cout << string(70, '=') << endl;

    RuntimeAnalyzer analyzer;

    // Problem 1 experiments
    cout << "\n### PROBLEM 1: MARINE PROTECTED AREA NETWORK FLOW ###" << endl;
    vector<int> p1_sizes = {10, 20, 30, 40, 50, 60, 70, 80};
    analyzer.experimentProblem1Greedy(p1_sizes, 5);

    // Problem 2 experiments
    cout << "\n### PROBLEM 2: HABITAT RESTORATION (NP-COMPLETE) ###" << endl;
    vector<pair<int, int>> p2_sizes = {
        {10, 20}, {20, 40}, {30, 60}, {40, 80},
        {50, 100}, {60, 120}, {70, 140}, {80, 160}
    };
    analyzer.experimentProblem2Greedy(p2_sizes, 5);

    // Optimal vs Greedy comparison
    cout << "\n### OPTIMAL VS GREEDY COMPARISON ###" << endl;
    analyzer.experimentOptimalVsGreedy(12);

    // Generate plotting script
    analyzer.generateGnuplotScript();

    cout << "\n" << string(70, '=') << endl;
    cout << " EXPERIMENTS COMPLETE" << endl;
    cout << string(70, '=') << endl;
    cout << "\nData files saved to: ../results/" << endl;
    cout << "  - problem1_data.txt" << endl;
    cout << "  - problem2_data.txt" << endl;
    cout << "  - optimal_vs_greedy_data.txt" << endl;
    cout << "\nTo generate plots, run:" << endl;
    cout << "  gnuplot ../results/plot.gnu" << endl;

    return 0;
}
