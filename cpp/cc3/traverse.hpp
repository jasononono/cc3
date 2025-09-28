#pragma once

#include <queue>
#include <vector>

#include "graph.hpp"


namespace cc3 {

    // BFS
    std::vector<int> bfs(const Graph &graph, int anchor = 0) {
        std::queue<int> q;
        std::vector<bool> visited(graph.order, false);
        std::vector<int> dist(graph.order, -1);

        q.push(anchor);
        visited[anchor] = true;
        dist[anchor] = 0;

        int current;

        while (!q.empty()) {
            current = q.front(); q.pop();
            for (Edge e : graph.list[current]) {
                if (!visited[e.dest]) {
                    q.push(e.dest);
                    visited[e.dest] = true;
                    dist[e.dest] = dist[current] + 1;
                }
            }
        } return dist;
    }
    
    // DFS
    void _dfs(const Graph &graph, int current, std::vector<bool> &visited) {
        visited[current] = true;
        for (Edge e : graph.list[current]) {
            if (!visited[e.dest]) {
                _dfs(graph, e.dest, visited);
            }
        }
    }

    std::vector<bool> dfs(const Graph &graph, int anchor = 0) {
        std::vector<bool> visited(graph.order, false);
        _dfs(graph, anchor, visited);
        return visited;
    }
}