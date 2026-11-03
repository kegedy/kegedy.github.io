v {xschem version=3.4.4 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 220 -200 220 -190 {lab=VDD}
N 220 -190 220 -170 {lab=VDD}
N 220 -190 250 -190 {lab=VDD}
N 250 -190 250 -140 {lab=VDD}
N 220 -140 250 -140 {lab=VDD}
N 220 -110 220 -90 {lab=OUT}
N 220 -90 220 -70 {lab=OUT}
N 220 -90 300 -90 {lab=OUT}
N 180 -140 140 -140 {lab=IN}
N 140 -140 140 -90 {lab=IN}
N 140 -90 140 -40 {lab=IN}
N 140 -40 180 -40 {lab=IN}
N 80 -90 140 -90 {lab=IN}
N 220 -10 220 10 {lab=GND}
N 220 10 220 20 {lab=GND}
N 220 10 250 10 {lab=GND}
N 250 10 250 -40 {lab=GND}
N 220 -40 250 -40 {lab=GND}
C {sky130_fd_pr/pfet_01v8.sym} 200 -140 0 0 {name=M1
L=0.15
W=2
nf=1 mult=1
ad=0.58 as=0.58
pd=4.58 ps=4.58
nrd=0.145 nrs=0.145
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 200 -40 0 0 {name=M2
L=0.15
W=1
nf=1 mult=1
ad=0.29 as=0.29
pd=2.58 ps=2.58
nrd=0.29 nrs=0.29
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {ipin.sym} 80 -90 0 0 {name=p1 lab=IN}
C {opin.sym} 300 -90 0 0 {name=p2 lab=OUT}
C {vdd.sym} 220 -200 0 0 {name=l1 lab=VDD}
C {gnd.sym} 220 20 0 0 {name=l2 lab=GND}
