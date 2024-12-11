#include "dtw.h"
#include "euclidean.h"
#include "matrix.h"
#include <float.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

DoubleMatrix *calculate_dtw_matrix(const Trajectory *seq1,
                                   const Trajectory *seq2) {
  int m = seq1->size;
  int n = seq2->size;

  DoubleMatrix *accumulatedCost = initialize_matrix(m, n, 0.0);
  if (accumulatedCost == NULL) {
    return NULL;
  }

  for (int i = 0; i < m; i++) {
    for (int j = 0; j < n; j++) {

      double point1[2] = {seq1->points[i].latitude, seq1->points[i].longitude};
      double point2[2] = {seq2->points[j].latitude, seq2->points[j].longitude};

      accumulatedCost->matrix[i][j] = distance(point1, point2, 2);

      if (i == 0 && j == 0) {
        continue;
      } else if (i == 0) {
        accumulatedCost->matrix[i][j] += accumulatedCost->matrix[i][j - 1];
      } else if (j == 0) {
        accumulatedCost->matrix[i][j] += accumulatedCost->matrix[i - 1][j];
      } else {
        accumulatedCost->matrix[i][j] +=
            fmin(accumulatedCost->matrix[i - 1][j],
                 fmin(accumulatedCost->matrix[i][j - 1],
                      accumulatedCost->matrix[i - 1][j - 1]));
      }
    }
  }

  return accumulatedCost;
}

int **calculate_optimal_path(DoubleMatrix *accumulatedCost, int *path_size) {
  int m = accumulatedCost->rows;
  int n = accumulatedCost->cols;

  int **optimalPath = (int **)malloc((m + n) * sizeof(int *));
  if (optimalPath == NULL) {
    return NULL;
  }

  *path_size = 0;
  int max_path_size = m + n - 1;

  for (int i = 0; i < max_path_size; ++i) {
    optimalPath[i] = (int *)malloc(2 * sizeof(int));
    if (optimalPath[i] == NULL) {
      for (int k = 0; k < i; ++k) {
        free(optimalPath[k]);
      }
      free(optimalPath);
      return NULL;
    }
  }

  int i = m - 1;
  int j = n - 1;

  while (i >= 0 || j >= 0) {
    if (*path_size >= max_path_size) {
      for (int k = 0; k < max_path_size; ++k) {
        free(optimalPath[k]);
      }
      free(optimalPath);
      return NULL;
    }

    optimalPath[*path_size][0] = i;
    optimalPath[*path_size][1] = j;
    (*path_size)++;

    if (i == 0 && j == 0) {
      break;
    }

    double minCost = DBL_MAX;

    if (i > 0 && j > 0) {
      minCost = fmin(accumulatedCost->matrix[i - 1][j],
                     fmin(accumulatedCost->matrix[i][j - 1],
                          accumulatedCost->matrix[i - 1][j - 1]));
    }
    if (i > 0 && j == 0) {
      minCost = accumulatedCost->matrix[i - 1][j];
    }
    if (j > 0 && i == 0) {
      minCost = accumulatedCost->matrix[i][j - 1];
    }

    if (i > 0 && j > 0 && accumulatedCost->matrix[i - 1][j - 1] == minCost) {
      i--;
      j--;
    } else if (i > 0 && accumulatedCost->matrix[i - 1][j] == minCost) {
      i--;
    } else if (j > 0) {
      j--;
    }
  }

  for (int k = 0; k < *path_size / 2; ++k) {
    int temp0 = optimalPath[k][0];
    int temp1 = optimalPath[k][1];
    optimalPath[k][0] = optimalPath[*path_size - 1 - k][0];
    optimalPath[k][1] = optimalPath[*path_size - 1 - k][1];
    optimalPath[*path_size - 1 - k][0] = temp0;
    optimalPath[*path_size - 1 - k][1] = temp1;
  }

  return optimalPath;
}

double calculate_cost_from_optimal_path(DoubleMatrix *accumulatedCost,
                                        int **optimalPath, int path_size) {
  double cost = 0.0;

  for (int i = 0; i < path_size; i++) {
    int x = optimalPath[i][0];
    int y = optimalPath[i][1];
    cost += accumulatedCost->matrix[x][y];
  }

  return cost;
}

double dtw_execute(const Trajectory *seq1,
                   const Trajectory *seq2) {
  DoubleMatrix *matrizCostos = calculate_dtw_matrix(seq1, seq2);
  if (matrizCostos == NULL) {
    return -1.0;
  }

  int path_size = 0;
  int **rutaOptima = calculate_optimal_path(matrizCostos, &path_size);
  if (rutaOptima == NULL) {
    free_matrix(matrizCostos);
    return -1.0;
  }

  double costDTW =
      calculate_cost_from_optimal_path(matrizCostos, rutaOptima, path_size);

  free_matrix(matrizCostos);

  for (int i = 0; i < path_size; ++i) {
    free(rutaOptima[i]);
  }
  free(rutaOptima);

  return costDTW;
}
