#!/usr/bin/env python
# coding: utf-8

# # Design Review Guide

# [Altium: PCB Review Pre-Checklist](https://resources.altium.com/p/pcb-design-and-review-checklist#before-submitting-your-board-for-pcb-design-review)
# 
# **Required**
# - Validate project/schematic
# - Update PCB from schematic
# - Repour all polygons
# - Pass DRC (design rule check) with no errors

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

# **Find unrouted pads on PCB**
# 
# ```
# (Net='No Net') and (IsPad=True)
# ```

# ## Simulation

# [Altium: How to Simulate a PCB Design](https://resources.altium.com/p/pcb-simulation-software#simulations-during-pcb-layout-and-routing)
#  - Front-end PCB Simulation and Analysis  
#  - Impedance Calculations in PCB Stackup Design
#  - Simulations During PCB Layout and Routing
#  - Post-Layout Simulations
#  - More Advanced PCB Simulations

# ## Decoupling Capacitors

# Resource: [Decoupling Capacitor Calculations](https://resources.altium.com/p/what-size-decoupling-capacitor-should-i-use-my-digital-ics)
# 
# - Use a combination of inrush current calculations and impedance spectrums to minimize PDN impedance

# ```{figure} img/new-caps-z-spectrum.png
# ---
# width: 400px
# ---
# PDN Impedance
# ```

# ## Power Distribution Network

# Goal is to ensure sufficient current and voltage to all loads.
# 
# Requirements:
# - Sufficient copper between sources and loads
# - Capacitor values and placement
# - VIAs sizes
# 
# Tools:
# - [PDN analyzer](https://resources.altium.com/p/the-basics-of-pdn-for-the-pcb-designer)
# - [Saturn PCB Design Toolkit](https://saturnpcb.com/saturn-pcb-toolkit/) 

# In[ ]:




