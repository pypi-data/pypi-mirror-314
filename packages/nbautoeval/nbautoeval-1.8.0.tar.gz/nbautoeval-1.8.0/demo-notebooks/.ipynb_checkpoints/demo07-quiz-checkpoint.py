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

# %% [markdown]
# # some quizzes 

# %%
# mostly for using under binder or in a devel tree
import sys
sys.path.append('..')

# %%
# for convenience in development
# %load_ext autoreload
# %autoreload 2

# %% [markdown]
# ## here we go
#
# in this notebook the correct answers are always the one starting with 'a'

# %%
# I hate importing * too, but let's keep it simple
from exercises.quizzes import *

# %% {"hide_input": true}
# basic single-answer

test_basic_single.display()

# %% {"hide_input": true}
# basic multiple-answers

test_basic_multiple.display()

# %% {"hide_input": true}
# by default options get shuffled
# this can be turned off with shuffle=False

test_unshuffle.display()

# %% {"hide_input": true}
# it's possible to select multiple-answers mode even if there's one correct answer

test_force_multiple.display()

# %% {"hide_input": true}
# it's possible to select multiple-answers mode even if there's one correct answer

test_none.display()

# %% {"hide_input": true}
test_code.display()

# %% {"hide_input": true}
test_code_multi.display()

# %% {"hide_input": true}
test_vertical.display()

# %%
# test_math.display()

# %% [markdown]
# ## under the hood

# %%
# !cat ../exercises/quizzes.py
