#include "lcss.h"

int is_within_threshold(double r, double s, double epsilon) {
    return fabs(r - s) <= epsilon;
}

double distance(
    const double *r,
    const double *s,
    size_t size_r,
    size_t size_s,
    double epsilon
){
    int **dp = (int **) malloc((size_r + 1) * sizeof(int *));
    for (int i = 0; i <= size_r; i++) {
        dp[i] = (int *) malloc((size_s + 1) * sizeof(int));
    }

    for (int i = 0; i <= size_r; i++) {
        dp[i][0] = 0;
    }
    for (int j = 0; j <= size_s; j++) {
        dp[0][j] = 0;
    }

    for (int i = 1; i <= size_r; i++) {
        for (int j = 1; j <= size_s; j++) {
            if (is_within_threshold(r[i - 1], s[j - 1], epsilon)) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = fmax(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }

    double result = dp[size_r][size_s];

    for (int i = 0; i <= size_r; i++) {
        free(dp[i]);
    }
    free(dp);

    return result / fmax(size_r, size_s); // Normalize
}
