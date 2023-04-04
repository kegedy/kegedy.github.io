#!/usr/bin/env python
# coding: utf-8

# # Design Review Guide

# [Altium: PCB Review Pre-Checklist](https://resources.altium.com/p/pcb-design-and-review-checklist#before-submitting-your-board-for-pcb-design-review)
# 
# **Required**
# - Validate project/schematic
# - Update PCB from schematic
# - Repour all polygons
# - Check design rule report passes with no errors

# ## Altium PCB Filter

# [Altium Designer Query Language](https://www.altium.com/documentation/altium-designer/working-with-the-query-language#!pcb_filter_panel)

# ### Check assembly text is oriented correctly
# 
# ```
# IsText and OnLayer('ASM  Top') and  (Rotation = 180000)
# ```

# ### Find traces of desired widths on a given layer
# 
# ```
# (OnLayer('L1') or OnLayer('L2')) and IsTrack and (Width > 0.381)
# ```
