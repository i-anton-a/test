def privetstvije():
    print ("Крестики Нолики ")
    print ("ввод в виде x y")
    print ("x - строка")
    print ("y - столбец")

def pole():
    print()
    print("    | 0 | 1 | 2 | ")
    print("  --------------- ")
    for i, table in enumerate(field):
        table_str = f"  {i} | {' | '.join(table)} | "
        print(table_str)
        print("  --------------- ")
    print()

def ask():
    while True:
        cords = input("Ваш ход: ").split()
        
        if len(cords) != 2:
            print("Введите 2 координаты!")
            continue
        
        x, y = cords
        
        if not(x.isdigit()) or not(y.isdigit()):
            print("Введите числа!")
            continue
        
        x, y = int(x), int(y)
        
        if 0 > x or x > 2 or  0 > y or  y > 2 :
            print("Координаты вне диапазона!")
            continue
        
        if field[x][y] != " ":
            print("Клетка занята!")
            continue
        
        return x, y
            
def condition_win():
    win = (((0,0), (0,1), (0,2)), ((1,0), (1,1), (1,2)), ((2,0), (2,1), (2,2)),
                ((0,0), (1,1), (2,2)), ((2,0), (1,1), (0,2)),
                ((0,0), (1,0), (2,0)), ((0,1), (1,1), (2,1)), ((0,2), (1,2), (2,2)))
    for cord in win:
        symbols = []
        for c in cord:
            symbols.append(field[c[0]][c[1]])
        if symbols == ["X", "X", "X"]:
            print("Выиграл игрок X")
            return True
        if symbols == ["0", "0", "0"]:
            print("Выиграл игрок 0")
            return True
    return False

privetstvije()
field = [[" "] * 3 for i in range(3) ]
count = 0
while True:
    count += 1
    pole()
    if count % 2 == 1:
        print("Ходит игрок X")
    else:
        print("Ходит игрок 0")
    
    x, y = ask()
    
    if count % 2 == 1:
        field[x][y] = "X"
    else:
        field[x][y] = "0"
    
    if condition_win():
        break
    
    if count == 9:
        print(" Ничья!")
        break