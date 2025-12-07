/**
 * Problem 2: Marine Habitat Restoration Planning (NP-Complete)
 * Author: Analysis of Algorithms Project 2
 * Date: December 2025
 *
 * This module implements the Marine Habitat Restoration Planning problem,
 * which reduces to the Budgeted Maximum Coverage problem (NP-Complete).
 */

#include <iostream>
#include <vector>
#include <string>
#include <set>
#include <algorithm>
#include <iomanip>
#include <cmath>

using namespace std;

/**
 * Restoration Site structure
 */
struct RestorationSite {
    string id;
    set<string> species;
    double cost;

    RestorationSite(const string& id, const set<string>& species, double cost)
        : id(id), species(species), cost(cost) {}
};

/**
 * Marine Habitat Restoration Problem Class
 *
 * Real-World Problem:
 * Select marine habitat restoration sites to maximize the number of
 * endangered species protected, subject to a limited budget.
 *
 * This reduces to Budgeted Maximum Coverage, which is NP-Complete.
 */
class HabitatRestorationProblem {
private:
    vector<RestorationSite> sites;
    set<string> all_species;

public:
    /**
     * Add a potential restoration site
     */
    void addRestorationSite(const string& site_id,
                           const set<string>& species_covered,
                           double restoration_cost) {
        sites.emplace_back(site_id, species_covered, restoration_cost);
        all_species.insert(species_covered.begin(), species_covered.end());
    }

    /**
     * Calculate total number of unique species covered
     */
    int calculateCoverage(const set<int>& selected_sites) const {
        set<string> covered_species;
        for (int idx : selected_sites) {
            if (idx >= 0 && idx < sites.size()) {
                covered_species.insert(sites[idx].species.begin(),
                                      sites[idx].species.end());
            }
        }
        return covered_species.size();
    }

    /**
     * Calculate total cost of selected sites
     */
    double calculateCost(const set<int>& selected_sites) const {
        double total = 0.0;
        for (int idx : selected_sites) {
            if (idx >= 0 && idx < sites.size()) {
                total += sites[idx].cost;
            }
        }
        return total;
    }

    /**
     * Greedy algorithm for budgeted maximum coverage
     *
     * Provides (1 - 1/e) approximation guarantee
     */
    tuple<set<int>, int, double> greedyCoverage(double budget) {
        set<int> selected;
        set<string> covered_species;
        double remaining_budget = budget;

        while (true) {
            int best_site = -1;
            double best_ratio = 0.0;
            set<string> best_new_species;

            // Find site with best marginal coverage per cost
            for (int idx = 0; idx < sites.size(); idx++) {
                if (selected.count(idx) == 0 &&
                    sites[idx].cost <= remaining_budget) {

                    // Calculate new species this site would add
                    set<string> new_species;
                    set_difference(sites[idx].species.begin(),
                                 sites[idx].species.end(),
                                 covered_species.begin(),
                                 covered_species.end(),
                                 inserter(new_species, new_species.begin()));

                    int marginal_coverage = new_species.size();

                    if (marginal_coverage > 0) {
                        double ratio = marginal_coverage / sites[idx].cost;

                        if (ratio > best_ratio) {
                            best_ratio = ratio;
                            best_site = idx;
                            best_new_species = new_species;
                        }
                    }
                }
            }

            if (best_site == -1) break;

            // Add best site
            selected.insert(best_site);
            covered_species.insert(best_new_species.begin(),
                                  best_new_species.end());
            remaining_budget -= sites[best_site].cost;
        }

        double total_cost = calculateCost(selected);
        return {selected, (int)covered_species.size(), total_cost};
    }

    /**
     * Simple greedy: always pick site with most uncovered species
     */
    tuple<set<int>, int, double> greedyCoverageSimple(double budget) {
        set<int> selected;
        set<string> covered_species;
        double remaining_budget = budget;

        while (true) {
            int best_site = -1;
            int best_marginal = 0;

            for (int idx = 0; idx < sites.size(); idx++) {
                if (selected.count(idx) == 0 &&
                    sites[idx].cost <= remaining_budget) {

                    set<string> new_species;
                    set_difference(sites[idx].species.begin(),
                                 sites[idx].species.end(),
                                 covered_species.begin(),
                                 covered_species.end(),
                                 inserter(new_species, new_species.begin()));

                    int marginal = new_species.size();
                    if (marginal > best_marginal) {
                        best_marginal = marginal;
                        best_site = idx;
                    }
                }
            }

            if (best_site == -1) break;

            selected.insert(best_site);
            covered_species.insert(sites[best_site].species.begin(),
                                  sites[best_site].species.end());
            remaining_budget -= sites[best_site].cost;
        }

        double total_cost = calculateCost(selected);
        return {selected, (int)covered_species.size(), total_cost};
    }

    /**
     * Optimal solution using exhaustive search (exponential time)
     * Only feasible for small instances (n <= 15)
     */
    tuple<set<int>, int, double> optimalSolutionSmall(double budget) {
        int n = sites.size();
        if (n > 20) {
            cerr << "Warning: Exhaustive search for n > 20 may be very slow!" << endl;
        }

        int best_coverage = 0;
        set<int> best_selection;
        double best_cost = 0.0;

        // Try all 2^n subsets
        for (long long mask = 0; mask < (1LL << n); mask++) {
            set<int> current_selection;
            double cost = 0.0;

            for (int i = 0; i < n; i++) {
                if (mask & (1LL << i)) {
                    current_selection.insert(i);
                    cost += sites[i].cost;
                }
            }

            if (cost <= budget) {
                int coverage = calculateCoverage(current_selection);
                if (coverage > best_coverage) {
                    best_coverage = coverage;
                    best_selection = current_selection;
                    best_cost = cost;
                }
            }
        }

        return {best_selection, best_coverage, best_cost};
    }

    /**
     * Print NP-Completeness demonstration
     */
    void demonstrateNPCompleteness() const {
        cout << "\n" << string(70, '=') << endl;
        cout << "NP-Completeness Demonstration" << endl;
        cout << string(70, '=') << endl;

        cout << "\n1. Problem Statement:" << endl;
        cout << "   Given restoration sites S, species universe U, costs c_i," << endl;
        cout << "   and budget B, select subset S' ⊆ S such that:" << endl;
        cout << "   - Total cost ≤ B" << endl;
        cout << "   - Coverage |∪_{i∈S'} U_i| is maximized" << endl;

        cout << "\n2. This is the Budgeted Maximum Coverage Problem:" << endl;
        cout << "   - Known to be NP-Complete (Khuller et al., 1999)" << endl;
        cout << "   - Reduction from Set Cover" << endl;

        cout << "\n3. Certificate Verification (in NP):" << endl;
        cout << "   Given a solution S', we can verify in polynomial time:" << endl;
        cout << "   - Check budget constraint: O(|S'|)" << endl;
        cout << "   - Count species coverage: O(|S'| × max species per site)" << endl;
        cout << "   - Total: O(n) where n is number of sites" << endl;

        cout << "\n4. Hardness:" << endl;
        cout << "   - Budgeted Max Coverage is NP-Hard" << endl;
        cout << "   - No polynomial-time algorithm unless P = NP" << endl;
        cout << "   - Best known approximation: (1 - 1/e) ≈ 0.632" << endl;
    }

    // Getters
    const vector<RestorationSite>& getSites() const { return sites; }
    const set<string>& getAllSpecies() const { return all_species; }
};
