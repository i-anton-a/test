from random import randint #нужен для генерации точек в AI

#класс иключений
class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"

class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"

class BoardWrongShipException(BoardException):
    pass

class Dot:
    '''класс точка
    '''
    def __init__(self, x, y):
        '''метод определения точек
           тут мы посто определяем координаты точки
           в сетке x y
        '''
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        '''метод сравнения двух объектов
           чтобы не писать каждый раз
           даный метод используется для сравнения
           возвращяет значение True или False
           стреляли мы по этим координатам или нет
        '''
        return self.x == other.x and self.y == other.y
    
    def __repr__(self):
        '''метод служит для вывода
           точек в консоль
           например мы выстрелили и хотим проверить
           есть ли данная точка выстрела в списке точек корабля
        '''
        return f"({self.x}, {self.y})"

class Ship:
    '''класс корабля
    '''
    def __init__(self, bow, l, o):
        '''конструктор описывающий поля
        '''
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l
    
    @property
    def dots(self):
        ship_dots = [] # список точек корабля
        for i in range(self.l):
            cur_x = self.bow.x 
            cur_y = self.bow.y
            
            if self.o == 0:
                cur_x += i
            
            elif self.o == 1:
                cur_y += i
            
            ship_dots.append(Dot(cur_x, cur_y))
        
        return ship_dots
    
    def shooten(self, shot):
        return shot in self.dots

class Board:
    '''класс игровое поле
    '''
    def __init__(self, hid = False, size = 6):
        self.size = size #размер
        self.hid = hid # нужно поле скрывать или нет
        
        self.count = 0 #количество пораженных кораблей
        
        self.field = [ ["O"]*size for _ in range(size) ] # размеры клеток где храним состояние
        
        self.busy = [] # либо точки занятые короблем либо куда стреляли
        self.ships = [] # список короблей доски
    
    def add_ship(self, ship):
        ''' размещение корабля
            проверяет что каждая точка корабля не выходит за граници
            и не занята
            походим точки и ставив квадратик а также запомин
            точки в которых есть корабль и которые с ним соседствует 
        '''
        
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)
        
        self.ships.append(ship)
        self.contour(ship)
            
    def contour(self, ship, verb = False):
        '''содержит свдиги вокруг коробля
           куда ставить корабль уже нельзя
        '''
        near = [
            (-1, -1), (-1, 0) , (-1, 1),
            (0, -1), (0, 0) , (0 , 1),
            (1, -1), (1, 0) , (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not(self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)
    
    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i+1} | " + " | ".join(row) + " |"
        
        if self.hid:
            res = res.replace("■", "O") # заменяем символы коробля на пустые символы
        return res
    
    def out(self, d):
        '''находится за пределами доски
        '''
        return not((0<= d.x < self.size) and (0<= d.y < self.size))

    def shot(self, d):
        ''' выстрел.
        '''
        if self.out(d):
            raise BoardOutException()
        
        if d in self.busy:
            raise BoardUsedException()
        
        self.busy.append(d)
        
        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb = True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True
        
        self.field[d.x][d.y] = "."
        print("Мимо!")
        return False
    
    def begin(self):
        ''' обнуляем. до игры храним точки куда ставим корабль
            во время игры храним точки попадания
        '''
        self.busy = []

class Player:
    '''класс игрока
    '''
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy
    
    def ask(self):
        raise NotImplementedError()
    
    def move(self):
        '''просим указать куда стрелять
        '''
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)

class AI(Player):
    '''типа искуственный интелек
       простейший тип
    '''
    def ask(self):
        '''случайно генерируем точки от 0 до 5
        '''
        d = Dot(randint(0,5), randint(0, 5))
        print(f"Ход компьютера: {d.x+1} {d.y+1}")
        return d

class User(Player):
    '''класс пользователя
    '''
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()
            
            if len(cords) != 2: #запрос координат что введено 2 точки
                print(" Введите 2 координаты! ")
                continue
            
            x, y = cords
            
            if not(x.isdigit()) or not(y.isdigit()): #проверяем что это числа
                print(" Введите числа! ")
                continue
            
            x, y = int(x), int(y)
            
            return Dot(x-1, y-1)

class Game:
    '''класс игры
    '''
    def __init__(self, size = 6):
        ''' конструктор. создаем две доски для компьютера и для игрока
            передаем доску AI и игроку. Доска по умолчанию 6х6
        '''
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True
        
        self.ai = AI(co, pl)
        self.us = User(pl, co)
    
    def random_board(self):
        '''гарантированно создает доску
        '''
        board = None
        while board is None:
            board = self.random_place()
        return board
    
    def random_place(self):
        '''пытаемся расставить каждый корабль на доске
           после того как расставили возвращяем игровую достку
        '''
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size = self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0,1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")
    
    
    def loop(self):
        '''игровой бесконечный цикл
        '''
        num = 0
        while True:
            print("-"*20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-"*20)
            print("Доска компьютера:")
            print(self.ai.board)
            if num % 2 == 0:
                print("-"*20)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-"*20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1
            
            if self.ai.board.count == 7:
                print("-"*20)
                print("Пользователь выиграл!")
                break
            
            if self.us.board.count == 7:
                print("-"*20)
                print("Компьютер выиграл!")
                break
            num += 1
            
    def start(self):
        self.greet()
        self.loop()
            
            
g = Game()
g.start()