import base64
import os
import cv2 as cv
from PIL import Image
import numpy as np
# 一次只能处理一个哦

def str_to_pic(picname):
    f = open(str(picname), 'rb')
    ls_f = base64.b64encode(f.read())
    f.close()
    print(ls_f)
    data = str(ls_f)
    new_data = data[2:-1]
    with open("data.txt",'w') as f:
        f.write(new_data)
    print('-' * 32)

def pic_to_str(dataname):
    with open(str(dataname), "r") as f:
        imgdata = base64.b64decode(f.read())
        file = open('test.jpg', 'wb')
        file.write(imgdata)
        file.close()

def png_to_jpg(picname):
    f = open(str(picname), 'rb')
    ls_f = base64.b64encode(f.read())
    f.close()
    print(ls_f)
    data = str(ls_f)
    new_data = data[2:-1]
    imgdata = base64.b64decode(new_data)
    file = open('test.jpg', 'wb')
    file.write(imgdata)
    file.close()


def cut(picname):
    img = cv.imread(str(picname))
    sp = img.shape
    sp1 = sp[0] #宽
    sp2 = sp[1] #长
    n = int(input("请输入分割图象数："))
    sp2_i = int(sp2 / n)
    sp2_n = int(sp2 / n)
    sp2_0 = 0
    while sp2_n <= sp2:
        for i in range(n):
            new_img = img[0:sp1,sp2_0:sp2_n]
            cv.imwrite('G:/BASE_64/1/GAN_img/'+str(i)+'.jpg',new_img)
            sp2_0 += sp2_i
            sp2_n += sp2_i
            print('第' + str(int(i) + 1) + '部分完成保存')

def watershed_function(image):
    # 前提：降噪
    blurred = cv.pyrMeanShiftFiltering(image, 25, 100)

    # 第一步：灰度处理
    gray = cv.cvtColor(blurred, cv.COLOR_BGR2GRAY)

    # 第二步：二值化处理
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
    #cv.imshow("binary", binary)

    # 第三步：距离变换
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    mb = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel,iterations=2)  # 连续两次开操作
    sure_bg = cv.dilate(mb, kernel, iterations=3) #对开操作的结果进行膨胀
    #cv.imshow("open then dilate", sure_bg)
    '''
        distance_TYpe = cv.DIST_L2：欧几何距离
        maskSize = 3
    '''
    distance = cv.distanceTransform(mb, cv.DIST_L2, 3)
    dist_output = cv.normalize(distance, 0, 1.0, cv.NORM_MINMAX)
    #cv.imshow("distance", dist_output*50)

    # 第四步：寻找种子
    ret, surface = cv.threshold(distance, distance.max()*0.6, 255, cv.THRESH_BINARY)
    #cv.imshow("surface", surface)

    # 第五步：生成marker
    surface_fg = np.uint8(surface) #将 float 转为8位
    unknown = cv.subtract(sure_bg, surface_fg)
    ret, markers = cv.connectedComponents(surface_fg) #连通区域
    print(ret)

    # 分水岭变换
    markers = markers + 1
    markers[unknown == 255] = 0
    markers = cv.watershed(image, markers=markers)
    image[markers == -1] = [0, 0, 255] #分水岭标记为红色
    #cv.imshow("watershed", image)
    cv.imwrite('G:/BASE_64/1/watershed/' + img , image)


choose = "0"
bc = '0'
bs = "0"
print("#模式1：图片转为base64编码")
print("#模式2：base64编码转为图片")
print("#模式3：png转jpg")
print("#模式4：裁剪图片")
print("#模式5：显示图片信息")
print("#模式6：分水岭算法边缘检测")
print("#模式7：EXIT")
print("#一次只能处理一个哦#")

while True:
    if choose == "0":
        choose = input('输入工作模式：')
    elif choose == "1":
        picname = input("请输入图片地址：")
        str_to_pic(picname)
        choose = "0"
    elif choose == "2":
        dataname = input("请输入base64编码文件地址：")
        pic_to_str(dataname)
        choose = "0"
    elif choose == "3":
        picname = input("请输入图片地址：")
        png_to_jpg(picname)
        choose = "0"
    elif choose == "4":
        picname = input('请输入图像名称及格式：')
        cut(picname)
        choose = "0"
    elif choose == "5":
        img = cv2.imread(str(picname))
        sp = img.shape
        print(sp)
        choose = "0"
    elif choose == "6":
        img = input('请输入图像名称及格式：')
        image = cv.imread(img)
        watershed_function(image)
        choose = "0"
    elif choose == "7":
        break
    else:
        choose = "0"
