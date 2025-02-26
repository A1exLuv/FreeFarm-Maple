import gdi_capture
import numpy as np
import cv2
import pyautogui
# set Moonlight and Maplestory 800*600
# These are colors taken from the mini-map in BGRA format.
PLAYER_BGRA = (68, 221, 255, 255)
RUNE_BGRA = (255, 102, 221, 255)
ENEMY_BGRA = (0, 0, 255, 255)
GUILD_BGRA = (255, 102, 102, 255)
BUDDY_BGRA = (225, 221, 17, 255)

button_rgb_ready = []

button_location_q = (592, 484)  # q按键位置 (x, y) 0
button_location_w = (622, 484)  # w按键位置 (x, y) 1
button_location_e = (652, 484)  # e按键位置 (x, y) 2
button_location_r = (682, 484)  # r按键位置 (x, y) 3
button_location_s = (622, 514)  # s按键位置 (x, y) 4
button_location_d = (652, 514)  # d按键位置 (x, y) 5
button_location_f = (682, 514)  # f按键位置 (x, y) 6
button_location_1 = (742, 514)  # 1按键位置 (x, y) 7

button_size = 30

class Game:
    def __init__(self, region):
        self.hwnd = gdi_capture.find_window_from_executable_name("MapleStory.exe")
        # self.hwnd = gdi_capture.find_window_from_executable_name("Moonlight.exe")
        # self.hwnd = gdi_capture.find_window_from_executable_name("r720 - Moonlight.exe")
        # print(f"窗口句柄: {self.hwnd}")
        # These values should represent pixel locations on the screen of the mini-map.
        self.left, self.top, self.right, self.bottom = region[0], region[1], region[2], region[3]
        global button_rgb_ready
        button_rgb_ready = [self.button_rgb(button_location_q, button_size),
                            self.button_rgb(button_location_w, button_size),
                            self.button_rgb(button_location_e, button_size),
                            self.button_rgb(button_location_r, button_size),
                            self.button_rgb(button_location_s, button_size),
                            self.button_rgb(button_location_d, button_size),
                            self.button_rgb(button_location_f, button_size),
                            self.button_rgb(button_location_1, button_size)]
        print (button_rgb_ready)


    def get_rune_image(self):
        """
        Takes a picture of the application window.
        """
        with gdi_capture.CaptureWindow(self.hwnd) as img:
            if img is None:
                # print("MapleStory.exe was not found.")
                print("Moonlight.exe was not found.")
                return None
            return img.copy()

    def locate(self, *color):
        """
        Returns the median location of BGRA tuple(s).
        """
        with gdi_capture.CaptureWindow(self.hwnd) as img:
            locations = []
            if img is None:
                # print("MapleStory.exe was not found.")
                print("Moonlight.exe was not found.")
            else:
                """
                The screenshot of the application window is returned as a 3-d np.ndarray, 
                containing 4-length np.ndarray(s) representing BGRA values of each pixel.
                """
                # Crop the image to show only the mini-map.
                img_cropped = img[self.top:self.bottom, self.left:self.right]
                height, width = img_cropped.shape[0], img_cropped.shape[1]
                # print(height, width)
                # Reshape the image from 3-d to 2-d by row-major order.
                img_reshaped = np.reshape(img_cropped, ((width * height), 4), order="C")
                for c in color:
                    sum_x, sum_y, count = 0, 0, 0
                    # Find all index(s) of np.ndarray matching a specified BGRA tuple.
                    matches = np.where(np.all((img_reshaped == c), axis=1))[0]
                    for idx in matches:
                        # Calculate the original (x, y) position of each matching index.
                        sum_x += idx % width
                        sum_y += idx // width
                        # sum_y += idx % height
                        count += 1
                    if count > 0:
                        x_pos = sum_x / count
                        y_pos = sum_y / count
                        locations.append((x_pos, y_pos))

            # test
            # print(locations)


            return locations

    def get_player_location(self):
        """
        Returns the (x, y) position of the player on the mini-map.
        """

        location = self.locate(PLAYER_BGRA)
        # print("player:",location)

        return location[0] if len(location) > 0 else None

    def get_rune_location(self):
        """
        Returns the (x, y) position of the rune on the mini-map.
        """
        location = self.locate(RUNE_BGRA)
        # print("rune:", location)
        return location[0] if len(location) > 0 else None

    def get_other_location(self):
        """
        Returns a boolean value representing the presence of any other players on the mini-map.
        """
        location = self.locate(ENEMY_BGRA, GUILD_BGRA, BUDDY_BGRA)
        return len(location) > 0

    # button_location[0], button_location[1]:(lefttop) x-position, y-position
    def button_rgb(self, button_location, button_size):
        with gdi_capture.CaptureWindow(self.hwnd) as img:
            if img is None:
                # print("MapleStory.exe was not found.")
                print("Moonlight.exe was not found.")
            else:
                # 截取指定区域的屏幕截图
                # screenshot = pyautogui.screenshot(
                #     region=(button_location[0], button_location[1], 30, 30))
                screenshot = img[button_location[1]:button_location[1]+button_size, button_location[0]:button_location[0]+button_size]
                # 将截图转换为 numpy 数组
                img = np.array(screenshot)

                # 转换为 RGB 颜色模式（pyautogui 截图是 RGB 模式）
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                # 获取按钮的中间区域颜色，这里假设按钮的中间部分最能代表按键状态
                # 取按键距离下边框5pixel位置
                # middle_x, middle_y = img_rgb.shape[1] // 2, img_rgb.shape[0] // 2
                middle_x, middle_y = img_rgb.shape[1] // 2, img_rgb.shape[0] -5
                color = img_rgb[middle_y, middle_x]  # 获取该位置的颜色

                #
                return color

    # button_location[0], button_location[1]:(lefttop) x-position, y-position
    def is_button_ready(self, button_location, button_size, num):
        with gdi_capture.CaptureWindow(self.hwnd) as img:
            if img is None:
                # print("MapleStory.exe was not found.")
                print("Moonlight.exe was not found.")
            else:
                # 截取指定区域的屏幕截图
                # screenshot = pyautogui.screenshot(
                #     region=(button_location[0], button_location[1], 30, 30))
                screenshot = img[button_location[1]:button_location[1]+button_size, button_location[0]:button_location[0]+button_size]
                # 将截图转换为 numpy 数组
                img = np.array(screenshot)

                # 转换为 RGB 颜色模式（pyautogui 截图是 RGB 模式）
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                # 获取按钮的中间区域颜色，这里假设按钮的中间部分最能代表按键状态
                # 取按键距离下边框5pixel位置
                # middle_x, middle_y = img_rgb.shape[1] // 2, img_rgb.shape[0] // 2
                middle_x, middle_y = img_rgb.shape[1] // 2, img_rgb.shape[0] -5
                color = img_rgb[middle_y, middle_x]  # 获取该位置的颜色


                # 判断按键是否变色
                r, g, b = color
                global button_rgb_ready
                r1, g1, b1 = button_rgb_ready[num]
                if abs(r - r1) == 0 and abs(g - g1) == 0 and abs(b - b1) == 0:  # 这里假设灰色的 RGB 值接近且较暗
                    return True  # 技能可用
                else:
                    return False  # 技能不可用
