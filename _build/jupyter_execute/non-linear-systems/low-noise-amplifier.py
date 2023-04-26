#!/usr/bin/env python
# coding: utf-8

# # Low Noise Amplifier

# ```{figure} low-noise-amplifier/inductive-degeneration.jpg
# :width: 250px
# Inductive Degeneration
# ```

# Looking at the gate of the LNA, a test voltage is applied to find the input impedance.  
# *Exclude the additional capacitance between the gate and source.*

# \begin{align*}
# Z_{in} &= \dfrac{1}{sC_{gs}} + L_1 s + \dfrac{g_m L_1}{C_{gs}}
# \end{align*}

# At resonance, the third term provides a real impedance that is matched to the source impedance $R_s$ ($50 \Omega$). This is simplified given $\omega_T \approx \dfrac{g_m}{C_{gs}}$.

# \begin{align*}
# Re(Z_{in}) &= \dfrac{g_m L_1}{C_{gs}} \\[1em]
# R_s &\approx L_1 \omega_T \\[1em]
# L_1 &\approx \dfrac{R_s}{\omega_T} = \dfrac{50}{2\pi \cdot 110G} \\[1em]
# L_1 &= 72 pH
# \end{align*}

# As a designer, there are two issues with this value.
# 
# 1. It cannot be implemented with most PDKs. Inductors on chip are planar (2D) and have limited range.
# 2. It doesn't resonant well due to small capacitance $C_{gs}$.
# 
# 
# However, it is possible to add a small capacitor in parallel with $C_{gs}$ such that $C_{tot} = C_{gs} + C_{gs}'$.  
# 
# The input impedance is now  
# 
# \begin{align*}
# Z_{in} &= \dfrac{1}{sC_{tot}} + L_1 s + \dfrac{g_m L_1}{C_{tot}}
# \end{align*}

# **Remaining Steps** 
# 
# Pick minimum value for $L_1$ that exists in the PDK and has sufficient $Q$. Then, perform ac small signal analysis to find input impedance and slowly increase $C_{gs}'$. 

# In[ ]:




