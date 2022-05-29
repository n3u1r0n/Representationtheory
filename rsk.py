import numpy as np


def sort_key_inclusion(segment):
  # the key is the negative interval length to get the inclusion
  # in falling order

  return segment[0] - segment[1]


def depth_helper(multisegment, i, cache):
  # calculates the depth of the segment i
  # and also stores it in the cache

  if (cached := cache.get(i)) is not None:
    return cached
  segments_bigger = np.where((multisegment[i,0] < multisegment[:,0]) * (multisegment[i,1] < multisegment[:,1]))[0]
  if len(segments_bigger) == 0:
    cache[i] = 0
    return 0
  cache[i] = max(map(lambda j: depth_helper(multisegment, j, cache), segments_bigger)) + 1
  return cache[i]


def get_depth(multisegment):
  # calculates the depth of the segments with the help of depth_helper
  # and it returns the cache as a numpy array
  
  cache = dict()
  for i in range(len(multisegment)):
    if cache.get(i) is None:
      depth_helper(multisegment, i, cache)
  return np.array([cache[i] for i in range(len(multisegment))])


def RSK_helper(multisegment):
  # does one iteration of RSK

  # get all the depths of the segments
  depth = get_depth(multisegment)
  max_depth = max(depth)

  # for all depths sort the segments with respect to inclusion
  ordered_segments = [
    sorted(map(list, multisegment[np.where(depth == d)[0]]), key=sort_key_inclusion)
    for d in range(max_depth + 1)
  ]

  # RSK magic
  ladder = np.array([
    [ordered_segments[d][-1][0], ordered_segments[d][0][-1]]
    for d in range(max_depth + 1)
  ])
  new_multisegment = np.array([
    [ordered_segments[d][i][0], ordered_segments[d][i + 1][-1]]
    for d in range(max_depth + 1)
    for i in range(len(ordered_segments[d]) - 1)
  ])
  return ladder, new_multisegment


def RSK(multisegment):
  # apply RSK_helper to the multisegment until it is empty

  ladders = []
  while len(multisegment) > 0:
    ladder, multisegment = RSK_helper(multisegment)
    ladders.append(ladder)
  return ladders