#ifndef FRECHET_H
#define FRECHET_H

#include <stddef.h>
#include <math.h>
#include <float.h>
#include <stdlib.h>

#include "euclidean.h"

double frechet_distance_rec(const double *p, const double *q, size_t i, size_t j, double **cache, size_t size);
double frechet_distance(const double *p, const double *q, size_t p_size, size_t q_size);

#endif
