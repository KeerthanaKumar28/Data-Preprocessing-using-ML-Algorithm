import random
import ast
import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Generate a random solution
def randomSolution(tsp):
    cities = list(range(len(tsp)))
    solution = []
    for _ in range(len(tsp)):
        randomCity = cities[random.randint(0, len(cities) - 1)]
        solution.append(randomCity)
        cities.remove(randomCity)
    return solution

# Calculate route length
def routelength(tsp, solution):
    length = 0
    for i in range(len(solution)):
        length += tsp[solution[i - 1]][solution[i]]
    return length

# Generate neighbours
def getNeighbour(solution):
    neighbours = []
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            neighbour = solution.copy()
            neighbour[i], neighbour[j] = neighbour[j], neighbour[i]
            neighbours.append(neighbour)
    return neighbours

# Get best neighbour
def getBestNeighbours(tsp, neighbours):
    bestRouteLength = routelength(tsp, neighbours[0])
    bestNeighbour = neighbours[0]
    for neighbour in neighbours:
        currentRouteLength = routelength(tsp, neighbour)
        if currentRouteLength < bestRouteLength:
            bestRouteLength = currentRouteLength
            bestNeighbour = neighbour
    return bestNeighbour, bestRouteLength

# Hill climbing algorithm
def hill_climbing(tsp, initial_solution):
    current_solution = initial_solution
    current_length = routelength(tsp, current_solution)
    route_lengths = []
    while True:
        neighbours = getNeighbour(current_solution)
        bestNeighbour, bestRouteLength = getBestNeighbours(tsp, neighbours)
        route_lengths.append(bestRouteLength)
        if bestRouteLength >= current_length:
            break
        current_solution = bestNeighbour
        current_length = bestRouteLength
    return current_solution, current_length, route_lengths

# Plot TSP solution
def plot_tsp_solution(tsp, solution, coordinates):
    plt.figure(figsize=(10, 6))
    x = [coordinates[i][0] for i in solution]
    y = [coordinates[i][1] for i in solution]
    plt.plot(x + [x[0]], y + [y[0]], 'bo-', markersize=6)
    for i, coord in enumerate(coordinates):
        plt.text(coord[0], coord[1], str(i), fontsize=12, color='red')
    plt.title("TSP Path Visualization")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True)
    st.pyplot(plt)

# Plot violin plot
def plot_violin(route_lengths):
    plt.figure(figsize=(10, 6))
    sns.violinplot(data=route_lengths, inner="quart")
    plt.title("Distribution of Route Lengths")
    plt.ylabel("Route Length")
    st.pyplot(plt)

# Plot bar plot
def plot_bar(initial_length, optimized_length):
    plt.figure(figsize=(10, 6))
    plt.bar(["Initial Route Length", "Optimized Route Length"], [initial_length, optimized_length], color=['skyblue', 'green'])
    plt.title("Comparison of Route Lengths")
    plt.ylabel("Route Length")
    plt.grid(axis='y')
    st.pyplot(plt)

# Generate random coordinates for cities
def generate_random_coordinates(num_cities):
    return [(random.randint(0, 100), random.randint(0, 100)) for _ in range(num_cities)]

# Set a background image
def set_background(url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url({url}) no-repeat center center fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Main Streamlit app
def main():
    st.title("Travelling Salesman Problem - Hill Climbing")

    # Set background image
    set_background("https://img.freepik.com/free-vector/pastel-coloured-hand-painted-alcohol-ink-background_1048-19853.jpg")

    # Input TSP distance matrix
    tsp_input = st.text_area("Enter the distance matrix (e.g., [[0, 400, 500], [400, 0, 300], [500, 300, 0]])")

    if st.button("Generate and Visualize Solution"):
        try:
            tsp = ast.literal_eval(tsp_input)
            if not isinstance(tsp, list) or not all(isinstance(row, list) for row in tsp):
                raise ValueError("Input must be a 2D list.")

            # Generate random coordinates for cities
            coordinates = generate_random_coordinates(len(tsp))

            # Generate initial random solution
            initial_solution = randomSolution(tsp)
            initial_length = routelength(tsp, initial_solution)
            st.write(f"**Initial Random Solution:** {initial_solution}")
            st.write(f"**Initial Route Length:** {initial_length}")

            # Perform hill climbing
            solution, length, route_lengths = hill_climbing(tsp, initial_solution)
            st.write(f"**Best Solution after Hill Climbing:** {solution}")
            st.write(f"**Best Route Length:** {length}")

            # Visualize solution
            plot_tsp_solution(tsp, solution, coordinates)

            # Visualize distribution of route lengths (violin plot)
            plot_violin(route_lengths)

            # Visualize comparison of initial and optimized lengths (bar plot)
            plot_bar(initial_length, length)
        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
