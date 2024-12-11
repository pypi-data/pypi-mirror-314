#ifndef DTW_H
#define DTW_H

#include "trajectory.h"
#include "matrix.h"

double dtw_execute(const Trajectory *seq1,
                   const Trajectory *seq2);

DoubleMatrix *calculate_dtw_matrix(const Trajectory *seq1,
                                   const Trajectory *seq2);

int **calculate_optimal_path(DoubleMatrix *accumulatedCost, int *path_size);

double calculate_cost_from_optimal_path(DoubleMatrix *accumulatedCost,
                                        int **optimalPath, int path_size);

#endif
