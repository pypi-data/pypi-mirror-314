#ifndef LCSS_H
#define LCSS_H

#include <stddef.h>
#include <stdlib.h>
#include <math.h>

double distance(
    const double *r,
    const double *s,
    size_t size_r,
    size_t size_s,
    double epsilon
);

#endif

