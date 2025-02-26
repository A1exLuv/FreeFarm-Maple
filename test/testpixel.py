import numpy as np
import cv2
import matplotlib.pyplot as plt


# 读取图像
img = cv2.imread('testpixel.png')

# 获取某个特定位置的像素值
x, y = 177, 86  # 假设要获取 (100, 50) 位置的像素
pixel_value = img[y, x]  # OpenCV 中是 [y, x] 顺序
print(pixel_value)

# 创建一个 100x100 的图像，并填充指定的颜色
color_img = np.zeros((100, 100, 3), dtype=np.uint8)
color_img[:] = pixel_value

# 显示颜色块
plt.imshow(color_img)
plt.axis('off')  # 不显示坐标轴
plt.show()

# # 创建一个 1x1 的图像来表示该颜色
# plt.imshow([[pixel_value]])
# plt.axis('off')  # 不显示坐标轴
# plt.show()