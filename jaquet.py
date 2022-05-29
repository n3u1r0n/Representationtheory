import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image


def jaquet(ladder, n):
  # convert a ladder to a matrix with pre-filled first and last columns
  # then let jaquet_helper generate all possible matrices given the inital matrix and n

  # n must be a partition of the size of the ladder
  assert sum(n) == ladder_size(ladder)
  k = len(n)
  r = len(ladder)
  # initialize the matrix with th first column being the ladder ends
  # and the last column being the ladder beginnings
  C = np.zeros((len(ladder), k + 1), dtype=int)
  C[:,0] = list(map(lambda segment: segment[1] + 1, ladder))
  C[:,-1] = list(map(lambda segment: segment[0], ladder))
  # generate all possible matrices corresponding to correct colorings
  for result in jaquet_helper(C, n):
    yield result


def jaquet_helper(C, n, k=1):
  # iteratively fill the k-th column of C with the next possible values
  # the possible values are generated by generate_columns

  # if all columns are filled, return the matrix
  if k == C.shape[1] - 1:
    yield C
    return
  # else generate the next columns iteratively
  for column in generate_columns(C[:,k-1], C[:,-1], n[k-1], bound=C[0,0] + 1):
    C[:,k] = column
    for result in jaquet_helper(C, n, k+1):
      yield result


def generate_columns(prev_column, last_column, n, bound):
  # the restrictions on the columns are:
  # 1. the column must be strictly decreasing
  # 2. the column must lie between the previous column and the last column (elementwise)
  # 3. the sum of the previous column minus the sum of the new column must be n

  # if a color is not available anymore return the previous column
  if n == 0:
    if prev_column[0] < bound:
      yield prev_column
    return
  # if we are on the last step of the ladder
  # we need to use up the missing amount of the color, if possible
  if len(prev_column) == 1:
    result = prev_column[0] - n
    if bound > result >= last_column[0]:
      yield result
    return
  # go through all possible values for the entry such that
  # 1. we do not use more the color more than n times
  # 2. the entry is between the previous column and the last column
  # 3. the column stays strictly decreasing, i.e. the last entry is strictly less than the bound
  for m in range(max(prev_column[0] - n, last_column[0]), min(prev_column[0] + 1, bound)):
    for column in generate_columns(prev_column[1:], last_column[1:], n - (prev_column[0] - m), m):
      yield np.r_[m, column]


def matrix_to_ladders(matrix):
  # convert a matrix result from jaquet to a list of ladders

  ladders = []
  # go through all colors, i.e. the 'spaces' between the columns
  # and create a ladder for each color
  for j in range(matrix.shape[1] - 1):
    ladders.append([])
    # then add all the segments to the ladder
    # if the segment is not empty
    for i in range(matrix.shape[0]):
      if matrix[i, j + 1] <= matrix[i, j] - 1:
        ladders[-1] += [[matrix[i, j + 1], matrix[i, j] - 1]]
      else:
        ladders[-1] += [None]
  return ladders


def ladder_size(ladder):
  # return the size of a ladder (number of grid points on the ladder)

  return sum(map(lambda segment: segment[1] - segment[0] + 1 if segment else 0, ladder))


def plot(*ladders, colors='rgbcmk'):
  # go trough all ladders and plot them in a different color

  for color, ladder in enumerate(ladders):
    x, y = list(zip(*[(x, -y) for y, segment in enumerate(ladder) if segment for x in range(segment[0], segment[1] + 1)]))
    if colors:
      plt.scatter(x, y, c=colors[color], s=100)
    else:
      plt.scatter(x, y, c=str(color / len(ladders)), s=100)      
  plt.axis('off')


# def make_gif(ladder, shape, *args, **kwargs):
#   name = str(ladder).replace(' ', '') + '-' + str(shape).replace(' ', '')
#   if not os.path.exists(name):
#     os.mkdir(name)
#   frames = []
#   for n, C in enumerate(jaquet(ladder, shape)):
#     plot(*matrix_to_ladders(C))
#     plt.savefig(os.path.join(name, '{}.jpg'.format(n)))
#     plt.clf()
#     frames.append(Image.open(os.path.join(name, '{}.jpg'.format(n))))
#   frame = frames[0]
#   frame.save('{}.gif'.format(name), format="GIF", append_images=frames,
#              save_all=True, duration=100, loop=0)