import matplotlib.pyplot as plt
from sklearn.manifold import MDS
import numpy as np
from numpy import sqrt
import time

distance_matrix = np.array([
    [0,   45,  60, 110, 280, 300, 420, 460, 350, 150],
    [45,   0,  50,  90, 260, 280, 400, 440, 330, 130],
    [60,  50,   0,  70, 240, 260, 380, 420, 310, 110],
    [110, 90,  70,   0, 200, 220, 340, 380, 270,  90],
    [280,260, 240, 200,   0, 180, 160, 220, 180, 170],
    [300,280, 260, 220, 180,   0, 240, 280, 230, 190],
    [420,400, 380, 340, 160, 240,   0, 160, 150, 290],
    [460,440, 420, 380, 220, 280, 160,   0, 100, 330],
    [350,330, 310, 270, 180, 230, 150, 100,   0, 220],
    [150,130, 110,  90, 170, 190, 290, 330, 220,   0]
])

def generate_coordinates_from_distance_matrix(distance_matrix):
    distance_matrix = (distance_matrix + distance_matrix.T) / 2
    np.fill_diagonal(distance_matrix, 0)
    mds = MDS(dissimilarity='precomputed', random_state=42)
    coordinates = mds.fit_transform(distance_matrix)
    return coordinates[:, 0], coordinates[:, 1]

X, Y = generate_coordinates_from_distance_matrix(distance_matrix)
n = len(X)

def calculate_path_length(path, X, Y):
    length = 0.0
    for i in range(len(path) - 1):
        length += sqrt((X[path[i]] - X[path[i+1]])**2 + (Y[path[i]] - Y[path[i+1]])**2)
    length += sqrt((X[path[-1]] - X[path[0]])**2 + (Y[path[-1]] - Y[path[0]])**2)
    return length

def greedy_tsp(X, Y, start_city=0):
    n = len(X)
    path = [start_city]
    unvisited = set(range(n)) - {start_city}
    while unvisited:
        last_city = path[-1]
        nearest_city = min(unvisited, key=lambda city: sqrt((X[last_city] - X[city])**2 + (Y[last_city] - Y[city])**2))
        path.append(nearest_city)
        unvisited.remove(nearest_city)
    return path

def two_opt_swap(path, X, Y, max_iterations=1000):
    improved = True
    iteration = 0
    best_path = path.copy()
    best_length = calculate_path_length(best_path, X, Y)
    n = len(path)
    
    while improved and iteration < max_iterations:
        improved = False
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                new_path = best_path[:i] + best_path[i:j][::-1] + best_path[j:]
                new_length = calculate_path_length(new_path, X, Y)
                if new_length < best_length:
                    best_path = new_path
                    best_length = new_length
                    improved = True
        iteration += 1
    return best_path

ib = 0
start_time = time.time()

initial_path = greedy_tsp(X, Y, ib)
optimized_path = two_opt_swap(initial_path, X, Y)
S = calculate_path_length(optimized_path, X, Y)
end_time = time.time()

plt.figure(figsize=(12, 8))
cities = [
    "Брест", "Кобрин", "Батчи", "Берёза", "Малорита", "Лида", "Орша", "Речица", "Дрогичин", "Ивацевичи"
]

for i, city in enumerate(cities):
    plt.text(X[i], Y[i], city, fontsize=10, ha='center', va='bottom')

optimized_path.append(optimized_path[0])
plt.plot(X[optimized_path], Y[optimized_path], 'b-', marker='o', markersize=8, linewidth=1.5, label=f"Оптимизированный путь: {S:.1f} км")
plt.scatter(X, Y, c='red', s=100)

plt.title(f"Решение задачи коммивояжера для {n} городов\nВремя работы: {end_time - start_time:.2f} сек.")
plt.legend(loc="upper left")
plt.grid(True)
plt.axis('equal')
plt.show()

# pip install virtualenv
# python -m venv venv
# Windows: venv\Scripts\activate
# MacOS: source venv/bin/activate
# pip install -r requirements.txt