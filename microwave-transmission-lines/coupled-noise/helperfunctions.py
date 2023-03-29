import sympy as sp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as pch

def RoundNonZeroDecimal(num, place, rnd='ceil'):
    # Requires numpy library
    # Examples:
    #   RoundNonZeroDecimal(0.0004512,1,'floor') -> 0.0045
    #   RoundNonZeroDecimal(0.0004512,1,'ceil') -> 0.0046
    #
    tmp = num # implement so that num can be array
    mag = 0
    
    if rnd=='ceil':
        while(abs(tmp)<1):
            tmp*=10
            mag+=1
        for i in range(place):
            tmp*=10
            mag+=1
        return int(np.ceil([tmp])[0])/(10**(mag)) 
    
    if rnd=='floor':
        while(abs(tmp)<1):
            tmp*=10
            mag+=1
        for i in range(place):
            tmp*=10
            mag+=1
        return int(np.floor([tmp])[0])/(10**(mag))
    
    else:
        raise ValueError('Invalid argument')
        return None
    
# Find Rise Time
def RiseTime(np_arr,fsv=None):
    # Find the rise time as defined: 10%-90% of rising slope
    # Returns the indexes x0,x1 corresponding to the 10%,90% values

    np_arr = np.abs(np_arr)
    x0,x1 = None,None
    
    # Final State Value: Median of final 10% elements
    if fsv==None: 
        fsv = np.median(np_arr[-int(0.1*len(np_arr)):])
        
    # 10% value
    V0 = 0.1*fsv

    # 90% value
    V1 = 0.9*fsv

    # start
    place=4
    while(1):
        try:
            floor = RoundNonZeroDecimal(V0,place,'floor')
            ceil = RoundNonZeroDecimal(V0,place,'ceil')
            x0 = np.where(np_arr<ceil)[0][-1]
        except Exception as e:
            place-=1
            if place<=-1:
                raise ValueError(f'Unable to find 10% value of final state value: {fsv}')
                break
            continue
        break

    #end
    place=4
    while(1):
        try:
            floor = RoundNonZeroDecimal(V1,place,'floor')
            ceil = RoundNonZeroDecimal(V1,place,'ceil')
            x1 = np.where(np_arr>floor)[0][0]
        except Exception as e:
            place-=1
            if place<=-1:
                raise ValueError(f'Unable to find 90% value of final state value: {fsv}')
                break
            continue
        break
    
    return x0,x1

# Find Fall Time
def FallTime(np_arr,fsv=None):
    # Find the fall time as defined: 90%-10% of rising slope
    # Returns the indexes x0,x1 corresponding to the 90%,10% values
    
    np_arr = np.abs(np_arr)
    x0,x1 = None,None
    
    # Final State Value: Median of final 10% elements
    if fsv==None: 
        fsv = np.median(np_arr[0:int(0.1*len(np_arr))])

    # 90% value
    V0 = 0.9*fsv    

    # 10% value
    V1 = 0.1*fsv

    # start
    place=4
    while(1):
        try:
            floor = RoundNonZeroDecimal(V0,place,'floor')
            ceil = RoundNonZeroDecimal(V0,place,'ceil')
            x0 = np.where(np_arr<ceil)[0][0]
        except Exception as e:
            place-=1
            if place<=-1:
                raise ValueError(f'Unable to find 10% value of final state value: {fsv}')
                break
            continue
        break

    #end
    place=4
    while(1):
        try:
            floor = RoundNonZeroDecimal(V1,place,'floor')
            ceil = RoundNonZeroDecimal(V1,place,'ceil')
            x1 = np.where(np_arr<ceil)[0][0]
        except Exception as e:
            place-=1
            if place<=-1:
                raise ValueError(f'Unable to find 90% value of final state value: {fsv}')
                break
            continue
        break
    
    return x0,x1


def WaveformDuration(np_arr,x0,x1,total_time,
                    mag=9,unit='ns',title=''):
    
    # Figure
    fig,ax = plt.subplots(figsize=(12,4))
    L = len(np_arr)
    x,res = np.linspace(0,total_time,L,endpoint=False,retstep=True)
    Ures = res*10**mag

    # Find V0
    V0 = np.median(np_arr[x0:x1])
    if method=='max':
        V0 = np.max(np_arr[x0:x1])
    elif method=='min':
        V0 = np.min(np_arr[x0:x1])
    
    # Plot
    ax.plot(x,np_arr,  # must be plotted in this order for Matplotlib 
        color='red' 
    )
    ax.scatter(x0*res,np_arr[x0],
        color='red',
        label=f't1 @ {round(x0*Ures,2)}{unit}'
    )
    ax.scatter(x1*res,np_arr[x1],
        color='red',
        label=f't2 @ {round(x1*Ures,2)}{unit}'
    )
    ax.plot(x,np.ones(L)*V0,
        color='red',
        linewidth=1.0,
        label='$Peak$'
    )
    ax.plot(x,np_arr,
        label='Measured Values'
    )

    # Labels
    ax.ticklabel_format(axis='x',style='sci', scilimits=(-mag,-mag))
    ax.set_title(f'{title} = {round(V0,4)} V')
    ax.set_xlabel('t (s)')
    ax.set_ylabel('V')
    plt.grid(True)
    plt.legend();

# Plot Waveform and Peak Voltage
def WaveformPeakPlt(np_arr,x0,x1,total_time,
                    method=None,mag=9,unit='ns',title=''):
    # Assumes 5ns window
    # Plots the given waveform and the peak voltage within [x0,x1]
    
    # Figure
    fig,ax = plt.subplots(figsize=(12,4))
    L = len(np_arr)
    x,res = np.linspace(0,total_time,L,endpoint=False,retstep=True)
    Ures = res*10**mag

    # Find V0
    V0 = np.median(np_arr[x0:x1])
    if method=='max':
        V0 = np.max(np_arr[x0:x1])
    elif method=='min':
        V0 = np.min(np_arr[x0:x1])
    
    # Plot
    ax.plot(x,np_arr,  # must be plotted in this order for Matplotlib 
        color='red' 
    )
    ax.scatter(x0*res,np_arr[x0],
        color='red',
        label=f't1 @ {round(x0*Ures,2)}{unit}'
    )
    ax.scatter(x1*res,np_arr[x1],
        color='red',
        label=f't2 @ {round(x1*Ures,2)}{unit}'
    )
    ax.plot(x,np.ones(L)*V0,
        color='red',
        linewidth=1.0,
        label='$Peak$'
    )
    ax.plot(x,np_arr,
        label='Measured Values'
    )

    # Labels
    ax.ticklabel_format(axis='x',style='sci', scilimits=(-mag,-mag))
    ax.set_title(f'{title} = {round(V0,4)} V')
    ax.set_xlabel('t (s)')
    ax.set_ylabel('V')
    plt.grid(True)
    plt.legend();
    
 # Plot Waveform and Rise Time
def WaveformRTimePlt(np_arr,x0,x1,total_time,
                     fsv=None,mag=9,unit='ns',title=''):
    # Assumes 5ns window
    # Plots the given waveform 
    #   and the rise time (defined as 10%-90%) between [x0,x1]
    
    # Figure
    fig,ax = plt.subplots(figsize=(12,4))
    L = len(np_arr)
    x,res = np.linspace(0,total_time,L,endpoint=False,retstep=True)
    Ures = res*10**mag
    
    # Parameters
    x10,x90 = RiseTime(np_arr[x0:x1],fsv=fsv)
    x10+=x0   # RiseTime returns index that is offset by x0
    x90+=x0   # RiseTime returns index that is offset by x0
    
    # Plot
    ax.plot(x,np_arr,
        label='Measured Values'
    )
    ax.scatter(x10*res,np_arr[x10],
        color='red',
        label=f'10% @ {round(x10*Ures,2)}{unit}'
    )
    ax.scatter(x90*res,np_arr[x90],
        color='red',
        label=f'90% @ {round(x90*Ures,2)}{unit}'
    )
    rt = RoundNonZeroDecimal((x90*Ures)-(x10*Ures),2)

    # Labels
    ax.ticklabel_format(axis='x',style='sci', scilimits=(-mag,-mag))
    ax.set_title(f'{title}: Rise Time = {rt}{unit}')
    ax.set_xlabel('t (s)')
    ax.set_ylabel('V')
    plt.grid(True)
    plt.legend();
    
# Area Approximation
def AreaApprox(f,a,b,n,offset):
    '''
    Returns the integral approximation of f(x)dx from a to b
    f : continuous waveform
    a : starting point
    b : ending point
    '''
    apprx = 0
    dxs,width = np.linspace(a,b,n,endpoint=False,retstep=True)
    for dx in dxs:
        dx = int(dx)
        midpoint = (f[dx]+f[dx+1])/2 # Use the midpoint approximation
        apprx += width*(midpoint-offset) # width is 1 second -> adjust by resolution
    return apprx[0]

# Plot Area Approximation
def Waveform_Area(f,a,b,n,offset=0,title=''):
    # Area Approximation Part2_board2_280ps Plot
    #
    A = AreaApprox(f,a,b,n,offset)
    dxs,width = np.linspace(a,b,n,endpoint=False,retstep=True)

    # plot
    fig,ax = plt.subplots(figsize=(12,4))
    for dx in dxs:
        dx = int(dx)
        midpoint = (f[dx]+f[dx+1])/2
        rect = pch.Rectangle(
            (dx,offset),
            width,
            midpoint[0]-offset,
            facecolor='#D3D3D3',
            edgecolor='grey'
        )
        ax.add_artist(rect)
    ax.plot(f)
    ax.plot(
        dxs,
        f[a:b],
        label=f'area = {round(A,4)}'
    )

    # labels
    ax.set_xlabel('t')
    ax.set_ylabel('V')
    ax.set_title(f'Area Approximation {title}')
    ax.grid(True)
    #plt.legend();
    return A