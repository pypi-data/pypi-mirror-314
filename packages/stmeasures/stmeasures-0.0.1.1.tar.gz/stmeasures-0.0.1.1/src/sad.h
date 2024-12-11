#ifndef SAD_H
#define SAD_H

#include <stddef.h>
#include "trajectory.h"

typedef struct {
    size_t *indices; 
    size_t size;     
    size_t capacity; 
} Cluster;

double calculate_distance(Point p1, Point p2);

Cluster *initialize_cluster(size_t capacity);
void add_to_cluster(Cluster *cluster, size_t index);
void free_cluster(Cluster *cluster);
Cluster **cluster_trajectory(Trajectory *trajectory, double epsilon, size_t *num_clusters);

Point calculate_centroid(Cluster *cluster, Trajectory *trajectory);


double spatial_assembling_distance(Trajectory *trajectory1, Trajectory *trajectory2, double epsilon);

#endif

