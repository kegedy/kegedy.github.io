#!/usr/bin/env python
# coding: utf-8

# # Resonance

# In[1]:


# Imports
import numpy as np
import pandas as pd
import sympy as sp
from sympy.utilities.lambdify import lambdify
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
from matplotlib.ticker import LogLocator


# In[2]:


import ipywidgets as widgets
from ipywidgets import HBox, VBox
import numpy as np
from IPython.display import display


# In[3]:


freq_slider = widgets.FloatSlider(
    value=2.,
    min=1.,
    max=10.0,
    step=0.1,
    description='Frequency:',
    readout_format='.1f',
)
freq_slider


# In[ ]:




