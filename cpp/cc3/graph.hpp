#pragma once

#include <vector>
#include <algorithm>


namespace cc3 {

    struct Edge {

        int dest;
        int weight;

        Edge(int d, int w) {
            dest = d;
            weight = w;
        }

        bool operator==(int other) const {
            return dest == other;
        }

        bool operator==(const Edge &other) const {
            return dest == other.dest && weight == other.weight;
        }
        
    };


    struct Graph {

        int order;
        int size;

        bool weighted;
        bool directed;

        std::vector<std::vector<int>> matrix;
        std::vector<std::vector<Edge>> list;

        Graph(int v = 0, bool w = false, bool d = false) {
            order = v;
            size = 0;

            weighted = w;
            directed = d;

            matrix = std::vector<std::vector<int>>();
            list = std::vector<std::vector<Edge>>();
        }

        void add_vertices(int amount = 1) {
            order += amount;

            for (std::vector<int> &i : matrix) {
                i.resize(order, 0);
            } matrix.resize(order, std::vector<int>(order, 0));

            list.resize(order, std::vector<Edge>());
        }

        // IS EDGE
        bool is_edge(int a, int b) {
            if (a >= order || b >= order) {return false;}
            return is_edge_matrix(a, b);
        }

        bool is_edge_matrix(int a, int b) { // O(1)
            return matrix[a][b] != 0;
        }

        bool is_edge_list(int a, int b) { // O(degree of a)
            for (const Edge &e : list[a]) {
                if (e == b) {return true;}
            } return false;
        }
        
        // ADD EDGE
        bool add_edge(int a, int b, int w = 1) {
            if (is_edge(a, b)) {return false;}

            if (a >= order || b >= order) {
                add_vertices(std::max(a, b) - order + 1);
            }

            _add_edge(a, b, w);
            if (!directed) {_add_edge(b, a, w);}

            size++; return true;
        }

        void _add_edge(int a, int b, int w) {
            if (!weighted) {w = 1;}
            matrix[a][b] = w;
            list[a].push_back(Edge(b, w));
        }

        // REMOVE EDGE
        bool remove_edge(int a, int b) {
            bool result = _remove_edge(a, b);
            if (!directed) {_remove_edge(b, a);}

            size--; return result;
        }

        bool _remove_edge(int a, int b) {
            matrix[a][b] = 0;
            for (int i = 0; i < list[a].size(); ++i) {
                if (list[a][i] == b) {
                    list[a].erase(list[a].begin() + i);
                    return true;
                }
            } return false;
        }

        // OUT DEGREE
        int out_degree(int v) {
            if (v >= order) {return -1;}
            return out_degree_list(v);
        }

        int out_degree_matrix(int v) { // O(n)
            int count = 0;
            for (int i : matrix[v]) {
                if (i) {count++;}
            }
            return count;
        }

        int out_degree_list(int v) { // O(1)
            return list[v].size();
        }

        // IN DEGREE
        int in_degree(int v) {
            if (v >= order) {return -1;}
            if (order < size) {
                return in_degree_matrix(v);
            } return in_degree_list(v);
        }

        int in_degree_matrix(int v) {
            int count = 0;
            for (int i = 0; i < order; ++i) {
                if (matrix[i][v]) {count++;}
            } return count;
        }

        int in_degree_list(int v) {
            int count = 0;
            for (const std::vector<Edge> &i : list) {
                for (const Edge &e : i) {
                    if (e == v) {count++;}
                }
            } return count;
        }

        // DEGREE
        int degree(int v) {
            if (v >= order) {return -1;}
            if (directed) {
                return in_degree(v) + out_degree(v);
            } return out_degree(v);
        }
    };
}