cimport cython
import cython
cimport numpy as np
import numpy as np
from libc.stdlib cimport malloc, free

cdef extern from "math.h":
    double pow(double x, double y)

cdef extern from "stdlib.h":
    void free(void* ptr)

@cython.boundscheck(False)
@cython.wraparound(False)
def lk_stat(double[:] periods, double[:] mag, double[:] magerr, double[:] Time):
    """
    Compute the Laffler-Kinman statistic for a given set of periods, magnitudes, and magnitude errors.

    Parameters:
    ----------
    periods : array-like of float
        Array of trial periods to evaluate the Laffler-Kinman statistic.
    mag : array-like of float
        Array of magnitudes corresponding to the time series data.
    magerr : array-like of float
        Array of magnitude errors corresponding to the magnitudes.
    Time : array-like of float
        Time series data.

    Returns:
    -------
    np.ndarray
        An array of theta values corresponding to each trial period.
    """
    cdef int periods_size = periods.shape[0]
    cdef int data_size = mag.shape[0]
    cdef double p
    cdef double* phi = <double*>malloc(data_size * sizeof(double))
    cdef int* nphi = <int*>malloc(data_size * sizeof(int))
    cdef double* sorted_mag = <double*>malloc(data_size * sizeof(double))
    cdef double* sorted_magerr = <double*>malloc(data_size * sizeof(double))
    cdef double* w = <double*>malloc((data_size - 1) * sizeof(double))
    cdef int* idx = <int*>malloc(data_size * sizeof(int))
    cdef int i, j, k
    cdef double sum_w, sum_w_diff_sq, sum_var, mean_m
    cdef np.ndarray[double, ndim=1] theta_array = np.zeros(periods_size, dtype=np.double)

    for i in range(periods_size):
        p = periods[i]
        
        for j in range(data_size):
            phi[j] = Time[j] / p
            nphi[j] = <int>phi[j]
            phi[j] -= nphi[j]
            idx[j] = j

        for j in range(data_size):
            for k in range(j + 1, data_size):
                if phi[idx[j]] > phi[idx[k]]:
                    idx[j], idx[k] = idx[k], idx[j]

        for j in range(data_size):
            sorted_mag[j] = mag[idx[j]]
            sorted_magerr[j] = magerr[idx[j]]

        for j in range(data_size - 1):
            w[j] = 1 / (pow(sorted_magerr[j + 1], 2) + pow(sorted_magerr[j], 2))

        sum_w = sum_w_diff_sq = sum_var = mean_m = 0
        for j in range(1, data_size):
            mean_m += sorted_mag[j]
        mean_m /= (data_size - 1)

        for j in range(1, data_size):
            sum_w += w[j - 1]
            sum_w_diff_sq += w[j - 1] * pow((sorted_mag[j] - sorted_mag[j - 1]), 2)
            sum_var += pow((sorted_mag[j] - mean_m), 2)

        theta_array[i] = sum_w_diff_sq / (sum_var * sum_w)

    free(phi)
    free(nphi)
    free(sorted_mag)
    free(sorted_magerr)
    free(w)
    free(idx)

    return theta_array

