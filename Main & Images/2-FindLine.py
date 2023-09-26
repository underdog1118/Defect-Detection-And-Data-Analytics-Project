# from cv2 import cv2
import cv2

import numpy as np

#用户修改
basic_height = 20.0
err_height = 2.0
# light_value = 100
#摄像头位置相关
camera_zero_bit_y = 100

def callback(object):
    pass

#############打开图片##############
def Open_pics(picnum):
    imgname = str(picnum) +'.jpg'
    Image0 = cv2.imread(imgname, 1)
    ImgLab = cv2.cvtColor(Image0, cv2.COLOR_BGR2Lab)
    return ImgLab  #返回LAB格式的图片 L亮度 AB颜色         

#############图片裁剪##############
def Pic_Window_Cut(img_original,ROI_x,ROI_y,ROI_w,ROI_h):
    Img_window = img_original[ROI_y: ROI_y + ROI_h, ROI_x : ROI_x + ROI_w]   # 裁剪坐标为[y0:y1, x0:x1]
    cv2.imshow('Img_window',Img_window)
    # cv2.waitKey(0)
    return Img_window

#############图片去除低亮度点##############
def BackgroundBlack(img_input, threshold):
    height = img_input.shape[0]        #将tuple中的元素取出，赋值给height，width，channels
    width = img_input.shape[1]
    for col in range(width):    #遍历每一列 640
        for row in range(height): #遍历该列中的每一行 480中的一部分
            if img_input[row][col][0] < threshold:     #img_input[row][col][0]代表图像中[row][col]这个点的LAB中的L参数，另外两个是AB
                img_input[row][col][0] = 0       #三个参数的范围都是0-255，0 代表全黑
                img_input[row][col][1] = 0
                img_input[row][col][2] = 0
    return img_input

#############图片过滤##############
def FindPointInCol(img_input):
    height = img_input.shape[0]        #将tuple中的元素取出，赋值给height，width，channels
    width = img_input.shape[1]
    LightPoint = []

    for col in range(width):    #遍历每一列 640
        Point_pos = 0
        Point_value = 0
        Point_value_max = 0

        for row in range(height): #遍历该列中的每一点 480中的一部分
            Point_value = img_input[row][col][0]
            # print('行：',row, img_lab[row][col][0])
            if Point_value > Point_value_max:
                Point_value_max = Point_value
                Point_pos = row
                # print(Point_pos)
        img_input[Point_pos][col][0] = 255   #对图像进行打点
        img_input[Point_pos][col][1] = 255
        img_input[Point_pos][col][2] = 255 
        LightPoint.insert(col, Point_pos)  #存储的只是从0,0开始的一维数组，包含了线条的点特征


    cv2.imshow("FindPointInCol", img_input)
    # cv2.waitKey(0)
    return LightPoint

#############对找到的点进行二次过滤，取一行中点最多的##############
def Lines_Filter(img_input, LightPoint):
    height = img_input.shape[0]        #将tuple中的元素取出，赋值给height，width，channels
    width = img_input.shape[1]

    Line_point_num = 0
    Line_point_num_max = 0
    Line_Pos = 0
    for row in range(1, height-1): #遍历该列中的每一行 480中的一部分
        for col in range(0, width):    #遍历每一列 640
            if LightPoint[col] == row :
                Line_point_num += 1
        if Line_point_num > Line_point_num_max:
            Line_point_num_max = Line_point_num
            Line_Pos = row
        Line_point_num = 0
    return Line_Pos

#############初次分析一张图像中一行的起始和结束点##############
def StartEnd_Point(width, height, LightPoint):
    Middle = int((width+height)/2)
    start = 0
    end = 0
    for col in range(Middle):
        if LightPoint[Middle - col] <= 1 or LightPoint[Middle - col]>=height - 1 :
            start = Middle - col
            break
    for col in range(Middle,width):
        if LightPoint[col] <= 1 or LightPoint[col]>=height - 1 :
            end = col
            break
    return start,end

#############计算所有图像的左点和右点平均值##############
def StartEnd_Caculate(LineStart_Point, LineEnd_Point, original_length):
    # 遍历所有数组元素
    for i in range(original_length):
        for j in range(0, original_length-i-1):
            if LineStart_Point[j] > LineStart_Point[j+1] :
                LineStart_Point[j], LineStart_Point[j+1] = LineStart_Point[j+1], LineStart_Point[j]

    for i in range(original_length):
        for j in range(0, original_length-i-1):
            if LineEnd_Point[j] > LineEnd_Point[j+1] :
                LineEnd_Point[j], LineEnd_Point[j+1] = LineEnd_Point[j+1], LineEnd_Point[j]

    nums = 0
    start = 0
    end = 0
    for i in range(2,int(original_length-2)):
        start+= LineStart_Point[i]
        nums += 1 
    start /= nums
    nums = 0
    for i in range(2,int(original_length-2)):
        end+= LineEnd_Point[i]
        nums += 1 
    end /= nums
    return int(start),int(end)


#############将计算好的宽度的一个面的二维数组保存在txt文件中##############
def PointSaveToTXT(facepoint, start_point, end_point, original_length, pixl_width):
    open("text.txt", 'w').close()
    textfile1 =  open('text.txt','a',encoding='utf8') # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
    data = []
    count = 0
    for picnum in range(original_length):
        for pointnum in range(int(end_point-start_point)):
            data.insert(int(picnum * pixl_width + pointnum),facepoint[picnum * pixl_width + start_point + pointnum])
            count+=1
            textfile1.write(str(facepoint[picnum * pixl_width + start_point + pointnum]))
            textfile1.write('#')
        textfile1.write('\n')

    #print(data)
    print('count=',count)




#############对激光线进行重新拟合，并且输出指定范围的点##############
def PointRecode(width, height, LightPoint, start_point, end_point):
    Middle = int(width/2)
    # print('width',str(width))
    # print('height',str(height))
    # print('Middle',str(Middle))
    # # print('step1')
    # start = 0
    # end = 0
    # # print('step1\n')
    # for col in range(Middle):
    #     # print('col',str(Middle - col),'point',str(LightPoint[Middle - col]))
    #     if LightPoint[Middle - col] <= 2 or LightPoint[Middle - col]>=height - 2 :
    #         start = Middle - col
    #         break

    # # print('step2\n')
    # for col in range(Middle,width):
    #     # print('col',str(col),'point',str(LightPoint[col]))
    #     if LightPoint[col] <= 2 or LightPoint[col]>=height - 2 :
    #         end = col
    #         break
    # # print('step3\n')
    # # print('\n')
    # Line_Width = end - start
    # Line_Middle = (end - start) / 2
    # # print('step1' + str(Line_Width) + '\n')
    # return Line_Width,Line_Middle






#############主程序##############
def main():
    LightPoint = []   #一张图像的图像最亮点，并且返回最亮点的坐标-例如LightPoint[1]代表某一张图片的第2个亮点的x坐标，LightPoint[2]代表某一张图片的第3个亮点的x坐标
    LineStart_Point = [] #每张图片的激光线条起始点
    LineEnd_Point = [] #每张图片的激光线条结束点-例如：LineEnd_Point[2]代表图片2的激光结束点的X坐标
    Line_Width = [] 
    face = []  #整个面的所有数据，每张图片生成一行的深度数据

    #输入长高
    original_length = int(input("please enter the length(mm): "))
    # original_height = int(input("please enter the height(mm): "))

    #第一张和最后一张不要
    original_length -= 2

    pixl_width = 600
    #遍历每一张图片，共original_length张
    for picnum in range(original_length):
        print("Picture",picnum+1,"handling...")
        ImgLab = Open_pics(picnum+1)  #打开第picnum张图

        ImgWindow = Pic_Window_Cut(ImgLab,20,250, pixl_width, 30)   #图片裁剪，x,y,w,h

        window_width = ImgWindow.shape[1]#开窗的宽度
        window_height = ImgWindow.shape[0]#开窗的高度

        Img = BackgroundBlack(ImgWindow,76)#开窗无效背景去除为黑色

        LightPoint = FindPointInCol(Img)#寻找处理后的图像最亮点，并且返回最亮点的坐标（一维数组）
        for j in range(pixl_width):
            face.insert(picnum*pixl_width+j, LightPoint[j])
            # print(LightPoint[j])
        start_point, end_point = StartEnd_Point(window_width,window_height,LightPoint);  #找到每一行的起始结束点，并且存储
        LineStart_Point.insert(picnum, start_point)#扫描该图像的最亮点，返回亮点的起始点和终点
        LineEnd_Point.insert(picnum, end_point)#扫描该图像的最亮点，返回亮点的起始点和终点

    print('start_point')
    print(LineStart_Point)
    print('end_point')
    print(LineEnd_Point)

    #计算平均起始点和结束点
    start_point,end_point = StartEnd_Caculate(LineStart_Point,LineEnd_Point,original_length)#########这里需要有一个滤波，对一整条的起始线进行滤波，也对结束线进行滤波，可以用排序，再去除头尾部分数据
    print('start_point_avrage',start_point)
    print('end_point_avrage',end_point)

    #保存在TXT文件中的高度数据，face:所有点的数据，start_point:激光线的开始点，end_point：激光线的结束点，original_length：图像数量，也就是物体长度，pixl_width：计算出来的激光线宽度
    PointSaveToTXT(face, start_point, end_point, original_length, pixl_width)


    print('pixl_width',end_point - start_point)
    

    # for picnum in range(0, 1):
    #     Line_Width.insert(picnum, (LineStartEnd_Point[0] + LineStartEnd_Point[1]) / 2)  ##########这里需要有一个起始点和终点平均值计算，用于接下来的三维拟合
    # pic_width = 0  #图片宽度计算

    # for picnum in range(0, 1):
    #     for point in range(0, pic_width):
    #         face.insert(picnum*pic_width+point, PointRecode(window_width, window_height, LightPoint, start_point, end_point)) #转换为二维数组





main()