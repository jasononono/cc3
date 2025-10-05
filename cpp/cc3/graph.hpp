#pragma once

#include <vector>
#include <algorithm>


namespace cc3 {

    struct Edge {

        int dest;
        int weight;
        bool weighted;

        Edge(int d, int w, bool b) {
            dest = d;
            weight = w;
            weighted = b;
        }

        bool operator==(int other) const {
            return dest == other;
        }

        bool operator==(const Edge &other) const {
            return dest == other.dest && weight == other.weight;
        }

        std::string to_string() const {
            if (weighted) {
                return "[" + std::to_string(dest) + " " + std::to_string(weight) + "]";
            } return "[" + std::to_string(dest) + "]";
            
        }
    };


    struct ListGraph {

        int order;
        int size;

        bool weighted;
        bool directed;

        std::vector<std::vector<Edge>> list;

        ListGraph(int v = 0, bool w = false, bool d = false) {
            order = 0;
            size = 0;

            weighted = w;
            directed = d;

            list = std::vector<std::vector<Edge>>();
            add_vertices(v);
        }

        std::string to_string() const {
            std::string result = "";
            for (int i = 0; i < order; ++i) {
                result += std::to_string(i) + " | ";
                for (int j = 0; j < list[i].size(); ++j) {
                    result += list[i][j].to_string();
                } result += "\n";
            } return result;
        }

        void add_vertices(int amount = 1) {
            order += amount;
            list.resize(order, std::vector<Edge>());
        }

        // IS EDGE
        bool is_edge(int a, int b) { // O(degree of a)
            if (a >= order || b >= order) {return false;}

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
            if (!weighted) {w = 1;}

            list[a].push_back(Edge(b, w, weighted));
            if (!directed) {list[b].push_back(Edge(a, w, weighted));}

            size++; return true;
        }

        // REMOVE EDGE
        bool remove_edge(int a, int b) {
            bool result = _remove_edge(a, b);
            if (!directed) {_remove_edge(b, a);}

            size--; return result;
        }

        bool _remove_edge(int a, int b) {
            for (int i = 0; i < list[a].size(); ++i) {
                if (list[a][i] == b) {
                    list[a].erase(list[a].begin() + i);
                    return true;
                }
            } return false;
        }

        // OUT DEGREE
        int out_degree(int v) { // O(1)
            if (v >= order) {return -1;}
            return list[v].size();
        }

        // IN DEGREE
        int in_degree(int v) { // O(e)
            if (v >= order) {return -1;}

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


    struct MatrixGraph {

        int order;
        int size;

        bool weighted;
        bool directed;

        std::vector<std::vector<int>> matrix;

        MatrixGraph(int v = 0, bool w = false, bool d = false) {
            order = 0;
            size = 0;

            weighted = w;
            directed = d;

            matrix = std::vector<std::vector<int>>();
            add_vertices(v);
        }

        void add_vertices(int amount = 1) {
            order += amount;

            for (std::vector<int> &i : matrix) {
                i.resize(order, 0);
            } matrix.resize(order, std::vector<int>(order, 0));
        }

        // IS EDGE
        bool is_edge(int a, int b) { // O(1)
            if (a >= order || b >= order) {return false;}
            return matrix[a][b] != 0;
        }
        
        // ADD EDGE
        bool add_edge(int a, int b, int w = 1) {
            if (is_edge(a, b)) {return false;}

            if (a >= order || b >= order) {
                add_vertices(std::max(a, b) - order + 1);
            }
            if (!weighted) {w = 1;}

            matrix[a][b] = w;
            if (!directed) {matrix[a][b] = w;}

            size++; return true;
        }

        // REMOVE EDGE
        bool remove_edge(int a, int b) {
            if (matrix[a][b] == 0) {return false;}

            matrix[a][b] = 0;
            if (!directed) {matrix[a][b] = 0;}

            size--; return true;
        }

        // OUT DEGREE
        int out_degree(int v) { // O(n)
            if (v >= order) {return -1;}
            
            int count = 0;
            for (int i : matrix[v]) {
                if (i) {count++;}
            }
            return count;
        }

        // IN DEGREE
        int in_degree(int v) { // O(n)
            if (v >= order) {return -1;}
            
            int count = 0;
            for (int i = 0; i < order; ++i) {
                if (matrix[i][v]) {count++;}
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