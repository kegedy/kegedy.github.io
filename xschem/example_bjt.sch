v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 220 -200 220 -170 {lab=VDD}
N 220 -110 220 -90 {lab=VE}
N 220 -90 220 -70 {lab=VE}
N 220 -90 300 -90 {lab=VE}
N 180 -40 150 -40 {lab=GND}
N 150 -40 150 10 {lab=GND}
N 150 10 220 10 {lab=GND}
N 220 -10 220 10 {lab=GND}
N 220 10 220 20 {lab=GND}
C {isource.sym} 220 -140 0 0 {name=I1 value=10u}
C {sky130_fd_pr/pnp_05v5.sym} 200 -40 0 0 {name=Q1
model=pnp_05v5_W3p40L3p40
m=1
spiceprefix=X
}
C {opin.sym} 300 -90 0 0 {name=p1 lab=VE}
C {vdd.sym} 220 -200 0 0 {name=l1 lab=VDD}
C {gnd.sym} 220 20 0 0 {name=l2 lab=GND}
