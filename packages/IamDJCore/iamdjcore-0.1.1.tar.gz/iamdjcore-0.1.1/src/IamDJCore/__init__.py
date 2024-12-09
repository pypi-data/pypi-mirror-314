import heapq
from heapq import heappop, heappush
from collections import deque

class search:
    
    def __init__(self):
        pass
    
    @staticmethod
    def dijkstra(graph, start):
        # Initialize distances with infinity and set the start node distance to 0
        distances = {node: float('infinity') for node in graph}
        distances[start] = 0
        priority_queue = [(0, start)]
        
        while priority_queue:
            current_distance, current_node = heappop(priority_queue)
            
            # Skip processing if we find a longer distance in the queue
            if current_distance > distances[current_node]:
                continue
            
            for neighbor in graph[current_node]:
                distance = current_distance + 1  # Assuming all edges have weight 1
                
                # Only consider this new path if it's better
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heappush(priority_queue, (distance, neighbor))
        
        return distances
    
    @staticmethod
    def Astar(graph, start, goal, heuristic):
        open_list = []
        heappush(open_list, (0 + heuristic[start], 0, start, []))
        closed_list = set()

        while open_list:
            _, cost, current, path = heappop(open_list)
            if current in closed_list:
                continue

            path = path + [current]
            if current == goal:
                return path

            closed_list.add(current)
            for neighbor in graph[current]:
                if neighbor not in closed_list:
                    heappush(open_list, (cost + 1 + heuristic[neighbor], cost + 1, neighbor, path))

        return None

    @staticmethod
    def greedy(graph, start, goal, heuristic):
        open_list = []
        heappush(open_list, (heuristic[start], start, []))
        closed_list = set()

        while open_list:
            _, current, path = heappop(open_list)
            if current in closed_list:
                continue

            path = path + [current]
            if current == goal:
                return path

            closed_list.add(current)
            for neighbor in graph[current]:
                if neighbor not in closed_list:
                    heappush(open_list, (heuristic[neighbor], neighbor, path))

        return None
    
    @staticmethod
    def bfs(graph, start):
        visited = set()
        queue = deque([start])
        visited.add(start)

        while queue:
            vertex = queue.popleft()
            print(vertex, end=" ")

            for neighbor in graph[vertex]:
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)
        print()  # For better output formatting

    @staticmethod
    def dfs(graph, start, visited=None):
        if visited is None:
            visited = set()
        visited.add(start)
        print(start, end=" ")

        for neighbor in graph[start]:
            if neighbor not in visited:
                search.dfs(graph, neighbor, visited)
        print()  # For better output formatting


# Sample graph represented as an adjacency list
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

# Perform BFS starting from vertex 'A'
print("BFS traversal starting from 'A':")
search.bfs(graph, 'A')

# Running Dijkstra's algorithm from node 'A'
distances = search.dijkstra(graph, 'A')
print("Dijkstra's distances:", distances)

# A* search from 'A' to 'D'
heuristic = {
    'A': 3,
    'B': 1,
    'C': 1,
    'D': 0,
    'E': 1,
    'F': 2
}
start = 'A'
goal = 'D'
path = search.Astar(graph, start, goal, heuristic)
print("Path found using A*:", path)

# Greedy Best-First Search from 'A' to 'D'
greedy_path = search.greedy(graph, start, goal, heuristic)
print("Path found using Greedy Best-First Search:", greedy_path)

# Perform DFS starting from vertex 'A'
print("DFS traversal starting from 'A':")
search.dfs(graph, 'A')