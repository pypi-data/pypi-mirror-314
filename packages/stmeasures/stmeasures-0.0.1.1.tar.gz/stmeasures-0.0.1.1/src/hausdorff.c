#include "hausdorff.h"

double point_distance(const double p1, const double p2) {
    return fabs(p1 - p2);
}

double max_min_distance(const double *p, const double *q, size_t p_size, size_t q_size) {
    double max_dist_p = -DBL_MAX;
    for (size_t i = 0; i < p_size; ++i) {
        double min_dist = DBL_MAX;
        for (size_t j = 0; j < q_size; ++j) {
            double dist = point_distance(p[i], q[j]);  // Directly calculate distance between points
            if (dist < min_dist) {
                min_dist = dist;
            }
        }
        if (min_dist > max_dist_p) {
            max_dist_p = min_dist;
        }
    }
    return max_dist_p;
}

double hausdorff_distance(const double *p, const double *q, size_t p_size, size_t q_size) {
    double max_dist_pq = max_min_distance(p, q, p_size, q_size);
    double max_dist_qp = max_min_distance(q, p, q_size, p_size);

    return fmax(max_dist_pq, max_dist_qp);
}
