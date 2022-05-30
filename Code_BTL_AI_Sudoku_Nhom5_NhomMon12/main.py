import pygame
import pygame_widgets as pw
from pygame_widgets.button import Button
import sys
import sinh

def DrawGrid():
    bg = pygame.image.load('anh/bg.jpg')
    screen.blit(bg,(0,0))
    # Vẽ các đường kẻ
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                # điền vào các ô không trống
                pygame.draw.rect(screen, (255,239,213), (i * inc, j * inc, inc + 1, inc + 1))
                # chèn các giá trị mặc định
                text = a_font.render(str(grid[i][j]), True, (0, 0, 0))
                screen.blit(text, (i * inc + 15, j * inc + 10))
    # Vẽ các đường theo chiều ngang và chiều dọc để tạo thành lưới
    for i in range(10):
        if i % 3 == 0:
            width = 10  # cứ 3 ô nhỏ -> dòng dày hơn
        else:
            width = 5
        pygame.draw.line(screen, (0, 0, 0), (i * inc, 0), (i * inc, 500), width)  # chiều dọc
        pygame.draw.line(screen, (0, 0, 0), (0, i * inc), (500, i * inc), width)  # chiều ngang
def DeleteBox(x,y):
    pygame.draw.rect(screen, (255,255,255), (x * inc, y * inc, inc + 1, inc + 1))

# Tim vi tri để giải dau tien
def FirstPos(gridArray):
    a = []
    b = []
    for k in range(81):
        a.append({1,2,3,4,5,6,7,8,9})
    for i in range(9):
        for j in range(9):
            if gridArray[i][j] == 0 :
                b.append(i*9+j)
                for ii in range(9):
                    a[i*9+j].discard(gridArray[ii][j])
                    a[i*9+j].discard(gridArray[i][ii])
                ii = i // 3
                jj = j // 3
                for i1 in range(ii * 3, ii * 3 + 3):
                    for j1 in range(jj * 3, jj * 3 + 3):
                        a[i*9+j].discard(gridArray[i1][j1])
    min = 10
    x = -1
    y = -1
    for k in range(81):
        if (len(a[k]))<min and gridArray[k//9][k%9]==0:
            x = k//9
            y = k%9
            min = len(a[k])
    return (x,y)

# Giai dua tren thuat toan quay lui
def SolveGrid(gridArray, i, j):
    global IsSolving
    IsSolving = False
    i, j = FirstPos(gridArray)
    print(str(i)+" : "+str(j))
    if i==-1 and j==-1:
        return True
    pygame.event.pump()  # được gọi mỗi vòng lặp
    for V in range(1, 10):  # thử các giá trị từ 1-9
        if IsUserValueValid(gridArray, i, j, V):  # Nếu giá trị khả dụng, thêm nó vào ô
            gridArray[i][j] = V
            if SolveGrid(gridArray, i, j):  # Nếu giá trị là chính xác, hãy giữ lại
                return True
            else:  # Nếu sai xóa nó khỏi ô, để ô trống
                gridArray[i][j] = 0
        screen.fill((255, 255, 255))
        DrawGrid()
        DrawSelectedBox()
        DrawModes()
        pygame.display.update()
        pygame.time.delay(0)
    return False


# Thiết lập vị trí của ô chọn
def SetMousePosition(p):
    global x, y
    if p[0] < 500 and p[1] < 500:
        x = p[0] // inc
        y = p[1] // inc


# kiểm tra xem giá trị được chèn có hợp lệ không
def IsUserValueValid(m, i, j, v):
    for ii in range(9):
        if m[i][ii] == v or m[ii][j] == v: # Kiểm tra các cột và hàng
            return False
    # Kiểm tra các ô hoặc các khối
    ii = i // 3
    jj = j // 3
    for i in range(ii * 3, ii * 3 + 3):
        for j in range(jj * 3, jj * 3 + 3):
            if m[i][j] == v:
                return False
    return True

# đánh dấu ô đã chọn
def DrawSelectedBox():
    for i in range(2):
        pygame.draw.line(screen, (0, 0, 255), (x * inc, (y + i) * inc), (x * inc + inc, (y + i) * inc), 5)
        pygame.draw.line(screen, (0, 0, 255), ((x + i) * inc, y * inc), ((x + i) * inc, y * inc + inc), 5)


# chèn giá trị do người dùng nhập vào ô đã chọn
def InsertValue(Value):
    grid[int(x)][int(y)] = Value
    text = a_font.render(str(Value), True, (0, 0, 0))
    screen.blit(text, (x * inc + 15, y * inc + 15))

# Hàm kiểm tra người dùng thắng trò chơi
def IsUserWin():
    for i in range(9):
        for j in range(9):
            if grid[int(i)][int(j)] == 0:
                return False
    return True


def DrawModes():
    TitleFont = pygame.font.SysFont("times", 20, "bold")
    AttributeFont = pygame.font.SysFont("times", 20)
    screen.blit(TitleFont.render("Phím chức năng:", True, (0, 0, 0)), (15, 505))
    screen.blit(AttributeFont.render("C: Xoá toàn bộ", True, (0, 0, 0)), (30, 530))
    screen.blit(AttributeFont.render("X: Xóa một ô", True, (0, 0, 0)), (30, 555))
    screen.blit(AttributeFont.render("Space: Tự động giải", True, (0, 0, 0)), (30, 580))
    screen.blit(TitleFont.render("Mức độ:", True, (0, 0, 0)), (250, 505))
    screen.blit(AttributeFont.render("E: Dễ", True, (0, 0, 0)), (265, 530))
    screen.blit(AttributeFont.render("A: Trung bình", True, (0, 0, 0)), (265, 555))
    screen.blit(AttributeFont.render("H: Khó", True, (0, 0, 0)), (265, 580))
    screen.blit(AttributeFont.render("R: Random", True, (0, 0, 0)), (265, 605))


def DisplayMessage(Message, Interval, Color):
    bg = pygame.image.load('anh/bg.jpg')
    screen.blit(bg,(0,0))
    text = a_font.render(Message, True, Color)
    text_rect = text.get_rect(center = screen.get_rect().center)
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(Interval)
    screen.fill((255, 255, 255))
    DrawModes()


def SetGridMode(Mode):
    global grid
    screen.fill((255, 255, 255))
    DrawModes()
    # Có 3 chế độ cố định -> 3 ma trận tạo sẵn
    if Mode == 0:  # Xóa lưới
        grid = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
    elif Mode == 1:  # Chế độ dễ
        grid = [
            [4, 1, 0, 2, 7, 0, 8, 0, 5],
            [0, 8, 5, 1, 4, 6, 0, 9, 7],
            [0, 7, 0, 5, 8, 0, 0, 4, 0],
            [9, 2, 7, 4, 5, 1, 3, 8, 6],
            [5, 3, 8, 6, 9, 7, 4, 1, 2],
            [1, 6, 4, 3, 2, 8, 7, 5, 9],
            [8, 5, 2, 7, 0, 4, 9, 0, 0],
            [0, 9, 0, 8, 0, 2, 5, 7, 4],
            [7, 4, 0, 9, 6, 5, 0, 2, 8],
        ]
    elif Mode == 2:  # Chế độ trung bình
        grid = [
            [7, 8, 0, 4, 0, 0, 1, 2, 0],
            [6, 0, 0, 0, 7, 5, 0, 0, 9],
            [0, 0, 0, 6, 0, 1, 0, 7, 8],
            [0, 0, 7, 0, 4, 0, 2, 6, 0],
            [0, 0, 1, 0, 5, 0, 9, 3, 0],
            [9, 0, 4, 0, 6, 0, 0, 0, 5],
            [0, 7, 0, 3, 0, 0, 0, 1, 2],
            [1, 2, 0, 0, 0, 7, 4, 0, 0],
            [0, 4, 9, 2, 0, 6, 0, 0, 7]
        ]
    elif Mode == 3:  # Chế độ khó
        grid = [
            [0, 0, 0, 0, 0, 5, 7, 0, 0],
            [0, 5, 0, 0, 2, 0, 0, 4, 0],
            [0, 0, 7, 9, 0, 0, 0, 0, 8],
            [0, 0, 1, 0, 0, 8, 0, 0, 3],
            [0, 9, 0, 0, 1, 0, 0, 8, 0],
            [7, 0, 0, 5, 0, 0, 9, 0, 0],
            [3, 0, 0, 0, 0, 2, 6, 0, 0],
            [0, 8, 0, 0, 6, 0, 0, 7, 0],
            [0, 0, 9, 1, 0, 0, 0, 0, 0],
        ]
    elif Mode == 4:  # Chế độ random
        grid = sinh.sinhCauHoi()

def HandleEvents():
    global IsRunning, grid, x, y, UserValue
    events = pygame.event.get()
    for event in events:
        # Thoát khỏi cửa sổ game
        if event.type == pygame.QUIT:
            IsRunning = False
            sys.exit()
        # Lấy vị trí chuột để chèn số
        if event.type == pygame.MOUSEBUTTONDOWN:
            SetMousePosition(pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN:
            if not IsSolving:
                if event.key == pygame.K_LEFT:
                    x -= 1
                if event.key == pygame.K_RIGHT:
                    x += 1
                if event.key == pygame.K_UP:
                    y -= 1
                if event.key == pygame.K_DOWN:
                    y += 1
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    UserValue = 1
                if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    UserValue = 2
                if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    UserValue = 3
                if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    UserValue = 4
                if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    UserValue = 5
                if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    UserValue = 6
                if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    UserValue = 7
                if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    UserValue = 8
                if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    UserValue = 9
                if event.key == pygame.K_c:
                    SetGridMode(0)
                if event.key == pygame.K_e:
                    SetGridMode(1)
                if event.key == pygame.K_a:
                    SetGridMode(2)
                if event.key == pygame.K_h:
                    SetGridMode(3)
                if event.key == pygame.K_r:
                    SetGridMode(4)
                if event.key == pygame.K_SPACE:
                    if SolveGrid(grid,0,0):
                        DisplayMessage("Đã giải xong câu đố!", 1000, (0, 255, 0))
                    else:
                        DisplayMessage("Không thể tìm thấy lời giải!", 1000, (255, 0, 0))
                if event.key == pygame.K_x:
                    print(str(x)+" "+str(y))
                    grid[x][y] = 0
                    DeleteBox(x,y)
                if event.key == pygame.K_p:
                    for i in range(9):
                        print(grid[i])
            DrawUserValue()

def DrawUserValue():
    global UserValue, IsSolving
    if UserValue > 0:
        if IsUserValueValid(grid, x, y, UserValue):
            if grid[int(x)][int(y)] == 0:
                InsertValue(UserValue)
                UserValue = 0
                if IsUserWin():
                    IsSolving = False
                    DisplayMessage("CHIẾN THẮNG!!!!", 1000, (0, 255, 0))
            else:
                UserValue = 0
        else:
            DisplayMessage("Giá trị không chính xác!", 500, (255, 0, 0))
            UserValue = 0


def InitializeComponent():
    DrawGrid()
    DrawSelectedBox()
    DrawModes()
    pygame.display.update()


def GameThread():
    InitializeComponent()
    while IsRunning:
        bg = pygame.image.load('anh/bg.jpg')
        screen.blit(bg,(0,0))
        HandleEvents()
        DrawGrid()
        DrawModes()
        DrawSelectedBox()
        DrawUserValue()
        pygame.display.update()


if __name__ == '__main__':
    pygame.font.init()
    screen = pygame.display.set_mode((500, 675))  # Kích thước cửa sổ game
    screen.fill((255, 255, 255))
    pygame.display.set_caption("SudokuApp")
    a_font = pygame.font.SysFont("times", 30, "bold")  # Các phông chữ khác nhau được sử dụng
    b_font = pygame.font.SysFont("times", 15, "bold")
    inc = 500 // 9  # Kích thước màn hình // Số hàng = độ dài mỗi ô
    x = 0
    y = 0
    UserValue = 0
    # Chọn chế độ chơi đầu tiên là chế độ dễ
    SetGridMode(1)
    IsRunning = True
    IsSolving = False
    GameThread()