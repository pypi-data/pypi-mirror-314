# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     formats: py:percent
#     notebook_metadata_filter: all,-language_info,-jupytext.text_representation.jupytext_version
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.4
#   kernelspec:
#     display_name: Python 3.7.4 64-bit
#     language: python
#     name: python37464bit1a196ee6e1e94bb2b672007eddde2808
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

# %% {"hide_input": false}
from ipywidgets import widgets
from IPython.display import clear_output


def create_multipleChoice_widget(description, options, correct_answer):
    if correct_answer not in options:
        options.append(correct_answer)
    
    correct_answer_index = options.index(correct_answer)
    
    radio_options = [(words, i) for i, words in enumerate(options)]
    alternativ = widgets.RadioButtons(
        options = radio_options,
        description = '',
        disabled = False
    )
    
    description_out = widgets.Output()
    with description_out:
        print(description)
        
    feedback_out = widgets.Output()

    def check_selection(b):
        a = int(alternativ.value)
        if a==correct_answer_index:
            s = '\x1b[6;30;42m' + "OK" + '\x1b[0m' +"\n" #green color
        else:
            s = '\x1b[5;30;41m' + "KO" + '\x1b[0m' +"\n" #red color
        with feedback_out:
            clear_output()
            print(s)
        return
    
    check = widgets.Button(description="submit")
    check.on_click(check_selection)
    
    
    return widgets.VBox([description_out, alternativ, check, feedback_out])


# %% {"hide_input": true}
Q1 = create_multipleChoice_widget('blablabla',['apple','banana','pear'],'pear')
Q2 = create_multipleChoice_widget('lalalalal',['cat','dog','mouse'],'dog')
Q3 = create_multipleChoice_widget('jajajajaj',['blue','white','red'],'white')

# %% {"hide_input": true}
display(Q1)
display(Q2)
display(Q3)


# %%
# %load_ext autoreload
# %autoreload 2

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
    options=[ipywidgets.HTML(value="<b>a</b>") ,'$\for x \in \mathbb{R}$', 'c'],
    description='radiobuttons')
r

# %%
r.value

# %%
widgets.HTML(
    value="Hello <b>World</b>",
    placeholder='Some HTML',
    description='Some HTML',
)

# %%
ipywidgets._version.__version__

# %%
from nbautoeval.multiple_choice_test import QuizQuestion, Option

# %%
# of course you're going to want to put this in separate files
test1_options = [
    Option("banana"),
    Option("pear"),
    Option("apple", correct=True),
]

display(QuizQuestion("Choose the right fruit", test1_options).widget())
