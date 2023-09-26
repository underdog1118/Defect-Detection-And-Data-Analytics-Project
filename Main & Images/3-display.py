import numpy as np
from mayavi import mlab
import math
import matplotlib.pyplot as plt
M=9#多项式阶数




def main():

    original_length = int(input("please enter the original_length(mm): "))

    pixl_width = int(input("please enter the pixl_width(mm): "))

    #掐头去尾图像
    original_length -= 2

    pixl_length = original_length*3
    x, y = np.ogrid[0:pixl_width:1,0:pixl_length:3]
    print(x,y)
    allpixl = pixl_width*original_length
    z=np.array(range(allpixl)).reshape(pixl_width,original_length)  
    #print(allpixl)
    print(z)
    #深度数据全部赋值为0
    for i in range(pixl_width):
        for j in range(original_length):
            z[i][j] = 0

    #打开文本文件，读取并且保存深度数据
    with open('text.txt') as lines:
        j = 0
        for line in lines:
            strnum = line.split('#')
            x_count = 0
            for i in range(pixl_width):
                z[i][j] = int(strnum[i])
            j += 1
            print(j)





#调用库
    pl=mlab.surf(x,y,z,warp_scale=5)
    mlab.axes(xlabel='x',ylabel='y',zlabel='z')
    mlab.outline(pl)
    mlab.colorbar()
    mlab.show()




main()
