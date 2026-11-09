v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 120 -330 120 -360 {lab=VDD}
N 120 -300 150 -300 {lab=VDD}
N 80 -300 50 -300 {lab=VSS}
N 120 -270 120 -180 {lab=S}
N 120 -180 120 -90 {lab=S}
N 80 -60 50 -60 {lab=VREF}
N 120 -30 120 0 {lab=VSS}
N 120 -60 150 -60 {lab=VSS}
N 120 -180 200 -180 {lab=S}
N 200 -180 200 -60 {lab=S}
N 200 -60 220 -60 {lab=S}
N 260 -90 260 -120 {lab=PB}
N 260 -30 260 0 {lab=VSS}
N 260 -60 290 -60 {lab=VSS}
N 440 -330 440 -360 {lab=VDD}
N 440 -300 470 -300 {lab=VDD}
N 400 -300 370 -300 {lab=PB}
N 640 -330 640 -360 {lab=VDD}
N 640 -300 670 -300 {lab=VDD}
N 600 -300 570 -300 {lab=PB}
N 840 -330 840 -360 {lab=VDD}
N 840 -300 870 -300 {lab=VDD}
N 800 -300 770 -300 {lab=PB}
N 440 -270 440 -180 {lab=A}
N 440 -180 440 -50 {lab=A}
N 400 -20 370 -20 {lab=VSS}
N 440 10 440 40 {lab=VSS}
N 640 -270 640 -180 {lab=B}
N 640 -180 640 -140 {lab=B}
N 640 -80 640 10 {lab=E2}
N 620 -110 590 -110 {lab=VSS}
N 600 40 570 40 {lab=VSS}
N 640 70 640 100 {lab=VSS}
N 840 -270 840 -180 {lab=VREF}
N 840 -180 840 -140 {lab=VREF}
N 840 -180 940 -180 {lab=VREF}
N 840 -80 840 10 {lab=E3}
N 820 -110 790 -110 {lab=VSS}
N 800 40 770 40 {lab=VSS}
N 840 70 840 100 {lab=VSS}
N 1060 -330 1060 -360 {lab=VDD}
N 1060 -300 1090 -300 {lab=VDD}
N 1020 -300 990 -300 {lab=PB}
N 1060 -270 1060 -120 {lab=NB}
N 1060 -120 1060 10 {lab=NB}
N 1020 40 990 40 {lab=NB}
N 1060 70 1060 100 {lab=VSS}
N 1060 40 1090 40 {lab=VSS}
N 1220 -330 1220 -360 {lab=VDD}
N 1480 -330 1480 -360 {lab=VDD}
N 1220 -300 1190 -300 {lab=VDD}
N 1480 -300 1510 -300 {lab=VDD}
N 1260 -300 1320 -300 {lab=N1}
N 1320 -300 1440 -300 {lab=N1}
N 1320 -300 1320 -340 {lab=N1}
N 1220 -270 1220 -220 {lab=N1}
N 1220 -220 1220 -180 {lab=N1}
N 1480 -270 1480 -220 {lab=PBO}
N 1480 -220 1480 -180 {lab=PBO}
N 1480 -220 1580 -220 {lab=PBO}
N 1180 -150 1150 -150 {lab=B}
N 1520 -150 1550 -150 {lab=A}
N 1220 -150 1250 -150 {lab=VSS}
N 1480 -150 1450 -150 {lab=VSS}
N 1220 -120 1220 -90 {lab=TAIL}
N 1220 -90 1310 -90 {lab=TAIL}
N 1480 -120 1480 -90 {lab=TAIL}
N 1480 -90 1310 -90 {lab=TAIL}
N 1310 -90 1310 -60 {lab=TAIL}
N 1270 -30 1240 -30 {lab=NB}
N 1310 0 1310 30 {lab=VSS}
N 1310 -30 1340 -30 {lab=VSS}
N 1580 -160 1580 -130 {lab=PB}
N 1700 -230 1700 -260 {lab=VDD}
N 1700 -170 1700 -140 {lab=PBO}
C {sky130_fd_pr/pfet_01v8.sym} 100 -300 0 0 {name=M9
L=8
W=0.42
nf=1 mult=1
ad=0.1218 as=0.1218
pd=1.42 ps=1.42
nrd=0.6905 nrs=0.6905
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {lab_pin.sym} 120 -360 3 0 {name=l1 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 150 -300 2 0 {name=l2 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 50 -300 0 0 {name=l3 sig_type=std_logic lab=VSS}
C {sky130_fd_pr/nfet_01v8.sym} 100 -60 0 0 {name=M10
L=1
W=1
nf=1 mult=1
ad=0.29 as=0.29
pd=2.58 ps=2.58
nrd=0.29 nrs=0.29
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {lab_pin.sym} 50 -60 0 0 {name=l5 sig_type=std_logic lab=VREF}
C {lab_pin.sym} 120 0 1 0 {name=l6 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 150 -60 2 0 {name=l7 sig_type=std_logic lab=VSS}
C {sky130_fd_pr/nfet_01v8.sym} 240 -60 0 0 {name=M11
L=1
W=0.42
nf=1 mult=1
ad=0.1218 as=0.1218
pd=1.42 ps=1.42
nrd=0.6905 nrs=0.6905
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {lab_pin.sym} 260 -120 3 0 {name=l9 sig_type=std_logic lab=PB}
C {lab_pin.sym} 260 0 1 0 {name=l10 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 290 -60 2 0 {name=l11 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 120 -180 2 0 {name=l12 sig_type=std_logic lab=S}
C {sky130_fd_pr/pfet_01v8.sym} 420 -300 0 0 {name=M1
L=4
W=8
nf=1 mult=1
ad=2.32 as=2.32
pd=16.58 ps=16.58
nrd=0.0362 nrs=0.0362
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 620 -300 0 0 {name=M2
L=4
W=8
nf=1 mult=1
ad=2.32 as=2.32
pd=16.58 ps=16.58
nrd=0.0362 nrs=0.0362
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 820 -300 0 0 {name=M3
L=4
W=8
nf=1 mult=1
ad=2.32 as=2.32
pd=16.58 ps=16.58
nrd=0.0362 nrs=0.0362
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {lab_pin.sym} 440 -360 3 0 {name=l16 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 470 -300 2 0 {name=l17 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 370 -300 0 0 {name=l18 sig_type=std_logic lab=PB}
C {lab_pin.sym} 640 -360 3 0 {name=l19 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 670 -300 2 0 {name=l20 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 570 -300 0 0 {name=l21 sig_type=std_logic lab=PB}
C {lab_pin.sym} 840 -360 3 0 {name=l22 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 870 -300 2 0 {name=l23 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 770 -300 0 0 {name=l24 sig_type=std_logic lab=PB}
C {sky130_fd_pr/pnp_05v5.sym} 420 -20 0 0 {name=Q1
model=pnp_05v5_W3p40L3p40
m=1
spiceprefix=X
}
C {lab_pin.sym} 440 -180 2 0 {name=l26 sig_type=std_logic lab=A}
C {lab_pin.sym} 370 -20 0 0 {name=l27 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 440 40 1 0 {name=l28 sig_type=std_logic lab=VSS}
C {sky130_fd_pr/res_xhigh_po_0p35.sym} 640 -110 0 0 {name=R1
L=2
model=res_xhigh_po_0p35
spiceprefix=X
mult=1}
C {sky130_fd_pr/pnp_05v5.sym} 620 40 0 0 {name=Q2
model=pnp_05v5_W3p40L3p40
m=8
spiceprefix=X
}
C {lab_pin.sym} 640 -180 2 0 {name=l31 sig_type=std_logic lab=B}
C {lab_pin.sym} 590 -110 0 0 {name=l32 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 570 40 0 0 {name=l33 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 640 100 1 0 {name=l34 sig_type=std_logic lab=VSS}
C {sky130_fd_pr/res_xhigh_po_0p35.sym} 840 -110 0 0 {name=R2
L=17.7
model=res_xhigh_po_0p35
spiceprefix=X
mult=1}
C {sky130_fd_pr/pnp_05v5.sym} 820 40 0 0 {name=Q3
model=pnp_05v5_W3p40L3p40
m=1
spiceprefix=X
}
C {opin.sym} 940 -180 0 0 {name=p3 lab=VREF}
C {lab_pin.sym} 790 -110 0 0 {name=l38 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 770 40 0 0 {name=l39 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 840 100 1 0 {name=l40 sig_type=std_logic lab=VSS}
C {sky130_fd_pr/pfet_01v8.sym} 1040 -300 0 0 {name=M12
L=4
W=8
nf=1 mult=1
ad=2.32 as=2.32
pd=16.58 ps=16.58
nrd=0.0362 nrs=0.0362
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {lab_pin.sym} 1060 -360 3 0 {name=l42 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1090 -300 2 0 {name=l43 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 990 -300 0 0 {name=l44 sig_type=std_logic lab=PB}
C {sky130_fd_pr/nfet_01v8.sym} 1040 40 0 0 {name=M13
L=4
W=8
nf=1 mult=1
ad=2.32 as=2.32
pd=16.58 ps=16.58
nrd=0.0362 nrs=0.0362
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {lab_pin.sym} 1060 -120 2 0 {name=l46 sig_type=std_logic lab=NB}
C {lab_pin.sym} 990 40 0 0 {name=l47 sig_type=std_logic lab=NB}
C {lab_pin.sym} 1060 100 1 0 {name=l48 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 1090 40 2 0 {name=l49 sig_type=std_logic lab=VSS}
C {sky130_fd_pr/pfet_01v8.sym} 1240 -300 0 1 {name=M7
L=4
W=4
nf=1 mult=1
ad=1.16 as=1.16
pd=8.58 ps=8.58
nrd=0.0725 nrs=0.0725
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet_01v8.sym} 1460 -300 0 0 {name=M8
L=4
W=4
nf=1 mult=1
ad=1.16 as=1.16
pd=8.58 ps=8.58
nrd=0.0725 nrs=0.0725
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {lab_pin.sym} 1220 -360 3 0 {name=l52 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1480 -360 3 0 {name=l53 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1190 -300 0 0 {name=l54 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1510 -300 2 0 {name=l55 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1320 -340 3 0 {name=l56 sig_type=std_logic lab=N1}
C {sky130_fd_pr/nfet_01v8_lvt.sym} 1200 -150 0 0 {name=M5
L=4
W=16
nf=1 mult=1
ad=4.64 as=4.64
pd=32.58 ps=32.58
nrd=0.0181 nrs=0.0181
sa=0 sb=0 sd=0
model=nfet_01v8_lvt
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8_lvt.sym} 1500 -150 0 1 {name=M6
L=4
W=16
nf=1 mult=1
ad=4.64 as=4.64
pd=32.58 ps=32.58
nrd=0.0181 nrs=0.0181
sa=0 sb=0 sd=0
model=nfet_01v8_lvt
spiceprefix=X
}
C {lab_pin.sym} 1220 -220 0 0 {name=l59 sig_type=std_logic lab=N1}
C {lab_pin.sym} 1480 -220 2 0 {name=l60 sig_type=std_logic lab=PBO}
C {lab_pin.sym} 1150 -150 0 0 {name=l61 sig_type=std_logic lab=B}
C {lab_pin.sym} 1550 -150 2 0 {name=l62 sig_type=std_logic lab=A}
C {lab_pin.sym} 1250 -150 2 0 {name=l63 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 1450 -150 0 0 {name=l64 sig_type=std_logic lab=VSS}
C {sky130_fd_pr/nfet_01v8.sym} 1290 -30 0 0 {name=M4
L=4
W=8
nf=1 mult=1
ad=2.32 as=2.32
pd=16.58 ps=16.58
nrd=0.0362 nrs=0.0362
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {lab_pin.sym} 1310 -90 3 0 {name=l66 sig_type=std_logic lab=TAIL}
C {lab_pin.sym} 1240 -30 0 0 {name=l67 sig_type=std_logic lab=NB}
C {lab_pin.sym} 1310 30 1 0 {name=l68 sig_type=std_logic lab=VSS}
C {lab_pin.sym} 1340 -30 2 0 {name=l69 sig_type=std_logic lab=VSS}
C {vsource.sym} 1580 -190 2 0 {name=Vloop value=0 savecurrent=false}
C {lab_pin.sym} 1580 -130 1 0 {name=l71 sig_type=std_logic lab=PB}
C {sky130_fd_pr/cap_mim_m3_1.sym} 1700 -200 0 0 {name=C1 model=cap_mim_m3_1 W=30 L=30 MF=1 spiceprefix=X}
C {lab_pin.sym} 1700 -260 3 0 {name=l73 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1700 -140 1 0 {name=l74 sig_type=std_logic lab=PBO}
C {iopin.sym} 0 -480 0 0 {name=p1 lab=VDD}
C {iopin.sym} 0 -440 0 0 {name=p2 lab=VSS}
T {Bandgap core: PTAT current + VBE (sky130, VDD 1.8 V, VREF 1.2 V)} -20 -560 0 0 0.5 0.5 {}
T {Start-up} 60 -420 0 0 0.35 0.35 {}
T {PTAT core: VA = VB, I = VT ln8 / R1} 400 -420 0 0 0.35 0.35 {}
T {Error amplifier (NMOS-LVT input, PMOS load)} 1020 -440 0 0 0.35 0.35 {}
T {Comp. ~1.8 pF} 1660 -300 0 0 0.35 0.35 {}
T {loop-break (0 V)} 1600 -120 0 0 0.3 0.3 {}
