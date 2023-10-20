# coding:utf-8
# from cv2 import cv2
import cv2

import serial.tools.list_ports
import time
import os
import numpy as np
import array
import sys  
# from gmssl import func

Lab_Value = [53, 100, -86, 80, -70, 50]
Lab_Value[0] = Lab_Value[0]*256/100
Lab_Value[1] = Lab_Value[1]*256/100
Lab_Value[2] = Lab_Value[2] + 128
Lab_Value[3] = Lab_Value[3] + 128
Lab_Value[4] = Lab_Value[4] + 128
Lab_Value[5] = Lab_Value[5] + 128

#打开端口，用来和设备通讯用
def OpenSerial():
    global ser
    port_list = list(serial.tools.list_ports.comports())
    # print(port_list)
    comlist = []
    
    if len(port_list) == 0:
        print('无可用串口')
    else:
        for port in port_list:
            if("CH340" in port[1]):
                comlist.append(port[0])
                print(port[0])
                ser = serial.Serial(comlist[0], 115200, timeout=0.5)
                # print(ser)
                time.sleep(1)
                break
        if len(comlist) == 0:
            print("not found CH340")
            while(1):
                pass
#串口写入数据
def DWritePort(ser,text):
    result = ser.write(text.encode("gbk"))  # 写数据
    return result
#串口发送数据后等待设备返回“完成”指令
def WaitPortFinish(commond):
    # print('waiting for moto')
    if(commond == 1):
        while(True):
            SerData = str(ser.readline())
            # print(SerData)
            if "GoToOk" in SerData:
                break 
    else:
        while(True):
            SerData = str(ser.readline())
            # print(SerData)
            if "ZeroOk" in SerData:
                break
#连续拍照
def TakePic(original_height, original_length):
    #两个电机的初始位置
    xposition = 510  
    yposition = original_height*10 + 240;

    # 选取摄像头，0为笔记本内置的摄像头，1,2···为外接的摄像头
    camera_number = 0
    cap = cv2.VideoCapture(camera_number  + cv2.CAP_DSHOW)

    #给装置发送信息，串口相关
    strA = "%04d" % xposition
    strB = "%04d" % yposition
    DataSend = 'A'+ strA +'B'+ strB +'\r'+'\n'
    DWritePort(ser,DataSend)
    WaitPortFinish(1)

    #跳过部分图像
    for i in range(20):
        ret, frame = cap.read()
        img = cv2.flip(frame, -1)
        cv2.imwrite('init.jpg', img) 
    time.sleep(1)

    #循环运动+拍照
    for index in range(original_length-1):
        #给装置发送信息，串口相关
        strA = "%04d" % xposition
        strB = "%04d" % yposition
        DataSend = 'A'+ strA +'B'+ strB +'\r'+'\n'
        DWritePort(ser,DataSend)
        WaitPortFinish(1)
        #拍照
        ret, frame = cap.read()
        img = cv2.flip(frame, -1) #拍的图片翻转一次
        if index:  #第一张废弃，因为没有初始化好
            cv2.imwrite(str(index)+'.jpg', img) 
            print('TakingPic-'+str(index))

        #每次移动1mm的距离
        xposition += 10

    return 0



#保养运动导轨时使用，让两个轴来回运动
def motorepair():
    OpenSerial()
    global ser
    while(True):
        print('wait\n')
        DWritePort(ser,'A1500B0000\r\n')
        WaitPortFinish(1)
        DWritePort(ser,'A0000B1000\r\n')
        WaitPortFinish(1)   

def main():
    #打开串口端口
    OpenSerial()
    #全局变量
    global ser

    # motorepair()

    #扫描对象的大致参数-长度
    original_length = int(input("please enter the length(mm): "))

    #扫描对象的大致参数-高度
    original_height = int(input("please enter the height(mm): "))

    #拍照并且处理得到线条
    #串口控制电机转动，移动扫描平台
    TakePic(original_height,original_length) 
    cv2.destroyAllWindows()


main()

ser.close()  