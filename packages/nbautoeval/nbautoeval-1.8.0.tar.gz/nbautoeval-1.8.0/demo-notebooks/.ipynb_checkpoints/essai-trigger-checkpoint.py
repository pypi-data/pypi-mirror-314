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
from ipywidgets import Text, Textarea, GridBox, Button

# %%
t = Textarea(value="# template\n", layout=dict(width='auto'))

def spy(event):
    if event['type'] not in ('change', ):
        return
    if event['name'] not in ('value', ):
        return
    print(event)
        

t.observe(spy)

# %%
t

# %% [markdown]
# ********
# ********
# ********

# %%
GridBox([Textarea(layout=dict(width='auto')), Button(description="click me")])

# %%
ta = Textarea(value="# template\ndef fact(n):\n    return 'your-code'", layout=dict(width='auto'))
button = Button(description="click me")
def clicked(*args):
    print(args)
button.on_click = clicked
GridBox([ta, button])


# %%
from ipywidgets import Checkbox

# %%
c = Checkbox(description='c')
def changed(event):
    if event['name'] != 'value':
        return
    print(f"event={event}, value={event['owner'].value}")

c.observe(changed)
c

# %%
c.value = True


# %%
def click2(*_):
    c.value = not c.value
    
#b = HTML(value="<span style='font-size:6px'>b</span>")
b = Button(
    description="o")
b.on_click(click2)
b

# %%
b.style.button_colortton_color = 'blue'

# %%
from nbautoeval.content import MarkdownContent

# %%
c = MarkdownContent("""# a title""").add_layout(dict(display="none"))
w = c.widget(); w

# %%
w.layout.display = "block"

# %%

# %%
css = """
--global-var: red;

.foo {
   background-color: var(--global-var);
}"""


# %%
HTML(f"<style>{css}</style>")

# %%
c2 = MarkdownContent("""# a title""").add_class("foo")
c2.widget()
