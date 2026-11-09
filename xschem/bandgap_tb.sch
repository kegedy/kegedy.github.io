v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {Bandgap testbench: the core as a single cell with external sources} -40 -460 0 0 0.5 0.5 {}
T {VDD carries DC + AC 1 so the same bench runs op, DC, AC (PSRR) and noise.
The decks in sim/bandgap/ reuse this bench for every test.} -40 -420 0 0 0.3 0.3 {}
N 80 -250 80 -220 {lab=VDD}
N 80 -160 80 -120 {lab=GND}
N 400 -300 400 -270 {lab=VDD}
N 400 -130 400 -120 {lab=GND}
N 490 -200 600 -200 {lab=VREF}
N 600 -200 600 -170 {lab=VREF}
N 600 -110 600 -120 {lab=GND}
N 600 -200 680 -200 {lab=VREF}
C {vsource.sym} 80 -190 0 0 {name=VSUP value="DC \{vdd\} AC 1 PWL(0 0 \{tr\} \{vdd\})" savecurrent=true}
C {lab_pin.sym} 80 -250 3 0 {name=l1 sig_type=std_logic lab=VDD}
C {gnd.sym} 80 -120 0 0 {name=l2 lab=GND}
C {bandgap_core.sym} 400 -200 0 0 {name=x1}
C {lab_pin.sym} 400 -300 3 0 {name=l3 sig_type=std_logic lab=VDD}
C {gnd.sym} 400 -120 0 0 {name=l4 lab=GND}
C {capa.sym} 600 -140 0 0 {name=CL value=1p m=1 footprint=1206 device="ceramic capacitor"}
C {gnd.sym} 600 -120 0 0 {name=l5 lab=GND}
C {opin.sym} 680 -200 0 0 {name=p1 lab=VREF}
C {code_shown.sym} 760 -380 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value=".lib $::SKYWATER_MODELS/sky130.lib.spice tt
.param vdd=1.8 tr=10u
.temp 27"}
C {code_shown.sym} 760 -230 0 0 {name=CONTROL only_toplevel=true value=".control
save all
op
print v(vref) i(vsup)
dc temp -40 125 1
plot v(vref)
.endc"}
