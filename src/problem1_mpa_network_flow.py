"""
Problem 1: Marine Protected Area Network Design using Network Flow
Author: Analysis of Algorithms Project 2
Date: December 2025

This module implements the reduction of Marine Protected Area (MPA) network design
to a Min-Cost Max-Flow problem.
"""

import networkx as nx
from typing import List, Dict, Tuple, Set
import numpy as np


class MPANetworkFlow:
    """
    Marine Protected Area Network Design using Network Flow.

    This class models the MPA design problem as a network flow problem where:
    - Source connects to spawning sites
    - Spawning sites connect to settlement habitats via ocean currents
    - Settlement habitats connect to sink
    - Protection costs constrain which sites can be selected
    """

    def __init__(self):
        self.graph = nx.DiGraph()
        self.spawning_sites = []
        self.settlement_sites = []
        self.source = 'SOURCE'
        self.sink = 'SINK'

    def add_spawning_site(self, site_id: str, spawning_capacity: float,
                          protection_cost: float):
        """
        Add a potential spawning site to the network.

        Args:
            site_id: Unique identifier for the spawning site
            spawning_capacity: Maximum larval output from this site
            protection_cost: Cost to protect this site
        """
        self.spawning_sites.append({
            'id': site_id,
            'capacity': spawning_capacity,
            'cost': protection_cost
        })

    def add_settlement_site(self, site_id: str, carrying_capacity: float,
                           protection_cost: float):
        """
        Add a settlement habitat site to the network.

        Args:
            site_id: Unique identifier for the settlement site
            carrying_capacity: Maximum larvae that can settle here
            protection_cost: Cost to protect this site
        """
        self.settlement_sites.append({
            'id': site_id,
            'capacity': carrying_capacity,
            'cost': protection_cost
        })

    def add_current_connection(self, from_site: str, to_site: str,
                              transport_capacity: float):
        """
        Add an ocean current connection between sites.

        Args:
            from_site: Source spawning site
            to_site: Destination settlement site
            transport_capacity: Larval transport rate via this current
        """
        self.graph.add_edge(from_site, to_site, capacity=transport_capacity)

    def build_flow_network(self, protected_spawning: Set[str],
                          protected_settlement: Set[str]):
        """
        Build the flow network for a given protection configuration.

        Args:
            protected_spawning: Set of protected spawning site IDs
            protected_settlement: Set of protected settlement site IDs

        Returns:
            NetworkX DiGraph representing the flow network
        """
        G = nx.DiGraph()

        # Add edges from source to protected spawning sites
        for site in self.spawning_sites:
            if site['id'] in protected_spawning:
                G.add_edge(self.source, site['id'], capacity=site['capacity'])

        # Add ocean current edges (only between protected sites)
        for u, v, data in self.graph.edges(data=True):
            if u in protected_spawning and v in protected_settlement:
                G.add_edge(u, v, capacity=data['capacity'])

        # Add edges from protected settlement sites to sink
        for site in self.settlement_sites:
            if site['id'] in protected_settlement:
                G.add_edge(site['id'], self.sink, capacity=site['capacity'])

        return G

    def calculate_total_cost(self, protected_spawning: Set[str],
                            protected_settlement: Set[str]) -> float:
        """
        Calculate total protection cost for a configuration.

        Args:
            protected_spawning: Set of protected spawning site IDs
            protected_settlement: Set of protected settlement site IDs

        Returns:
            Total cost of protecting all specified sites
        """
        total = 0.0
        for site in self.spawning_sites:
            if site['id'] in protected_spawning:
                total += site['cost']
        for site in self.settlement_sites:
            if site['id'] in protected_settlement:
                total += site['cost']
        return total

    def solve_max_flow(self, protected_spawning: Set[str],
                      protected_settlement: Set[str]) -> Tuple[float, Dict]:
        """
        Solve maximum flow problem for given protection configuration.

        Args:
            protected_spawning: Set of protected spawning site IDs
            protected_settlement: Set of protected settlement site IDs

        Returns:
            Tuple of (max_flow_value, flow_dict)
        """
        G = self.build_flow_network(protected_spawning, protected_settlement)

        if not G.has_node(self.source) or not G.has_node(self.sink):
            return 0.0, {}

        try:
            flow_value, flow_dict = nx.maximum_flow(G, self.source, self.sink)
            return flow_value, flow_dict
        except nx.NetworkXError:
            return 0.0, {}

    def greedy_site_selection(self, budget: float) -> Tuple[Set[str], Set[str], float]:
        """
        Greedy algorithm to select sites within budget to maximize flow.

        This is a heuristic approach since the budget-constrained version
        is NP-hard.

        Args:
            budget: Maximum budget for site protection

        Returns:
            Tuple of (protected_spawning, protected_settlement, max_flow)
        """
        # Start with empty protection sets
        protected_spawning = set()
        protected_settlement = set()
        current_cost = 0.0
        current_flow = 0.0

        # Create list of all sites with cost-effectiveness estimates
        all_sites = []

        for site in self.spawning_sites:
            # Estimate value as spawning capacity
            all_sites.append({
                'id': site['id'],
                'cost': site['cost'],
                'type': 'spawning',
                'value': site['capacity']
            })

        for site in self.settlement_sites:
            # Estimate value as carrying capacity
            all_sites.append({
                'id': site['id'],
                'cost': site['cost'],
                'type': 'settlement',
                'value': site['capacity']
            })

        # Sort by cost-effectiveness (value/cost ratio)
        all_sites.sort(key=lambda x: x['value'] / x['cost'] if x['cost'] > 0 else float('inf'),
                      reverse=True)

        # Greedily add sites
        for site in all_sites:
            if current_cost + site['cost'] <= budget:
                if site['type'] == 'spawning':
                    protected_spawning.add(site['id'])
                else:
                    protected_settlement.add(site['id'])
                current_cost += site['cost']

                # Recalculate flow
                flow, _ = self.solve_max_flow(protected_spawning, protected_settlement)
                current_flow = flow

        return protected_spawning, protected_settlement, current_flow

    def optimal_site_selection_small(self, budget: float) -> Tuple[Set[str], Set[str], float]:
        """
        Exhaustive search for optimal site selection (only for small instances).

        Args:
            budget: Maximum budget for site protection

        Returns:
            Tuple of (protected_spawning, protected_settlement, max_flow)
        """
        from itertools import combinations, product

        best_flow = 0.0
        best_spawning = set()
        best_settlement = set()

        n_spawning = len(self.spawning_sites)
        n_settlement = len(self.settlement_sites)

        # Try all combinations of spawning sites
        for r_spawn in range(n_spawning + 1):
            for spawn_combo in combinations(range(n_spawning), r_spawn):
                # Try all combinations of settlement sites
                for r_settle in range(n_settlement + 1):
                    for settle_combo in combinations(range(n_settlement), r_settle):
                        # Build protection sets
                        prot_spawn = {self.spawning_sites[i]['id'] for i in spawn_combo}
                        prot_settle = {self.settlement_sites[i]['id'] for i in settle_combo}

                        # Check budget
                        cost = self.calculate_total_cost(prot_spawn, prot_settle)
                        if cost <= budget:
                            # Calculate flow
                            flow, _ = self.solve_max_flow(prot_spawn, prot_settle)
                            if flow > best_flow:
                                best_flow = flow
                                best_spawning = prot_spawn
                                best_settlement = prot_settle

        return best_spawning, best_settlement, best_flow


def create_sample_instance():
    """
    Create a sample MPA network instance for testing.

    Returns:
        Configured MPANetworkFlow instance
    """
    mpa = MPANetworkFlow()

    # Add spawning sites (S1, S2, S3)
    mpa.add_spawning_site('S1', spawning_capacity=100, protection_cost=10)
    mpa.add_spawning_site('S2', spawning_capacity=150, protection_cost=15)
    mpa.add_spawning_site('S3', spawning_capacity=80, protection_cost=8)

    # Add settlement sites (H1, H2, H3)
    mpa.add_settlement_site('H1', carrying_capacity=120, protection_cost=12)
    mpa.add_settlement_site('H2', carrying_capacity=100, protection_cost=10)
    mpa.add_settlement_site('H3', carrying_capacity=90, protection_cost=9)

    # Add ocean current connections
    mpa.add_current_connection('S1', 'H1', transport_capacity=60)
    mpa.add_current_connection('S1', 'H2', transport_capacity=50)
    mpa.add_current_connection('S2', 'H1', transport_capacity=80)
    mpa.add_current_connection('S2', 'H3', transport_capacity=70)
    mpa.add_current_connection('S3', 'H2', transport_capacity=60)
    mpa.add_current_connection('S3', 'H3', transport_capacity=40)

    return mpa


if __name__ == '__main__':
    # Example usage
    mpa = create_sample_instance()
    budget = 50

    print("Marine Protected Area Network Flow Problem")
    print("=" * 60)
    print(f"\nBudget: ${budget}")

    # Solve using greedy algorithm
    print("\n--- Greedy Solution ---")
    prot_spawn, prot_settle, max_flow = mpa.greedy_site_selection(budget)
    cost = mpa.calculate_total_cost(prot_spawn, prot_settle)
    print(f"Protected Spawning Sites: {sorted(prot_spawn)}")
    print(f"Protected Settlement Sites: {sorted(prot_settle)}")
    print(f"Total Cost: ${cost}")
    print(f"Maximum Larval Flow: {max_flow}")

    # Solve optimally for small instance
    print("\n--- Optimal Solution (Exhaustive Search) ---")
    opt_spawn, opt_settle, opt_flow = mpa.optimal_site_selection_small(budget)
    opt_cost = mpa.calculate_total_cost(opt_spawn, opt_settle)
    print(f"Protected Spawning Sites: {sorted(opt_spawn)}")
    print(f"Protected Settlement Sites: {sorted(opt_settle)}")
    print(f"Total Cost: ${opt_cost}")
    print(f"Maximum Larval Flow: {opt_flow}")
