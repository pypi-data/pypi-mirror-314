#include "manhattan.h"

double s_m_distance(const double a, const double b)
{
    return fabs(a - b);
}

double m_distance(const double *p, const double *q, size_t size)
{
    double sum_of_diffs = 0.0;

    for (size_t i = 0; i < size; ++i) {
        sum_of_diffs += s_m_distance(p[i], q[i]);
    }

    return sum_of_diffs;
}
