# 3. Grid Problems Are Graph Problems

Treat every cell as a node. Its neighboring cells are connected nodes.

## Four directions

```cpp
int dr[] = {-1, 0, 1, 0};
int dc[] = {0, 1, 0, -1};

for (int direction = 0; direction < 4; direction++) {
    int newRow = row + dr[direction];
    int newCol = col + dc[direction];

    if (newRow >= 0 && newRow < rows &&
        newCol >= 0 && newCol < cols) {
        // valid neighboring cell
    }
}
```

## Common patterns

### Count groups

For every unvisited valid cell, start BFS/DFS and increase the answer.

Used in Number of Islands and Number of Enclaves.

### Spread from many cells

Put every starting cell into the queue before BFS begins.

```text
all rotten oranges -> queue -> BFS together
```

This is **multi-source BFS**. Used in Rotten Oranges and 01 Matrix.

### Boundary traversal

Start from valid boundary cells and mark everything reachable from them.

Used in Surrounded Regions and Number of Enclaves.

## Important checks

- Validate row and column before accessing the grid.
- Mark visited when adding a cell to the queue.
- Check whether diagonal movement is allowed.
- You may modify the grid instead of using a separate visited matrix when the problem allows it.

