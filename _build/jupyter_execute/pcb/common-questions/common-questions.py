#!/usr/bin/env python
# coding: utf-8

# # Common Questions

# ## Q1: How wide should I make my trace?
# 
# [PCB Trace Inductance and Width: How Wide is Too Wide?](https://resources.altium.com/p/pcb-trace-inductance-and-width-how-wide-too-wide)

# - Goal: minimize PCB trace inductance per unit length while keeping impedance constant  
# - Wheeler implementation produces less than 0.7% error which is much better than IPC-2141
# 
# $$
# \begin{align*}
#  L &= \dfrac{Z_0(w,h,t)}{c} \sqrt{\epsilon_{eff}(w,h,t)}  \\[0.5em]
#  C &= \dfrac{L}{Z_0(w,h,t)^2} \\[0.5em]
#  Z_0 &= \text{defined by Waddell’s equations for microstrip impedance}
# \end{align*}
# $$

# ```{figure} trace-geometry.png
# Trace Geometry
# ```

# ## Q2: Should unused area in signal planes be filled with copper pours?
# 
# [On Shaky Ground—the Arguments Against Copper Pours](https://resources.altium.com/p/shaky-ground-arguments-against-copper-pours#the-history-of-ground-pours)
# - Ground pours resemble patch antennas and can emit noise
# - When the copper is thick, desoldering and service operations are more difficult

# ## Q3: Where should I place my current sensor?
# 
# [Current Sensing: Where to Place the Sense Resistor](https://www.analog.com/en/technical-articles/switch-mode-power-supply-current-sensing-part-2-where-to-place-the-sense-resistor.html)
# 
# - Placing sense resistor after inductor provides best signal to noise ratios. Ultimately, resistor should be replaced with hall sensor to improve dissipated power if it's within budget (\$).

# ```{figure} Rsense.jpg
# ---
# width: 400px
# ---
# Sense Resistor in Switch Mode Power Supply
# ```

# ## Q4: How do I choose I gate driver for my design?
# 
# [Gate resistor for power devices](https://www.infineon.com/dgdl/Infineon-EiceDRIVER-Gate_resistor_for_power_devices-ApplicationNotes-v01_00-EN.pdf?fileId=5546d462518ffd8501523ee694b74f18)  
# [Isolated Gate Drivers—What, Why, and How?](https://www.analog.com/en/analog-dialogue/articles/isolated-gate-drivers-what-why-and-how.html)  
# [Peak Current of Isolated Gate Drivers](https://www.analog.com/en/analog-dialogue/articles/peak-current-of-isolated-gate-drivers.html)

# |  Design             | Component  |
# | :------------------ | :--------- |
# | Gate Driver         | [NCP5901B](https://www.digikey.com/en/products/detail/onsemi/NCP5901BDR2G/2512539)   |
# | MOSFET              | [TPH8R903NL](https://www.digikey.com/en/products/detail/toshiba-semiconductor-and-storage/TPH8R903NL-LQ/4332031)     |
# | Switching Frequency | 100kHz     |

# Gate driver performance
# 
# $$
# \begin{align*}
#  i_G &= \dfrac{Q_G}{t_{r}}  \\[0.5em]
#  i_G &= \dfrac{3nF \cdot 12V}{16ns}  \\[0.5em]
#  i_G &= 2.25A  \\[0.5em]
# \end{align*}
# $$

# Rush current 
# 
# $$
# \begin{align*}
#  i_G(\text{rush}) &= 
# \end{align*}
# $$
