import numpy as np

class Array:
  @classmethod
  def arange(cls, start, stop, step = 1):
    return np.arange(start, stop + step, step)
