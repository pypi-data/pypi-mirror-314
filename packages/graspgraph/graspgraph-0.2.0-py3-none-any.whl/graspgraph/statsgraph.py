import numpy as np
from .array import *
from .figure import *

class SimpleStats:
  def __init__(self, values):
    self.__Values = tuple(values)
    if 0 < len(values):
      self.__Avg = sum(values) / len(values)
      self.__Min = min(values)
      self.__Max = max(values)
    else:
      self.__Avg = self.__Min = self.__Max = 0

  @property
  def Values(self):
    return self.__Values

  @property
  def Avg(self):
    return self.__Avg

  @property
  def Min(self):
    return self.__Min

  @property
  def Max(self):
    return self.__Max

class MultipleStats:
  def __init__(self, values, maxCount = 0):
    self.__Values = tuple(values)
    self.__Avg = []
    self.__Min = []
    self.__Max = []
    count = len(values)
    maxCount = min(max(maxCount, 0), count)
    if count <= maxCount:
      self.__Avg = self.__Min = self.__Max = self.__Values
    else:
      for splitedValues in np.array_split(values, maxCount):
        stats = SimpleStats(splitedValues)
        self.__Avg.append(stats.Avg)
        self.__Min.append(stats.Min)
        self.__Max.append(stats.Max)
    self.__Avg = tuple(self.__Avg)
    self.__Min = tuple(self.__Min)
    self.__Max = tuple(self.__Max)

  @property
  def Values(self):
    return self.__Values

  @property
  def Avg(self):
    return self.__Avg

  @property
  def Min(self):
    return self.__Min

  @property
  def Max(self):
    return self.__Max

class StatsgraphAxis:
  def __init__(self, values, maxCount = 0, tick = None):
    self.__Values = tuple(values)
    self.MaxCount = maxCount
    if tick is None:
      tick = FigureTick()
    self.Tick = tick

  @property
  def Values(self):
    return self.__Values

  @property
  def MaxCount(self):
    return self.__MaxCount

  @MaxCount.setter
  def MaxCount(self, value):
    if value <= 0:
      value = max(len(self.__Values), 1)
    self.__MaxCount = value

class Statsgraph:
  def __init__(self, xAxis, yAxis, colors = None):
    self.XAxis = xAxis
    self.YAxis = yAxis
    if colors is None:
      colors = FigureColors()
    self.Colors = colors

  def to_figure(self):
    if len(self.YAxis.Values) <= self.XAxis.MaxCount:
      xValues = self.XAxis.Values
      xDtick = self.XAxis.Tick.Dtick
    else:
      tick = self.XAxis.Values[1] - self.XAxis.Values[0]
      step = (self.XAxis.Values[-1] - self.XAxis.Values[0] + tick) / self.XAxis.MaxCount
      xValues = Array.arange(self.XAxis.Values[0] + step - tick, self.XAxis.Values[-1], step)
      xDtick = max(step, self.XAxis.Tick.Dtick)
      if xValues[-1] <= xDtick:
        xDtick = step
    ySimpleStats = SimpleStats(self.YAxis.Values)
    yMultipleStats = MultipleStats(self.YAxis.Values, self.XAxis.MaxCount)
    return FigureFactory.stats(
      xValues,
      [yMultipleStats.Min, yMultipleStats.Avg, yMultipleStats.Max],
      [ySimpleStats.Min, min(self.YAxis.Tick.Dtick * self.YAxis.MaxCount + ySimpleStats.Min, ySimpleStats.Max)],
      [FigureTick(xDtick, self.XAxis.Tick.Format), self.YAxis.Tick],
      self.Colors)

  def to_figure_helper(self):
    return FigureHelper(self.to_figure())
