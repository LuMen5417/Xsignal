# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 14:27:49 2017

@author: Administrator
"""

#!/usr/bin/python

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import numpy as np
import wget
import os

xLineNum = 1

    

lineNum = 0
RssiTbl = []
NoiseTbl = []
SnrTbl = []

'''
with open('snr.log', 'r') as fd:
    for line in fd:
        lineNum += 1
        if (lineNum - 48)%54 == 0:
            tbl = line.split()
            print(tuple(tbl))
            RssiTbl.append(tuple(tbl))

        if (lineNum - 10)%54 == 0:
            tbl_noise = line.split()
            print(tuple(tbl_noise))
            NoiseTbl.append(tuple(tbl_noise))
'''

#y1 = [int(ValueArray[3][5:],16) for ValueArray in RssiTbl]
#x1 = range(len(y1))

#y2 = [(-((255 - int(ValueArray[3][5:],16))+1) - 30) for ValueArray in NoiseTbl]
#x2 = range(len(y2))

y1 = []
x1 = []

y2 = []
x2 = []

fig = plt.figure(figsize=(8, 4))

#fig 1
ax1 = fig.add_subplot(311)
ax1.set_ylim(-130, -60)
defx=100
ax1.set_xlim(0,defx)

#line, = ax1.plot(y1[4], lw=2)
line1, = ax1.plot(0, 0,'-', color='red', label="RSSI")
ax1.set_ylabel("dbm")
ax1.set_xlabel("s")

#fig 2
ax2 = fig.add_subplot(312)
ax2.set_ylim(-100, -90)

line2, = ax2.plot(0, 0, '-', color='green', label="Noise")
ax2.set_ylabel("dbm")
ax2.set_xlabel("s")
ax2.set_xlim(0,defx)

#fig 3
ax3 = fig.add_subplot(313)
ax3.set_ylim(-5, 30)

line3, = ax3.plot(0, 0, '-', color='blue', label="SNR")
ax3.set_ylabel("dbm")
ax3.set_xlabel("s")
ax3.set_xlim(0,defx)

legend1 = ax1.legend(loc=(.80, .86))
legend2 = ax2.legend(loc=(.80, .86))
legend3 = ax3.legend(loc=(.80, .86))
ax1.grid(True)
ax2.grid(True)
ax3.grid(True)

def update(i):
    global defx
    
    label = 'timestep {0}'.format(i)
    print(label)
    
    filename=wget.download("http://192.168.8.1:82/snr.log")
    lineNumber = 0
    
    time.sleep(0.05)
    
    with open(filename, 'r') as fd:
        for line in fd:  
            lineNumber += 1
            if(lineNumber == 48):
                tbl = line.split()
                print(tuple(tbl))
                RssiTbl.append(tuple(tbl))
            if(lineNumber == 10):
                tbl_noise = line.split()
                print(tuple(tbl_noise))
                NoiseTbl.append(tuple(tbl_noise))
            if(lineNumber == 49):
                tbl_snr = line.split()
                print(tuple(tbl_snr))
                SnrTbl.append(tuple(tbl_snr))
                
    os.remove(filename)
    #os.remove(filename)
    
    y1 = [(-((255 - int(ValueArray[3][5:],16))+1)) for ValueArray in RssiTbl]
    x1 = range(len(y1))

    y2 = [(-((255 - int(ValueArray[3][5:],16))+1)) for ValueArray in NoiseTbl]
    x2 = range(len(y2))
    
    y3 = [int(ValueArray[3][5:],16) for ValueArray in SnrTbl]
    x3 = range(len(y3))
    
    
    # 更新直线和x轴（用一个新的x轴的标签）。
    # 用元组（Tuple）的形式返回在这一帧要被重新绘图的物体
    line1.set_xdata(range(i))
    yx1 = [ y1[j] for j in range(i) ]
    line1.set_ydata(yx1)  # 这里是重点，更新y轴的数据
    
    line2.set_xdata(range(i))
    yx2 = [ y2[k] for k in range(i) ]
    line2.set_ydata(yx2)  # 这里是重点，更新y轴的数据
    
    line3.set_xdata(range(i))
    yx3 = [ y3[l] for l in range(i) ]
    line3.set_ydata(yx3)  # 这里是重点，更新y轴的数据
    
    ax1.set_xlabel(label)    # 这里是重点，更新x轴的标签
    if(i-defx > 0):
        defx+=defx
        ax1.set_xlim(0,defx)
        ax2.set_xlim(0,defx)
        ax3.set_xlim(0,defx)
    
    return line1, ax1, line2, ax2

def init():
    pass

# FuncAnimation 会在每一帧都调用“update” 函数。
# 在这里设置一个10帧的动画，每帧之间间隔200毫秒
anim = animation.FuncAnimation(fig, update, interval=1000)
plt.show()