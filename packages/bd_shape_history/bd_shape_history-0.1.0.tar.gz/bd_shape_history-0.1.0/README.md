# Build132d Shape History

A tool to manage and visualize the modification history of Build123D objects.

## Installation

```
pip install bd_shape_history
```

## Usage

Assuming a simple part created in 3 steps:

```py
box = _.Box(3, 3, 1)
cbox = _.chamfer(box.edges()[0], 0.5)
cboxh = cbox - _.Cylinder(0.75, 1)
```

We can build the history with:

```py
hm = ShapeHistory.from_globals()
```

And then display it `diff()` (here with [VScode OCP CAD viewer](https://github.com/bernhard-42/vscode-ocp-cad-viewer/)):

```py
ov.set_defaults(render_edges=False)
ov.show(*hm.diff(), names=hm.labels())
```

This shows a visual diff between each step:

![](./docs/images/step1.png) ![](./docs/images/step2.png) ![](./docs/images/step3.png)

Notice how the object is colored:
- new faces and edges are green and light green;
- unchanged faces and edges are gray and black;
- modified faces and edges are dark green and olive

See the `examples` folder for more details.

## How does it work

ShapeHistory compares the hash of faces, edges and vertices between each steps:

- a face or edge whose hash is found on the previous step is considered unmodified;
- a face whose all edges are not found in the previous step is considered added (and same for edge / vertices);
- otherwise the face or edge is considered modified.
