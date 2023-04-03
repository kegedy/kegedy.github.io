#!/usr/bin/env python
# coding: utf-8

# # Discussions

# ## Q1: Trace width
# 
# [PCB Trace Inductance and Width: How Wide is Too Wide?](https://resources.altium.com/p/pcb-trace-inductance-and-width-how-wide-too-wide)

# - Goal: minimize PCB trace inductance per unit length while keeping impedance constant  
# - Wheeler implementation produces less than 0.7% error which is much better than IPC-2141
# 
# \begin{align*}
#  L &= \dfrac{Z_0(w,h,t)}{c} \sqrt{\epsilon_{eff}(w,h,t)}  \\[0.5em]
#  C &= \dfrac{L}{Z_0(w,h,t)^2} \\[0.5em]
#  Z_0 &= \text{Waddell’s equations for microstrip impedance}
# \end{align*}

# ```{figure} trace-geometry.png
# Trace Geometry
# ```

# ## Q2: Filling unused area in signal planes with copper pours
# 
# [On Shaky Ground—the Arguments Against Copper Pours](https://resources.altium.com/p/shaky-ground-arguments-against-copper-pours#the-history-of-ground-pours)
# - Ground pours resemble patch antennas and can emit noise
# - When the copper is thick, desoldering and service operations are more difficult

# ## Q3: Current sensor location
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

# ## Q4: Gate driver protection
# 
# [Gate resistor for power devices](https://www.infineon.com/dgdl/Infineon-EiceDRIVER-Gate_resistor_for_power_devices-ApplicationNotes-v01_00-EN.pdf?fileId=5546d462518ffd8501523ee694b74f18)  
# [Peak Current of Isolated Gate Drivers](https://www.analog.com/en/analog-dialogue/articles/peak-current-of-isolated-gate-drivers.html)
# 

# ```{figure} TypicalApplication.png
# Typical Application
# ```

# |  Design             | Component  |
# | :------------------: | :---------: |
# | Gate Driver         | [STDRIVEG600](https://www.st.com/resource/en/datasheet/stdriveg600.pdf)   |
# | MOSFET              | [TPH8R903NL](https://www.digikey.com/en/products/detail/toshiba-semiconductor-and-storage/TPH8R903NL-LQ/4332031)     |
# 
# 

# Given PVCC = 5V, VBO = 20V and gate driver specs:  
# 
# | Source | Source | Sink | $R_{\text{DS_on}}$ | $R_{\text{DS_off}}$ |
# | :-- | :-- | :-- | :-- | :-- |
# | 6.0V | 1.3A | 2.4A | 2.0$\Omega$ | 1.2$\Omega$ |
# | 15V  | 5.5A | 6.0A | 1.25$\Omega$ | 0.9$\Omega$ |

# \begin{center}
# \begin{tabular}{ c c c }
#  cell1 & cell2 & cell3 \\ 
#  cell4 & cell5 & cell6 \\  
#  cell7 & cell8 & cell9    
# \end{tabular}
# \end{center}

# **High Side Calculations**  
# 
# \begin{align*}
# I_{\text{charging_peak}} &= \dfrac{V_{BO}}{R_{\text{DS_on}} + R_{\text{G_on}}} \\[0.5em]
# 5.5A &= \dfrac{20}{1.25 + R_{\text{G_on}}} \\[0.5em]
# R_{\text{G_on}} &= 2.39 \Omega \\[0.5em]
# I_{\text{discharging_peak}} &= \dfrac{V_{BO}}{R_{\text{DS_off}} + R_{\text{G_off}}}\\[0.5em] 
# 6.0A &= \dfrac{20}{0.9 + R_{\text{G_off}}} \\[0.5em]
# R_{\text{G_off}} &= 2.43 \Omega \\[0.5em]
# \end{align*}
# 

# **Low Side Calculations** 
# 
# \begin{align*}
# I_{\text{charging_peak}} &= \dfrac{PVCC}{R_{\text{DS_on}} + R_{\text{G_on}}} \\[0.5em]
# 1.3A &= \dfrac{5}{2.0 + R_{\text{G_on}}} \\[0.5em]
# R_{\text{G_on}} &= 1.85 \Omega \\[0.5em]
# I_{\text{discharging_peak}} &= \dfrac{PVCC}{R_{\text{DS_off}} + R_{\text{G_off}}}\\[0.5em] 
# 2.4A &= \dfrac{5}{1.2 + R_{\text{G_off}}} \\[0.5em]
# R_{\text{G_off}} &= 0.89 \Omega \\[0.5em]
# \end{align*}

# **Resistor Size**
# 
# Additionally, power dissipated through the resistor is 
# \begin{equation} 
# P = C V^2 f 
# \end{equation}
# for selecting components.

# 
