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
from ipywidgets import Layout
Layout(width='100px')

# %%
from ipywidgets import Checkbox
class Foo: pass
foo = Foo()

# %%
c = Checkbox(description='hey')
def closure():
    foo.saved = c.value
c.on_click = closure
    


# %%
c

# %%
foo.saved

# %%
box1

# %%
box1.add_class('wrong')

# %%
widgets.HTML('<style>.wrong{ background-color:red; }</style>')

# %%
box1.description_tooltip = 'I am the tooltop'

# %%
box1.keys

# %%
box1.description

# %%
from ipywidgets import HBox, HTMLMath, Checkbox

# %%
cb = Checkbox()
hm = HTMLMath('$$\forall x\in\mathbb{R}$$')
qq = widgets.HBox([cb, hm]); qq

# %%
hm.description_tooltip= 'HEY'

# %% [markdown]
# # markdown-it

# %%
from ipywidgets import HTMLMath

# %%
from IPython.display import display

from markdown_it import MarkdownIt

# %%
inline = r"the text and $\forall$ right there"

# %%
paragraph = r"""
a paragraph

$$
\forall
$$

and the rest"""

# %%
real = r"""### contents

most contents can be written *in markdown* with `code inside`
<br> and even math $\forall x\in\mathbb{R}$"""

# %%
realspace = r"""### contents

most contents can be written *in markdown* with `code inside`
<br> and even math $ \forall x\in\mathbb{R}$"""

# %%
br = "line1<br>line2"


# %%
def samples(md):
    # for n in "inline", "paragraph", "real", "realspace", "br":
    for n in "br", :
        s = eval(n)
        m = md.render(s)
        print(10*'=', n, '->', m)
        display(HTMLMath(m))


# %%
samples(md := MarkdownIt("default"))

# %%
md.get_active_rules()

# %%
samples(md)

# %%
for rule in md.get_active_rules()['block']:
    if rule != 'paragraph': 
        md.disable(rule)
        samples(md)
        print(f"removing {rule}")


# %%
# md.enable?

