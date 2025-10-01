#pragma once

#include <queue>
#include <deque>
#include <vector>

#include "graph.hpp"


namespace cc3 {

    // BFS
    std::vector<int> bfs(const ListGraph &graph, int anchor = 0) {
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

    std::vector<int> bfs(const MatrixGraph &graph, int anchor = 0) {
        std::queue<int> q;
        std::vector<bool> visited(graph.order, false);
        std::vector<int> dist(graph.order, -1);

        q.push(anchor);
        visited[anchor] = true;
        dist[anchor] = 0;

        int current;

        while (!q.empty()) {
            current = q.front(); q.pop();
            for (int e = 0; e < graph.matrix[current].size(); ++e) {
                if (graph.matrix[current][e] != 0 && !visited[e]) {
                    q.push(e);
                    visited[e] = true;
                    dist[e] = dist[current] + 1;
                }
            }
        } return dist;
    }

    // 0-1 BFS
    std::vector<int> zero_one_bfs(const ListGraph &graph, int anchor = 0) {
        std::deque<int> d;
        std::vector<bool> visited(graph.order, false);
        std::vector<int> dist(graph.order, -1);

        d.push_back(anchor);
        visited[anchor] = true;
        dist[anchor] = 0;

        int current;

        while (!d.empty()) {
            current = d.front(); d.pop_front();
            for (Edge e : graph.list[current]) {
                if (!visited[e.dest]) {
                    if (e.weight) {
                        d.push_back(e.dest);
                        dist[e.dest] = dist[current] + 1;
                    } else {
                        d.push_front(e.dest);
                        dist[e.dest] = dist[current];
                    }
                    visited[e.dest] = true;
                }
            }
        } return dist;
    }
    
    // DFS
    std::vector<bool> dfs(const ListGraph &graph, int anchor = 0) {
        std::vector<bool> visited(graph.order, false);
        _dfs(graph, anchor, visited);
        return visited;
    }

    void _dfs(const ListGraph &graph, int current, std::vector<bool> &visited) {
        visited[current] = true;
        for (Edge e : graph.list[current]) {
            if (!visited[e.dest]) {
                _dfs(graph, e.dest, visited);
            }
        }
    }

    std::vector<bool> dfs(const MatrixGraph &graph, int anchor = 0) {
       std::vector<bool> visited(graph.order, false);
        _dfs(graph, anchor, visited);
        return visited;
    }

    void _dfs(const MatrixGraph &graph, int current, std::vector<bool> &visited) {
        visited[current] = true;
        for (int e = 0; e < graph.matrix[current].size(); ++e) {
            if (graph.matrix[current][e] != 0 && !visited[e]) {
                _dfs(graph, e, visited);
            }
        }
    }
}