import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, DBSCAN

#load datasets
datasets = {}
filenames = ['noisy_circles.txt', 'noisy_moons.txt', 'blobs.txt', 'aniso.txt', 'no_structure.txt']
for file in filenames:
    data = np.loadtxt(f'Task3/{file}')
    datasets[file.split('.')[0]] = data

#scatterplots to visualize datasets
fig, axes = plt.subplots(1, 5, figsize=(20, 4))
for ax, (name, data) in zip(axes, datasets.items()):
    ax.scatter(data[:, 0], data[:, 1], s=10)
    ax.set_title(name)
plt.suptitle('Original Datasets')
plt.show()

#K-Means clustering and visualization
kmeans_clusters = {
    'noisy_circles': 2,
    'noisy_moons': 2,
    'blobs': 3,
    'aniso': 3,
    'no_structure': 3
}

fig, axes = plt.subplots(1, 5, figsize=(20, 4))
for ax, (name, data) in zip(axes, datasets.items()):
    kmeans = KMeans(n_clusters=kmeans_clusters[name], random_state=0)
    labels = kmeans.fit_predict(data)
    ax.scatter(data[:, 0], data[:, 1], c=labels, cmap='viridis', s=10)
    ax.set_title(f'K-Means: {name}')
plt.suptitle('K-Means Clustering Results')
plt.show()

#DBSCAN clustering and visualization
#set custom eps values for different datasets
dbscan_params = {
    'noisy_circles': {'eps': 0.2, 'min_samples': 5},
    'noisy_moons': {'eps': 0.2, 'min_samples': 5},
    'blobs': {'eps': 0.3, 'min_samples': 5},
    'aniso': {'eps': 0.3, 'min_samples': 5},
    'no_structure': {'eps': 0.3, 'min_samples': 5}
}

fig, axes = plt.subplots(1, 5, figsize=(20, 4))
for ax, (name, data) in zip(axes, datasets.items()):
    params = dbscan_params[name]
    db = DBSCAN(eps=params['eps'], min_samples=params['min_samples'])
    labels = db.fit_predict(data)
    ax.scatter(data[:, 0], data[:, 1], c=labels, cmap='plasma', s=10)
    ax.set_title(f'DBSCAN: {name}')
plt.suptitle('DBSCAN Clustering Results')
plt.show()
