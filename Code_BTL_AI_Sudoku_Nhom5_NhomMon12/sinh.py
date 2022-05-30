import random

def kiem_tra(q, gia_tri, dong, cot):
    for i in range(len(q[0])):
        if q[i][cot] == gia_tri and i != dong:
            return False
    for i in range(len(q)):
        if q[dong][i] == gia_tri and i != cot:
            return False
    x = cot // 3
    y = dong // 3
    for i in range(y*3, y*3+3):
        for j in range(x*3, x*3+3):
            if q[i][j] == gia_tri and i != dong and j != cot:
                return False
    return True

def tim_o_trong(a):
    for d in range(9):
        for c in range(9):
            if a[d][c] == 0:
                return d, c
    return None

def giai(q):
    tim_thay = tim_o_trong(q)
    if not tim_thay:
        return True
    else:
        d, c = tim_thay
    for i in range(1,10):
        if kiem_tra(q, i, d, c):
            q[d][c] = i
            if giai(q):
                return True
            else:
                q[d][c] = 0
    return False

def inMaTran(q):
    print("*********************")
    for d in range(len(q)):
        if d % 3 == 0 and d != 0:
            print("- - - - - - - - - - -")
        for c in range(len(q[0])):
            if c % 3 == 0 and c != 0:
                print("| ", end ="")
            if c == 8:
                print(str(q[d][c]))
            else:
                print(str(q[d][c]) + " ", end = "")
    print("*********************")

def sinhCauHoi():
    # Ma trận chứa câu hỏi đầy đủ
    a = [[1,2,3,4,5,6,7,8,9],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]]
    
    #Hoán vị hàng đầu tiên
    for i in range(random.randint(1, 10)): 
        c = random.randint(0,8)
        d = random.randint(0,8)
        e = a[0][c]
        a[0][c] = a[0][d]
        a[0][d] = e
    # dùng quay lui sinh ma trận sudoku
    giai(a)
    inMaTran(a)
    var = random.randint(1,80) #Số lượng các ô hiện
    # Ma trận câu hỏi random các ô hiện
    q = [[0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]]
    #Tính vị trí các ô hiện và gán vào ma trận kết quả
    for i in range(var): 
        while 1:
            n = random.randint(0,8)
            m = random.randint(0,8)
            if q[n][m] == 0:
                q[n][m] = a[m][n]
                break
    return q