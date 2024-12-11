#ifndef MATRIX_H
#define MATRIX_H

typedef struct {
  double **matrix;
  int rows;
  int cols;
} DoubleMatrix;

DoubleMatrix *initialize_matrix(int rows, int cols, double initial_value);

void free_matrix(DoubleMatrix *mat);

#endif
