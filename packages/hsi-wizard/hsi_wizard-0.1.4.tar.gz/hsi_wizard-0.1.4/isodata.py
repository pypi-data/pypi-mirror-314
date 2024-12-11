#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2012 - 2013
# Matías Herranz <matiasherranz@gmail.com>
# Joaquín Tita <joaquintita@gmail.com>
#
# https://github.com/PyRadar/pyradar/blob/master/pyradar/classifiers/isodata.py
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.

import numpy as np
from scipy.cluster import vq
from typing import Tuple


def quit_low_change_in_clusters(centers: np.ndarray, last_centers: np.ndarray, theta_o: float) -> bool:
    """Stop algorithm by low change in the clusters values between each iteration.

    :param centers: Cluster centers
    :param last_centers: Last cluster centers
    :param theta_o: threshold change in the clusters between each iter
    :return: True if it should stop, otherwise False.
    """
    qt = False
    if centers.shape == last_centers.shape:
        thresholds = np.abs((centers - last_centers) / (last_centers + 1))

        if np.all(thresholds <= theta_o):  # percent of change in [0:1]
            qt = True

    return qt


def discard_clusters(img_class_flat: np.ndarray,
                     centers: np.ndarray,
                     clusters_list: np.ndarray,
                     theta_m: int) -> Tuple[np.ndarray, np.ndarray, int]:
    """Discard clusters with fewer than theta_m.

    :param img_class_flat: Classes of the flatten image
    :param centers: Cluster centers
    :param clusters_list: List of clusters
    :param theta_m: threshold value for min number in each cluster
    :return: Tuple of the new cluster centers, a list of the new clusters and a new value for k_
    """
    k_ = centers.shape[0]
    to_delete = np.array([])
    assert centers.shape[0] == clusters_list.size, \
        "ERROR: discard_cluster() centers and clusters_list size are different"
    for cluster in range(k_):
        indices = np.where(img_class_flat == clusters_list[cluster])[0]
        total_per_cluster = indices.size
        if total_per_cluster <= theta_m:
            to_delete = np.append(to_delete, cluster)

    if to_delete.size:
        to_delete = np.array(to_delete, dtype=int)
        new_centers = np.delete(centers, to_delete, axis=0)
        new_clusters_list = np.delete(clusters_list, to_delete)
    else:
        new_centers = centers
        new_clusters_list = clusters_list

    # new_centers, new_clusters_list = sort_arrays_by_first(new_centers, new_clusters_list)
    assert new_centers.shape[0] == new_clusters_list.size, \
        "ERROR: discard_cluster() centers and clusters_list size are different"

    return new_centers, new_clusters_list, k_


def update_clusters(img_flat: np.ndarray,
                    img_class_flat: np.ndarray,
                    centers: np.ndarray,
                    clusters_list: np.ndarray) -> Tuple[np.ndarray, np.ndarray, int]:
    """Update clusters.

    :param img_flat: Flatten image
    :param img_class_flat: Classes of the flatten image
    :param centers: Cluster centers
    :param clusters_list: List of clusters
    :return: Tuple of the new cluster centers, a list of the new clusters and a new value for k_
    """
    k_ = centers.shape[0]
    new_centers = np.zeros((k_, img_flat.shape[1]))
    new_clusters_list = np.array([])

    assert centers.shape[0] == clusters_list.size, \
        "ERROR: update_clusters() centers and clusters_list size are different"

    for cluster in range(k_):
        indices = np.where(img_class_flat == clusters_list[cluster])[0]
        # get whole cluster
        cluster_values = img_flat[indices, :]
        new_cluster = cluster_values.mean(axis=0)
        new_centers[cluster, :] = new_cluster
        new_clusters_list = np.append(new_clusters_list, cluster)

    new_centers, new_clusters_list = sort_arrays_by_first(new_centers, new_clusters_list)

    assert new_centers.shape[0] == new_clusters_list.size, \
        "ERROR: update_clusters() centers and clusters_list size are different"

    return new_centers, new_clusters_list, k_


def initial_clusters(img_flat: np.ndarray, k_: int, method: str = "linspace") -> np.ndarray | None:
    """Define initial clusters centers as startup.

    By default, the method is "linspace". Other method available is "random".

    :param img_flat: Flatten image
    :param k_:
    :param method: Method for initially defining cluster centers
    :return: Initial cluster centers
    """
    methods_available = ["linspace", "random"]
    v = img_flat.shape[1]
    assert method in methods_available, f"ERROR: method {method} is not valid."
    if method == "linspace":
        maximum, minimum = img_flat.max(axis=0), img_flat.min(axis=0)
        centers = np.array([np.linspace(minimum[i], maximum[i], k_) for i in range(v)]).T
    elif method == "random":
        start, end = 0, img_flat.shape[0]
        indices = np.random.randint(start, end, k_)
        centers = img_flat[indices]
    else:
        return None

    return centers


def sort_arrays_by_first(centers: np.ndarray, clusters_list: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Sort the array 'centers' and with the indices of the sorted centers order the array 'clusters_list'.

    Example: centers=[22, 33, 0, 11] and cluster_list=[7,6,5,4]
    returns  (array([ 0, 11, 22, 33]), array([5, 4, 7, 6]))

    :param centers: Cluster centers
    :param clusters_list: List of clusters
    :return: Tuple of the sorted centers and the sorted cluster list
    """
    assert centers.shape[0] == clusters_list.size, \
        "ERROR: sort_arrays_by_first centers and clusters_list size are not equal"

    indices = np.argsort(centers[:, 0])

    sorted_centers = centers[indices, :]
    sorted_clusters_list = clusters_list[indices]

    return sorted_centers, sorted_clusters_list


# Todos
def split_clusters(img_flat: np.ndarray,
                   img_class_flat: np.ndarray,
                   centers: np.ndarray,
                   clusters_list: np.ndarray,
                   theta_s: float,
                   theta_m: int) -> Tuple[np.ndarray, np.ndarray, int]:
    """Split clusters to form new clusters.

    :param img_flat: Flatten image
    :param img_class_flat: Classes of the flatten image
    :param centers: Cluster centers
    :param clusters_list: List of clusters
    :param theta_s: threshold value for standard deviation (for split)
    :param theta_m: threshold value for min number in each cluster
    :return: Tuple of the new cluster centers, a list of the new clusters and a new value for k_
    """
    assert centers.shape[0] == clusters_list.size, "ERROR: split() centers and clusters_list size are different"

    delta = 10
    k_ = centers.shape[0]
    count_per_cluster = np.zeros(k_)
    stddev = np.array([])

    avg_dists_to_clusters, k_ = compute_avg_distance(img_flat, img_class_flat, centers, clusters_list)
    d, k_ = compute_overall_distance(img_class_flat, avg_dists_to_clusters, clusters_list)

    # compute all the standard deviation of the clusters
    for cluster in range(k_):
        indices = np.where(img_class_flat == clusters_list[cluster])[0]
        count_per_cluster[cluster] = indices.size
        value = ((img_flat[indices] - centers[cluster]) ** 2).sum()
        value /= count_per_cluster[cluster]
        value = np.sqrt(value)
        stddev = np.append(stddev, value)

    cluster = stddev.argmax()
    max_stddev = stddev[cluster]
    max_clusters_list = int(clusters_list.max())

    if max_stddev > theta_s:
        if avg_dists_to_clusters[cluster] >= d:
            if count_per_cluster[cluster] > (2.0 * theta_m):
                old_cluster = centers[cluster, :]

                new_cluster_1 = old_cluster + delta
                new_cluster_1 = new_cluster_1.reshape(1, -1)
                new_cluster_2 = old_cluster - delta
                new_cluster_2 = new_cluster_2.reshape(1, -1)

                centers = np.delete(centers, cluster, axis=0)
                clusters_list = np.delete(clusters_list, cluster)

                centers = np.concatenate((centers, new_cluster_1), axis=0)
                centers = np.concatenate((centers, new_cluster_2), axis=0)
                clusters_list = np.append(clusters_list, max_clusters_list+1)
                clusters_list = np.append(clusters_list, max_clusters_list+2)

                centers, clusters_list = sort_arrays_by_first(centers, clusters_list)

                assert centers.shape[0] == clusters_list.size, \
                    "ERROR: split() centers and clusters_list size are different"

    return centers, clusters_list, k_


def compute_avg_distance(img_flat: np.ndarray,
                         img_class_flat: np.ndarray,
                         centers: np.ndarray,
                         clusters_list: np.ndarray) -> Tuple[np.ndarray, int]:
    """Computes all the average distances to the center in each cluster.

    :param img_flat: Flatten image
    :param img_class_flat: Classes of flatten image
    :param centers: Cluster centers
    :param clusters_list: List of clusters
    :return: Tuple containing the average distances as well as the value for k_
    """
    k_ = centers.shape[0]
    avg_dists_to_clusters = np.zeros(k_)

    for cluster in range(k_):
        indices = np.where(img_class_flat == clusters_list[cluster])[0]

        cluster_points = img_flat[indices]
        avg_dists_to_clusters[cluster] = np.mean(np.linalg.norm(cluster_points - centers[cluster], axis=1))

    return avg_dists_to_clusters, k_


def compute_overall_distance(img_class_flat: np.ndarray,
                             avg_dists_to_clusters: np.ndarray,
                             clusters_list: np.ndarray) -> Tuple[float, int]:
    """Computes the overall distance of the samples from their respective cluster centers.

    :param img_class_flat: Classes of the flatten image
    :param avg_dists_to_clusters: Average distances
    :param clusters_list: List of clusters
    :return: Tuple containing the overall distances as well the value for k_
    """
    k_ = avg_dists_to_clusters.size
    total_count = 0
    total_dist = 0

    for cluster in range(k_):
        nbr_points = len(np.where(img_class_flat == clusters_list[cluster])[0])
        total_dist += avg_dists_to_clusters[cluster] * nbr_points
        total_count += nbr_points

    d = total_dist / total_count

    return d, k_


def merge_clusters(img_class_flat: np.ndarray,
                   centers: np.ndarray,
                   clusters_list: np.ndarray,
                   p: int,
                   theta_c: int,
                   k_: int) -> Tuple[np.ndarray, np.ndarray, int]:
    """Merge by pair of clusters in 'below_threshold' to form new clusters.

    Todo: adaptation for 3d images
    :param img_class_flat: Classes of the flatten image
    :param centers: Cluster centers
    :param clusters_list: List of clusters
    :param p: max number of pairs of clusters which can be merged
    :param theta_c: threshold value for pairwise distances (for merge)
    :param k_:
    :return: Tuple of the new cluster centers, a list of the new clusters and a new value for k_
    """
    pair_dists = compute_pairwise_distances(centers)

    first_p_elements = pair_dists[:p]

    below_threshold = [(c1, c2) for d, (c1, c2) in first_p_elements if d < theta_c]

    if below_threshold:
        k_ = centers.size
        count_per_cluster = np.zeros(k_)
        to_add = np.array([])  # new clusters to add
        to_delete = np.array([])  # clusters to delete

        for cluster in range(k_):
            result = np.where(img_class_flat == clusters_list[cluster])
            indices = result[0]
            count_per_cluster[cluster] = indices.size

        for c1, c2 in below_threshold:
            c1_count = float(count_per_cluster[c1]) + 1
            c2_count = float(count_per_cluster[c2])
            factor = 1.0 / (c1_count + c2_count)
            weight_c1 = c1_count * centers[c1]
            weight_c2 = c2_count * centers[c2]

            value = round(factor * (weight_c1 + weight_c2))

            to_add = np.append(to_add, value)
            to_delete = np.append(to_delete, [c1, c2])

        # delete old clusters and their indices from the available array
        centers = np.delete(centers, to_delete)
        clusters_list = np.delete(clusters_list, to_delete)

        # generate new indices for the new clusters
        # starting from the max index 'to_add.size' times
        start = int(clusters_list.max())
        end = to_add.size + start

        centers = np.append(centers, to_add)
        clusters_list = np.append(clusters_list, range(start, end))

        centers, clusters_list = sort_arrays_by_first(centers, clusters_list)

    return centers, clusters_list, k_


def compute_pairwise_distances(centers: np.ndarray) -> list:
    """Compute the pairwise distances 'pair_dists', between every two clusters centers and returns them sorted.

    Todo: adaptation for 3d images
    :param centers: Cluster centers
    :return: a list with tuples, where every tuple has in its first coord the distance between to clusters, and in the
             second coord has a tuple, with the numbers of the clusters measured
    """
    pair_dists = []
    size = centers.size

    for i in range(size):
        for j in range(size):
            if i > j:
                d = np.abs(centers[i] - centers[j])
                pair_dists.append((d, (i, j)))

    # return it sorted on the first elem
    return sorted(pair_dists)


def isodata(img: np.ndarray,
            k: int = 5,
            it: int = 100,
            p: int = 2,
            theta_m: int = 10,
            theta_s: float = 0.1,
            theta_c: int = 2,
            theta_o: float = 0.05,
            k_: int = None) -> np.ndarray:
    """Classify a numpy 'img' using Isodata algorithm.

    :param img: an input np.ndarray that contains the image to classify
    :param k: number of clusters desired
    :param it: max number of iterations
    :param p: max number of pairs of clusters which can be merged
    :param theta_m: threshold value for min number in each cluster
    :param theta_s: threshold value for standard deviation (for split)
    :param theta_c: threshold value for pairwise distances (for merge)
    :param theta_o: threshold change in the clusters between each iter
    :param k_:
    :return: np.ndarray with the classification
    """
    if k_ is None:
        k_ = k

    x, y, _ = img.shape  # for reshaping at the end
    img_flat = img.reshape(-1, img.shape[2])
    clusters_list = np.arange(k_)  # number of clusters available

    print(f"Isodata(info): Starting algorithm with {k_} classes")
    centers = initial_clusters(img_flat, k_, "linspace")

    i = 0
    img_class_flat = None
    for i in range(it):
        last_centers = centers.copy()
        # assign each of the samples to the closest cluster center
        img_class_flat, dists = vq.vq(img_flat, centers)
        centers, clusters_list, k_ = discard_clusters(img_class_flat, centers, clusters_list, theta_m)
        centers, clusters_list, k_ = update_clusters(img_flat, img_class_flat, centers, clusters_list)
        k_ = centers.shape[0]

        if k_ <= (k / 2.0):  # too few clusters => split clusters
            centers, clusters_list, k_ = split_clusters(img_flat, img_class_flat, centers,
                                                        clusters_list, theta_s, theta_m)
            pass

        elif k_ > (k * 2.0):  # too many clusters => merge clusters
            centers, clusters_list, k_ = merge_clusters(img_class_flat, centers, clusters_list, p, theta_c, k_)
            pass
        else:  # nor split or merge are needed
            pass

        if quit_low_change_in_clusters(centers, last_centers, theta_o):
            break

    print(f"Isodata(info): Finished with {k_} classes")
    print(f"Isodata(info): Number of Iterations: {i + 1}")

    return img_class_flat.reshape(x, y)


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import os
    import numpy as np
    from cube_filter import cast_to_uint8
    from load_dc import load
    from fusion import dc_reg

    path = r'C:\Users\tomen\Documents\mir_imgs'
    output = r'C:\Users\tomen\Documents\mir_imgs\output'

    # img = plt.imread(path)
    dc = load(path=path)  # from folder into datacube
    dc = dc_reg(dc=dc)  # registration of single datacube
    image = dc.cube

    image = np.transpose(cast_to_uint8(data=image), (1, 2, 0))  # cast cube into uint8, then transpose to (1, 2, 0)
    res = isodata(img=image, k_=5, k=10)
    plt.imsave(os.path.join(output, 'test.tiff'), res, cmap='plasma')
