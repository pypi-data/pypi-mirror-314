#ifndef RDP_H
#define RDP_H

#include "coordinates.h"

double perpendicular_distance(const Point *p, const Point *line_start,
                              const Point *line_end);

void simplify_line(const CoordinateSequence *input, double tolerance,
                   CoordinateSequence *output);

CoordinateSequence rdp_execute(const CoordinateSequence *input,
                               double tolerance);

#endif
