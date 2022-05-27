#Tham khảo:
#     + GV. Trần Nhật Quang
#     + Russell 2016 Artificial intelligence a modern approach
#     + Thuật toán Chebyshev distance: http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html#diagonal-distance

class Node:
    '''
    Mỗi node gồm các thông tin:
    position: tọa độ trong mê cung
    parent: node cha của node hiện tại 
    f: hàm lượng giá
    g: độ dài quãng đường thực tế từ start_node đến node hiện tại
    h: hàm Heuristics, ước lượng khoảng cách từ node hiện tại cho đến goal_node, theo thuat toan Chebyshev distance
    '''

    def __init__(self, position, parent = None, f_value = 0, g_value = 0, h_value = 0):
        self.position = position
        self.parent = parent
        self.f = f_value
        self.g = g_value
        self.h = h_value

    def __eq__(self, other):
        '''Dùng để so sánh 2 node'''
        return self.position == other.position

    def ChildNode(self, maze):
        '''
        Dùng để sinh ra các node con của node hiện tại
        maze: là ma trận chứa mê cung
        '''
        children = []

        # for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
        for new_position in [(0,-1),(0,1),(-1,0),(1,0)]:
            #get node position
            node_position = (self.position[0] + new_position[0], self.position[1] + new_position[1])
            node_position = (int(node_position[0]),int(node_position[1]))

            #Kiểm tra position của node có hợp lệ hay không (có nằm trong maze hay không)
            if node_position[0] < 0 or node_position[0] > (len(maze) - 1) or node_position[1] < 0 or node_position[1] > (len(maze[len(maze) - 1]) - 1):
                continue

            #Kiểm tra có đi nhầm vào ô chứa vật cản hay không 
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            #Tạo node mới
            new_node = Node(position = node_position, parent = self)

            #Thêm new_node vào children 
            children.append(new_node)

        return children


def astar(maze, start, end):
    #Khoi tao cac node start va end
    start_node = Node(position = start)
    end_node = Node(position = end)

    #Khoi tao open_list va closed_list
    open_list = []
    closed_list = []

    #Them start node vao open_list
    open_list.append(start_node)

    while len(open_list) > 0:  #while open_list is not EMPTY

        current_node = open_list[0]
        current_index = 0

        #Tim node co ham f nho nhat co trong open_list
        for index, node in enumerate(open_list):
            if node.f < current_node.f:
                current_index = index
                current_node = node

        open_list.pop(current_index)
        closed_list.append(current_node)

        #Kiem tra current_node co phai la end_node khong
        if current_node == end_node:
            #Path cho biết đường đi từ start node đến goal_node 
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent

            return path[::-1] #dao nguoc lai

        #Nguoc lai, current_node khong phai la end_node
        #Expand các child node của current_node
        children = current_node.ChildNode(maze)
        for child in children:
            #Tinh gia tri f, g, h cua child node

            child.g = current_node.g + 1
            #Ham heuristic, tinh theo thuat toan Chebyshev distance, tham khao tai http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html#diagonal-distance
            dx = abs(child.position[0] - end_node.position[0])
            dy = abs(child.position[1] - end_node.position[1])
            child.h = (dx + dy) - min(dx, dy)
            child.f = child.g + child.h

            def Check(list):
                '''
                Dùng để kiểm tra xem child đã có trong list hay chưa. Nếu đã tồn tại, mà child.g nhỏ hơn (đường đi qua child có chi phí thấp hơn), thì replace đường đi cũ bằng đường đi mới (đi qua node child)
                list: open_list hoặc losed_list
                '''
                for index, node in enumerate(list):
                    if node == child and node.g > child.g:
                        list.pop(index)
                        open_list.append(child)
                        return 

            #Kiem tra child node
            if child not in open_list and child not in closed_list:
                open_list.append(child)
            elif child in open_list:
                Check(open_list)
            elif child in closed_list:
                Check(closed_list)
            else:
                continue
