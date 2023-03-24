#!/usr/bin/env python
# coding: utf-8

# # Coupled Resonators and Voltage Rectification

# ## Topics

# - Mutual inductance of two shielded-loop resonators
# - Effects of distance and alignment on mutual inductance
# - Critical coupling distance
# - Full-wave bridge rectifiers

# ```{figure} img/complete-circuit-model.png
# Coupled Shielded-Loop Resonator with Load
# ```

# ## Calculating Mutual Inductance

# ```{figure} img/axially-aligned-coupled-loops.png
# Mutual Inductance for Axially Aligned Coupled Loops
# ```

# $$
# \begin{align*}
# M = \mu \sqrt{r_1 r_2}\bigg((\dfrac{2}{k} - k)\ K(k) - \dfrac{2}{k}E(k) \bigg)
# \end{align*}
# $$  
# 
# where $K(k)$ is the complete elliptical integral with radius $r_1$ and $E(k)$ is the complete elliptical integral with radius $r_2$.
# 
# $$
# \begin{align*}
# K(k) &= \int_{0}^{\frac{\pi}{2}} \dfrac{d \beta}{\sqrt{1-k^2 sin^2 \beta}} \\[0.5em]
# E(k) &= \int_{0}^{\frac{\pi}{2}} d\beta \sqrt{1-k^2 sin^2 \beta} \\[0.5em]
# k &= \sqrt{\dfrac{4r_1 r_2}{(r_1 + r_2)^2 + d^2}}
# \end{align*}
# $$  

# ## Input Impedance of Coupled Shielded-Loop Resonators

# At resonance, the input impedance to the coupled shielded-loop simplifies to
# 
# $$
# \begin{align*}
# Z_{in} &= \dfrac{v_x}{i_1} = R_1 + j\bigg(\omega L_1 - \dfrac{1}{\omega C_1} \bigg) + \dfrac{(\omega M)^2}{R_2 + R_L + j\bigg(\omega L_2 - \dfrac{1}{\omega C_2} \bigg)} \bigg|_{\ \omega \ = \ \omega_0} \\[0.5em]
# Z_{in}(\omega_0) &= R_{in}(\omega_0) = R_1 + \dfrac{(\omega_0 M)^2}{R_2 + R_L} 
# \end{align*}
# $$

# ## Feedline Effects

# The load impedance $Z_L$ is designed to the characteristic impedance $Z_0$ of the transmission line to eliminate feedline effect and reduce the circuit model.
# 
# $$Z_L = Z_0 = 50 \Omega$$

# ```{figure} img/impedance-simplification.png
# Mutual Inductance for Axially Aligned Coupled Loops
# ```

# ## Weak, Critical and Strong Coupling

# Isolated loop resonance occurs when
# 
# $$\omega = \omega_0 = \dfrac{1}{\sqrt{LC}} $$

# Coupled loop resonance also occurs when
# 
# $$\bigg(\omega L - \dfrac{1}{\omega C} \bigg)^2 = (\omega M)^2 - (R + R_L)^2 $$

# Solving this quadratic equation results in multiple solutions depending on the mutual inductance and/or distance.  
# 
# **Strong coupling**
# $$\omega M > R + R_L$$
# 
# - Odd mode solution: resonance is slightly less than $\omega_0$ and the currents in the coupled loops are 180° out-of-phase
# - Even mode solution: resonance is slightly greater than $\omega_0$ and the currents in the coupled loops are in-phase
# - Resonant frequency $\omega_0$, the current in the load loop leads that of the source loop by approximately 90°

# **Critical coupling**
# 
# $$\omega M = R + R_L$$
# 
# The even and odd mode frequencies merge into the resonant frequency $\omega_0$

# **Weak coupling**
# 
# $$\omega M < R + R_L$$
# 
# In weak coupling, there is only one resonant frequency $\omega_0$

# ## Power Transfer

# The power transfer efficiency of a wireless power transfer system is the ratio of power delivered to the
# load $P_L$ and the power available from the source $P_A$.

# $$P_A = \dfrac{|V_S|^2}{8Re\{Z_S\}}$$
# 
# - $Z_S$ characteristic impedance of the voltage source where $Re\{Z_S\} = R_S$
# - $V_S$ peak voltage of the source
# - $P_A$ power available from the source if the source impedance is terminated in an impedance equal to its complex conjugate

# For a system operating at critical or weak coupling, the power transfer efficiency is  
# 
# $$\eta = \dfrac{4R_L^2(\omega_0 M)^2}{\bigg((R+R_L)^2 + (\omega_0 M)^2\bigg)^2}$$

# For a system operating at strong coupling, the power transfer efficiency is  
# 
# $$\eta = \dfrac{R_L^2}{(R+R_L)^2}$$

# ## Voltage Rectification

# In[ ]:




