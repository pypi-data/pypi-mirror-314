# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     cell_metadata_json: true
#     formats: py:percent
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

# %% {"hide_input": false}
from ipywidgets import widgets
from IPython.display import clear_output


# %%
class Foo:
    def __init__(self, x):
        self.x = x
        
    def _repr_html_(self):
        return f"&lt;<b>Foo</b>{self.x}&gt;"


# %%
foo = Foo(10); foo

# %% [markdown]
# <style>
# .ok {
#     background-color: green;
# }
# </style>

# %% [markdown]
# <style>
# .ok {
#     background-color: green;
# }
# </style>

# %%
from IPython.display import display
from IPython.display import HTML as ipython_HTML

import ipywidgets
from ipywidgets import HTML as widgets_HTML


out = widgets.Output(layout={'border': '1px solid black'})
out.append_display_data(ipython_HTML("<b>Question</b><br>Hello"))
out

# %%
import ipywidgets
from ipywidgets import RadioButtons


# %%
r = RadioButtons(
    options=[ipywidgets.HTML(value="<b>a</b>") , '<b>bold</b>', '$\for x \in \mathbb{R}$', 'c'],
    description='radiobuttons')
r

# %%
r.value

# %%
h = widgets.HTML(
    value="Hello <b>World</b>",
    placeholder='Some HTML',
    description='Some HTML',
)
h

# %%
ipywidgets._version.__version__

# %%
t = widgets.ToggleButtons(
    options=[('Slow', 0), ('Regular', 1), ('Fast', 2)],
    description='Speed:',
    disabled=False,
    button_style='', # 'success', 'info', 'warning', 'danger' or ''
    tooltips=['Description of slow', 'Description of regular', 'Description of fast'],
#     icons=['check'] * 3
)
t

# %%
t.value

# %%
s = widgets.SelectMultiple(
    options=['Apples', 'Oranges', 'Pears'],
    value=['Oranges'],
    #rows=10,
    description='Fruits',
    disabled=False
)
s


# %%
def row(desc):
    return widgets.Checkbox(description=desc, value=False, indent=False)

r1, r2, r3 = row('black vs white'), row('wide vs broad'), row('<b>bold</b>')
c = widgets.VBox([r1, r2, r3])

c

# %%
r1.value

# %%
ipywidgets._version.__version__

# %%
widgets_HTML("<b>bold</b>")

# %%
o = widgets.Output(layout={'margin': '10px',
                    'padding': '3px',
                    'border': '0.5px solid #888',
                    'width': 'max-content',
                    })
with o:
    print('\x1b[6;30;42m' + " OK " + '\x1b[0m')
    
o

# %%
o2 = widgets.Output(layout={'margin': '0px',
                            'padding': '0px',
                            'border': '0.5px solid #888',
                            'width': 'max-content',
                            })
with o2:
    display(widgets.HTML('<i class="fa fa-check"></i>'))
    
o2

# %%
c = widgets_HTML('<span class="fa fa-check"></span>', 
             layout={'color': 'red'})
c

# %%
with o2:
    clear_output()
    display(c)
o2.layout.border='5px solid green'

# %%
b = widgets.Button(description="  ") 
b

# %%
b.description="Hey"

# %%
b.description='<span class="fa fa-check"></span>'

# %%
display(b)

# %%
h = widgets.HTML("<i class='fa fa-check'></i>", description="Hey", layout={'margin': '10px'})
h


# %%
h.description

# %%
for k in dir(h):
    try:
        if 'check' in getattr(h, k):
            print(k)
    except:
        pass


# %%
type(dir(h))

# %%
h.value

# %%
h.value="<i class='fa fa-circle'></i>"

# %%
l=type(h.layout)

# %%
isinstance(l, dict)

# %%
c = widgets.HBox(
    [widgets.Checkbox(description="", layout={'width': 'max-content'}), 
     widgets.HTMLMath(r"$$\forall x \in A$$", layout={'width': 'max-content'})],
    layout={'justify-content': 'flex-start'},
)
c

# %%
m = widgets.HTMLMath(value=r"$$\forall x \in A$$"); m

# %%
from IPython.display import display
from ipywidgets import Checkbox, VBox

box1 = Checkbox(False, description='checker')
box2 = Checkbox(False, description='chess')
display(VBox([box1, box2]))

def changed(b):
    if b['name'] == 'value':
        print(b['new'])

box1.observe(changed)
box2.observe(changed)


# %%
import lorem
body = ' '.join(lorem.sentence() for _ in range(5))

# %%
widgets.HTML(body, layout={'width': '200px'})

# %%
widgets.HTMLMath(body, layout={'width': '200px'})

# %%
body_math = body + '$$\exists x \in \mathbb{R}$$' + body

# %%
widgets.HTMLMath(body_math)

# %%
widgets.HTMLMath("$$\exists x \in \mathbb{R}$$")

# %%
widgets.HTML("$$\exists x \in \mathbb{R}$$")

# %%
code = """# a sample Python code

def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n-1)"""

# %%
widgets.HTML(f"<code>{code}</code>")

# %%
widgets.HTML(f"<code><pre>{code}</pre></code>")

# %%
widgets.HTMLMath(f"<code>{code}</code>")

# %%
widgets.HTMLMath(f"<code><pre>{code}</pre></code>")

# %%
widgets.HTMLMath(f"<code><pre>{code}</pre></code>", layout={'width': '100px'})

# %%
from nbautoeval.multiple_choice_test import Chunk, CodeChunk

# %%
Chunk(code, is_code=True).widget()

# %%
Chunk(body).widget()

# %%
Chunk(body, layout_dict={'width': '300px'}).widget()

# %%
from ipywidgets import Layout
Layout(width='100px')

# %%
Chunk('<img src="../media/inria-25.png"></img>').widget()

# %%
dir(h)

# %%
type(h._ipython_display_())

# %%
h.description_tooltip

# %%
h.value

# %%
from ipywidgets import GridBox

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
"""

# %%
widgets.HTML(f"<style>{css}</style>")

# %%
l1, l2, l3, l4 = Chunk("<b>Appel</b>", classes=['center']),Chunk("<b>Attendu</b>"), Chunk("<b>Obtenu</b>"), Chunk("")

# %%
r11 = CodeChunk("percentages('ACGTACGA')")
r12 = CodeChunk("""{ 'A': 37.5,
  'C': 25.0,
  'G': 25.0,
  'T': 12.5}""")
r13 = CodeChunk("""'your code'""")
r14 = Chunk("<b>KO</b>", layout_dict=dict(padding="8px"))

# %%
r21 = CodeChunk("""percentages(
'ACGTACGATCGATCGATGCTCGTTGCTCGTAGCGCT')""")
r22 = CodeChunk("""{ 'A': 16.666666666666668,
  'C': 27.77777777777778,
  'G': 27.77777777777778,
  'T': 27.77777777777778}""")
r23 = CodeChunk(r22.body)
r24 = Chunk("<b>OK</b>", layout_dict=dict(padding="3px"))

# %%
layout = Layout(grid_template_columns='repeat(4, max-content)')

grid_widgets = [x.widget() for x in (l1, l2, l3, l4, r11, r12, r13, r14, r21, r22, r23, r24)]

GridBox(grid_widgets, layout=layout).add_class("row-separator")

# %%
for chunk in (r11, r12, r13, r14): chunk.add_class("red")

# %%
for chunk in (r21, r22, r23, r24): chunk.add_class("green")

# %%
for chunk in (l1, r11, r21): chunk.add_class("right")
