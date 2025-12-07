/**
 * Problem 1: Marine Protected Area Network Design using Network Flow
 * Author: Analysis of Algorithms Project 2
 * Date: December 2025
 *
 * This module implements the reduction of Marine Protected Area (MPA) network design
 * to a Min-Cost Max-Flow problem using C++.
 */

#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <set>
#include <queue>
#include <algorithm>
#include <limits>
#include <cmath>
#include <iomanip>

using namespace std;

const double INF = numeric_limits<double>::infinity();

/**
 * Edge structure for flow network
 */
struct Edge {
    int to;
    double capacity;
    double flow;
    int reverseEdge;
};

/**
 * Site structure
 */
struct Site {
    string id;
    double capacity;
    double cost;

    Site(const string& id, double cap, double cost)
        : id(id), capacity(cap), cost(cost) {}
};

/**
 * Marine Protected Area Network Flow Class
 *
 * Models MPA design as a network flow problem where:
 * - Source connects to spawning sites
 * - Spawning sites connect to settlement habitats via ocean currents
 * - Settlement habitats connect to sink
 */
class MPANetworkFlow {
private:
    vector<Site> spawning_sites;
    vector<Site> settlement_sites;
    map<string, int> site_to_index;
    vector<vector<Edge>> adjacency_list;
    int num_nodes;
    int source_idx;
    int sink_idx;

    // Current edges (spawning -> settlement)
    struct Current {
        string from;
        string to;
        double capacity;
    };
    vector<Current> currents;

public:
    MPANetworkFlow() : num_nodes(0), source_idx(-1), sink_idx(-1) {}

    /**
     * Add a potential spawning site
     */
    void addSpawningSite(const string& site_id, double spawning_capacity,
                        double protection_cost) {
        spawning_sites.emplace_back(site_id, spawning_capacity, protection_cost);
    }

    /**
     * Add a settlement habitat site
     */
    void addSettlementSite(const string& site_id, double carrying_capacity,
                          double protection_cost) {
        settlement_sites.emplace_back(site_id, carrying_capacity, protection_cost);
    }

    /**
     * Add an ocean current connection
     */
    void addCurrentConnection(const string& from_site, const string& to_site,
                             double transport_capacity) {
        currents.push_back({from_site, to_site, transport_capacity});
    }

    /**
     * Build flow network for given protection configuration
     */
    void buildFlowNetwork(const set<string>& protected_spawning,
                         const set<string>& protected_settlement) {
        site_to_index.clear();
        num_nodes = 0;

        // Assign indices: source, spawning sites, settlement sites, sink
        source_idx = num_nodes++;
        site_to_index["SOURCE"] = source_idx;

        for (const auto& site : spawning_sites) {
            if (protected_spawning.count(site.id)) {
                site_to_index[site.id] = num_nodes++;
            }
        }

        for (const auto& site : settlement_sites) {
            if (protected_settlement.count(site.id)) {
                site_to_index[site.id] = num_nodes++;
            }
        }

        sink_idx = num_nodes++;
        site_to_index["SINK"] = sink_idx;

        // Initialize adjacency list
        adjacency_list.assign(num_nodes, vector<Edge>());

        // Add source -> spawning edges
        for (const auto& site : spawning_sites) {
            if (protected_spawning.count(site.id)) {
                addEdge(source_idx, site_to_index[site.id], site.capacity);
            }
        }

        // Add current edges (spawning -> settlement)
        for (const auto& current : currents) {
            if (protected_spawning.count(current.from) &&
                protected_settlement.count(current.to)) {
                int from_idx = site_to_index[current.from];
                int to_idx = site_to_index[current.to];
                addEdge(from_idx, to_idx, current.capacity);
            }
        }

        // Add settlement -> sink edges
        for (const auto& site : settlement_sites) {
            if (protected_settlement.count(site.id)) {
                addEdge(site_to_index[site.id], sink_idx, site.capacity);
            }
        }
    }

    /**
     * Add edge to flow network (with reverse edge for residual graph)
     */
    void addEdge(int from, int to, double capacity) {
        Edge forward = {to, capacity, 0.0, (int)adjacency_list[to].size()};
        Edge backward = {from, 0.0, 0.0, (int)adjacency_list[from].size()};
        adjacency_list[from].push_back(forward);
        adjacency_list[to].push_back(backward);
    }

    /**
     * BFS to find augmenting path (Edmonds-Karp)
     */
    bool bfs(vector<int>& parent, vector<int>& parent_edge) {
        parent.assign(num_nodes, -1);
        parent_edge.assign(num_nodes, -1);
        parent[source_idx] = source_idx;

        queue<int> q;
        q.push(source_idx);

        while (!q.empty()) {
            int u = q.front();
            q.pop();

            for (int i = 0; i < adjacency_list[u].size(); i++) {
                Edge& e = adjacency_list[u][i];
                if (parent[e.to] == -1 && e.capacity > e.flow) {
                    parent[e.to] = u;
                    parent_edge[e.to] = i;
                    if (e.to == sink_idx) return true;
                    q.push(e.to);
                }
            }
        }
        return false;
    }

    /**
     * Compute maximum flow using Edmonds-Karp algorithm (BFS-based Ford-Fulkerson)
     */
    double computeMaxFlow() {
        double max_flow = 0.0;
        vector<int> parent, parent_edge;

        while (bfs(parent, parent_edge)) {
            // Find minimum residual capacity along path
            double path_flow = INF;
            for (int v = sink_idx; v != source_idx; v = parent[v]) {
                int u = parent[v];
                int edge_idx = parent_edge[v];
                path_flow = min(path_flow,
                    adjacency_list[u][edge_idx].capacity -
                    adjacency_list[u][edge_idx].flow);
            }

            // Update flows along path
            for (int v = sink_idx; v != source_idx; v = parent[v]) {
                int u = parent[v];
                int edge_idx = parent_edge[v];
                adjacency_list[u][edge_idx].flow += path_flow;

                // Update reverse edge
                int rev_idx = adjacency_list[u][edge_idx].reverseEdge;
                adjacency_list[v][rev_idx].flow -= path_flow;
            }

            max_flow += path_flow;
        }

        return max_flow;
    }

    /**
     * Calculate total protection cost
     */
    double calculateTotalCost(const set<string>& protected_spawning,
                             const set<string>& protected_settlement) const {
        double total = 0.0;
        for (const auto& site : spawning_sites) {
            if (protected_spawning.count(site.id)) {
                total += site.cost;
            }
        }
        for (const auto& site : settlement_sites) {
            if (protected_settlement.count(site.id)) {
                total += site.cost;
            }
        }
        return total;
    }

    /**
     * Solve max flow for given configuration
     */
    pair<double, double> solveMaxFlow(const set<string>& protected_spawning,
                                     const set<string>& protected_settlement) {
        if (protected_spawning.empty() || protected_settlement.empty()) {
            return {0.0, 0.0};
        }

        buildFlowNetwork(protected_spawning, protected_settlement);
        double flow = computeMaxFlow();
        double cost = calculateTotalCost(protected_spawning, protected_settlement);
        return {flow, cost};
    }

    /**
     * Greedy site selection to maximize flow within budget
     */
    tuple<set<string>, set<string>, double> greedySiteSelection(double budget) {
        set<string> protected_spawning;
        set<string> protected_settlement;
        double current_cost = 0.0;

        // Create list of all sites with cost-effectiveness
        struct SiteValue {
            string id;
            double cost;
            double value;
            bool is_spawning;

            bool operator<(const SiteValue& other) const {
                double ratio1 = (cost > 0) ? value / cost : INF;
                double ratio2 = (other.cost > 0) ? other.value / other.cost : INF;
                return ratio1 > ratio2;
            }
        };

        vector<SiteValue> all_sites;

        for (const auto& site : spawning_sites) {
            all_sites.push_back({site.id, site.cost, site.capacity, true});
        }

        for (const auto& site : settlement_sites) {
            all_sites.push_back({site.id, site.cost, site.capacity, false});
        }

        // Sort by value/cost ratio
        sort(all_sites.begin(), all_sites.end());

        // Greedily add sites
        for (const auto& site : all_sites) {
            if (current_cost + site.cost <= budget) {
                if (site.is_spawning) {
                    protected_spawning.insert(site.id);
                } else {
                    protected_settlement.insert(site.id);
                }
                current_cost += site.cost;
            }
        }

        auto [flow, cost] = solveMaxFlow(protected_spawning, protected_settlement);
        return {protected_spawning, protected_settlement, flow};
    }

    /**
     * Get all sites for exhaustive search
     */
    const vector<Site>& getSpawningSites() const { return spawning_sites; }
    const vector<Site>& getSettlementSites() const { return settlement_sites; }
};

