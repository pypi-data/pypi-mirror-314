from pdf2image import convert_from_path
from .path import *

class Pdf:
  def __init__(self, pages = []):
    self.Pages = pages

  def load(self, filePath):
    self.Pages = convert_from_path(filePath)
    return self

  def save(self, filePath, pageIndex = 0):
    path = Path.from_file_path(filePath)
    self.Pages[pageIndex].save(filePath, path.Ext.upper())
    return self

  @classmethod
  def convert(cls, fromFilePath, toFilePath):
    Pdf().load(fromFilePath).save(toFilePath)
