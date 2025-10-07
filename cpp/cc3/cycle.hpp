#pragma once

#include <vector>

#include "graph.hpp"


namespace cc3 {

    // UNDIRECTED LIST GRAPH
    bool _find_cycle_list_undirected(const ListGraph &graph, int current, int parent, std::vector<bool> &visited) {
        visited[current] = true;
        for (const Edge &e : graph.list[current]) {
            if (e.dest == parent) {continue;}
            if (visited[e.dest] || _find_cycle_list_undirected(graph, e.dest, current, visited)) {return true;}
        } return false;
    }

    bool find_cycle_undirected(const ListGraph &graph) {
        std::vector<bool> visited(graph.order, false);
        for (int i = 0; i < graph.order; ++i) {
            if (!visited[i] && _find_cycle_list_undirected(graph, i, -1, visited)) {return true;}
        } return false;
    }

    // UNDIRECTED MATRIX GRAPH
    bool _find_cycle_matrix_undirected(const MatrixGraph &graph, int current, int parent, std::vector<bool> &visited) {
        visited[current] = true;
        for (int i = 0; i < graph.order; ++i) {
            if (!graph.matrix[current][i] || i == parent) {continue;}
            if (visited[i] || _find_cycle_matrix_undirected(graph, i, current, visited)) {return true;}
        } return false;
    }

    bool find_cycle_undirected(const MatrixGraph &graph) {
        std::vector<bool> visited(graph.order, false);
        for (int i = 0; i < graph.order; ++i) {
            if (!visited[i] && _find_cycle_matrix_undirected(graph, i, -1, visited)) {return true;}
        } return false;
    }

    // DIRECTED LIST GRAPH
    bool _find_cycle_list_directed(const ListGraph &graph, int current, std::vector<int> &visited) {
        visited[current] = 1;
        for (const Edge &e : graph.list[current]) {
            if (visited[e.dest] == 1 || (!visited[e.dest] && _find_cycle_list_directed(graph, e.dest, visited))) {return true;}
        } visited[current] = 2;
        return false;
    }

    bool find_cycle_directed(const ListGraph &graph) {
        std::vector<int> visited(graph.order, 0);
        for (int i = 0; i < graph.order; ++i) {
            if (!visited[i] && _find_cycle_list_directed(graph, i, visited)) {return true;}
        } return false;
    }

    // DIRECTED MATRIX GRAPH
    bool _find_cycle_matrix_directed(const MatrixGraph &graph, int current, std::vector<int> &visited) {
        visited[current] = 1;
        for (int i = 0; i < graph.order; ++i) {
            if (!graph.matrix[current][i]) {continue;}
            if (visited[i] == 1 || (!visited[i] && _find_cycle_matrix_directed(graph, i, visited))) {return true;}
        } visited[current] = 2;
        return false;
    }

    bool find_cycle_directed(const MatrixGraph &graph) {
        std::vector<int> visited(graph.order, 0);
        for (int i = 0; i < graph.order; ++i) {
            if (!visited[i] && _find_cycle_matrix_directed(graph, i, visited)) {return true;}
        } return false;
    }

    // CYCLE DETECTION
    bool find_cycle(const ListGraph &graph) {
        if (graph.directed) {
            return find_cycle_directed(graph);
        } else {
            return find_cycle_undirected(graph);
        }
    }

    bool find_cycle(const MatrixGraph &graph) {
        if (graph.directed) {
            return find_cycle_directed(graph);
        } else {
            return find_cycle_undirected(graph);
        }
    }

}