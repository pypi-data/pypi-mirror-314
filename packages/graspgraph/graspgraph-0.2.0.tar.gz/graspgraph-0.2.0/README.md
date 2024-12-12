# graspgraph
Create easy-to-understand graphs

## Versions

|Version|Summary|
|:--|:--|
|0.2.0|Add dbergraph|
|0.1.0|Release graspgraph|

## Installation
### graspgraph
`pip install graspgraph`

### [Graphviz](https://graphviz.org/download/)

### [Poppler](https://github.com/Belval/pdf2image?tab=readme-ov-file)

## Usage
### statsgraph
![](./images/stats/usage.png)
```python
import graspgraph as gg

statsgraph = gg.Statsgraph(
  gg.StatsgraphAxis([1, 2, 3, 4, 5]),
  gg.StatsgraphAxis([11, 12, 13, 14, 15]),
  gg.FigureColors(line = "blue"))
figure = statsgraph.to_figure_helper()
figure.LayoutTitleText = "<b>[statsgraph]<br>タイトル</b>"
figure.XTitleText = "X軸"
figure.YTitleText = "Y軸"
figure.write_image("./images/stats/usage.png")
```

### dbergraph
![](./images/dber/usage.png)
```python
import graspgraph as gg

dbergraph = gg.Dbergraph(gg.Database().load("./images/dber/database_input.yaml"))
dbergraph.Database.update()
prefix = "./images/dber/usage"
pdfFilePath = gg.Path.join(prefix, "pdf")
pngFilePath = gg.Path.join(prefix, "png")
dot = dbergraph.to_dot_helper()
dot.TitleText = "<b>[dbergraph]</b>"
dot.write_image(pdfFilePath)
gg.Pdf.convert(pdfFilePath, pngFilePath)
```
