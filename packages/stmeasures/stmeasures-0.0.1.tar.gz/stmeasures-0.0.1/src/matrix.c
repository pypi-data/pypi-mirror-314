#include "matrix.h"
#include <stdio.h>
#include <stdlib.h>

DoubleMatrix *initialize_matrix(int rows, int cols, double initial_value) {
  DoubleMatrix *mat = (DoubleMatrix *)malloc(sizeof(DoubleMatrix));
  if (mat == NULL) {
    return NULL;
  }

  mat->rows = rows;
  mat->cols = cols;

  mat->matrix = (double **)malloc(rows * sizeof(double *));
  if (mat->matrix == NULL) {
    free(mat);
    return NULL;
  }

  for (int i = 0; i < rows; i++) {
    mat->matrix[i] = (double *)malloc(cols * sizeof(double));
    if (mat->matrix[i] == NULL) {
      for (int j = 0; j < i; j++) {
        free(mat->matrix[j]);
      }
      free(mat->matrix);
      free(mat);
      return NULL;
    }

    for (int j = 0; j < cols; j++) {
      mat->matrix[i][j] = initial_value;
    }
  }

  return mat;
}

void free_matrix(DoubleMatrix *mat) {
  if (mat == NULL)
    return;

  for (int i = 0; i < mat->rows; i++) {
    free(mat->matrix[i]);
  }
  free(mat->matrix);
  free(mat);
}
