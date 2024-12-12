import graphviz
import os

class DotColors:
  def __init__(self, title = "black", cluster = "black", tableFont = "black", tableFrame = "gray", relation = "skyblue", background = "white"):
    self.Title = title
    self.Cluster = cluster
    self.TableFont = tableFont
    self.TableFrame = tableFrame
    self.Relation = relation
    self.Background = background

class DotFactory:
  @classmethod
  def dber(cls, database, colors, fontName):
    databases = {}
    for table in database.Tables:
      if table.Namespace in databases:
        databases[table.Namespace].append(table)
      else:
        databases[table.Namespace] = [table]
    dot = graphviz.Digraph()
    dot.graph_attr["label"] = "<>"
    dot.graph_attr["labelloc"] = "t"
    dot.graph_attr["labeljust"] = "c"
    dot.graph_attr["fontcolor"] = colors.Title
    dot.graph_attr["margin"] = "0"
    dot.graph_attr["rankdir"] = "LR"
    dot.graph_attr["dpi"] = "350"
    dot.graph_attr["bgcolor"] = colors.Background
    dot.node_attr["fontname"] = fontName
    dot.node_attr["shape"] = "none"
    dot.edge_attr["color"] = colors.Relation
    relations = []
    for database in sorted(databases.items()):
      with dot.subgraph(name = """cluster_{}""".format(database[0])) as sg:
        sg.attr(label = database[0], labeljust = "l", color = colors.Cluster, fontcolor = colors.Cluster)
        for table in database[1]:
          nodeName = table.path().replace(".", "_")
          strings = []
          strings.append("""<<font color="{}"><table border="1" cellspacing="0" cellpadding="0" color="{}" bgcolor="{}"><tr><td colspan="2"><b>{}</b></td></tr>""".format(colors.TableFont, colors.TableFrame, colors.TableFrame, table.display_name()))
          for column in table.Columns:
            strings.append("""<tr><td bgcolor="{}" cellpadding="2" port="{}"> {} </td><td bgcolor="{}" cellpadding="2" align="left"> {} </td><td bgcolor="{}" cellpadding="2" align="left"> {} </td></tr>""".format(colors.Background, column.Name, column.display_name(), colors.Background, column.Type, colors.Background, column.Caption))
            srcId = """{}:{}""".format(nodeName, column.Name)
            for relation in column.Relations:
              paths = relation.split(".")
              columnName = paths.pop()
              relations.append([srcId, """{}:{}""".format("_".join(paths), columnName)])
          strings.append("</table></font>>")
          sg.node(nodeName, "".join(strings))
    for relation in relations:
      dot.edge(relation[1], relation[0], dir = "back", arrowtail = "crow")
    return dot

class DotHelper:
  def __init__(self, dot):
    self.Dot = dot

  @property
  def TitleText(self):
    return self.Dot.graph_attr["label"][1:][:-1]

  @TitleText.setter
  def TitleText(self, value):
    self.Dot.graph_attr["label"] = """<{}>""".format(value)

  def write_image(self, filePath, cleanup = False, view = False):
    self.Dot.render("""{}.dot""".format(os.path.splitext(filePath)[0]), outfile = filePath, cleanup = cleanup, view = view)
