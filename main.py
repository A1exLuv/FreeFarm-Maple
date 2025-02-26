"freefarm-maple started on 2025/2/26 by Alex"
import time
import random
import threading


from rune_solver import find_arrow_directions
from interception import *
from game import Game
from player import Player
from capture import Capture

# go_to阈值
x_summon,y_summon = 4,15
x_mid,y_mid = 4,10

# 按键绑定
keybinding_w = False
keybinding_e = True
keybinding_r = False
keybinding_s = True
keybinding_d = True
keybinding_f = False
keybinding_t = True


button_location_q = (592, 484)  # q按键位置 (x, y) 0
button_location_w = (622, 484)  # w按键位置 (x, y) 1
button_location_e = (652, 484)  # e按键位置 (x, y) 2
button_location_r = (682, 484)  # r按键位置 (x, y) 3
button_location_s = (622, 514)  # s按键位置 (x, y) 4
button_location_d = (652, 514)  # d按键位置 (x, y) 5
button_location_f = (682, 514)  # f按键位置 (x, y) 6
button_location_1 = (742, 514)  # 1按键位置 (x, y) 7

button_size = 30

def bind(context):
    context.set_filter(interception.is_keyboard, interception_filter_key_state.INTERCEPTION_FILTER_KEY_ALL.value)
    print("Click any key on your keyboard.")
    device = None
    while True:
        device = context.wait()
        if interception.is_keyboard(device):
            print(f"Bound to keyboard: {context.get_HWID(device)}.")
            c.set_filter(interception.is_keyboard, 0)
            break
    return device

def solve_rune(g, p, target):
    """
    Given the (x, y) location of a rune, the bot will attempt to move the player to the rune and solve it.
    """
    while True:
        print("Pathing towards rune...")
        p.go_to(target, 2, 7)
        # Activate the rune.
        time.sleep(1)
        p.press("SPACE")
        # Take a picture of the rune.
        time.sleep(1)
        img = g.get_rune_image()
        print("Attempting to solve rune...")
        directions = find_arrow_directions(img)

        if len(directions) == 4:
            print(f"Directions: {directions}.")
            for d, _ in directions:
                p.press(d)

            # The player dot will be blocking the rune dot, attempt to move left/right to unblock it.
            p.hold("LEFT")
            time.sleep(random.uniform(0.5, 1.25))
            p.release("LEFT")

            p.hold("RIGHT")
            time.sleep(random.uniform(0.5, 1.25))
            p.release("RIGHT")

            rune_location = g.get_rune_location()
            if rune_location is None:
                print("Rune has been solved.")
                break
            else:
                print("Trying again...")




if __name__ == "__main__":
    # Get minimap location
    capture = Capture()._main()
    target = ((capture[2]-capture[0])/2, (capture[3]-capture[1])/2)
    print(capture, target)
    # This setup is required for Interception to mimic your keyboard.
    c = interception()
    d = bind(c)
    g = Game(capture) #minimap:left,top,right,bot
    g1 = Game((0,0,800,800))
    p = Player(c, d, g)
    Summon = False


    while True:
        if keybinding_w == False:
            # 喷泉
            if g1.is_button_ready(button_location_q, button_size, 0):
                p.go_to((random.uniform(10, 15), target[1]), x_summon, y_summon)
                time.sleep(random.uniform(0.5, 0.75))
                p.press("Q")
                time.sleep(random.uniform(0.7, 0.75))
                Summon = True
            if Summon == True:
                p.go_to((target[0] * 2 - random.uniform(10, 15), target[1]), x_summon, y_summon)
                time.sleep(random.uniform(0.5, 0.75))
                p.press("W")
                time.sleep(random.uniform(0.7, 0.75))
                Summon = False
        else:
            # 喷泉
            if g1.is_button_ready(button_location_q, button_size, 0):
                p.go_to((random.uniform(10, 15), target[1]), x_summon, y_summon)
                time.sleep(random.uniform(0.5, 0.75))
                p.press("Q")
                time.sleep(random.uniform(0.7, 0.75))
            if g1.is_button_ready(button_location_w, button_size, 1):
                p.go_to((target[0] * 2 - random.uniform(10, 15), target[1]), x_summon, y_summon)
                time.sleep(random.uniform(0.5, 0.75))
                p.press("W")
                time.sleep(random.uniform(0.7, 0.75))
        # 有人
        other_location = g.get_other_location()
        if other_location > 0:
            print("A player has entered your map.")
        # 符文出现
        rune_location = g.get_rune_location()
        if rune_location is not None:
            print("A rune has appeared.")
            solve_rune(g, p, rune_location)
        # 蜘蛛
        if keybinding_e:
            if g1.is_button_ready(button_location_e, button_size, 2):
                p.press("E")
                time.sleep(random.uniform(0.7, 0.75))
        # 密特拉
        if keybinding_r:
            if g1.is_button_ready(button_location_r, button_size, 3):
                p.press("R")
                time.sleep(random.uniform(0.7, 0.75))
        # s
        if keybinding_s:
            if g1.is_button_ready(button_location_s, button_size, 4):
                p.press("S")
                time.sleep(random.uniform(0.7, 0.75))
        # d
        if keybinding_d:
            if g1.is_button_ready(button_location_d, button_size, 5):
                p.press("D")
                time.sleep(random.uniform(0.7, 0.75))
        # f
        if keybinding_f:
            if g1.is_button_ready(button_location_f, button_size, 6):
                p.press("F")
                time.sleep(random.uniform(0.7, 0.75))
        # 跑中心
        print("Running...")
        p.go_to(target, x_mid, y_mid)
        # 移动
        if random.random() < 0.02:
            p.hold("LEFT")
            time.sleep(random.uniform(0.1, 0.15))
            p.release("LEFT")
        if random.random() < 0.02:
            p.hold("RIGHT")
            time.sleep(random.uniform(0.1, 0.15))
            p.release("RIGHT")

        # 主攻
        p.press("A")
        time.sleep(random.uniform(0.7, 0.75))

        # p.press("W")
        # time.sleep(3)
        # p.go_to(target)
        # p.press("LEFT")
        # time.sleep(0.5)
        # p.hold("E")
        # time.sleep(0.5)
        # p.release("E")
        # p.go_to(target)
        # p.press("RIGHT")
        # time.sleep(0.5)
        # p.hold("E")
        # time.sleep(0.5)
        # p.release("E")
        # time.sleep(3)
