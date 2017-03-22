Tkinter Builder from YAML
=========================

This library is a python library to build Tkinter windows from YAML.

## How to use

```
from tkyml import TKYML

yamldata = open("xxxx.yaml", "r").read()
frame = TKYML(root, yamldata)
```

And you'll get `frame`, a `Tkinter.Frame` instance.

## How to write YAML file

Currently 3 sections are required: `grids`, `widgets` and `bind`.

### Widgets

Widgets are positioned using Tkinter's `grid` method. Therefore you need to
plan for each widget a cell in a table-style layout.

Each key in the `widgets:` section has following syntax:

    WidgetType(ROW, COLUMN)(NSWE) WidgetName
    WidgetType(ROW1-ROW2, COLUMN1-COLUMN2)(NSWE) WidgetName

Some examples:
    
    Label(0, 0)         A Label widget at row 0, column 0
    Label(0, 0-5)       A Label widget at row 0, spans over column 0 to 5
    Label(0, 0)(NSWE)   A Label widget at row 0 col 0, sticky to N,S,W,E 4 directions
    Label(0, 0)(NSWE)  lblHello
                        A label as above, with name lblHello(can be accessed using `frame.lblHello`

The value corresponding to the key is another associated array, containing
all options for initialization(via `widget.config`), e.g.:

    Label(0,0):
        text: Text for the Label
        bg: red         # background color
        fg: green       # foreground color

For `Frame` widgets, another option `contains` can be added. The value of this
is another associated array as `widget:` in root section. Therefore you may
nest widgets using Frames:

    Frame(0,0):
        bg: red
        contains:
            Frame(0,0):     # an empty Frame within the red frame
                bg: blue
            Label(1,0):
                text: hello # some text below the blue frame

**NOTICE**: all named widgets, even they are nested in another widget, are
attached to the top parent(the TKYML instance). Their names have to be unique.

### Event Bindings

Specify the events you want to `bind:`
    
    bind:
        widgetName1:
            - click     # bind the click event to `widgetName1`

The event handler will be assumed to be `widgetName1_click`. You need to write
a function and associate it to the TKYML instance. If the callback function
doesn't exist, TKYML will simply do nothing.

### Grids

By default grids are not adjusted when window is resized. You need to configure
grids' rows and columns, and assign them **weights**. To do this, put values
in `grids:` section:

    grids:
        __root__:
            rows:
                0: 
                    weight: 1
                    minsize: 5
            cols:
                0:
                    weight: 1
        customFrame1:
            rows:
                0: { weight: 1, minsize: 5 }

`customFrame1` should correspond to a previously defined Frame widget. The
`__root__` refers to the TKYML instance itself.
