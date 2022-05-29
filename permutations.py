import numpy as np


def dyck_paths(n, k=0, height=0):
  # generates all dyck paths of length n
  if height == n - k:
    yield np.array([-1] * (n - k), dtype=int)
    return
  if height > 0:
    for path in dyck_paths(n, k + 1, height - 1):
      yield np.r_[-1, path]
  if height + 1 <= n - k:
    for path in dyck_paths(n, k + 1, height + 1):
      yield np.r_[1, path]


def dyck_path_to_permutation(path):
  heights = np.cumsum(path)[path == -1]
  values = list(range(len(heights) + 1, 0, -1))
  result = np.zeros(len(heights) + 1, dtype=int)
  for n, height in enumerate(heights):
    result[n] = values.pop(height)
  result[-1] = values[0]
  return result


def avoiding_permutations(n):
  for path in dyck_paths(2 * n):
    yield dyck_path_to_permutation(path)