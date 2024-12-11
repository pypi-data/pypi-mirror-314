#include "rdp.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double perpendicular_distance(const Point *p, const Point *line_start,
                              const Point *line_end) {
  double dx = line_end->longitude - line_start->longitude;
  double dy = line_end->latitude - line_start->latitude;

  if (dx == 0.0 && dy == 0.0) {
    return sqrt(pow(p->longitude - line_start->longitude, 2) +
                pow(p->latitude - line_start->latitude, 2));
  }

  double u = ((p->longitude - line_start->longitude) * dx +
              (p->latitude - line_start->latitude) * dy) /
             (dx * dx + dy * dy);

  if (u < 0.0) {
    return sqrt(pow(p->longitude - line_start->longitude, 2) +
                pow(p->latitude - line_start->latitude, 2));
  }
  if (u > 1.0) {
    return sqrt(pow(p->longitude - line_end->longitude, 2) +
                pow(p->latitude - line_end->latitude, 2));
  }

  double x = line_start->longitude + u * dx;
  double y = line_start->latitude + u * dy;

  return sqrt(pow(p->longitude - x, 2) + pow(p->latitude - y, 2));
}

void simplify_line(const CoordinateSequence *input, double tolerance,
                   CoordinateSequence *output) {
  if (input == NULL || output == NULL || tolerance < 0) {
    fprintf(stderr, "Error: Entrada inválida en simplify_line\n");
    return;
  }

  if (input->size < 2) {
    output->points = (Point *)malloc(input->size * sizeof(Point));
    if (output->points == NULL) {
      fprintf(stderr,
              "Error: No se pudo asignar memoria para output->points\n");
      return;
    }
    for (size_t i = 0; i < input->size; ++i) {
      output->points[i] = input->points[i];
    }
    output->size = input->size;
    return;
  }

  // Encontrar el punto con la mayor distancia perpendicular
  double max_distance = 0.0;
  size_t max_index = 0;
  const Point *start = &input->points[0];
  const Point *end = &input->points[input->size - 1];

  for (size_t i = 1; i < input->size - 1; ++i) {
    double distance = perpendicular_distance(&input->points[i], start, end);
    if (distance > max_distance) {
      max_distance = distance;
      max_index = i;
    }
  }

  // Si la distancia máxima es mayor que la tolerancia, simplificar
  // recursivamente
  if (max_distance > tolerance) {
    CoordinateSequence left_subsequence = {input->points, max_index + 1};
    CoordinateSequence right_subsequence = {&input->points[max_index],
                                            input->size - max_index};
    CoordinateSequence simplified_left = {NULL, 0};
    CoordinateSequence simplified_right = {NULL, 0};

    simplify_line(&left_subsequence, tolerance, &simplified_left);
    simplify_line(&right_subsequence, tolerance, &simplified_right);

    if (simplified_left.points == NULL || simplified_right.points == NULL) {
      fprintf(stderr, "Error: Fallo en la simplificación recursiva\n");
      free(simplified_left.points);
      free(simplified_right.points);
      return;
    }

    output->size = simplified_left.size + simplified_right.size - 1;
    output->points = (Point *)malloc(output->size * sizeof(Point));
    if (output->points == NULL) {
      fprintf(stderr,
              "Error: No se pudo asignar memoria para output->points\n");
      free(simplified_left.points);
      free(simplified_right.points);
      return;
    }

    for (size_t i = 0; i < simplified_left.size; ++i) {
      output->points[i] = simplified_left.points[i];
    }
    for (size_t i = 1; i < simplified_right.size; ++i) {
      output->points[simplified_left.size + i - 1] = simplified_right.points[i];
    }

    free(simplified_left.points);
    free(simplified_right.points);
  } else {
    output->size = 2;
    output->points = (Point *)malloc(2 * sizeof(Point));
    if (output->points == NULL) {
      fprintf(stderr,
              "Error: No se pudo asignar memoria para output->points\n");
      return;
    }
    output->points[0] = *start;
    output->points[1] = *end;
  }
}

CoordinateSequence rdp_execute(const CoordinateSequence *input,
                               double tolerance) {
  CoordinateSequence output = {NULL, 0};
  simplify_line(input, tolerance, &output);
  return output;
}
