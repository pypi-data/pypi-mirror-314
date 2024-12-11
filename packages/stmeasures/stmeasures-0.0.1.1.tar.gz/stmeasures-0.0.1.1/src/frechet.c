#include "frechet.h"

double frechet_distance_rec(const double *p, const double *q, size_t i, size_t j, double **cache, size_t size) {
    if (cache[i][j] != -1.0) {
        return cache[i][j];
    }

    if (i == 0 && j == 0) {
        cache[i][j] = distance(&p[i], &q[j], size);  // Use the euclidean distance function
    } else if (i == 0) {
        cache[i][j] = fmax(frechet_distance_rec(p, q, i, j - 1, cache, size), distance(&p[i], &q[j], size));
    } else if (j == 0) {
        cache[i][j] = fmax(frechet_distance_rec(p, q, i - 1, j, cache, size), distance(&p[i], &q[j], size));
    } else {
        double option1 = frechet_distance_rec(p, q, i - 1, j, cache, size);
        double option2 = frechet_distance_rec(p, q, i, j - 1, cache, size);
        double option3 = frechet_distance_rec(p, q, i - 1, j - 1, cache, size);
        cache[i][j] = fmax(fmin(fmin(option1, option2), option3), distance(&p[i], &q[j], size));
    }

    return cache[i][j];
}

double frechet_distance(const double *p, const double *q, size_t p_size, size_t q_size) {
    double **cache = malloc(p_size * sizeof(double *));
    for (size_t i = 0; i < p_size; ++i) {
        cache[i] = malloc(q_size * sizeof(double));
        for (size_t j = 0; j < q_size; ++j) {
            cache[i][j] = -1.0;
        }
    }

    double result = frechet_distance_rec(p, q, p_size - 1, q_size - 1, cache, 1);  // The last parameter '1' is for size

    for (size_t i = 0; i < p_size; ++i) {
        free(cache[i]);
    }
    free(cache);

    return result;
}
