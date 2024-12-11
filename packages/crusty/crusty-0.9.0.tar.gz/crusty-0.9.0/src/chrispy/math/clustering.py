
import numpy as np
import os

from sklearn.cluster import KMeans, DBSCAN, OPTICS
from sklearn.metrics import silhouette_samples, silhouette_score

def kmeans(data: list[np.ndarray],
           n_clusters: int | list[int]):
    
    if isinstance(n_clusters, int): n_clusters = [n_clusters]#

    print(f'\nCompute kmeans clusters (N = {n_clusters})...\n')
    
    data_stacked = np.stack(data, axis = -1)
    data_valid = ~np.isnan(data_stacked)

    mask = np.all(data_valid, axis = -1)

    data_masked = data_stacked[mask]
    
    labels = []
    centroids = []
    scores = []

    for i, nc in enumerate(n_clusters):

        kmeans = KMeans(n_clusters = nc)
        labels.append(kmeans.fit_predict(data_masked))
        centroids.append(kmeans.cluster_centers_)

        scores.append(silhouette_score(data_masked, 
                                        labels[i]))
            
        print(f'\nFor n_clusters = {nc}, silhouette score is {scores[i]}...\n')
    
    i_opt = np.argmax(scores)
    
    labels_opt = labels[i_opt]
    centroids_opt = centroids[i_opt]
    scores_opt = scores[i_opt]

    return labels_opt, centroids_opt, scores_opt


def dbscan(data: list[np.ndarray],
           weights: np.ndarray | None = None,
           **kwargs):
    
    from joblib import effective_n_jobs

    print(f'\nCompute DBscan clusters')
    print(f'with {effective_n_jobs(-1)} cpus...\n')

    shape = data[0].shape

    if weights is None: weights = np.ones(shape)

    data.append(weights)

    data_stacked = np.stack(data, 
                            axis = -1)
    
    data_valid = ~np.isnan(data_stacked)

    mask = np.all(data_valid, axis = -1)

    data_masked = data_stacked[mask]

    print(f'\nNumber of points:')
    print(f'{data_masked.shape[0]}\n')
    print(f'\nNumber of features:') 
    print(f'{data_masked.shape[1]-1}\n')

    clusterer = DBSCAN(**kwargs, n_jobs = -1)
        
    labels = clusterer.fit_predict(data_masked[:, :-1],
                                   sample_weight = data_masked[:, -1])
    
    array_r = np.zeros(shape)
    array_r[:] = np.nan
    array_r[mask] = labels

    return array_r


def optics(data: list[np.ndarray],
           **kwargs):
    
    from joblib import effective_n_jobs, parallel_config
    from dask_jobqueue import SLURMCluster
    from dask.distributed import Client
    
    #cluster = SLURMCluster(processes = 1, cores = 128, memory = '1GB')
    #client = Client(cluster)

    print(f'\nCompute DBscan clusters')
    print(f'with {effective_n_jobs(-1)} cpus...\n')

    shape = data[0].shape
    
    data_stacked = np.stack(data, axis = -1)
    data_valid = ~np.isnan(data_stacked)

    mask = np.all(data_valid, axis = -1)

    data_masked = data_stacked[mask]

    print(f'\nNumber of points:')
    print(f'{data_masked.shape[0]}\n')
    print(f'\nNumber of features:') 
    print(f'{data_masked.shape[1]}\n')

    clusterer = OPTICS(**kwargs, n_jobs = -1)

    #with parallel_config('dask', n_jobs = -1):
        
    labels = clusterer.fit_predict(data_masked)
    
    array_r = np.zeros(shape)
    array_r[:] = np.nan
    array_r[mask] = labels

    return array_r


def hp_dbscan(file: os.PathLike,
              dataset: str,
              dir_build: os.PathLike,
              epsilon: float,
              min_points: int):
    
    import subprocess
    #import sys
    #sys.path.append(dir_build)
    #
    #import hpdbscan
    #import h5py

    #print(f'\nCompute DBSCAN clusters')
    #print(f'in highly parallel fashion...\n')

    #clusterer = hpdbscan.HPDBSCAN(epsilon = epsilon,
    #                              min_points = min_points)
    #
    #labels = clusterer.cluster(file, dataset)


    command = ' '.join([
              f'srun',
              '-n', '128',
              f'{dir_build}/hpdbscan',
              '-t', '128',
              '-m', f'{min_points}',
              '-e', f'{epsilon}',
              '-i', f'{file}',
              '-o', f'{file}',
              '--input-dataset',
              f'{dataset}',
              '--output-dataset',
              f'CLUSTERS'])

    print('\nExecute:')
    print(f'\n{command}\n')

    subprocess.call(command, shell = True)

    print(f'\nDone!\n')
