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
from nbautoeval.multiple_choice_test import Chunk, CodeChunk

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
HTML(f"<style>{css}</style>")

# %%
h = HTML("Hey", style=dict(font_weight='bold'))
h

# %% cell_style="split"
type(h.style)

# %% cell_style="split"
h.style.keys

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

r12.widget().style = dict(font_weight='bold')

GridBox(grid_widgets, layout=layout).add_class("row-separator")

# %%
for chunk in (r11, r12, r13, r14): chunk.add_class("red")

# %%
for chunk in (r21, r22, r23, r24): chunk.add_class("green")

# %%
for chunk in (l1, r11, r21): chunk.add_class("right")

# %% [markdown]
# ********
# ********
# ********

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
ta = Textarea(value="# template\ndef fact(n):\n    'your-code'", layout=dict(width='auto'))
button = Button(description="click me")
GridBox([ta, button])

# %% [markdown]
# ********
# ********
# ********
