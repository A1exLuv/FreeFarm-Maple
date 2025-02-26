from PIL import Image

# RGB 颜色
PLAYER_BGRA = (68, 221, 255, 255)
RUNE_BGRA = (255, 102, 221, 255)
ENEMY_BGRA = (0, 0, 255, 255)
GUILD_BGRA = (255, 102, 102, 255)
BUDDY_BGRA = (225, 221, 17, 255)

PLAYER_RGB = (255, 221, 68)
RUNE_RGB = (221, 102, 255)
ENEMY_RGB = (255, 0, 0)
GUILD_RGB = (102, 102, 255)
BUDDY_RGB = (17, 221, 225)


# 创建 100x100 的图像并填充该颜色
img = Image.new("RGB", (100, 100), BUDDY_RGB)

# 显示图像
img.show()