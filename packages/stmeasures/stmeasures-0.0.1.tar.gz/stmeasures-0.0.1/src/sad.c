#include "sad.h"
#include "trajectory.h"
#include <stdlib.h>
#include <math.h>
#include <float.h>
#include <stdbool.h>
#include <stdio.h>


double calculate_distance(Point p1, Point p2) {
    return sqrt(pow(p2.latitude - p1.latitude, 2) + pow(p2.longitude - p1.longitude, 2));
}

Cluster *initialize_cluster(size_t capacity) {
    Cluster *cluster = (Cluster *)malloc(sizeof(Cluster));
    cluster->indices = (size_t *)malloc(capacity * sizeof(size_t));
    cluster->size = 0;
    cluster->capacity = capacity;
    return cluster;
}

void add_to_cluster(Cluster *cluster, size_t index) {
    if (cluster->size == cluster->capacity) {
        cluster->capacity *= 2;
        cluster->indices = (size_t *)realloc(cluster->indices, cluster->capacity * sizeof(size_t));
    }
    cluster->indices[cluster->size++] = index;
}

void free_cluster(Cluster *cluster) {
    free(cluster->indices);
    free(cluster);
}

Cluster **cluster_trajectory(Trajectory *trajectory, double epsilon, size_t *num_clusters) {
    bool *used = (bool *)calloc(trajectory->size, sizeof(bool));
    Cluster **clusters = (Cluster **)malloc(trajectory->size * sizeof(Cluster *));
    *num_clusters = 0;

    for (size_t i = 0; i < trajectory->size; i++) {
        if (used[i]) continue;

        Cluster *cluster = initialize_cluster(10);
        add_to_cluster(cluster, i);
        used[i] = true;

        for (size_t j = 0; j < trajectory->size; j++) {
            if (!used[j] && calculate_distance(trajectory->points[i], trajectory->points[j]) <= epsilon) {
                add_to_cluster(cluster, j);
                used[j] = true;
            }
        }

        clusters[(*num_clusters)++] = cluster;
    }

    free(used);
    return clusters;
}

Point calculate_centroid(Cluster *cluster, Trajectory *trajectory) {
    double sum_lat = 0.0, sum_lon = 0.0;
    for (size_t i = 0; i < cluster->size; i++) {
        sum_lat += trajectory->points[cluster->indices[i]].latitude;
        sum_lon += trajectory->points[cluster->indices[i]].longitude;
    }
    Point centroid = {sum_lat / cluster->size, sum_lon / cluster->size};
    return centroid;
}

double spatial_assembling_distance(Trajectory *trajectory1, Trajectory *trajectory2, double epsilon) {
    size_t num_clusters1, num_clusters2;
    Cluster **clusters1 = cluster_trajectory(trajectory1, epsilon, &num_clusters1);
    Cluster **clusters2 = cluster_trajectory(trajectory2, epsilon, &num_clusters2);

    if (num_clusters1 == 0 || num_clusters2 == 0) {
        return DBL_MAX;
    }

    Point *centroids1 = (Point *)malloc(num_clusters1 * sizeof(Point));
    Point *centroids2 = (Point *)malloc(num_clusters2 * sizeof(Point));

    for (size_t i = 0; i < num_clusters1; i++) {
        centroids1[i] = calculate_centroid(clusters1[i], trajectory1);
    }
    for (size_t i = 0; i < num_clusters2; i++) {
        centroids2[i] = calculate_centroid(clusters2[i], trajectory2);
    }

    double min_distance = DBL_MAX;
    for (size_t i = 0; i < num_clusters1; i++) {
        for (size_t j = 0; j < num_clusters2; j++) {
            double distance = calculate_distance(centroids1[i], centroids2[j]);
            if (distance < min_distance) {
                min_distance = distance;
            }
        }
    }

    for (size_t i = 0; i < num_clusters1; i++) {
        free_cluster(clusters1[i]);
    }
    for (size_t i = 0; i < num_clusters2; i++) {
        free_cluster(clusters2[i]);
    }
    free(clusters1);
    free(clusters2);
    free(centroids1);
    free(centroids2);

    return min_distance;
}

