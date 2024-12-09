import heapq

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
            current_distance, current_node = heapq.heappop(priority_queue)
            
            # Skip processing if we find a longer distance in the queue
            if current_distance > distances[current_node]:
                continue
            
            for neighbor, weight in graph[current_node].items():
                distance = current_distance + weight
                
                # Only consider this new path if it's better
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))
        
        return distances

# Sample graph represented as an adjacency list
