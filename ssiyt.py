import numpy as np
from rsk import RSK


def ladders_to_SSIYT(ladders):
  # converts a list of ladders to the two corresponding SSIYTs

  return (
    np.array([
      [ladder[d][0] if d < len(ladder) else None for d in range(len(ladders[0]))]
      for ladder in ladders
    ], dtype=object),
    np.array([
      [ladder[d][1] if d < len(ladder) else None for d in range(len(ladders[0]))]
      for ladder in ladders
    ], dtype=object)
  )


def shape(SSIYT):
  # calculates the shape of the SSIYT

  return (s := np.array([
    0 if len(a := np.where(row != None)[0]) == 0 else a[-1] + 1
    for row in SSIYT
  ]))[s != 0]


def cut_down_SSIYT(SSIYT):
  # cuts down the SSIYT to the smallest possible shape without useless None rows or columns

  return SSIYT[:len(s := shape(SSIYT)),:s[0]]


def smaller_shape(shape1, shape2):
  # a shape is smaller than an other shape if the following criteria are met
  # its length is smaller or equal to the other shape's length
  # for all j, the sum of the first j elements is larger or equal the sum of the first j elements of the other shape

  if len(shape1) > len(shape2): return False
  for j in range(len(shape1)):
    if sum(shape1[:j]) < sum(shape2[:j]): return False
  return sum(shape1) == sum(shape2)


def smaller_SSIYT(SSIYT1, SSIYT2):
  # one SSIYT is smaller than another if for all r
  # the shape of SSIYT1 >= r is smaller than the shape of SSIYT2 >= r

  for r in range(min(SSIYT_min(SSIYT1), SSIYT_min(SSIYT2)), max(SSIYT_max(SSIYT1), SSIYT_max(SSIYT2)) + 1):
    if not smaller_shape(shape(SSIYT_greater_equal(SSIYT1, r)), shape(SSIYT_greater_equal(SSIYT2, r))):
      return False
  return True


def smaller(multisegment1, multisegment2):
  # compare the SSIYT's corresponding to the multisegments

  P1, Q1 = ladders_to_SSIYT(RSK(multisegment1))
  P2, Q2 = ladders_to_SSIYT(RSK(multisegment2))
  return smaller_SSIYT(P1, P2) and smaller_SSIYT(Q1, Q2)


def SSIYT_greater_equal(SSIYT, bound):
  # return the SSIYT where elements are >= bound

  result = np.copy(SSIYT)
  result[result == None] = bound - 1
  result[result < bound] = None
  return result


def SSIYT_max(SSIYT):
  # get the max of the SSIYT

  return np.max(SSIYT[SSIYT != None])


def SSIYT_min(SSIYT):
  # get the min of the SSIYT

  return np.min(SSIYT[SSIYT != None])