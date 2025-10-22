"""
TSP Solver Module
Berisi implementasi berbagai algoritma heuristik untuk Traveling Salesman Problem
"""

import math
import random
import copy

# --- 0. Pembuatan Data dan Fungsi Helper ---

def generate_cities(num_cities, max_x=1000, max_y=1000):
    """Membuat kamus data kota secara acak."""
    data = {}
    for i in range(1, num_cities + 1):
        data[i] = {
            'X': random.randint(0, max_x),
            'Y': random.randint(0, max_y)
        }
    return data

def calculate_distance(city1_id, city2_id, data):
    """Menghitung jarak Euclidean antara dua kota."""
    try:
        coord1 = data[city1_id]
        coord2 = data[city2_id]
        return math.sqrt((coord1['X'] - coord2['X'])**2 + (coord1['Y'] - coord2['Y'])**2)
    except KeyError:
        return float('inf')

def precompute_distances(cities_list, data):
    """Membuat matriks (kamus) jarak untuk pencarian cepat."""
    dist_matrix = {c1: {} for c1 in cities_list}
    for c1 in cities_list:
        for c2 in cities_list:
            dist = calculate_distance(c1, c2, data)
            dist_matrix[c1][c2] = dist
            dist_matrix[c2][c1] = dist
    return dist_matrix

def calculate_tour_distance(tour, dist_matrix):
    """Menghitung total jarak dari sebuah tur (daftar ID kota)."""
    if not tour:
        return 0
    distance = 0
    for i in range(len(tour)):
        c1 = tour[i]
        c2 = tour[(i + 1) % len(tour)]
        distance += dist_matrix[c1][c2]
    return distance

# --- 1. Nearest Neighbor (NN) ---

def nearest_neighbor(start_node, cities_list, dist_matrix):
    """Membangun tur menggunakan Nearest Neighbor dari satu titik awal."""
    unvisited = set(cities_list)
    current_city = start_node
    tour = [current_city]
    unvisited.remove(current_city)
    
    while unvisited:
        nearest_city = min(unvisited, key=lambda city: dist_matrix[current_city][city])
        tour.append(nearest_city)
        unvisited.remove(nearest_city)
        current_city = nearest_city
        
    return tour

def solve_nn_all_starts(cities_list, dist_matrix):
    """Menjalankan Nearest Neighbor dari semua titik awal dan mengembalikan yang terbaik."""
    best_tour = []
    min_distance = float('inf')
    
    for start_node in cities_list:
        tour = nearest_neighbor(start_node, cities_list, dist_matrix)
        distance = calculate_tour_distance(tour, dist_matrix)
        if distance < min_distance:
            min_distance = distance
            best_tour = tour
            
    return best_tour, min_distance

# --- 2. Insertion Heuristics (General) ---

def find_best_insertion(subtour, node_to_insert, dist_matrix):
    """Menemukan posisi penyisipan termurah untuk sebuah node ke dalam subtour."""
    min_cost = float('inf')
    best_position = -1
    
    for i in range(len(subtour)):
        c1 = subtour[i]
        c2 = subtour[(i + 1) % len(subtour)]
        
        cost = dist_matrix[c1][node_to_insert] + dist_matrix[node_to_insert][c2] - dist_matrix[c1][c2]
        
        if cost < min_cost:
            min_cost = cost
            best_position = i + 1
            
    return best_position, min_cost

# --- 2a. Nearest Insertion (NI) ---

def select_initial_nearest(start_node, unvisited, dist_matrix):
    """Pilih kota terdekat dari start_node untuk memulai subtour."""
    return min(unvisited, key=lambda r: dist_matrix[start_node][r])

def select_nearest(subtour, unvisited, dist_matrix):
    """Temukan node r (belum di tur) terdekat dengan node j (di dalam tur)."""
    min_dist = float('inf')
    best_node = -1
    for r in unvisited:
        for j in subtour:
            dist = dist_matrix[r][j]
            if dist < min_dist:
                min_dist = dist
                best_node = r
    return best_node

# --- 2b. Farthest Insertion (FI) ---

def select_initial_farthest(start_node, unvisited, dist_matrix):
    """Pilih kota terjauh dari start_node untuk memulai subtour."""
    return max(unvisited, key=lambda k: dist_matrix[start_node][k])

def select_farthest(subtour, unvisited, dist_matrix):
    """Pilih node k yang jarak minimumnya ke subtour adalah yang terbesar."""
    best_node = -1
    max_of_min_dists = -1
    for k in unvisited:
        min_dist_to_subtour = min(dist_matrix[k][j] for j in subtour)
        if min_dist_to_subtour > max_of_min_dists:
            max_of_min_dists = min_dist_to_subtour
            best_node = k
    return best_node

# --- 2c. Arbitrary Insertion (AI) ---

def select_initial_arbitrary(start_node, unvisited, dist_matrix):
    """Pilih kota secara acak untuk memulai subtour."""
    return random.choice(list(unvisited))

def select_arbitrary(subtour, unvisited, dist_matrix):
    """Pilih kota secara acak dari yang belum dikunjungi."""
    return random.choice(list(unvisited))

# --- Generic Insertion Solver ---

def generic_insertion(start_node, cities_list, dist_matrix, initial_select_func, select_func):
    """Algoritma penyisipan generik yang mengambil fungsi seleksi."""
    unvisited = set(cities_list)
    subtour = [start_node]
    unvisited.remove(start_node)
    
    if not unvisited:
        return subtour
        
    second_node = initial_select_func(start_node, unvisited, dist_matrix)
    subtour.append(second_node)
    unvisited.remove(second_node)
    
    while unvisited:
        node_to_insert = select_func(subtour, unvisited, dist_matrix)
        if node_to_insert is None:
            break
            
        position, cost = find_best_insertion(subtour, node_to_insert, dist_matrix)
        subtour.insert(position, node_to_insert)
        unvisited.remove(node_to_insert)
        
    return subtour

def solve_insertion_all_starts(cities_list, dist_matrix, strategy, num_runs=1):
    """Wrapper untuk menjalankan NI, FI, AI dari semua titik awal."""
    strategy_map = {
        'nearest': (select_initial_nearest, select_nearest),
        'farthest': (select_initial_farthest, select_farthest),
        'arbitrary': (select_initial_arbitrary, select_arbitrary)
    }
    initial_func, select_func = strategy_map[strategy]
    
    best_tour = []
    min_distance = float('inf')
    
    total_runs = num_runs if strategy == 'arbitrary' else 1
    
    for start_node in cities_list:
        for _ in range(total_runs):
            tour = generic_insertion(start_node, cities_list, dist_matrix, initial_func, select_func)
            distance = calculate_tour_distance(tour, dist_matrix)
            if distance < min_distance:
                min_distance = distance
                best_tour = tour
                
    return best_tour, min_distance

# --- 2d. Cheapest Insertion (CI) ---

def cheapest_insertion(start_node, cities_list, dist_matrix):
    """Implementasi Cheapest Insertion."""
    unvisited = set(cities_list)
    subtour = [start_node]
    unvisited.remove(start_node)
    
    if not unvisited:
        return subtour
        
    second_node = min(unvisited, key=lambda k: dist_matrix[start_node][k])
    subtour.append(second_node)
    unvisited.remove(second_node)
    
    while unvisited:
        overall_best_node = -1
        overall_best_pos = -1
        overall_min_cost = float('inf')
        
        for k in unvisited:
            position, cost = find_best_insertion(subtour, k, dist_matrix)
            if cost < overall_min_cost:
                overall_min_cost = cost
                overall_best_node = k
                overall_best_pos = position
                
        if overall_best_node != -1:
            subtour.insert(overall_best_pos, overall_best_node)
            unvisited.remove(overall_best_node)
        else:
            break
            
    return subtour

def solve_ci_all_starts(cities_list, dist_matrix):
    """Wrapper untuk menjalankan Cheapest Insertion dari semua titik awal."""
    best_tour = []
    min_distance = float('inf')
    
    for start_node in cities_list:
        tour = cheapest_insertion(start_node, cities_list, dist_matrix)
        distance = calculate_tour_distance(tour, dist_matrix)
        if distance < min_distance:
            min_distance = distance
            best_tour = tour
            
    return best_tour, min_distance

# --- 3. 3-Opt Improvement Heuristic ---

def three_opt(initial_tour, dist_matrix):
    """
    Memperbaiki tur menggunakan 3-Opt.
    Mencoba 7 kemungkinan pembalikan segmen untuk setiap 3 pemutusan.
    Menggunakan strategi 'first improvement'.
    """
    best_tour = copy.deepcopy(initial_tour)
    n = len(best_tour)
    improved = True
    
    while improved:
        improved = False
        best_distance = calculate_tour_distance(best_tour, dist_matrix)
        
        for i in range(0, n - 3):
            for j in range(i + 1, n - 2):
                for k in range(j + 1, n - 1):
                    if improved:
                        break
                    
                    # Ambil segmen-segmen
                    S1 = best_tour[0:i+1]
                    S2 = best_tour[i+1:j+1]
                    S3 = best_tour[j+1:k+1]
                    S4 = best_tour[k+1:n]
                    
                    S2_rev = S2[::-1]
                    S3_rev = S3[::-1]
                    
                    # 7 kemungkinan rekoneksi
                    candidates = [
                        S1 + S2 + S3_rev + S4,
                        S1 + S2_rev + S3 + S4,
                        S1 + S2_rev + S3_rev + S4,
                        S1 + S3 + S2 + S4,
                        S1 + S3_rev + S2 + S4,
                        S1 + S3 + S2_rev + S4,
                        S1 + S3_rev + S2_rev + S4
                    ]
                    
                    for new_tour in candidates:
                        new_dist = calculate_tour_distance(new_tour, dist_matrix)
                        if new_dist < best_distance - 1e-9:
                            best_tour = new_tour
                            best_distance = new_dist
                            improved = True
                            break
                    
                    if improved:
                        break
                if improved:
                    break
            if improved:
                break
            
    return best_tour, calculate_tour_distance(best_tour, dist_matrix)


# --- 4. Fungsi Utilitas untuk Streamlit ---

def validate_cities_data(data):
    """Validasi format data kota."""
    if not isinstance(data, dict):
        return False, "Data harus berupa dictionary"
    
    for city_id, coords in data.items():
        if not isinstance(coords, dict):
            return False, f"Koordinat kota {city_id} harus berupa dictionary"
        if 'X' not in coords or 'Y' not in coords:
            return False, f"Koordinat kota {city_id} harus memiliki 'X' dan 'Y'"
        try:
            float(coords['X'])
            float(coords['Y'])
        except (ValueError, TypeError):
            return False, f"Koordinat kota {city_id} harus berupa angka"
    
    return True, "Valid"

def export_results_to_csv(results):
    """Export hasil ke format CSV."""
    import pandas as pd
    df = pd.DataFrame([
        {k: v for k, v in r.items() if k != 'Tour'}
        for r in results
    ])
    return df.to_csv(index=False)