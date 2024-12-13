import numpy as np

def pairwise_distances_raw(points):
    n = points.shape[0]
    distances = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            distances[i, j] = np.sqrt(np.sum((points[i] - points[j]) ** 2))
    return distances

def pairwise_distances_np(points):
    squared_diff = np.sum((points[:, np.newaxis, :] - points[np.newaxis, :, :]) ** 2, axis=-1)
    return np.sqrt(squared_diff)

def add_one(points):
    return points + 1
