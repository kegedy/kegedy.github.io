#!/usr/bin/env python
# coding: utf-8

# # Controller Requirements

# ## Plant Approximation

# **Second Order System**
# 
# \begin{align*}
# P(s) = K\dfrac{\omega_0^2}{s^2 + 2\zeta \omega_0 s + \omega_0^2}
# \end{align*}

# ## Convert Time Requirements
# 
# Given
# - $t_r$ rise time  
# - $t_p$ peak time  
# - $t_s$ settling time  

# **Use given phase margin (or calculate) to solve for $\zeta$.**  
# 
# \begin{align*}
#  M_p &= \dfrac{\text{overshoot}}{V_{ref}} \dfrac{[V]}{[V]}\ \text{ [unitless]} \\[1em]
#  M_p &= e^{-\bigg(\dfrac{\pi \zeta}{\sqrt{1-\zeta^2}}\bigg)}
# \end{align*}

# **Use $\zeta$ to solve for $\omega_0$.**
# 
# \begin{align*}
#  t_r &= \dfrac{\pi - \tan^{-1}\bigg(\sqrt{\frac{1-\zeta^2}{\zeta}}\bigg)}{\omega_0 \sqrt{1-\zeta^2}} 
#  \approx \dfrac{5}{3 \omega_0 \sqrt{1-\zeta^2}} \\[1em]
#  t_p &= \dfrac{\pi}{\omega_0 \sqrt{1-\zeta^2}}
# \end{align*}

# **Solve for $\omega_n$ based on settling requirements**
# 
# \begin{align*}
#  \text{[2% of $V_{ref}$] }\ \ t_s &= \dfrac{4}{\zeta \omega_n}  \\[1em]
#  \text{[5% of $V_{ref}$] }\ \ t_s &= \dfrac{3}{\zeta \omega_n}
# \end{align*}

# ## Controller Properties

# Open Loop general design:
# - $C(s)$ should have high gain such that $ |C(s) \cdot P(s) | $ has high gain at frequencies where disturbance is present
# - $C(s)$ should have low gain such that $|C(s) \cdot P(s) |$ has low gain at frequencies where noise is present
# 
# Step 1. Integral Controller 
# \begin{align*}
# C(s) = \dfrac{K_1}{s}
# \end{align*}
# 
# Step 2. Proportional Integral (PI) Controller
# - Add zero immediately after gain cross frequency $\omega_c$
# 
# \begin{align*}
# C(s) &= K_p + \dfrac{K_i}{s} \\[1em]
#  &= \dfrac{sK_p+K_i}{s} \\[1em]
#  &= K_1\dfrac{s/\alpha+1}{s}
# \end{align*}

# ## Check Design

# Bode response should have the following properties
# 
# \begin{align*}
# \text{PM (deg)} &= \bigg[\tan^{-1}\bigg(\frac{2\zeta}{\sqrt{1-2\zeta^2}}\bigg) \bigg] \cdot \dfrac{180}{\pi} \\[1em]
# \omega_c \text{ (rad)} &= \omega_0 \sqrt{1-2\zeta^2}
# \end{align*}

# ```{figure} controller-requirements/matlab-margin.png
# ```
# 
# [MATLAB Bode Response](https://www.mathworks.com/help/control/ref/dynamicsystem.margin.html):
# MATLAB defines multiple cross over frequencies. The gain crossover frequency we're interested in is Wcp.

# In[ ]:




