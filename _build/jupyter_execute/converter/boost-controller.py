#!/usr/bin/env python
# coding: utf-8

# # Boost Controller

# ## Dynamic Modeling

# ### Averaged Inductor Current $\langle i(t) \rangle$ and Averaged Capacitor Voltage $\langle v(t) \rangle$ 

# **Volt-Seconds**

# $$\begin{align*}
# \langle v_{L}(t)\rangle = L\frac{d}{dt} \langle i(t)\rangle &= 
# \bigg[\bigg(\langle{v_g}(t)\rangle-\langle i(t)\rangle R_{on} \bigg)d(t) + \bigg( \langle{v_g}(t)\rangle-\langle i(t)\rangle R_{on} - \langle v(t)\rangle \bigg)d'(t) \bigg] \\[0.5em]
# \langle v_{L}(t)\rangle = L\frac{d}{dt} \langle i(t)\rangle &= 
# \bigg[\langle{v_g}(t)\rangle-\langle i(t)\rangle R_{on} - \langle v(t)\rangle d'(t) \bigg] \\[0.5em]
# \frac{d}{dt} \langle i(t)\rangle &= 
# \begin{matrix}
# \dfrac{1}{L} \\[1em]
# \end{matrix} 
# \bigg[\langle{v_g}(t)\rangle-\langle i(t)\rangle R_{on} - \langle v(t)\rangle d'(t) \bigg] \\[0.5em]
# \end{align*}$$

# **Charge Balance**

# $$
# \begin{align*}
# \langle i_C (t) \rangle = 
# C\frac{d}{dt} \langle v(t)\rangle &= 
# \bigg[\bigg(\dfrac{-\langle v(t)\rangle}{R}\bigg)d(t) +\bigg(\langle i(t)\rangle -\frac{\langle v(t)\rangle}{R} \bigg)d'(t)\bigg] \\[1em]
# \langle i_C (t) \rangle = 
# C\frac{d}{dt} \langle v(t)\rangle &= 
# \bigg[\dfrac{-\langle v(t)\rangle}{R} + \langle i(t)\rangle d'(t) \bigg] \\[1em]
#  \frac{d}{dt} \langle v(t)\rangle &= 
# \begin{matrix}
# \dfrac{1}{C} \\[1em]
# \end{matrix}
# \bigg[\dfrac{-\langle v(t)\rangle}{R} + \langle i(t)\rangle d'(t) \bigg] \\[1em]
# \end{align*}
# $$

# **Differential Solution** 

# Given  $\ x = 
# \begin{bmatrix}
# \langle i(t)\rangle \\
# \langle v(t)\rangle
# \end{bmatrix}$, 
# u = 
# $\begin{bmatrix}
# d(t) \\
# \langle v_g(t)\rangle
# \end{bmatrix}$ 
# 
# $$
# \begin{align*}
# \dot{x} &= f(x(t),u(t)) = \dfrac{d}{dt}
# \begin{bmatrix}
# \langle i(t)\rangle \\[1em]
# \langle v(t)\rangle
# \end{bmatrix} = 
# \begin{matrix}
# \dfrac{1}{L} \\[0.5em]
# \dfrac{1}{C}
# \end{matrix}
# \begin{bmatrix}
# \langle{v_g}(t)\rangle-\langle i(t)\rangle R_{on} - \langle v(t)\rangle d'(t) \\[1em]
# \dfrac{-\langle v(t)\rangle}{R} + \langle i(t)\rangle d'(t)s
# \end{bmatrix} \\[0.5em]
# \end{align*}$$

# ### Linearized Small-Signal Model

# **Derive a linearized small-signal model**

# $$
# \begin{align*}
# \dot{\hat{x}}(t) &\approx A \hat{x}(t) + B \hat{u}(t) \\[0.5em]
# \hat{y}(t) &= C \hat{x}(t) + E  \hat{u}(t) 
# \end{align*}
# $$
# 
# **where** 
# 
# $$
# \begin{matrix}
# x(t) = \hat{x}(t) + X && X = 
# \begin{bmatrix}
# I \\
# V
# \end{bmatrix} \\[0.5em] 
# u(t) = \hat{u}(t) + U && U = 
# \begin{bmatrix}
# D \\
# V_g 
# \end{bmatrix}
# \\[0.5em]
# \end{matrix}
# $$

# **Volt-Seconds (Large Signal)**
# 
# $$\begin{align*}
# \langle v_{L}(t)\rangle &= L\frac{d}{dt} \langle i(t)\rangle = 
# \bigg[\langle{v_g}(t)\rangle-\langle i(t)\rangle R_{on} - \langle v(t)\rangle d'(t) \bigg]  = 0\\[0.5em]
# 0 &=  V_g - I R_{on} - VD'   \\[0.5em]
# VD' &= V_g - I R_{on} \\[0.5em]
# V &= \dfrac{V_g - I R_{on}}{D'} \bigg|_{I = \dfrac{V}{D'R} }  \\[0.5em]
# V &= \dfrac{V_g - \dfrac{V}{D'R} R_{on}}{D'} \\[0.5em]
# V &= \dfrac{V_g}{D'}\cdot \dfrac{1}{1+\dfrac{ R_{on}}{D'^2 R}} \\[0.5em]
# \end{align*}$$

# **Charge Balance (Large Signal)**
# 
# $$\begin{align*}
# \langle i_C (t) \rangle &= 
# C\frac{d}{dt} \langle v(t)\rangle = 
# \bigg[\dfrac{-\langle v(t)\rangle}{R} + \langle i(t)\rangle d'(t) \bigg] = 0\\[1em]
# 0 &=\dfrac{-V}{R} + I D' \\[1em]
# I &= \dfrac{V}{D'R} \\[1em]
# I &= \dfrac{1}{D'R}\cdot \frac{V_g}{D'}\cdot \dfrac{1}{1+\dfrac{ R_{on}}{D'^2 R}} \\[1em]
# I &= \frac{V_g}{D'^2 R}\cdot \dfrac{1}{1+\dfrac{ R_{on}}{D'^2 R}} \\[1em]
# \end{align*}$$

# **Find A, B, C, D**

# $A = \dfrac{d}{d\hat{x}(t)} f(x(t),u(t))\bigg|_{x=X,u=U} = $  
# 
# $\begin{bmatrix}
# \dfrac{\partial f_1}{\partial x_1} & \dfrac{\partial f_1}{\partial x_2} \\[.5em] 
# \dfrac{\partial f_2}{\partial x_1} & \dfrac{\partial f_2}{\partial x_2}
# \end{bmatrix} = 
# \begin{bmatrix}
# \dfrac{\partial f_1}{\partial \langle \hat{i}(t)\rangle} & \dfrac{\partial f_1}{\partial \langle \hat{v}(t)\rangle} \\[.5em] 
# \dfrac{\partial f_2}{\partial \langle \hat{i}(t)\rangle} & \dfrac{\partial f_2}{\partial \langle \hat{v}(t)\rangle}
# \end{bmatrix} = 
# \begin{bmatrix}
# \dfrac{-R_{on}}{L} & \dfrac{-D'}{L} \\[.5em]
# \dfrac{D'}{C} & \dfrac{-1}{RC}
# \end{bmatrix}
# $

# $ B = \dfrac{d}{\partial{\hat{u}(t)}} f(x(t),u(t))\bigg|_{x=X,u=U} =  $  
# 
# $\begin{bmatrix}
# \dfrac{\partial f_1}{\partial u_1} & \dfrac{\partial f_1}{\partial u_2} \\[0.5em] 
# \dfrac{\partial f_2}{\partial u_1} & \dfrac{\partial f_2}{\partial u_2}
# \end{bmatrix} = 
# \begin{bmatrix}
# \dfrac{\partial f_1}{\partial \hat{d}(t)} & \dfrac{\partial f_1}{\partial \langle \hat{v_g}(t)\rangle} \\[1.5em] 
# \dfrac{\partial f_2}{\partial \hat{d}(t)} & \dfrac{\partial f_2}{\partial \langle \hat{v_g}(t)\rangle}
# \end{bmatrix} =$
# $\begin{bmatrix}
# \dfrac{V}{L} & \dfrac{1}{L} \\[0.5em]
# \dfrac{-I}{C} & 0
# \end{bmatrix} = 
# \begin{bmatrix}
# \dfrac{V_g}{D'L}\cdot \dfrac{1}{1+\dfrac{ R_{on}}{D'^2 R}} & \dfrac{1}{L} \\[0.5em]
# \dfrac{-V_g}{D'^2 RC}\cdot \dfrac{1}{1+\dfrac{ R_{on}}{D'^2 R}} & 0
# \end{bmatrix} $

# $C = 
# \begin{bmatrix}
# 0 & 1  \\
# 1 & 0
# \end{bmatrix}$
# 
# $E = 
# \begin{bmatrix}
# 0 & 0 \\
# 0 & 0
# \end{bmatrix}$

# ### System Outputs in Frequency Domain

# $\begin{align*}
# \dot{\hat{x}}(t) &= A \hat{x}(t) + B \hat{u}(t) \\[0.5em]
# \dot{\hat{y}}(t) &= C \hat{x}(t) + D \hat{u}(t) \\[0.5em]
#  \text{Laplace Transform } &\\[0.5em]
# s\hat{x}(s) &= A \hat{x}(s) + B \hat{u}(s) \\[0.5em]
# sI\hat{x}(s) - A \hat{x}(s) &= B \hat{u}(s) \\[0.5em]
# \hat{x}(s) &= \left(sI-A\right)^{-1}B \hat{u}(s) \\[0.5em]
# \hat{y}(s) &= \bigg(C(sI-A)^{-1}B +E \bigg)\hat{u}(s) = G(s) \hat{u}(s)
# \end{align*}$

# **Solver** 
# 
# $G(s) = 
# \begin{bmatrix}
# G_{id}(s) & G_{ig}(s) \\[1em]
# G_{vd}(s) & G_{vg}(s)
# \end{bmatrix} = 
# $

# In[ ]:




