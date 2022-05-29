import numpy as np


def random_multisegment(n, upper_bound=5, lower_bound=0):
  # generates a random multisegment with n segments
  # all between lower_bound and upper_bound
  
  a = np.random.randint(lower_bound, upper_bound, (n, 1))
  b = np.random.randint(lower_bound, upper_bound, (n, 1))
  return np.concatenate((np.minimum(a, b), np.maximum(a, b)), axis=1)


def random_ladder(max_segment_count=5, max_segment_length=4, max_shift=2):
  ladder = [[0, np.random.randint(max_segment_length + 1)]]
  for _ in range(np.random.randint(max_segment_count + 1) - 1):
    ladder.append([ladder[-1][0] + (shift := np.random.randint(1, max_shift + 1)), max(ladder[-1][1] + 1, ladder[-1][0] + shift + np.random.randint(max_segment_length + 1))])
  return ladder[::-1]


# def random_ssiyt(n, m, upper_bound=5, lower_bound=0):
#   result = np.random.randint(lower_bound, upper_bound, (n, m)).astype(object)
#   for row in range(n):
#     for col in range(m):
#       if row == 0:
#         if col != 0:
#           if result[row, col] >= result[row, col - 1]:
#             result[row, col] = result[row, col - 1] - 1
#       else:
#         if result[row, col] >= result[row, col - 1]:
#           result[row, col] = result[row, col - 1] - 1
#         if result[row, col] > result[row - 1, col]:
#           result[row, col] = result[row - 1, col]
#   result[result < lower_bound] = None
#   return result