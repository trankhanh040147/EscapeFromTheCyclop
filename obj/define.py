from win32api import GetSystemMetrics

# Size of SCREEN
WORLD_X = GetSystemMetrics(0)
WORLD_Y = GetSystemMetrics(1)
U = WORLD_X/1536
# Tốc độ khung hình
FPS = 60

# Một số màu
RED = (255,0,0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
ALPHA = GREEN

# player size
PLAYER_SIZE = (int(WORLD_X/15), int(WORLD_X/15))

# nửa đường chéo rect player
PLAYER_RADIUS = int(PLAYER_SIZE[0]/10)

# Vị trí bắt đầu của player
PLAYER_START_POS = [int(WORLD_X/2), int(WORLD_Y/2)]

# Tốc độ di chuyển player
PLAYER_SPEED = int(WORLD_X/500)

# MONSTER size
MONSTER_SIZE = (int(WORLD_X/30), int(WORLD_X/30))

# nửa đường chéo rect player
MONSTER_RADIUS = int(MONSTER_SIZE[0]/15)

# Tốc độ di chuyển MONSTER
MONSTER_SPEED = int(WORLD_X/500)

# Block size
BLOCK_SIZE = (int(WORLD_X/30), int(WORLD_X/30))

# key animation
ANIMATION = 4