"""
Problem 2: Marine Habitat Restoration Planning (NP-Complete)
Author: Analysis of Algorithms Project 2
Date: December 2025

This module implements the Marine Habitat Restoration Planning problem,
which reduces to the Budgeted Maximum Coverage problem (NP-Complete).

Problem: Given multiple potential restoration sites, each covering different
species habitats with associated costs, select sites within budget to maximize
species coverage.
"""

from typing import List, Dict, Set, Tuple
import numpy as np


class HabitatRestorationProblem:
    """
    Marine Habitat Restoration Planning Problem.

    Real-World Problem:
    A conservation agency needs to select marine habitat restoration sites
    to maximize the number of endangered species protected, subject to a
    limited budget. Each restoration site:
    - Provides habitat for a subset of species
    - Has a restoration cost
    - May have overlapping species coverage with other sites

    This reduces to Budgeted Maximum Coverage, which is NP-Complete.
    """

    def __init__(self):
        self.sites = []
        self.all_species = set()

    def add_restoration_site(self, site_id: str, species_covered: Set[str],
                            restoration_cost: float):
        """
        Add a potential restoration site.

        Args:
            site_id: Unique identifier for the site
            species_covered: Set of species that would benefit from this site
            restoration_cost: Cost to restore this site
        """
        self.sites.append({
            'id': site_id,
            'species': set(species_covered),
            'cost': restoration_cost
        })
        self.all_species.update(species_covered)

    def calculate_coverage(self, selected_sites: Set[int]) -> int:
        """
        Calculate total number of unique species covered by selected sites.

        Args:
            selected_sites: Set of site indices

        Returns:
            Number of unique species covered
        """
        covered_species = set()
        for idx in selected_sites:
            if 0 <= idx < len(self.sites):
                covered_species.update(self.sites[idx]['species'])
        return len(covered_species)

    def calculate_cost(self, selected_sites: Set[int]) -> float:
        """
        Calculate total cost of selected sites.

        Args:
            selected_sites: Set of site indices

        Returns:
            Total restoration cost
        """
        total = 0.0
        for idx in selected_sites:
            if 0 <= idx < len(self.sites):
                total += self.sites[idx]['cost']
        return total

    def greedy_coverage(self, budget: float) -> Tuple[Set[int], int, float]:
        """
        Greedy algorithm for budgeted maximum coverage.

        At each step, select the site that provides the maximum marginal
        coverage per unit cost (cost-effectiveness ratio).

        This provides a (1 - 1/e) approximation guarantee for maximum coverage.

        Args:
            budget: Maximum budget for restoration

        Returns:
            Tuple of (selected_site_indices, species_covered, total_cost)
        """
        selected = set()
        covered_species = set()
        remaining_budget = budget

        while True:
            best_site = -1
            best_ratio = 0.0
            best_new_species = set()

            # Find site with best marginal coverage per cost
            for idx, site in enumerate(self.sites):
                if idx not in selected and site['cost'] <= remaining_budget:
                    # Calculate new species this site would add
                    new_species = site['species'] - covered_species
                    marginal_coverage = len(new_species)

                    if marginal_coverage > 0:
                        # Cost-effectiveness ratio
                        ratio = marginal_coverage / site['cost']

                        if ratio > best_ratio:
                            best_ratio = ratio
                            best_site = idx
                            best_new_species = new_species

            # If no beneficial site found, stop
            if best_site == -1:
                break

            # Add best site
            selected.add(best_site)
            covered_species.update(best_new_species)
            remaining_budget -= self.sites[best_site]['cost']

        total_cost = self.calculate_cost(selected)
        return selected, len(covered_species), total_cost

    def greedy_coverage_simple(self, budget: float) -> Tuple[Set[int], int, float]:
        """
        Simple greedy: always pick site with most uncovered species that fits budget.

        Args:
            budget: Maximum budget for restoration

        Returns:
            Tuple of (selected_site_indices, species_covered, total_cost)
        """
        selected = set()
        covered_species = set()
        remaining_budget = budget

        while True:
            best_site = -1
            best_marginal = 0

            # Find site with maximum marginal coverage
            for idx, site in enumerate(self.sites):
                if idx not in selected and site['cost'] <= remaining_budget:
                    new_species = site['species'] - covered_species
                    marginal = len(new_species)

                    if marginal > best_marginal:
                        best_marginal = marginal
                        best_site = idx

            if best_site == -1:
                break

            selected.add(best_site)
            covered_species.update(self.sites[best_site]['species'])
            remaining_budget -= self.sites[best_site]['cost']

        total_cost = self.calculate_cost(selected)
        return selected, len(covered_species), total_cost

    def optimal_solution_small(self, budget: float) -> Tuple[Set[int], int, float]:
        """
        Optimal solution using exhaustive search (exponential time).
        Only feasible for small instances.

        Args:
            budget: Maximum budget for restoration

        Returns:
            Tuple of (selected_site_indices, species_covered, total_cost)
        """
        from itertools import combinations

        n = len(self.sites)
        best_coverage = 0
        best_selection = set()
        best_cost = 0.0

        # Try all possible subsets
        for r in range(n + 1):
            for combo in combinations(range(n), r):
                selected = set(combo)
                cost = self.calculate_cost(selected)

                if cost <= budget:
                    coverage = self.calculate_coverage(selected)
                    if coverage > best_coverage:
                        best_coverage = coverage
                        best_selection = selected
                        best_cost = cost

        return best_selection, best_coverage, best_cost

    def reduction_to_set_cover(self) -> Dict:
        """
        Show the reduction to Budgeted Maximum Coverage (Set Cover variant).

        Returns:
            Dictionary describing the reduction
        """
        reduction = {
            'universe': self.all_species,
            'sets': [],
            'costs': []
        }

        for site in self.sites:
            reduction['sets'].append(site['species'])
            reduction['costs'].append(site['cost'])

        return reduction


def create_sample_instance():
    """
    Create a sample habitat restoration instance.

    Returns:
        Configured HabitatRestorationProblem instance
    """
    problem = HabitatRestorationProblem()

    # Define species
    # Each site covers different combinations of endangered marine species

    problem.add_restoration_site(
        'Site_A',
        species_covered={'SeaTurtle', 'Coral_A', 'Grouper', 'Seahorse'},
        restoration_cost=25.0
    )

    problem.add_restoration_site(
        'Site_B',
        species_covered={'SeaTurtle', 'Dolphin', 'Coral_B', 'Mangrove'},
        restoration_cost=30.0
    )

    problem.add_restoration_site(
        'Site_C',
        species_covered={'Grouper', 'Coral_A', 'Coral_C', 'Sponge'},
        restoration_cost=20.0
    )

    problem.add_restoration_site(
        'Site_D',
        species_covered={'Dolphin', 'Whale', 'Seahorse', 'Coral_B'},
        restoration_cost=35.0
    )

    problem.add_restoration_site(
        'Site_E',
        species_covered={'Mangrove', 'Coral_C', 'Sponge', 'Oyster'},
        restoration_cost=18.0
    )

    problem.add_restoration_site(
        'Site_F',
        species_covered={'Whale', 'Oyster', 'SeaTurtle', 'Coral_A'},
        restoration_cost=28.0
    )

    return problem


def demonstrate_np_completeness():
    """
    Demonstrate that this problem is NP-Complete through reduction
    from Budgeted Maximum Coverage.
    """
    print("\n" + "=" * 70)
    print("NP-Completeness Demonstration")
    print("=" * 70)

    print("\n1. Problem Statement:")
    print("   Given restoration sites S, species universe U, costs c_i,")
    print("   and budget B, select subset S' ⊆ S such that:")
    print("   - Total cost ≤ B")
    print("   - Coverage |∪_{i∈S'} U_i| is maximized")

    print("\n2. This is the Budgeted Maximum Coverage Problem:")
    print("   - Known to be NP-Complete (Khuller et al., 1999)")
    print("   - Reduction from Set Cover")

    print("\n3. Certificate Verification (in NP):")
    print("   Given a solution S', we can verify in polynomial time:")
    print("   - Check budget constraint: O(|S'|)")
    print("   - Count species coverage: O(|S'| × max species per site)")
    print("   - Total: O(n) where n is number of sites")

    print("\n4. Hardness:")
    print("   - Budgeted Max Coverage is NP-Hard")
    print("   - No polynomial-time algorithm unless P = NP")
    print("   - Best known approximation: (1 - 1/e) ≈ 0.632")


if __name__ == '__main__':
    print("Marine Habitat Restoration Planning Problem")
    print("(Reduces to Budgeted Maximum Coverage - NP-Complete)")
    print("=" * 70)

    problem = create_sample_instance()
    budget = 60.0

    print(f"\nTotal species in ecosystem: {len(problem.all_species)}")
    print(f"Species: {sorted(problem.all_species)}")
    print(f"\nNumber of restoration sites: {len(problem.sites)}")
    print(f"Budget: ${budget}")

    print("\n" + "-" * 70)
    print("Site Details:")
    print("-" * 70)
    for idx, site in enumerate(problem.sites):
        print(f"{idx}. {site['id']}: ${site['cost']:.0f} - "
              f"Covers {len(site['species'])} species: {sorted(site['species'])}")

    # Greedy solution (cost-effectiveness)
    print("\n" + "=" * 70)
    print("GREEDY SOLUTION (Cost-Effectiveness Ratio)")
    print("=" * 70)
    selected, coverage, cost = problem.greedy_coverage(budget)
    print(f"Selected sites: {[problem.sites[i]['id'] for i in sorted(selected)]}")
    print(f"Total cost: ${cost:.2f}")
    print(f"Species covered: {coverage} / {len(problem.all_species)}")
    print(f"Coverage percentage: {100 * coverage / len(problem.all_species):.1f}%")

    # Simple greedy solution
    print("\n" + "=" * 70)
    print("GREEDY SOLUTION (Maximum Marginal Coverage)")
    print("=" * 70)
    selected2, coverage2, cost2 = problem.greedy_coverage_simple(budget)
    print(f"Selected sites: {[problem.sites[i]['id'] for i in sorted(selected2)]}")
    print(f"Total cost: ${cost2:.2f}")
    print(f"Species covered: {coverage2} / {len(problem.all_species)}")
    print(f"Coverage percentage: {100 * coverage2 / len(problem.all_species):.1f}%")

    # Optimal solution (small instance only)
    print("\n" + "=" * 70)
    print("OPTIMAL SOLUTION (Exhaustive Search)")
    print("=" * 70)
    opt_selected, opt_coverage, opt_cost = problem.optimal_solution_small(budget)
    print(f"Selected sites: {[problem.sites[i]['id'] for i in sorted(opt_selected)]}")
    print(f"Total cost: ${opt_cost:.2f}")
    print(f"Species covered: {opt_coverage} / {len(problem.all_species)}")
    print(f"Coverage percentage: {100 * opt_coverage / len(problem.all_species):.1f}%")

    print(f"\nGreedy approximation ratio: {coverage / opt_coverage:.3f}")

    # Demonstrate NP-completeness
    demonstrate_np_completeness()
