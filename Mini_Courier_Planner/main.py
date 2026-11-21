# MINI COURIER PLANNER
# PHASE 1: PROBLEM DESIGN

# Step 1: Store parcel information

parcels = [
    {
        "id": "P1",
        "destination": "A",
        "weight": 4,
        "value": 100,
        "priority": "High"
    },
    {
        "id": "P2",
        "destination": "B",
        "weight": 3,
        "value": 80,
        "priority": "Medium"
    },
    {
        "id": "P3",
        "destination": "C",
        "weight": 5,
        "value": 150,
        "priority": "High"
    },
    {
        "id": "P4",
        "destination": "D",
        "weight": 2,
        "value": 60,
        "priority": "Low"
    },
    {
        "id": "P5",
        "destination": "E",
        "weight": 6,
        "value": 200,
        "priority": "High"
    }
]

# Step 2: Define vehicle capacity

vehicle_capacity = 10

# Step 3: Create road network (Graph)

graph = {
    "Warehouse": {"A": 4, "B": 6},
    "A": {"Warehouse": 4, "B": 2, "C": 5},
    "B": {"Warehouse": 6, "A": 2, "C": 3, "D": 7},
    "C": {"A": 5, "B": 3, "D": 4, "E": 6},
    "D": {"B": 7, "C": 4, "E": 2},
    "E": {"C": 6, "D": 2}
}

# Step 4: Display parcel information

print("===== MINI COURIER PLANNER =====")

print("\nAVAILABLE PARCELS")

for parcel in parcels:
    print(parcel)

# Step 5: Display vehicle capacity

print("\nVehicle Capacity:", vehicle_capacity, "kg")

# Step 6: Display graph

print("\nROAD NETWORK")
print()
for location, roads in graph.items():
    print(location, ":", roads)

# print("\nPhase 1 Data Created Successfully!")






# PHASE 2 - PART A: MERGE SORT

# Assign numerical values to priorities
priority_order = {
    "High": 1,
    "Medium": 2,
    "Low": 3
}


def merge_sort(parcel_list):

    # Base condition
    if len(parcel_list) <= 1:
        return parcel_list

    # Divide the list into two halves
    mid = len(parcel_list) // 2

    left = merge_sort(parcel_list[:mid])
    right = merge_sort(parcel_list[mid:])

    # Merge the sorted halves
    result = []

    i = 0
    j = 0

    while i < len(left) and j < len(right):

        if priority_order[left[i]["priority"]] <= priority_order[right[j]["priority"]]:
            result.append(left[i])
            i += 1

        else:
            result.append(right[j])
            j += 1

    # Add remaining elements
    result.extend(left[i:])
    result.extend(right[j:])

    return result


# Sort parcels
sorted_parcels = merge_sort(parcels)

# Display sorted parcels
print("\n===== PARCELS AFTER SORTING =====")

for parcel in sorted_parcels:
    print(
        parcel["id"],
        "-",
        parcel["priority"],
        "-",
        parcel["destination"]
    )


# PHASE 2 - PART B: 0/1 KNAPSACK

def knapsack(parcels, capacity):

    n = len(parcels)

    # Create DP table filled with zeros
    dp = [[0 for w in range(capacity + 1)]
          for i in range(n + 1)]

    # Fill the DP table
    for i in range(1, n + 1):

        weight = parcels[i - 1]["weight"]
        value = parcels[i - 1]["value"]

        for w in range(capacity + 1):

            # If parcel weight exceeds capacity
            if weight > w:
                dp[i][w] = dp[i - 1][w]

            else:
                # Exclude parcel
                exclude = dp[i - 1][w]

                # Include parcel
                include = value + dp[i - 1][w - weight]

                # Choose maximum value
                dp[i][w] = max(include, exclude)

    # Find selected parcels using backtracking
    selected = []
    w = capacity

    for i in range(n, 0, -1):

        if dp[i][w] != dp[i - 1][w]:

            selected.append(parcels[i - 1])
            w -= parcels[i - 1]["weight"]

    selected.reverse()

    return dp, selected


# Run Knapsack
dp_table, selected_parcels = knapsack(
    parcels, vehicle_capacity
)

# Display results
print("\n===== KNAPSACK RESULTS =====")

total_weight = 0
total_value = 0

for parcel in selected_parcels:

    print("Selected:", parcel["id"])

    total_weight += parcel["weight"]
    total_value += parcel["value"]

print("\nTotal Weight:", total_weight, "kg")
print("Total Value:", total_value)

print("\nMaximum Vehicle Capacity:",
      vehicle_capacity, "kg")

# Display DP Table
print("\n===== DP TABLE =====")

for row in dp_table:
    print(row)





# PHASE 3 - PART A: DIJKSTRA ALGORITHM

import heapq


def dijkstra(graph, start):

    # Initially, all distances are infinity
    distances = {}

    for location in graph:
        distances[location] = float('inf')

    # Starting location has distance zero
    distances[start] = 0

    # Store the previous location for path reconstruction
    previous = {}

    # Priority queue: (distance, location)
    priority_queue = [(0, start)]

    while priority_queue:

        current_distance, current = heapq.heappop(
            priority_queue
        )

        # Skip already processed entries
        if current_distance > distances[current]:
            continue

        # Check neighbouring locations
        for neighbour, weight in graph[current].items():

            new_distance = current_distance + weight

            # Update if a shorter path is found
            if new_distance < distances[neighbour]:

                distances[neighbour] = new_distance
                previous[neighbour] = current

                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbour)
                )

    return distances, previous


# Function to reconstruct shortest path
def get_path(previous, destination):

    path = []
    current = destination

    while current in previous:
        path.append(current)
        current = previous[current]

    path.append("Warehouse")
    path.reverse()

    return path


# Run Dijkstra from Warehouse
distances, previous = dijkstra(graph, "Warehouse")

print("\n===== DIJKSTRA SHORTEST PATHS =====")

for location in graph:

    if location == "Warehouse":
        continue

    path = get_path(previous, location)

    print("\nDestination:", location)
    print("Shortest Path:", " -> ".join(path))
    print("Distance:", distances[location], "km")


# PHASE 3 - PART B: NEAREST NEIGHBOR TSP

def nearest_neighbor_tsp(graph, start):

    # All locations that need to be visited
    unvisited = set(graph.keys())

    # Remove starting location from delivery locations
    unvisited.remove(start)

    # Current location
    current = start

    # Store delivery route
    route = [start]

    total_distance = 0

    while unvisited:

        # Calculate shortest distances from current location
        distances, previous = dijkstra(graph, current)

        # Find nearest unvisited location
        next_location = min(
            unvisited,
            key=lambda location: distances[location]
        )

        # Add distance to total
        total_distance += distances[next_location]

        # Move to next location
        current = next_location

        route.append(current)

        # Mark location as visited
        unvisited.remove(current)

    # Return to Warehouse
    distances, previous = dijkstra(graph, current)

    total_distance += distances[start]

    route.append(start)

    return route, total_distance


# Run TSP
delivery_route, route_distance = nearest_neighbor_tsp(
    graph, "Warehouse"
)

print("\n===== NEAREST NEIGHBOR TSP =====")

print("Delivery Route:")

print(" -> ".join(delivery_route))

print("Total Route Distance:", route_distance, "km")






# # PHASE 4 - PERFORMANCE TESTING

import time

# Measure Merge Sort execution time

start_time = time.perf_counter()

sorted_parcels = merge_sort(parcels)

end_time = time.perf_counter()

merge_sort_time = end_time - start_time

print("\n===== PERFORMANCE ANALYSIS =====")

print("Merge Sort Execution Time:",
      merge_sort_time, "seconds")


# Generate sample parcels for testing

def generate_parcels(n):

    test_data = []

    priorities = ["High", "Medium", "Low"]

    for i in range(n):

        parcel = {
            "id": "P" + str(i),
            "destination": "A",
            "weight": (i % 10) + 1,
            "value": (i % 100) + 10,
            "priority": priorities[i % 3]
        }

        test_data.append(parcel)

    return test_data


# Test different input sizes

sizes = [10, 100, 500, 1000]

print("\n===== MERGE SORT COMPARISON =====")

for size in sizes:

    test_data = generate_parcels(size)

    start = time.perf_counter()

    merge_sort(test_data)

    end = time.perf_counter()

    print(
        "Parcels:", size,
        "| Time:", end - start,
        "seconds"
    )


# KNAPSACK PERFORMANCE TESTING

print("\n===== KNAPSACK PERFORMANCE =====")

sizes = [10, 50, 100, 200]

for size in sizes:

    test_data = generate_parcels(size)

    start = time.perf_counter()

    knapsack(test_data, 100)

    end = time.perf_counter()

    print(
        "Parcels:", size,
        "| Time:", end - start,
        "seconds"
    )


# # PERFORMANCE GRAPH

import matplotlib.pyplot as plt

sizes = [10, 100, 500, 1000]

merge_times = []

for size in sizes:

    test_data = generate_parcels(size)

    start = time.perf_counter()

    merge_sort(test_data)

    end = time.perf_counter()

    merge_times.append(end - start)


# Draw graph
plt.plot(
    sizes,
    merge_times,
    marker='o',
    label='Merge Sort'
)

plt.xlabel("Number of Parcels")
plt.ylabel("Execution Time (seconds)")

plt.title("Merge Sort Performance Analysis")

plt.legend()
plt.grid(True)

plt.savefig("performance_chart.png")

plt.show()



# -----------------------------------------
# PHASE 4 - DIJKSTRA PERFORMANCE TESTING
# -----------------------------------------

print("\n===== DIJKSTRA PERFORMANCE =====")

dijkstra_times = []

for i in range(3):
    start = time.perf_counter()

    dijkstra(graph, "Warehouse")

    end = time.perf_counter()

    dijkstra_times.append(end - start)

dijkstra_avg = sum(dijkstra_times) / len(dijkstra_times)

print("Number of Locations:", len(graph))
print("Average Dijkstra Time:", dijkstra_avg, "seconds")


# -----------------------------------------
# PHASE 4 - TSP PERFORMANCE TESTING
# -----------------------------------------

print("\n===== TSP PERFORMANCE =====")

tsp_times = []

for i in range(3):
    start = time.perf_counter()

    nearest_neighbor_tsp(graph, "Warehouse")

    end = time.perf_counter()

    tsp_times.append(end - start)

tsp_avg = sum(tsp_times) / len(tsp_times)

print("Number of Locations:", len(graph))
print("Average TSP Time:", tsp_avg, "seconds")


# -----------------------------------------
# PHASE 4 - COMBINED PERFORMANCE GRAPH
# -----------------------------------------

algorithms = [
    "Merge Sort",
    "Dijkstra",
    "Nearest Neighbor TSP"
]

execution_times = [
    merge_sort_time,
    dijkstra_avg,
    tsp_avg
]

plt.figure(figsize=(8, 5))

plt.bar(algorithms, execution_times)

plt.xlabel("Algorithms")
plt.ylabel("Execution Time (seconds)")
plt.title("Courier Planner Algorithm Performance")

plt.xticks(rotation=15)
plt.grid(axis="y")

plt.tight_layout()

plt.savefig("combined_performance.png")

plt.show()

print("\nAll Performance Testing Completed!")
