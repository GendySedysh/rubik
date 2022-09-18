from copy import copy, deepcopy
from random import randint

class Cube:
    solved_cube = [
        [   # UP
            ['W', 'W', 'W'],
            ['W', 'W', 'W'],
            ['W', 'W', 'W'],
        ],
        [   # DOWN
            ['Y', 'Y', 'Y'],
            ['Y', 'Y', 'Y'],
            ['Y', 'Y', 'Y'],
        ],
        [   # LEFT
            ['O', 'O', 'O'],
            ['O', 'O', 'O'],
            ['O', 'O', 'O'],
        ],
        [   # RIGHT
            ['R', 'R', 'R'],
            ['R', 'R', 'R'],
            ['R', 'R', 'R'],
        ],
        [   #FRONT
            ['G', 'G', 'G'],
            ['G', 'G', 'G'],
            ['G', 'G', 'G'],
        ],
        [   #BACK
            ['B', 'B', 'B'],
            ['B', 'B', 'B'],
            ['B', 'B', 'B'],
        ],
    ]

    def __init__(self):
        self.list_sides = ['U', 'D', 'L', 'R', 'F', 'B']
        self.cube = deepcopy(self.solved_cube)
        self.cube_sides = self.parse_sides()
        self.moves = {'move_U':self.move_U,
                        'move_D':self.move_D,
                        'move_L':self.move_L,
                        'move_R':self.move_R,
                        'move_B':self.move_B,
                        'move_F':self.move_F, }
        self.movelist = []

    def parse_sides(self):
        dir_sides = {}
        tmp = 0
        for i in self.list_sides:
            dir_sides[i] = self.cube[tmp]
            tmp += 1
        return dir_sides

    def display_cube(self):
        str_1 = str_2 = str_3 = ''
        for i in range(6):
            str_1 += self.list_sides[i] + ': ' + str(self.cube[i][0]) + '   '
        for i in range(6):
            str_2 += '   ' + str(self.cube[i][1]) + '   '
        for i in range(6):
            str_3 += '   ' + str(self.cube[i][2]) + '   '
        print(str_1)
        print(str_2)
        print(str_3)
        print('_____________________')

    def move_U(self):
        backup_cube = deepcopy(self.cube)
        # turn top only
        for i in range(0, 3):
            self.cube[0][i][0] = backup_cube[0][2][i]
            self.cube[0][i][1] = backup_cube[0][1][i]
            self.cube[0][i][2] = backup_cube[0][0][i]
        # turn rest
        for i, j in [(2, 4), (3, 5), (4, 3), (5, 2)]:
            self.cube[i][0][0] = backup_cube[j][0][0]
            self.cube[i][0][1] = backup_cube[j][0][1]
            self.cube[i][0][2] = backup_cube[j][0][2]

    def move_D(self):
        backup_cube = deepcopy(self.cube)
        # turn bottom only
        for i in range(0, 3):
            self.cube[1][i][0] = backup_cube[1][2][i]
            self.cube[1][i][1] = backup_cube[1][1][i]
            self.cube[1][i][2] = backup_cube[1][0][i]
        # turn rest
        for i, j in [(2, 5), (3, 4), (4, 2), (5, 3)]:
            self.cube[i][2][0] = backup_cube[j][2][0]
            self.cube[i][2][1] = backup_cube[j][2][1]
            self.cube[i][2][2] = backup_cube[j][2][2]

    def move_L(self):
        backup_cube = deepcopy(self.cube)
        # turn left only
        for i in range(0, 3):
            self.cube[2][i][0] = backup_cube[2][2][i]
            self.cube[2][i][1] = backup_cube[2][1][i]
            self.cube[2][i][2] = backup_cube[2][0][i]
        # change top-part
        self.cube[0][0][0] = backup_cube[5][2][2]
        self.cube[0][1][0] = backup_cube[5][1][2]
        self.cube[0][2][0] = backup_cube[5][0][2]
        # change bottom-part
        self.cube[1][0][0] = backup_cube[4][0][0]
        self.cube[1][1][0] = backup_cube[4][1][0]
        self.cube[1][2][0] = backup_cube[4][2][0]
        # change front-part
        self.cube[4][0][0] = backup_cube[0][0][0]
        self.cube[4][1][0] = backup_cube[0][1][0]
        self.cube[4][2][0] = backup_cube[0][2][0]
        # change back-part
        self.cube[5][0][2] = backup_cube[1][2][0]
        self.cube[5][1][2] = backup_cube[1][1][0]
        self.cube[5][2][2] = backup_cube[1][0][0]

    def move_R(self):
        backup_cube = deepcopy(self.cube)
        # turn right only
        for i in range(0, 3):
            self.cube[3][i][0] = backup_cube[3][2][i]
            self.cube[3][i][1] = backup_cube[3][1][i]
            self.cube[3][i][2] = backup_cube[3][0][i]
        # change top-part
        self.cube[0][0][2] = backup_cube[4][0][2]
        self.cube[0][1][2] = backup_cube[4][1][2]
        self.cube[0][2][2] = backup_cube[4][2][2]
        # change bottom-part
        self.cube[1][0][2] = backup_cube[5][2][0]
        self.cube[1][1][2] = backup_cube[5][1][0]
        self.cube[1][2][2] = backup_cube[5][0][0]
        # change front-part
        self.cube[4][0][2] = backup_cube[1][0][2]
        self.cube[4][1][2] = backup_cube[1][1][2]
        self.cube[4][2][2] = backup_cube[1][2][2]
        # change back-part
        self.cube[5][0][0] = backup_cube[0][2][2]
        self.cube[5][1][0] = backup_cube[0][1][2]
        self.cube[5][2][0] = backup_cube[0][0][2]

    def move_F(self):
        backup_cube = deepcopy(self.cube)
        # turn front only
        for i in range(0, 3):
            self.cube[4][i][0] = backup_cube[4][2][i]
            self.cube[4][i][1] = backup_cube[4][1][i]
            self.cube[4][i][2] = backup_cube[4][0][i]
        # change top-part
        self.cube[0][2][0] = backup_cube[2][2][2]
        self.cube[0][2][1] = backup_cube[2][1][2]
        self.cube[0][2][2] = backup_cube[2][0][2]
        # change bottom-part
        self.cube[1][0][0] = backup_cube[3][2][0]
        self.cube[1][0][1] = backup_cube[3][1][0]
        self.cube[1][0][2] = backup_cube[3][0][0]
        # change left-part
        self.cube[2][0][2] = backup_cube[1][0][0]
        self.cube[2][1][2] = backup_cube[1][0][1]
        self.cube[2][2][2] = backup_cube[1][0][2]
        # change right-part
        self.cube[3][0][0] = backup_cube[0][2][0]
        self.cube[3][1][0] = backup_cube[0][2][1]
        self.cube[3][2][0] = backup_cube[0][2][2]

    def move_B(self):
        backup_cube = deepcopy(self.cube)
        # turn back only
        for i in range(0, 3):
            self.cube[5][i][0] = backup_cube[5][2][i]
            self.cube[5][i][1] = backup_cube[5][1][i]
            self.cube[5][i][2] = backup_cube[5][0][i]
        # change top-part
        self.cube[0][0][0] = backup_cube[3][0][2]
        self.cube[0][0][1] = backup_cube[3][1][2]
        self.cube[0][0][2] = backup_cube[3][2][2]
        # change bottom-part
        self.cube[1][2][0] = backup_cube[2][0][0]
        self.cube[1][2][1] = backup_cube[2][1][0]
        self.cube[1][2][2] = backup_cube[2][2][0]
        # change left-part
        self.cube[2][0][0] = backup_cube[0][0][2]
        self.cube[2][1][0] = backup_cube[0][0][1]
        self.cube[2][2][0] = backup_cube[0][0][0]
        # change right-part
        self.cube[3][0][2] = backup_cube[1][2][2]
        self.cube[3][1][2] = backup_cube[1][2][1]
        self.cube[3][2][2] = backup_cube[1][2][0]
    
    def reverse_move(self, move):
        for i in range(3):
            self.moves[move]()

    def double_move(self, move):
        for i in range(2):
            self.moves[move]()

    def random_start(self, moves_num : int):
        moves =  ['move_U', 'move_D', 'move_L', 'move_R', 'move_B', 'move_F']
        dir_moves = {'move_U' : 'U', 'move_D' : 'D', 'move_L' : 'L', 'move_R' : 'R', 'move_B' : 'B', 'move_F' : 'F'}
        movelist = []
        print('\nRandomized movelist:')
        for i in range(moves_num):
            tmp_move = moves[randint(0, 5)]
            movelist.append(tmp_move)
            print(dir_moves[tmp_move])
        print()
        return movelist
    
    def execute_movelist(self, movelist: list):
        for i in movelist:
            self.moves[i]()
    
    def parse_moveset(self, input_str : str):
        list_move = ['U', 'D', 'L', 'R', 'B', 'F']
        dir_moves = {'U' : 'move_U', 'D' : 'move_D', 'L' : 'move_L', 'R' : 'move_R', 'B' : 'move_B', 'F' : 'move_F'}
        movelist = []
        input_list = input_str.split(sep=' ')
        input_list = list(filter(None, input_list))
        
        # CHECK FOR UNVALID SHIT
        for i in input_list:
            if (len(i) > 2 ) or (i[0] not in list_move):
                print('INVALID LIST')
                exit(0)
            else:
                if (len(i) == 2):
                    if (i[1] == "'"):
                        for j in range(3):
                            movelist.append(dir_moves[i[0]])
                    elif (i[1] == '2'):
                        for j in range(2):
                            movelist.append(dir_moves[i[0]])
                    else:
                        print('INVALID LIST')
                        exit(0)
                else:
                    movelist.append(dir_moves[i[0]])
        return movelist
