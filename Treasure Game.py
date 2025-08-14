import random
import time
from collections import deque

# Game constants
GRID_SIZE = 5
INITIAL_HEALTH = 3

# Symbols for the grid
TREASURE = "T"
TRAP = "X"
POWER_UP = "P"
OBSTACLE = "O"
EMPTY = "."

# Directions for movement
DIRECTIONS = {"W": (-1, 0), "S": (1, 0), "A": (0, -1), "D": (0, 1)}

# To Generate grid
def generate_grid():
    grid = [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    
    # Place treasure
    t_x, t_y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
    grid[t_x][t_y] = TREASURE
    
    # Place traps, power-ups, and obstacles
    for _ in range(3):
        while True:
            x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
            if grid[x][y] == EMPTY:
                grid[x][y] = random.choice([TRAP, POWER_UP, OBSTACLE])
                break
    
    return grid, (t_x, t_y)

# Display grid with player positions
def print_grid(grid, player_positions):
    temp_grid = [row[:] for row in grid]
    for i, (px, py, _) in enumerate(player_positions):
        temp_grid[px][py] = str(i+1)  # Show player number on grid
    
    for row in temp_grid:
        print(" ".join(row))
    print()

# Check if position is valid
def is_valid(x, y):
    return 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE

# 📌 Binary Search to Identify Best Region
def binary_search_treasure(grid):
    # Search row-wise and column-wise for the treasure
    for row in range(GRID_SIZE):
        if TREASURE in grid[row]:
            return (row, grid[row].index(TREASURE))
    return None  # Should never happen since we always place a treasure

# 📌 BFS Pathfinding (Shortest & Safest Route)
def bfs(grid, start, target):
    queue = deque([(start, [])])  # (current position, path taken)
    visited = set()
    
    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == target:
            return path + [(x, y)]
        
        for dx, dy in DIRECTIONS.values():
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny) and grid[nx][ny] != OBSTACLE and (nx, ny) not in visited:
                queue.append(((nx, ny), path + [(x, y)]))
                visited.add((nx, ny))
    
    return []  # No path found

# 📌 DFS Pathfinding (Alternative Exploration)
def dfs(grid, start, target, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []

    x, y = start
    if start == target:
        return path + [start]
    
    visited.add(start)
    
    for dx, dy in DIRECTIONS.values():
        nx, ny = x + dx, y + dy
        if is_valid(nx, ny) and grid[nx][ny] != OBSTACLE and (nx, ny) not in visited:
            result = dfs(grid, (nx, ny), target, visited, path + [start])
            if result:
                return result
    
    return []

# Main game loop
def play_game():
    grid, treasure_pos = generate_grid()
    num_players = 2  # Modify for multiplayer
    players = [(0, 0, INITIAL_HEALTH)] * num_players  # (x, y, health)

    while True:
        for i in range(num_players):
            x, y, health = players[i]

            # Display turn information
            print(f"\n--- Player {i+1}'s Turn ---")
            print(f"Health: {health} ❤️")
            print_grid(grid, players)

            # Player chooses manual movement or AI search
            choice = input("Choose action - Move (WASD) or AI Search (BFS/DFS/BS): ").upper()

            if choice in DIRECTIONS:  # Manual movement
                nx, ny = x + DIRECTIONS[choice][0], y + DIRECTIONS[choice][1]

                if is_valid(nx, ny):
                    if grid[nx][ny] == TREASURE:
                        print(f"🎉 Player {i+1} wins! 🎉")
                        return
                    elif grid[nx][ny] == TRAP:
                        health -= 1
                        print(f"⚠️ You stepped on a trap! Health: {health} ❤️")
                        if health == 0:
                            print(f"💀 Player {i+1} has been eliminated! 💀")
                            return
                    elif grid[nx][ny] == POWER_UP:
                        health += 1
                        print(f"✨ You found a power-up! Health: {health} ❤️")

                    players[i] = (nx, ny, health)

                else:
                    print("❌ Invalid move! Stay within the grid.")

            elif choice == "BFS":  # Use BFS to find shortest path
                path = bfs(grid, (x, y), treasure_pos)
                if path:
                    print(f"🔍 BFS Found Path: {path}")
                    players[i] = (*path[1], health)
                else:
                    print("❌ No valid BFS path found!")

            elif choice == "DFS":  # Use DFS to explore deep paths
                path = dfs(grid, (x, y), treasure_pos)
                if path:
                    print(f"🔎 DFS Exploring Path: {path}")
                    players[i] = (*path[1], health)
                else:
                    print("❌ No valid DFS path found!")

            elif choice == "BS":  # Use Binary Search to locate treasure row
                found_pos = binary_search_treasure(grid)
                print(f"🧭 Binary Search Suggests Checking Row {found_pos[0]}")

            else:
                print("❌ Invalid input! Use W, A, S, D or AI search options.")

            # Health warning if low
            if health == 1:
                print("⚠️ Warning: Your health is critically low! ⚠️")

            time.sleep(1)

# Run the game
if __name__ == "__main__":
    play_game()
