import cv2
import numpy as np
import pyautogui
from tensorflow.python.ops.gen_functional_ops import While

def button_rgb(button_location, button_size):
    # 截取指定区域的屏幕截图
    screenshot = pyautogui.screenshot(region=(button_location[0], button_location[1], button_size[0], button_size[1]))

    # 将截图转换为 numpy 数组
    img = np.array(screenshot)

    # 转换为 RGB 颜色模式（pyautogui 截图是 RGB 模式）
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 获取按钮的中间区域颜色，这里假设按钮的中间部分最能代表按键状态
    middle_x, middle_y = img_rgb.shape[1] // 2, img_rgb.shape[0] // 2
    color = img_rgb[middle_y, middle_x]  # 获取该位置的颜色

    # 将可使用状态的技能中心点rgb存入全局变量button_rgb_ready[num]
    return color

def is_button_in_cd(button_location, button_size,num):
    # 截取指定区域的屏幕截图
    screenshot = pyautogui.screenshot(region=(button_location[0], button_location[1], button_size[0], button_size[1]))

    # 将截图转换为 numpy 数组
    img = np.array(screenshot)

    # 转换为 RGB 颜色模式（pyautogui 截图是 RGB 模式）
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 获取按钮的中间区域颜色，这里假设按钮的中间部分最能代表按键状态
    middle_x, middle_y = img_rgb.shape[1] // 2, img_rgb.shape[0] // 2
    color = img_rgb[middle_y, middle_x]  # 获取该位置的颜色

    # 判断按键是否变色
    r, g, b = color
    global button_rgb_ready
    r1, g1, b1 = button_rgb_ready[num]
    if abs(r - r1) < 5 and abs(g - g1) < 5 and abs(b - b1) < 5:  # 这里假设灰色的 RGB 值接近且较暗
        return True  # 按键可用
    else:
        return False  # 按键不可用

# 假设按钮位置为 (100, 100) 且大小为 (50, 50)
button_location_q = (592, 514)  # 按键位置 (x, y)

button_location_w = (630, 550)  # 按键位置 (x, y)
button_size = (30, 30)        # 按键的尺寸 (宽, 高)

global button_rgb_ready
button_rgb_ready = [button_rgb(button_location_q, button_size),
                    button_rgb(button_location_w, button_size)]
while True:
 if is_button_in_cd(button_location_q, button_size, 0):
    print("q技能可用。")
 else:
    print("q技能不可用。")
 if is_button_in_cd(button_location_w, button_size, 1):
    print("w技能可用。")
 else:
    print("w技能不可用。")
