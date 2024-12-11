#include "edit_distance.h"

double ers(
    const double *r,
    const double *s,
    size_t size_r,
    size_t size_s,
    double sigma,
    double cost_del,
    double cost_ins,
    double subcost_outside_sigma,
    double subcost_within_sigma
)
{
    int rows = ((size_r + 1) / 2) + 1;
    int cols = ((size_s + 1) / 2) + 1;
    double dp[rows][cols];

    dp[0][0] = 0;
	for (int i = 1; i < rows; i++) { // m == 0
		dp[i][0] = size_s;
		// dp[i][0] = i; // Papers define: n if m = 0
	}
	for (int i = 1; i < cols; i++) { // n == 0
		dp[0][i] = size_r;
		// dp[0][i] = i; // Papers define: m if n = 0
	}

    for (int i = 1; i < rows; i++) {
        for (int j = 1; j < cols; j++) {
            int irx = 2*(i-1)+0;
            int iry = 2*(i-1)+1;
            int jsx = 2*(j-1)+0;
            int jsy = 2*(j-1)+1;

            double mdx = s_m_distance(r[irx], s[jsx]);
            double mdy = s_m_distance(r[iry], s[jsy]);

            double subcost = subcost_outside_sigma;
            if (mdx <= sigma && mdy <= sigma) {
                subcost = subcost_within_sigma;
            }

            double min_cost = fmin(INFINITY, dp[i - 1][j -1] + subcost);
            // Deletion from R
            min_cost = fmin(min_cost, dp[i - 1][j] + cost_del);
            // Insertion into S
            min_cost = fmin(min_cost, dp[i][j - 1] + cost_ins);

            dp[i][j] = min_cost;
        }
    }

    return dp[rows - 1][cols - 1];
}

double erp(
    const double *r,
    const double *s,
    size_t size_r,
    size_t size_s,
    double g
){
    int m = size_r;
    int n = size_s;
    double dp[m + 1][n + 1];

    dp[0][0] = 0.0;
	for (int i = 1; i <= m; i++) {
		dp[i][0] = dp[i - 1][0] + s_m_distance(r[i - 1], g);
	}
	for (int j = 1; j <= n; j++) {
		dp[0][j] = dp[0][j - 1] + s_m_distance(s[j - 1], g);
	}

    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            double cost_match = dp[i - 1][j - 1] + s_m_distance(r[i - 1], s[j - 1]);
            double cost_gap_r = dp[i - 1][j] + s_m_distance(r[i - 1], g);
            double cost_gap_s = dp[i][j - 1] + s_m_distance(s[j - 1], g);

            dp[i][j] = fmin(cost_match, fmin(cost_gap_r, cost_gap_s));
        }
    }

    return dp[m][n];
}
