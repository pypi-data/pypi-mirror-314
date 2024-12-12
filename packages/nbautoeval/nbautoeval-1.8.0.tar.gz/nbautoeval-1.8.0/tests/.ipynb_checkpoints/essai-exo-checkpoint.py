# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     notebook_metadata_filter: all,-language_info,-jupytext.text_representation.jupytext_version
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
#   toc:
#     base_numbering: 1
#     nav_menu: {}
#     number_sections: true
#     sideBar: true
#     skip_h1_title: false
#     title_cell: Table of Contents
#     title_sidebar: Contents
#     toc_cell: false
#     toc_position: {}
#     toc_section_display: true
#     toc_window_display: false
# ---

# %%
import sys
sys.path.append("..")

# %%
# %load_ext autoreload
# %autoreload 2

# %%
from ipywidgets import Layout, GridBox, HTML

# %%
css = """
.green, .green code {
    background-color: #d6e9ce;
} 
.red, .red code {
    background-color: #efd6d6;
}
.center {
    justify-self: center;
}
.right {
    justify-self: right;
}
.row-separator {
    row-gap: 10px;
}
.span2 {
    grid-column: 3 / span 2;
}
"""

# %%
HTML(f"<style>{css}</style>")

# %%
h = HTML("Hey", style=dict(font_weight='bold'))
h

# %% cell_style="split"
type(h.style)

# %% cell_style="split"
h.style.keys

# %%
layout = Layout(grid_template_columns='repeat(4, max-content)')

grid_widgets = [x.widget() for x in (l1, l2, l3, r11, r12, r13, r14, r21, r22, r23, r24)]

r12.widget().style = dict(font_weight='bold')

GridBox(grid_widgets, layout=layout).add_class("row-separator")

# %%
layout = Layout(grid_template_columns='repeat(4, max-content)')

grid_widgets = [x.widget() for x in (l1, l2, l3, l4, r11, r12, r13, r14, r21, r22, r23, r24)]

r12.widget().style = dict(font_weight='bold')

GridBox(grid_widgets, layout=layout).add_class("row-separator")

# %%
for chunk in (r11, r12, r13, r14): chunk.add_class("red")

# %%
for chunk in (r21, r22, r23, r24): chunk.add_class("green")

# %%
for chunk in (l1, r11, r21): chunk.add_class("center")

# %% [markdown]
# ********
# ********
# ********

# %%
#from nbautoeval.multiple_choice_test import *
#from nbautoeval.renderer import *

# %%
from nbautoeval import Renderer, PPrintRenderer
default_renderer = Renderer()

PythonArea(list(range(5)), default_renderer).widget()

# %%
str_renderer = Renderer()

PythonArea(list(range(5)), str_renderer).widget()

# %%
r22bis = Area("$$\exists x \in \mathbb{R}$$"); r22bis.widget()

# %%
pretty_renderer = PPrintRenderer(width=40)
r23bis = PythonArea(list(range(20)), pretty_renderer); r23bis.widget()

# %%
layout = Layout(grid_template_columns='repeat(4, max-content)')

grid_widgets = [x.widget() for x in (l1, l2, l3, l4, r11, r12, r13, r14, r21, r22bis, r23bis, r24)]

r12.widget().style = dict(font_weight='bold')

g = GridBox(grid_widgets, layout=layout).add_class("row-separator"); g

# %%
for w in g.children[8:]: w.add_class('green')

# %%
import pprint

# %%
pprint.pprint({'a': 1, 'b': 2, 'c': 3, 'd': 4}, width=20, compact=True, indent=2)

# %%
HTML("<span class=red style='font-size:50px;'>Hey there</span>")

# %%
HTML("<span style='font-size:50px;'><span class='red'>Hey there</span></span>")

# %%
Area

# %%
Area("hey").widget()

# %%
obj = {'C': 27.77777777777778, 'A': 16.666666666666668, 'G': 27.77777777777778, 'T': 27.77777777777778}
from nbautoeval import PPrintRenderer

# %%
PPrintRenderer(width=30).render(obj)

# %%
import numpy as np
from matplotlib.pyplot import imshow

# %%
a = np.zeros(9).reshape((3,3))
a[0,0] = 1

# %%
w=imshow(a)

# %%
from ipywidgets import HBox, Image, Output

# %%
# HBox([Image(value=w)])

# %%
display(w)

# %%
# display?

# %%
hasattr(w, '_repr_html_')

# %%
# Image?

# %%
[x for x in dir(w) if 'url' in x.lower()]

# %%
w._url

# %%
display(w)

# %%
o = Output(); o

# %%
with o:
    imshow(a)

# %%
h = HTML('<span style="display: flex">foo</span>')
h.style.display
GridBox([h,h,h,h], layout={'grid_template_columns': 'repeat(4, 1fr)'})

# %%
import html3


# %%
dir(html3)

# %%
help(html3)

# %%
import dominate

# %%
from dominate.tags import div, span

# %%
box = div(cls="correction")
with box:
    for i in range(4):
        with span(f"item {i+1}"):
            pass


# %%
box.render(pretty=False)

# %%
from ipywidgets import HTML, HTMLMath
from myst_parser.main import to_html

# %%
raw = r"**bold** and $\forall$"; raw

# %% cell_style="split"
HTML(raw)

# %% cell_style="split"
HTMLMath(raw)

# %%
aftermd = to_html(raw); aftermd

# %% cell_style="split"
HTML(aftermd)

# %% cell_style="split"
HTMLMath(aftermd)

# %%
# to_html?

# %%
from myst_parser.main import default_parser
parser = default_parser("html")
parser.disable("math_single").disable("math_inline")
parser.get_active_rules()

# %%
aftermd2 = parser.render(raw); aftermd2

# %% cell_style="split"
HTML(aftermd2)

# %% cell_style="split"
HTMLMath(aftermd2)

# %%
from ipywidgets import Layout, HBox, VBox, Checkbox, Button, HTML, HTMLMath, Text, Label

# %%
feedback_area = VBox([HBox([HTML("<span>question</span>"), 
                            HTML("<span class='right'>right</span><span class='wrong'>wrong</span>")])])

feedback_area

# %%
div_wid = feedback_area.children[0].children[1]

# %%
div_wid.value = "<span class='right'>right</span><span class='wrong'>updated</span>"

# %% [markdown]
# # Outputs

# %%
tmpfile = "nba-image.png"

# %% [markdown]
# <img src='file:///tmp/nba-image.png'>

# %% tags=[]
from ipywidgets import Image, HBox, HTML

def convenience():
    with open(tmpfile, 'rb') as feed:
        image_bytes = feed.read()
    result = Image(value=image_bytes, format='png',
                   width='300px',
                   layout={})
    return result

o1, o2 = convenience(), convenience()

h = HBox([o1, o2])
h

# %%
import numpy as np
from matplotlib.pyplot import imshow

a1 = np.array([[1, 2], [3, 4]])
a2 = np.array([[1, 2], [3, 5]])

o1.append_display_data(imshow(a1))

# %%
with o2:
    imshow(a2)


# %%
def checkers(size):
    """
    Un damier
    le coin (0, 0) vaut 0
    """
    I, J = np.indices((size, size))
    return (I + J) % 2



# %%
from matplotlib.pyplot import imshow

# %%
imshow(checkers(3))

# %%
