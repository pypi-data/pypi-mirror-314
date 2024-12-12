import os

class Path:
  def __init__(self, directory = ".", file = "", ext = ""):
    self.Directory = directory
    self.File = file
    self.Ext = ext

  def makedirs(self):
    os.makedirs(self.Directory, exist_ok = True)

  def to_string(self):
    return Path.join(self.File, self.Ext, self.Directory)

  @classmethod
  def from_file_path(cls, filePath):
    directory, fileAndExt = os.path.split(filePath)
    file, ext = os.path.splitext(fileAndExt)
    return Path(directory, file, ext[1:])

  @classmethod
  def join(cls, file, ext, directory = None):
    if directory is None:
      return """{}.{}""".format(file, ext)
    return """{}/{}.{}""".format(directory, file, ext)
