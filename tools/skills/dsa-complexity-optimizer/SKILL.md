---
name: dsa-complexity-optimizer
description: >-
  Data Structures, Algorithms & Complexity Optimization skill (CT 552, CT 551).
  Audits Big-O space/time asymptotic bounds, selects optimal data structures
  (balanced trees, heaps, tries, disjoint sets), and optimizes graph traversals
  and dynamic programming routines.
---

# Data Structures & Algorithmic Complexity Optimizer (`dsa-complexity-optimizer`)

Derived from **CT 552 (Data Structure and Algorithms)** and **CT 551 (Discrete Structure)** in the BE ECIE curriculum.

This skill equips agents to perform rigorous asymptotic complexity auditing ($O(1)$ to $O(2^n)$), eliminate algorithmic bottlenecks, select optimal abstract data types, and architect provably efficient graph traversals and dynamic programming pipelines.

---

## 1. Operating Rules & Asymptotic Standards

1. **Tight Bound Specification:** Never state loose bounds; provide tight Big-$\Theta$ bounds when average and worst cases align.
2. **Space-Time Trade-off Transparency:** Always declare auxiliary memory complexity alongside time complexity (e.g., $O(V)$ space for Dijkstra with min-heap).
3. **Cache & Constant Factor Realism:** A theoretical $O(N)$ algorithm with heavy memory indirection (e.g. pointer chasing across linked nodes) can run slower than an $O(N \log N)$ algorithm operating on contiguous cache-friendly arrays.

---

## 2. Core Capabilities & Workflows

### Capability A: Asymptotic Complexity Audit & Profiling
Analyze functions for nested iteration, hidden library costs (e.g. Python list slicing inside loops), and recursion depth:

| Target Routine | Time Complexity (Best / Avg / Worst) | Space Complexity | Primary Bottleneck | Optimization Strategy |
| :--- | :--- | :--- | :--- | :--- |
| Naive Search | $O(1) / O(N) / O(N)$ | $O(1)$ | Linear scan | Hash Map ($O(1)$ amortized) or Sorted Binary Search ($O(\log N)$) |
| Nested Loop Filter | $O(N^2) / O(N^2) / O(N^2)$ | $O(1)$ | Pairwise comparison | Two-pointer technique or prefix-sum array ($O(N)$) |
| Recursive Fibonacci | $O(2^N)$ | $O(N)$ | Redundant subproblems | Memoization / Bottom-up DP ($O(N)$ time, $O(1)$ space) |
| All-Pairs Path | $O(V^3)$ | $O(V^2)$ | Dense matrix traversal | Johnson's algorithm for sparse graphs ($O(V^2 \log V + VE)$) |

### Capability B: Abstract Data Type (ADT) Selection Matrix
Choose the mathematically optimal data structure for the target access pattern:

* **Frequent Priority Lookups:** Min/Max Binary Heap or Fibonacci Heap ($O(1)$ peek, $O(\log N)$ insert/extract).
* **Ordered Range Queries:** AVL Tree or Red-Black Tree ($O(\log N)$ search/insert/delete with strict balancing guarantees).
* **Prefix / String Matching:** Trie or Radix Tree ($O(L)$ where $L$ is string length, independent of dictionary size $N$).
* **Disjoint Connectivity / Cycle Detection:** Disjoint Set Union (DSU) with Path Compression & Union by Rank ($\approx O(\alpha(N))$ nearly constant time).
* **Sliding Window Min/Max:** Monotonic Queue / Deque ($O(N)$ total time across all window shifts).

### Capability C: Graph Algorithm Synthesis
Scaffold optimal graph traversals:
- **Unweighted Shortest Path:** Breadth-First Search (BFS) — $O(V + E)$
- **Non-Negative Weighted Shortest Path:** Dijkstra with Min-Heap — $O((V + E) \log V)$
- **General Weighted with Negative Edges:** Bellman-Ford — $O(VE)$ or SPFA
- **Minimum Spanning Tree:** Kruskal's (with DSU) — $O(E \log E)$ or Prim's — $O(E \log V)$
- **Strongly Connected Components:** Tarjan's or Kosaraju's algorithm — $O(V + E)$
