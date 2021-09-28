# -*- coding: utf-8 -*-
import cv2
import numpy as np
# 输入头像的文件位置以及名字，但是不要后缀，这是为了后面保存方便
path = 'q_p'
name = path + '.jpg'
# 读取国旗头像框，百度图片下的，分辨率低，效果一般，这个读取路径以及名字需要正确
img_src = cv2.imread('p5.png')
# 读取头像图片
target = cv2.imread(name)
# 调整两个图片长宽一致，这里是根据国旗头像框的长宽决定的，因为它的分辨率低，迁就它
img_src = cv2.resize(img_src, (600, 600), interpolation=cv2.INTER_LINEAR)
target = cv2.resize(target, (600, 600), interpolation=cv2.INTER_LINEAR)
# 高斯滤波
img = cv2.GaussianBlur(img_src, (5, 5), 0)
# 下面是一个做掩膜的过程
# 首先是BGR 2 GRAY灰度图
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 掩膜：利用阈值函数cv2.threshold()，将灰度图转换为二值图
ret, mask_img = cv2.threshold(img_gray, 230, 255, cv2.THRESH_BINARY)
ret, mask_target = cv2.threshold(img_gray, 230, 255, cv2.THRESH_BINARY_INV)
# 将掩膜图像转换为与原图像相同的BGR形式
mask_img = cv2.cvtColor(mask_img, cv2.COLOR_GRAY2BGR)
mask_target = cv2.cvtColor(mask_target, cv2.COLOR_GRAY2BGR)
# 对图像进行按位操作，按位于：取色素值小的（黑色最小）
# 按位或：取色素值大的（白色最大）（按位或与是个人理解）
target_after_mask = cv2.bitwise_or(target, mask_target)
img_after_mask = cv2.bitwise_or(img_src, mask_img)
# 将用掩膜处理过的图像按位与，参照上面说明，则国旗应该在新头像上了
fin = cv2.bitwise_and(target_after_mask, img_after_mask)
#最后再加个滤波，模糊边界，使图片看起来更平滑
fin = cv2.medianBlur(fin, 5)

while 1:
    cv2.imshow('fina', fin)
    # 按 esc 退出显示
    if cv2.waitKey(1) & 0xFF == 27:
        break
# 保存新头像，这里就用到了开头定义的path，这里是在原图像名字后面加1来区分，
# 因为我试了几个不同的图片，对结果进行对比，所以需要区分
save_name = path + '1.jpg'
cv2.imwrite(save_name,fin)
cv2.destroyAllWindows()
