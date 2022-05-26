#%%
from tarfile import BLOCKSIZE
from win32api import GetSystemMetrics

# Size of SCREEN
WORLD_X = GetSystemMetrics(0)
WORLD_Y = GetSystemMetrics(1)

def toPos(p):
        rx= p[0] % 30
        ry = p[1] % 30
        xpos = p[0]//30 - 1*(rx==0)
        ypos = p[1]//30 - 1*(ry==0)
        return [xpos,ypos]

def toPixel(p):
        """Chuyển toạ độ khối block --> toạ độ pixel (lấy giá trị giữa khối block)"""
        x = p[0]*30 + 15
        y = p[1]*30 +15
        return [x,y]

print(toPos([36,95]))
print(toPixel([0,0]))


#%%
s = (0,1)
print()
# %%
def toArena(pos):
        #Kiểm tra xem toạ độ hiện tại đang nằm ở area nào 
        x = pos[0]
        y = pos[1]
        if 1<=x<=7 and 1<=y<=13:
            return 1
        elif 1<=x<=7 and 15<=y<=28:
            return 2
        elif 9<=x<=15 and 1<=y<=13:
            return 3
        elif 9<=x<=15 and 15<=y<=28:
            return 4

print(toArena([7,3]))

print(toArena([6,1]))

print(toArena([8,4]))

print(toArena([2,4]))
# %%

def initArena(arena_num,x1,y1,x2,y2):
        """Khởi tạo arena với:
        x1,y1: Toạ độ điểm nhỏ góc trái trên
        x2,y2: Toạ đổ điểm góc phải dưới"""

        arena[arena_num] = []

        col = y2-y1+1
        #Số hàng
        row = x2-x1+1
        #Số cột

        for i in range(0,row):
            arena[arena_num].append(col*[0])

        for x in range(0,row):
            for y in range(0,col):
                arena[arena_num][x][y] = maze[x1+x][y1+y]

arena = [[],[],[],[]]

maze = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1], [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1], [1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 
0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1], [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1], [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1], [1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1], [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1], [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1], [1, 0, 0, 1, 0, 0, 
1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1], [1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 
0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

initArena(0,0,0,8,14)

print(arena[0])




            
# %%
def toPos(p):
        """Chuyển toạ độ pixel --> toạ độ khối blocks"""
        # Lấy số dư
        rx= p[0] % BLOCK_SIZE[0]
        ry = p[1] % BLOCK_SIZE[1]

        xpos = p[0]//BLOCK_SIZE[0] - 1*(rx==0)
        ypos = p[1]//BLOCK_SIZE[1] - 1*(ry==0)

        if xpos == -1: xpos = 0
        if ypos == -1: ypos = 0 

        # return (xpos,ypos)
        return [xpos,ypos]

#%%
from win32api import GetSystemMetrics

# Size of SCREEN
WORLD_X = GetSystemMetrics(0)
WORLD_Y = GetSystemMetrics(1)

print(WORLD_X,WORLD_Y)
        
BLOCK_SIZE = (int(WORLD_X/30), int(WORLD_Y/30))

print(BLOCK_SIZE[0],BLOCK_SIZE[1])

print(toPos([753,456]))


# %%
