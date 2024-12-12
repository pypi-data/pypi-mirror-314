class Font:
  __Instance = None

  def __init__(self, name = "Yu Mincho Demibold"):
    self.Name = name

  @classmethod
  def instance(cls):
    if cls.__Instance is None:
      cls.__Instance = Font()
    return cls.__Instance
