#!/usr/bin/env python
# coding: utf-8

# # Bandgap Reference
# 
# The need for temperature-independent references are essential for modern applications and rapidly changing environments. This article discusses the negative and positive temperature coefficients (TC) of a bipolar device and how to cancel their effects to create a stable reference.
# 

# ## CTAT: Complementary to Absolute Temperature

# For a bipolar device, the forward voltage of a *pn*-junction diode exhibits a negative TC.
# 
# $$
# \begin{align*}
# I_C &= I_s\ e^{(V_{BE}/V_T)} \text{ where } V_T = \frac{kT}{q} \\
# I_S &= bT^{4+m}\ e^{(-\frac{Eg}{kT})} \\[0.5em]
# V_{BE} &= V_T\ ln{\left(\frac{I_C}{I_S} \right)}  \\[0.5em]
# \dfrac{\partial V_{BE}}{\partial T} &= \dfrac{\partial V_T}{\partial T}\ ln{\dfrac{I_C}{I_S}} - \dfrac{V_T}{I_S} \dfrac{\partial I_S}{\partial T}  \\[0.5em]
# \dfrac{V_T}{I_S} \dfrac{\partial I_S}{\partial T} &= (4+m)\dfrac{V_T}{T} + \dfrac{E_g}{kT^2}V_T \\[0.5em]
# \dfrac{\partial V_{BE}}{\partial T} &= \dfrac{V_T}{T}\ ln{\dfrac{I_C}{I_S}} - (4+m)\dfrac{V_T}{T} + \dfrac{E_g}{kT^2}V_T \\[0.5em]
# &= \dfrac{V_{BE}-(4+m)V_T - E_g/q}{T}
# \end{align*}
# $$
# 
# Thus, at $T=300K$ and $V_{BE} \approx 750$mV, the change in TC voltage with respect to temperature is $\partial V_{BE}/ \partial T \approx -1.5$mV.

# ## PTAT: Proportional to Absolute Temperature

# ```{figure} PTAT.png
# :width: 300px
# PTAT Circuit
# ```

# Figure 1 shows two bipolar transistors operating with ideal current sources. The difference between their base-emitter voltages is directly proportional to absolute temperature. The circuit emphasizes design choices by scaling bias current *n* and number of devices *m*.
# 
# $$
# \begin{align*}
# \Delta V_{BE} &= V_{BE1} - V_{BE2} \\[0.5em]
# &= V_T\ ln{(\dfrac{n I_0}{I_{S}})} - V_T\ ln{(\dfrac{I_0}{mI_{S}})} \\[0.5em]
# &= V_T\ ln{(nm)} \\[0.5em]
# &= \dfrac{kT}{q}\ ln{(nm)} \\[0.5em]
# \dfrac{\partial}{\partial T} \Delta V_{BE} &=  \dfrac{\partial}{\partial T} \dfrac{kT}{q}\ ln{(nm)}\\[0.5em]
# &= \dfrac{k}{q}\ ln{(nm)}
# \end{align*}
# $$
# 
# The positive temperature coefficient is proportional to $\frac{k}{q}$ such that 
# 
# $$\dfrac{\partial }{\partial T}\Delta V_{BE} =  \alpha\ 0.087 \text{mV/C.}$$

# ## Bandgap Reference

# Now a temperature independent reference can be obtained by combining the negative and positive coefficients mentioned previously. The reference is defined as
# 
# $$
# \begin{align*}
# V_{REF} &= \alpha_1 V_{BE} + \alpha_2 V_T ln(nm)
# \end{align*}
# $$
# 
# For simplicity, $\alpha_1$ is chosen to be 1. Then $V_{REF}$ is
# 
# $$
# \begin{align*}
# V_{REF} &= V_{BE} + \alpha_2 V_T ln(m)
# \end{align*}
# $$
# 
# where $m$ is the number of devices.

# In[ ]:




