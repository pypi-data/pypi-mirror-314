#ifndef COORDINATES_H
#define COORDINATES_H

#include <stddef.h>

typedef struct {
  double latitude;
  double longitude;
} Point;

typedef struct {
  Point *points; // Apuntador a un arreglo de puntos
  size_t size;   // Tamaño del arreglo
} Trajectory;

#endif
