#!/usr/bin/env python
# coding: utf-8

# # Impedance Transformation

# ## Quality Factor

# \begin{align*}
# Q_s &= \dfrac{|X_s|}{R_s}  \\[1em]
# Q_P &= \dfrac{R_p}{|X_p|} \\[1em]
# \end{align*}

# ## Series to Parallel

# ```{figure} impedance-transformation/impedance-transformation.jpg
# :width: 350px
# Series to Parallel Conversion
# ```

# **R & C**
# 
# \begin{align*}
# Q_s &= \dfrac{1}{\omega C_s R_s}\\[1em]
# Q_P &= \dfrac{\omega C_p R_p}{1} \\[1em]
# \end{align*}

# **Equate Impedances**
# 
# \begin{align*}
# R_s + \dfrac{1}{j\omega C_s} &= R_p \parallel \dfrac{1}{j\omega C_p} \\[1em]
# \dfrac{j\omega R_s C_s + 1}{j\omega C_s} &= \dfrac{\dfrac{R_p}{j\omega C_p}}{R_p + \dfrac{1}{j\omega C_p}} \\[1em]
# \dfrac{j\omega R_s C_s + 1}{j\omega C_s} &= \dfrac{\dfrac{R_p}{j\omega C_p}}{\dfrac{j\omega R_p C_p + 1}{j\omega C_p}} \\[1em]
# \dfrac{j\omega R_s C_s + 1}{j\omega C_s} &= \dfrac{R_p}{j\omega R_p C_p + 1} \\[1em]
# -\omega^2 R_s C_s R_p C_p & + j \omega R_s C_s + j \omega R_P C_p + 1 = j \omega R_p C_s \\[1em]
# \text{equate real} &  \text{ and imaginary}  \\[1em]
# \omega^2 R_s C_s R_p C_p = 1 \ \ & \text{ & } \ \
# R_s C_s + R_P C_p - R_p C_s = 0 \\[1em]
# \cdots \\[1em]
# R_p &= (Q_s^2 + 1)R_s \\[1em]
# C_p &= \dfrac{Q_s^2}{Q_s^2+1}
# \end{align*}

# **R & L**

# \begin{align*}
# Q_s &= \dfrac{\omega L_s}{ R_s}\\[1em]
# Q_P &= \dfrac{R_p}{\omega L_p} \\[1em]
# \end{align*}

# **Equate Impedances**
# 
# \begin{align*}
# R_s + j\omega L_s &= R_p \parallel j\omega L_p \\[1em]
# R_s + j\omega L_s  &= \dfrac{j\omega R_p L_p}{R_p + j\omega L_p} \\[1em]
#   &= \dfrac{j\omega R_p L_p}{R_p + j\omega L_p} \dfrac{R_p - j\omega L_p}{R_p - j\omega L_p}\\[1em]
#   &= \dfrac{(\omega L_p)^2 R_p + j\omega L_p R_p^2}{R_p^2 + \omega^2 L_p^2}\\[1em]
#   \text{equate real} &  \text{ and imaginary}  \\[1em]
#   \cdots  \\[1em]
# R_p &= (Q_s^2 + 1)R_s \\[1em]
# C_p &= \dfrac{Q_s^2}{Q_s^2+1}
# \end{align*}

# **Thus, as long as $Q_s^2 \gg 1$ then** 
# 
# \begin{align*}
# R_p &\approx Q_s^2 R_s \\[1em]
# C_p &\approx C_s
# \end{align*}

# In[ ]:




