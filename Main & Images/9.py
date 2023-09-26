def main():
    #变量
    Line_start_point = [] #每张图片的激光线条起始点
    Line_end_point = [] #每张图片的激光线条结束点-Line_end_point[2]代表图片2的激光结束点的X坐标
    face = []  #整个面的所有数据，每张图片生成一行的深度数据
    line_row_history = [] #每张图片的激光线条起始点
    #输入长高
    original_length = int(input("please enter the length(mm): "))
    #第一张和最后一张不要
    original_length -= 2
    for picnum in range(original_length):
        #打开图片文件
        img_input = Open_pics(picnum + 1)
        #宽度计算
        width = img_input.shape[1]
        #提高亮度
        image = imgBrightness(img_input, 0.8, 3)
        #大津阈值计算一下基本的阈值
        threshold_otsu, img_otsu = cv2.threshold(image, 50 , 255, cv2.THRESH_OTSU)
        #阈值还需要做个增益才能投入使用
        if(threshold_otsu < 140):
            threshold = threshold_otsu + 60
        #二值化
        ret0, img_binary = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
        #二值化的图像用来计算一个基准的扫描起始线，以及作为阈值参考，没有任何其他用途
        line_row = Line_row_scan(img_binary)
        line_row_history.insert(picnum, int(line_row))
        #提取线条
        line = PointScan(image, line_row, threshold, 30)
        line = PointFilter(width, line, line_row)
        #每张图片的起始结束点计算
        left, right = start_end(width, line)
        Line_start_point.insert(picnum, left)#扫描该图像的最亮点，返回亮点的起始点和终点
        Line_end_point.insert(picnum, right)#结束点
        #检查中间是否有断点
        for col in range(left, right):
            if line[col] == 0:
                line[col] = line_row
        #保存线条到二维数组face
        for j in range(width):
            face.insert(picnum*width+j, line[j])
        #创建新白板并且绘制结果的线条
        white_board = creat_whiteboard(image);
        for col in range(640):
            white_board[int(line[col])][col] = 0 #在白板上绘制黑色线条
            img_binary[line_row][col] = 100      #在灰度图上绘制基准线
        print(picnum)
        #图像显示
        #cv2.imshow("origin", image)
        #cv2.imshow("threshold", img_binary)
        # cv2.imshow("white_board", white_board)
        #print(threshold)
        # cv2.waitKey(0)

    #计算平均起始点和结束点
    start_point_average, end_point_average = start_end_average(Line_start_point, Line_end_point, original_length)

    for picnum in range(original_length):
        for col in range(start_point_average, end_point_average):
            if face[picnum*width+col] == 0:
                face[picnum*width+col] = line_row_history[picnum]

    print('start:' + str(start_point_average) + '    end:' + str(end_point_average))

    print('width:' + str(end_point_average - start_point_average))
    PointSaveToTXT(face, start_point_average, end_point_average, original_length, width)