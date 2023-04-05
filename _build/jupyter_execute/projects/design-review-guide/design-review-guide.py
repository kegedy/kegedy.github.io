#!/usr/bin/env python
# coding: utf-8

# # Design Review Guide

# [Altium: PCB Review Pre-Checklist](https://resources.altium.com/p/pcb-design-and-review-checklist#before-submitting-your-board-for-pcb-design-review)
# 
# **Required**
# - Validate project/schematic
# - Update PCB from schematic
# - Repour all polygons
# - Pass DLR (design rule report) with no errors

# ## Altium PCB Filter

# [Altium Designer Query Language](https://www.altium.com/documentation/altium-designer/working-with-the-query-language#!pcb_filter_panel)

# **Check assembly text is oriented correctly**
# 
# ```
# IsText and OnLayer('ASM  Top') and  (Rotation = 180000)
# ```

# **Find traces of desired widths on a given layer**
# 
# ```
# (OnLayer('L1') or OnLayer('L2')) and IsTrack and (Width > 0.381)
# ```

# ## Simulation

# [Altium: How to Simulate a PCB Design](https://resources.altium.com/p/pcb-simulation-software#simulations-during-pcb-layout-and-routing)
#  - Front-end PCB Simulation and Analysis  
#  - Impedance Calculations in PCB Stackup Design
#  - Simulations During PCB Layout and Routing
#  - Post-Layout Simulations
#  - More Advanced PCB Simulations

# In[ ]:




