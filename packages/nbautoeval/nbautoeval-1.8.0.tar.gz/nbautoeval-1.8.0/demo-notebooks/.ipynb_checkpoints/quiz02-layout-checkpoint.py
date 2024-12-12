# -*- coding: utf-8 -*-
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
# # more on quizzes 

# %% {"scrolled": true}
# mostly for using under binder or in a devel tree
import sys
sys.path.append('..')

# %% [markdown]
# ## code contents

# %% {"hide_input": false, "scrolled": false}
from nbautoeval import run_yaml_quiz
run_yaml_quiz("quiz02-code", "quiz-demo-code")

# %%
# XXX this is for testing purposes only XXX
from nbautoeval.storage import storage_clear
storage_clear("demo-code-exoname")

# %% [markdown]
# ## under the hood

# %% [markdown]
# Here's the code that defines the above quizzes

# %% {"scrolled": false, "cell_style": "center"}
# !cat yaml/quiz02-code.yaml
