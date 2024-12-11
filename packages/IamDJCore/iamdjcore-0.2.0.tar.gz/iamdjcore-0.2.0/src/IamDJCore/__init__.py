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
        
class Sort:
    def __init__(self):
        pass

    @staticmethod
    def bubble_sort(arr):
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]

    @staticmethod
    def insertion_sort(arr):
        for i in range(1, len(arr)):
            j = i
            while j > 0 and arr[j - 1] > arr[j]:
                arr[j - 1], arr[j] = arr[j], arr[j - 1]
                j -= 1
        return arr

    @staticmethod
    def selection_sort(arr):
        n = len(arr)
        for i in range(n):
            min_index = i
            for j in range(i + 1, n):
                if arr[j] < arr[min_index]:
                    min_index = j
            arr[i], arr[min_index] = arr[min_index], arr[i]
        return arr

    @staticmethod
    def quick_sort(arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[0]
        left = [i for i in arr[1:] if i < pivot]
        right = [i for i in arr[1:] if i >= pivot]
        return Sort.quick_sort(left) + [pivot] + Sort.quick_sort(right)

    @staticmethod
    def bucket_sort(arr):
        if len(arr) == 0:
            return arr

        max_value = max(arr)
        bucket_count = len(arr)
        buckets = [[] for _ in range(bucket_count)]

        for item in arr:
            bucket_index = int(item * bucket_count / (max_value + 1))
            buckets[bucket_index].append(item)

        sorted_array = []
        for bucket in buckets:
            bucket.sort()
            sorted_array.extend(bucket)

        return sorted_array

    @staticmethod
    def shell_sort(arr):
        n = len(arr)
        gap = 1
        while gap < n // 3:
            gap = gap * 3 + 1

        while gap > 0:
            for start in range(gap):
                Sort.gap_insertion_sort(arr, start, gap)
            gap //= 3
        return arr

    @staticmethod
    def gap_insertion_sort(arr, start, gap):
        for i in range(start + gap, len(arr), gap):
            current_value = arr[i]
            position = i
            while position >= gap and arr[position - gap] > current_value:
                arr[position] = arr[position - gap]
                position -= gap
            arr[position] = current_value

    @staticmethod
    def merge_sort(arr):
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]

        left = Sort.merge_sort(left)
        right = Sort.merge_sort(right)

        return Sort.merge(left, right)

    @staticmethod
    def merge(left, right):
        merged = []
        left_index = 0
        right_index = 0

        while left_index < len(left) and right_index < len(right):
            if left[left_index] <= right[right_index]:
                merged.append(left[left_index])
                left_index += 1
            else:
                merged.append(right[right_index])
                right_index += 1

        merged += left[left_index:]
        merged += right[right_index:]

        return merged

    @staticmethod
    def radix_sort(arr):
        max_num = max(arr)
        exp = 1
        while max_num // exp > 0:
            Sort.counting_sort(arr, exp)
            exp *= 10
        return arr

    @staticmethod
    def counting_sort(arr, exp):
        n = len(arr)
        output = [0] * n
        count = [0] * 10  # Assuming base 10

        for i in range(n):
            index = arr[i] // exp
            count[index % 10] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        for i in range(n - 1, -1, -1):
            index = arr[i] // exp
            output[count[index % 10] - 1] = arr[i]
            count[index % 10] -= 1

        for i in range(n):
            arr[i] = output[i]

    @staticmethod
    def comb_sort(arr):
        n = len(arr)
        gap = n
        shrink = 1.3  # Shrink factor
        sorted = False

        while not sorted:
            gap = int(gap / shrink)
            if gap < 1:
                gap = 1
            sorted = True

            for i in range(n - gap):
                if arr[i] > arr[i + gap]:
                    arr[i], arr[i + gap] = arr[i + gap], arr[i]
                    sorted = False

        return arr

    @staticmethod
    def timsort(arr):
        min_run = 32
        n = len(arr)

        for start in range(0, n, min_run):
            end = min(start + min_run, n)
            Sort.insertion_sort(arr[start:end])

        size = min_run
        while size < n:
            for left in range(0, n, size * 2):
                mid = left + size - 1
                right = min((left + 2 * size - 1), (n - 1))

                if mid < right:
                    merged_array = Sort.merge(arr[left:mid + 1], arr[mid + 1:right + 1])
                    arr[left:left + len(merged_array)] = merged_array

            size *= 2

        return arr
