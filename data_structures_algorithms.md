# Explain these data structures: Stacks, Queues, Trees, Heap, Arrays, Dictionaries

* Stack: A stack is a Last-In-First-Out (LIFO) data structure, meaning the last element added is the first to be removed. It supports two main operations: push (to add an element) and pop (to remove the top element). Stacks are used in function calls (call stack), undo mechanisms, and depth-first search algorithms.

* Queue: A queue follows the First-In-First-Out (FIFO) principle, meaning elements are added at the back and removed from the front. Operations include enqueue (to add an element) and dequeue (to remove an element). Queues are used in task scheduling, breadth-first search, and buffering systems.

* Tree: A tree is a hierarchical data structure with nodes connected by edges. The top node is called the root, and each node can have child nodes. Types of trees include binary trees (each node has at most two children), binary search trees (BSTs, where the left child is smaller and the right child is larger), and more specialized trees like AVL trees and B-trees.

* Heap: A heap is a special type of binary tree that satisfies the heap property. In a min-heap, the parent node is always smaller than its children, while in a max-heap, the parent is always larger. Heaps are commonly used in priority queues and heap sort algorithms.

* Array: An array is a collection of elements stored in contiguous memory locations. It provides fast access to elements via indexing but has a fixed size in most languages. Operations like insertion and deletion can be expensive unless modifying the last element.

* Dictionary (HashMap): A dictionary (or hashmap) stores key-value pairs, allowing for fast lookups, insertions, and deletions. It uses a hashing function to map keys to indices. Collisions are handled using techniques like chaining or open addressing.

# Breadth first search vs depth first search, recursion, brute force algorithms

Breadth-First Search vs. Depth-First Search:
* Breadth-First Search (BFS): Explores all nodes at the current level before moving to the next level. It uses a queue for traversal and is useful for finding the shortest path in unweighted graphs.

* Depth-First Search (DFS): Explores as far as possible along each branch before backtracking. It uses a stack (or recursion) and is useful for maze-solving, cycle detection, and topological sorting.

* Recursion:
Recursion is a technique where a function calls itself to solve a problem. It is useful for problems that can be broken down into smaller subproblems, such as tree traversal and divide-and-conquer algorithms. However, recursion can lead to high memory usage due to the call stack.

Brute Force Algorithms:
* A brute force algorithm tries all possible solutions to find the correct one. It is simple to implement but inefficient for large inputs. Examples include checking all substrings for pattern matching or trying all possible combinations in a search problem.

# The trade-offs Big O notation for both space and time complexity

* Time Complexity: Measures how the running time of an algorithm grows with input size. Common complexities include O(1) (constant time), O(log n) (logarithmic), O(n) (linear), O(n log n) (log-linear), O(n²) (quadratic), and O(2ⁿ) (exponential).

* Space Complexity: Measures how much extra memory an algorithm uses. Iterative solutions generally use O(1) space, while recursive solutions may use O(n) due to the call stack. Algorithms like mergesort require additional space for merging, while in-place sorting algorithms like quicksort use minimal extra memory.
