"""
Compare the speed of using NumPy multiplication vs list comprehensions to
perform the matrix product of a stack of matrices with a matrix of vectors. This
test proves that the NumPy route is close to 2-orders of magnitude faster.
"""

import time
import numpy as np
import r3f
import itrm
import tkz

KK = np.round(10**np.arange(1, 6, 0.1)).astype(int)
K_max = KK[-1]
tt = np.zeros((len(KK), 2))

# Build the stack of rotation matrices.
r = np.random.uniform(-np.pi, np.pi, K_max)
p = np.random.uniform(-np.pi/2 + r3f.TOL, np.pi/2 - r3f.TOL, K_max)
y = np.random.uniform(-np.pi, np.pi, K_max)

# Build the matrix of rotation vectors.
vec = np.random.randn(3, K_max)

for n, K in enumerate(KK):
    C = r3f.rpy_to_dcm([r, p, y])

    # Try the numpy route.
    tic = time.perf_counter()
    out = np.zeros((3, K))
    out[0] = C[:K, 0, 0]*vec[0, :K] + C[:K, 0, 1]*vec[1, :K] + C[:K, 0, 2]*vec[2, :K]
    out[1] = C[:K, 1, 0]*vec[0, :K] + C[:K, 1, 1]*vec[1, :K] + C[:K, 1, 2]*vec[2, :K]
    out[2] = C[:K, 2, 0]*vec[0, :K] + C[:K, 2, 1]*vec[1, :K] + C[:K, 2, 2]*vec[2, :K]
    toc = time.perf_counter()
    tt[n, 0] = toc - tic

    # Try the list comprehension route.
    tic = time.perf_counter()
    out = np.array([
        [C[k, 0, 0]*vec[0, k] + C[k, 0, 1]*vec[1, k] + C[k, 0, 2]*vec[2, k]
            for k in range(K)],
        [C[k, 0, 1]*vec[0, k] + C[k, 1, 1]*vec[1, k] + C[k, 1, 2]*vec[2, k]
            for k in range(K)],
        [C[k, 0, 2]*vec[0, k] + C[k, 2, 1]*vec[1, k] + C[k, 2, 2]*vec[2, k]
            for k in range(K)]])
    toc = time.perf_counter()
    tt[n, 1] = toc - tic

itrm.iplot(KK, tt.T, label="NumPy, List", rows=0.5, lg="xy")

if 0:
    fig = tkz.graph("matmul3d")
    fig.plot(KK.astype(float), tt[:, 0], label="NumPy")
    fig.plot(KK.astype(float), tt[:, 1], label="List")
    fig.xlog = True
    fig.ylog = True
    fig.xlabel = "Array length"
    fig.ylabel = "Time"
    fig.render()
