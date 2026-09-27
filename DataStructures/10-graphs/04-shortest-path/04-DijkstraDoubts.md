# Dijkstra — Common Doubts

## Why Store Both Distance and Node?

The priority queue stores:

```text
{distance used to reach this node, node}
```

A node can enter the queue more than once because a shorter path may be discovered later. The queued distance tells us which path produced that particular entry.

```cpp
auto [currentDistance, node] = minHeap.top();
minHeap.pop();

if (currentDistance > distance[node]) continue;
```

The condition skips an old queue entry after a better path has already been found.

## Which Distance Should Relax Edges?

Prefer the distance taken from the queue:

```cpp
for (auto [neighbor, weight] : graph[node]) {
    if (distance[neighbor] > currentDistance + weight) {
        distance[neighbor] = currentDistance + weight;
        minHeap.push({distance[neighbor], neighbor});
    }
}
```

Using `distance[node]` can also work in normal Dijkstra, but using `currentDistance` makes the current path explicit and pairs naturally with the outdated-entry check.

## Cheapest Flights Within K Stops

This problem has two constraints:

- Total cost
- Number of stops

A single `distance[node]` value does not fully describe the state. A cheaper path using too many stops may not be usable, while a more expensive path using fewer stops may lead to the answer.

The state must include stops, node, and cost:

```text
{stops, node, cost}
```

This is not ordinary Dijkstra. It is a constrained shortest-path problem. Another simple solution is Bellman-Ford relaxation for at most `K + 1` edges.

## Rules to Remember

1. Standard Dijkstra works only with non-negative weights.
2. Store `{distance, node}` in the min-heap.
3. Skip an entry when its queued distance is greater than the current best distance.
4. If the problem adds another constraint, that constraint may need to become part of the state.

