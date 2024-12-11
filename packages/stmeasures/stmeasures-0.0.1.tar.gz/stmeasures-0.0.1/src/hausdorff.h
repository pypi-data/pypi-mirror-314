#ifndef HAUSDORFF_H
#define HAUSDORFF_H

#include <stddef.h>
#include <math.h>
#include <float.h>
#include <stdlib.h>

double hausdorff_distance(const double *p, const double *q, size_t p_size, size_t q_size);

#endif
