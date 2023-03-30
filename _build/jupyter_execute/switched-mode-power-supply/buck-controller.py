#!/usr/bin/env python
# coding: utf-8

# # Buck Controller

# Find the small signal output voltage to duty ratio $G_{vd}(s)$ and small signal output current to duty ratio $G_{id}(s)$ transfer functions. General form defined as
# \begin{align*}
# G_0 \dfrac{1-\dfrac{s}{w_z}}{1+\dfrac{s}{Qw_0}+ \left(\dfrac{s}{\omega_0} \right)^2} .\\
# \end{align*}
# 

# **Volt-Seconds**

# \begin{align*}
# \langle v_{L}(t)\rangle &= L\frac{d}{dt} \langle i(t)\rangle = 
# \bigg[\bigg(\langle{v_g}(t)\rangle -  \langle i(t)\rangle R_{on} - \langle i(t)\rangle R_L - \langle v(t)\rangle \bigg)d(t) + \bigg( -  \langle i(t)\rangle R_{on} - \langle i(t)\rangle R_L - \langle v(t)\rangle \bigg)d'(t) \bigg] \\[1em]
# \langle v_{L}(t)\rangle &= L\frac{d}{dt} \langle i(t)\rangle = 
# \bigg[\langle{v_g}(t)\rangle d(t) -  \langle i(t)\rangle R_{on} - \langle i(t)\rangle R_L - \langle v(t)\rangle \bigg] \\[1em]
# V_L &= V_g D - I R_{on} - I R_L - V \\[1em]
# V_L &= V_g D - \dfrac{V}{R} R_{on} - \dfrac{V}{R} R_L - V \\[1em]
# \end{align*}

# **Charge Balance**

# \begin{align*}
# \langle i_C (t) \rangle &= 
# C\frac{d}{dt} \langle v(t)\rangle = 
# \bigg[\bigg(\langle i(t)\rangle -\frac{\langle v(t)\rangle}{R} \bigg)d(t) +\bigg(\langle i(t)\rangle -\frac{\langle v(t)\rangle}{R} \bigg)d'(t) \bigg] \\[1em]
# \langle i_C (t) \rangle &= 
# C\frac{d}{dt} \langle v(t)\rangle = 
# \bigg[\langle i(t)\rangle -\frac{\langle v(t)\rangle}{R} \bigg] \\[1em]
# I &= \dfrac{V}{R}
# \end{align*}

# **System Inputs** 

# \begin{align*}
# \dot{x} = \dfrac{d}{dt}
# \begin{bmatrix}
# \langle \hat{i}(t)\rangle \\
# \langle \hat{v}(t)\rangle
# \end{bmatrix} = 
# \begin{matrix}
# \dfrac{1}{L} \\[1em]
# \dfrac{1}{C}
# \end{matrix}
# \begin{bmatrix}
# \langle{v_g}(t)\rangle d(t) -  \langle i(t)\rangle R_{on} - \langle i(t)\rangle R_L - \langle v(t)\rangle \\[1em]
# \langle i(t)\rangle - \dfrac{\langle v(t)\rangle}{R}
# \end{bmatrix} 
# \end{align*}

# ## Linearized Small-Signal Model

# **Derive a linearized small-signal model**

# \begin{align*}
# \dot{\hat{x}}(t) &\approx A \hat{x}(t) + B \hat{u}(t) \\[0.5em]
# \hat{y}(t) &= C \hat{x}(t) + E  \hat{u}(t) 
# \end{align*}
# 
# **where** 
# 
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

# **Find A, B, C, D**
# 
# \begin{align*}
# A = \dfrac{d}{d\hat{x}(t)} f(x(t),u(t))\bigg|_{x=X,u=U} &= 
# \begin{bmatrix}
# \ \ \dfrac{\partial f_1}{\partial x_1} & \dfrac{\partial f_1}{\partial x_2} \ \ \\[1em] 
# \ \ \dfrac{\partial f_2}{\partial x_1} & \dfrac{\partial f_2}{\partial x_2} \ \
# \end{bmatrix}\bigg|_{x,u} = 
# \begin{bmatrix}
# \dfrac{\partial f_1}{\partial \langle \hat{i}(t)\rangle} & \dfrac{\partial f_1}{\partial \langle \hat{v}(t)\rangle} \\[1em] 
# \dfrac{\partial f_2}{\partial \langle \hat{i}(t)\rangle} & \dfrac{\partial f_2}{\partial \langle \hat{v}(t)\rangle}
# \end{bmatrix}\bigg|_{x,u} \\[1em]
# A &= 
# \begin{bmatrix}
# \dfrac{-(R_{on} + R_L)}{L} & \dfrac{-1}{L} \\[1em]
# \dfrac{1}{C} & \dfrac{-1}{RC}
# \end{bmatrix}
# \end{align*}

# \begin{align*} B = \dfrac{d}{d\hat{u}(t)} f(x(t),u(t))\bigg|_{x=X,u=U} &= 
# \begin{bmatrix}
# \dfrac{\partial f_1}{\partial u_1} & \dfrac{\partial f_1}{\partial u_2} \\[1em] 
# \dfrac{\partial f_2}{\partial u_1} & \dfrac{\partial f_2}{\partial u_2}
# \end{bmatrix}\bigg|_{x,u} = 
# \begin{bmatrix}
# \dfrac{\partial f_1}{\partial \hat{d'}(t)} & \dfrac{\partial f_1}{\partial \langle \hat{v_g}(t)\rangle} \\[1em] 
# \dfrac{\partial f_2}{\partial \hat{d'}(t)} & \dfrac{\partial f_2}{\partial \langle \hat{v_g}(t)\rangle}
# \end{bmatrix}\bigg|_{x,u} \\[1em]
# B &= 
# \begin{bmatrix}
# \dfrac{V_g}{L} & \dfrac{D}{L} \\[1em]
# 0 & 0
# \end{bmatrix}
# \end{align*}

# C = 
# \begin{bmatrix}
# 0 & 1  \\
# 1 & 0
# \end{bmatrix}
# 
# E = 
# \begin{bmatrix}
# 0 & 0 \\
# 0 & 0
# \end{bmatrix}

# ## System Outputs in Frequency Domain

# \begin{align*}
# \dot{\hat{x}}(t) &= A \hat{x}(t) + B \hat{u}(t) \\[0.5em]
# \dot{\hat{y}}(t) &= C \hat{x}(t) + D \hat{u}(t) \\[0.5em]
#  \text{Laplace Transform } &\\[0.5em]
# s\hat{x}(s) &= A \hat{x}(s) + B \hat{u}(s) \\[0.5em]
# sI\hat{x}(s) - A \hat{x}(s) &= B \hat{u}(s) \\[0.5em]
# \hat{x}(s) &= \left(sI-A\right)^{-1}B \hat{u}(s) \\[0.5em]
# \hat{y}(s) &= \bigg(C(sI-A)^{-1}B +E \bigg)\hat{u}(s) = G(s) \hat{u}(s)
# \end{align*}

# **Solver** 
# 
# G(s) = 
# \begin{bmatrix}
# G_{id}(s) & G_{ig}(s) \\[1em]
# G_{vd}(s) & G_{vg}(s)
# \end{bmatrix} = 
# \begin{bmatrix}
# V_g \dfrac{RCs+1}{RLCs^2 + (R R_L C + L)s + R +R_L + R_{on}} & 
# D \dfrac{RCs+1}{RRLCs^2 + (R R_L C + L)s + R +R_L + R_{on}} \\[1em]
# R V_g \dfrac{1}{RLCs^2 + (R R_L C + L)s + R +R_L + R_{on}} & 
# R D \dfrac{1}{RLCs^2 + (R R_L C + L)s + R +R_L + R_{on}}
# \end{bmatrix}

# <hr>
# 
# **Small signal output voltage to duty ratio transfer function**
# \begin{align*}
# G_{vd}(s) &= G_0 \dfrac{1-\dfrac{s}{w_z}}{1+\dfrac{s}{Qw_0}+ \left(\dfrac{s}{\omega_0} \right)^2} \\
# G_{vd}(s) &= R V_g \dfrac{1}{RLCs^2 + (R R_L C + L)s + R +R_L + R_{on}}  \\
# \end{align*}

# <hr>
# 
# **Small signal output current to duty ratio transfer function**
# \begin{align*}
# G_{id}(s) &= G_0 \dfrac{1-\dfrac{s}{w_z}}{1+\dfrac{s}{Qw_0}+ \left(\dfrac{s}{\omega_0} \right)^2} \\[1em]
# G_{id}(s) &= V_g \dfrac{RCs+1}{RLCs^2 + (R R_L C + L)s + R +R_L + R_{on}}   \\[1em]
# \end{align*}
