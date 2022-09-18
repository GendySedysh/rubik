from copy import copy, deepcopy
import cube

class Solver():
    def __init__(self, cube : cube.Cube):
        self.cube = cube
        self.logs = []
        self.tranlation = {
            'U': {'move_U':'move_B', 'move_D':'move_F', 'move_L':'move_L', 'move_R':'move_R', 'move_F':'move_U', 'move_B':'move_D'},
            'D': {'move_U':'move_F', 'move_D':'move_B', 'move_L':'move_L', 'move_R':'move_R', 'move_F':'move_D', 'move_B':'move_U'},
            'L': {'move_U':'move_U', 'move_D':'move_D', 'move_L':'move_B', 'move_R':'move_F', 'move_F':'move_L', 'move_B':'move_R'},
            'R': {'move_U':'move_U', 'move_D':'move_D', 'move_L':'move_F', 'move_R':'move_B', 'move_F':'move_R', 'move_B':'move_L'},
            'F': {'move_U':'move_U', 'move_D':'move_D', 'move_L':'move_L', 'move_R':'move_R', 'move_F':'move_F', 'move_B':'move_B'},
            'B': {'move_U':'move_U', 'move_D':'move_D', 'move_L':'move_R', 'move_R':'move_L', 'move_F':'move_B', 'move_B':'move_F'}
            }

        self.rev_tranlation = { 'move_U':'move_D', 'move_D':'move_U', 'move_L':'move_R',
                                'move_R':'move_L', 'move_F':'move_F', 'move_B':'move_B' }
    
    '''
        Делает перемещения 'move' куба относительно 'side',
        переводя это в обычные ходы 
    '''
    def moves_by_side(self, move:str, side: str, cube : cube.Cube):
        cube.moves[self.tranlation[side][move]]()
    
    def translate_movelist_by_side(self, side, movelist:list):
        ret_movelist = []
        for move in movelist:
            ret_movelist.append(self.tranlation[side][move])
        return ret_movelist

    def step_1_check_white_on_side(self, side):
        places_for_white = {'L':[['F', 1, 0], ['D', 1, 0], ['B', 1, 2]],
                            'F':[['L', 1, 2], ['D', 0, 1], ['R', 1, 0]], 
                            'R':[['F', 1, 2], ['D', 1, 2], ['B', 1, 0]],
                            'B':[['L', 1, 0], ['D', 2, 1], ['R', 1, 2]]}
        
        check_list = places_for_white[side]
        for piece in check_list:
            if (self.cube.cube_sides[piece[0]][piece[1]][piece[2]] == 'W'):
                return 1
        return 0

    def step_1_push_white_down(self):
        sides = ['L', 'F', 'R', 'B']
        places_for_white = {'L':[1, 0], 'F':[2, 1], 'R':[1, 2], 'B':[0, 1]}

        for side in sides:
            if (self.cube.cube_sides[side][0][1] == 'W' or self.cube.cube_sides[side][2][1] == 'W'):
                while (self.cube.cube_sides['U'][places_for_white[side][0]][places_for_white[side][1]] == 'W'):
                    self.cube.move_U()
                    self.logs.append('move_U')
                self.moves_by_side('move_F', side, self.cube)
                self.logs.append(self.tranlation[side]['move_F'])

    def step_1_check_cross_created(self):
        places_for_white = {'L':[1, 0], 'F':[2, 1], 'R':[1, 2], 'B':[0, 1]}
        sides = ['L', 'F', 'R', 'B']
        ret_list = []
        for side in sides:
            if (self.cube.cube_sides['U'][places_for_white[side][0]][places_for_white[side][1]] != 'W'):
                ret_list.append(side)
        return ret_list

    def step_1_rotate(self):
        places_for_white = {'L':[1, 0], 'F':[2, 1], 'R':[1, 2], 'B':[0, 1]}
        sides = ['L', 'F', 'R', 'B']
        self.step_1_push_white_down()

        broken_list = self.step_1_check_cross_created()

        while len(broken_list) != 0:
            for side in sides:
                piece = places_for_white[side]
                if (self.step_1_check_white_on_side(side) == 1):
                    while (self.cube.cube_sides['U'][piece[0]][piece[1]] == 'W'):
                        self.cube.move_U()
                        self.logs.append('move_U')
                    while (self.cube.cube_sides['U'][piece[0]][piece[1]] != 'W'):
                        self.moves_by_side('move_F', side, self.cube)
                        self.logs.append(self.tranlation[side]['move_F'])
            self.step_1_push_white_down()
            broken_list = self.step_1_check_cross_created()
    
    def step_1_normilize_cross(self):
        while self.cube.cube_sides['F'][1][1] != self.cube.cube_sides['F'][0][1]:
            self.cube.move_U()
            self.logs.append('move_U')

        sides = ['L', 'F', 'R', 'B']
        ret_list = []
        for side in sides:
            if (self.cube.cube_sides[side][1][1] != self.cube.cube_sides[side][0][1]):
                ret_list.append(side)
        return (ret_list)

    def step_1_hz(self):
        movelist = ['move_R', 'move_R', 'move_R', 'move_L', 'move_U', 'move_U',
                    'move_R', 'move_L', 'move_L', 'move_L', 'move_U', 'move_U']
        self.cube.execute_movelist(movelist)
        self.logs += movelist

    def step_1_rotate_to_norm(self):
        broken_list = self.step_1_normilize_cross()
        while len(broken_list) != 0:
            if (len(broken_list) == 2 and 'L' in broken_list and 'R' in broken_list):
                self.step_1_hz()
            else:
                if (self.cube.cube_sides['R'][0][1] == 'B'):
                    movelist = ['move_R', 'move_U', 'move_R', 'move_R', 'move_R',
                                'move_U', 'move_U', 'move_U', 'move_R']
                    self.cube.execute_movelist(movelist)
                    self.logs += movelist
                if (self.cube.cube_sides['L'][0][1] == 'B'):
                    movelist = ['move_B', 'move_U', 'move_B', 'move_B', 'move_B',
                                'move_U', 'move_U', 'move_U', 'move_B']
                    self.cube.execute_movelist(movelist)
                    self.logs += movelist
            broken_list = self.step_1_normilize_cross()

    def step_1(self, flag: bool):
        self.step_1_rotate()
        self.step_1_rotate_to_norm()

        if (flag == True):
            print('STEP 1 complete')
            self.cube.display_cube()
    
    def check_step_2(self):
        sides = ['L', 'F', 'R', 'B',]
        for side in sides:
            if (self.cube.cube_sides[side][0][0] != self.cube.cube_sides[side][1][1] and
                self.cube.cube_sides[side][0][2] != self.cube.cube_sides[side][1][1]):
                return 0
        for slice in self.cube.cube_sides['U']:
            for piece in slice:
                if piece != 'W':
                    return 0
        return 1

    def count_white_on_last_slice(self):
        sides = ['L', 'F', 'R', 'B',]
        ret = 0
        for side in sides:
            for piece in self.cube.cube_sides[side][2]:
                if piece == 'W':
                    ret+=1
        for slice in self.cube.cube_sides['D']:
            for piece in slice:
                if piece == 'W':
                    ret+=1
        return ret

    def step_2_is_it_white(self, pieces):
        for piece in pieces:
            if self.cube.cube_sides[piece[0]][piece[1]][piece[2]] == 'W':
                return 1
        return 0

    def step_2_pif_paf(self, side):
        movelist = ['move_R', 'move_R', 'move_R', 'move_D', 'move_R']
        trans_movelist = self.translate_movelist_by_side(side, movelist)
        self.cube.execute_movelist(trans_movelist)
        self.logs += trans_movelist

    def step_2_push_whites_down_first(self):
        sides = ['L', 'F', 'R', 'B']
        up_slice_to_check = {   'L':[['L', 0, 2], ['U', 2, 0], ['F', 0, 0]],
                                'F':[['F', 0, 2], ['U', 2, 2], ['R', 0, 0]], 
                                'R':[['R', 0, 2], ['U', 0, 2], ['B', 0, 0]],
                                'B':[['B', 0, 2], ['U', 0, 0], ['L', 0, 0]] }

        down_slice_to_check = { 'L':[['L', 2, 2], ['D', 0, 0], ['F', 2, 0]],
                                'F':[['F', 2, 2], ['D', 0, 2], ['R', 2, 0]], 
                                'R':[['R', 2, 2], ['D', 2, 2], ['B', 2, 0]],
                                'B':[['B', 2, 2], ['D', 2, 0], ['L', 2, 0]] }
        for side in sides:
            up_check_list = up_slice_to_check[side]
            if self.step_2_is_it_white(up_check_list) == 1:
                check_list = down_slice_to_check[side]
                while self.step_2_is_it_white(check_list) != 0:
                    self.cube.move_D()
                    self.logs.append('move_D')
                movelist = ['move_R', 'move_R', 'move_R']
                trans_movelist = self.translate_movelist_by_side(side, movelist)
                self.cube.execute_movelist(trans_movelist)
                self.logs += trans_movelist
                while self.step_2_is_it_white(check_list) != 0:
                    self.cube.move_D()
                    self.logs.append('move_D')
                self.moves_by_side('move_R', side, self.cube)
                self.logs.append(self.tranlation[side]['move_R'])
    
    def step_2_push_whites_down_second(self):
        sides = ['L', 'F', 'R', 'B']
        up_slice_to_check = {   'L':[['L', 0, 2], ['F', 0, 0]],
                                'F':[['F', 0, 2], ['R', 0, 0]], 
                                'R':[['R', 0, 2], ['B', 0, 0]],
                                'B':[['B', 0, 2], ['L', 0, 0]] }

        down_slice_to_check = { 'L':[['L', 2, 2], ['D', 0, 0], ['F', 2, 0]],
                                'F':[['F', 2, 2], ['D', 0, 2], ['R', 2, 0]], 
                                'R':[['R', 2, 2], ['D', 2, 2], ['B', 2, 0]],
                                'B':[['B', 2, 2], ['D', 2, 0], ['L', 2, 0]] }
        for side in sides:
            up_check_list = up_slice_to_check[side]
            if self.step_2_is_it_white(up_check_list) == 1:
                check_list = down_slice_to_check[side]
                while self.step_2_is_it_white(check_list) != 0:
                    self.cube.move_D()
                    self.logs.append('move_D')
                movelist = ['move_R', 'move_R', 'move_R']
                trans_movelist = self.translate_movelist_by_side(side, movelist)
                self.cube.execute_movelist(trans_movelist)
                self.logs += trans_movelist
                while self.step_2_is_it_white(check_list) != 0:
                    self.cube.move_D()
                    self.logs.append('move_D')
                self.moves_by_side('move_R', side, self.cube)
                self.logs.append(self.tranlation[side]['move_R'])

    def step_2_check_side(self, checklist):
        for piece in checklist:
            if self.cube.cube_sides[piece[0]][piece[1]][piece[2]] != self.cube.cube_sides[piece[0]][1][1]:
                return 0
        return 1

    def step_2_check(self):
        up_slice_to_check = {   'L':[['L', 0, 2], ['U', 2, 0], ['F', 0, 0]],
                                'F':[['F', 0, 2], ['U', 2, 2], ['R', 0, 0]], 
                                'R':[['R', 0, 2], ['U', 0, 2], ['B', 0, 0]],
                                'B':[['B', 0, 2], ['U', 0, 0], ['L', 0, 0]] }
        sides = ['L', 'F', 'R', 'B']
        ret_list = []
        for side in sides:
            checklist = up_slice_to_check[side]
            if (self.step_2_check_side(checklist) == 0):
                ret_list.append(side)
        return (ret_list)
    
    def step_2_return_colors_of_piece(self, checklist):
        ret_list = []
        for check in checklist:
            ret_list.append(self.cube.cube_sides[check[0]][check[1]][check[2]])
        return list(set(ret_list))
    
    def step_2_is_colors_ok(self, side, colors):
        ok_colors = {   'L':['W', 'O', 'B'],
                        'F':['W', 'G', 'O'],
                        'R':['W', 'R', 'G'],
                        'B':['W', 'B', 'R']}
        side_ok = ok_colors[side]
        for color in colors:
            if color not in side_ok:
                return 0
        return 1
    
    def step_2_rotate_shit(self, side, checklist):
        white_on = ''
        for check in checklist:
            if (self.cube.cube_sides[check[0]][check[1]][check[2]] == 'W'):
                white_on = check[0]
        
        if (white_on == side):
            movelist = ['move_F', 'move_F', 'move_F', 'move_D', 'move_D', 'move_D', 'move_F']
            trans_movelist = self.translate_movelist_by_side(side, movelist)
            self.cube.execute_movelist(trans_movelist)
            self.logs += trans_movelist
        elif (white_on == 'D'):
            movelist = ['move_F', 'move_F', 'move_F', 'move_R', 'move_R', 'move_R',
                        'move_D', 'move_D', 'move_R', 'move_F']
            trans_movelist = self.translate_movelist_by_side(side, movelist)
            self.cube.execute_movelist(trans_movelist)
            self.logs += trans_movelist
        else:
            movelist = ['move_L', 'move_D', 'move_L', 'move_L', 'move_L']
            trans_movelist = self.translate_movelist_by_side(side, movelist)
            self.cube.execute_movelist(trans_movelist)
            self.logs += trans_movelist
    
    def step_2_rotation(self):
        sides = ['L', 'F', 'R', 'B']
        down_slice_to_check = { 'L':[['L', 2, 0], ['D', 2, 0], ['B', 2, 2]],
                                'F':[['F', 2, 0], ['D', 0, 0], ['L', 2, 2]], 
                                'R':[['R', 2, 0], ['D', 0, 2], ['F', 2, 2]],
                                'B':[['B', 2, 0], ['D', 2, 2], ['R', 2, 2]] }
        broken_list = self.step_2_check()

        tmp = 0
        while (len(broken_list) != 0):
            if tmp == 16:
                self.step_2_push_whites_down_first()
            for side in sides:
                checklist = down_slice_to_check[side]
                col_list = self.step_2_return_colors_of_piece(checklist)
                tmp = 0
                while (self.step_2_is_colors_ok(side, col_list) == 0 and tmp != 4):
                    self.cube.move_D()
                    self.logs.append('move_D')
                    col_list = self.step_2_return_colors_of_piece(checklist)
                    tmp+=1
                if (self.step_2_is_colors_ok(side, col_list) == 1):
                    self.step_2_rotate_shit(side, checklist)
                else:
                    self.step_2_push_whites_down_second()
            tmp += 1
            broken_list = self.step_2_check()

    def step_2(self, flag: bool):
        self.step_2_rotation()

        if (flag == True):
            print('STEP 2 complete')
            self.cube.display_cube()

    def step_3_rot_left(self, side):
        movelist = ['move_D', 'move_L', 'move_D', 'move_D', 'move_D', 'move_L', 'move_L', 'move_L',
                    'move_D', 'move_D', 'move_D', 'move_F', 'move_F', 'move_F', 'move_D', 'move_F']
        trans_movelist = self.translate_movelist_by_side(side, movelist)
        self.cube.execute_movelist(trans_movelist)
        self.logs += trans_movelist
    
    def step_3_rot_right(self, side):
        movelist = ['move_D', 'move_D', 'move_D', 'move_R', 'move_R', 'move_R', 'move_D', 'move_R',
                    'move_D', 'move_F', 'move_D', 'move_D', 'move_D', 'move_F', 'move_F', 'move_F']
        trans_movelist = self.translate_movelist_by_side(side, movelist)
        self.cube.execute_movelist(trans_movelist)
        self.logs += trans_movelist

    def step_3_rotation(self, side:str, ext:bool, ext_2:bool):
        check_piece = {'L':[1, 0], 'F':[0, 1], 'R':[1, 2], 'B':[2, 1]}
        side_color = {'L':['B', 'G'], 'F':['O', 'R'], 'R':['G', 'B'], 'B':['R', 'O']}

        bottom_color = self.cube.cube_sides['D'][check_piece[side][0]][check_piece[side][1]]
        left_color = self.cube.cube_sides[side][1][0]
        mid_color = self.cube.cube_sides[side][1][1]
        right_color = self.cube.cube_sides[side][1][2]


        if (bottom_color == side_color[side][0] or (mid_color != left_color and ext)):
            self.step_3_rot_left(side)
        elif (bottom_color == side_color[side][1] or (mid_color != right_color and ext)):
            self.step_3_rot_right(side)
        
        if (ext_2 == True):
            tmp = 0
            while (bottom_color != side_color[side][0] or bottom_color != side_color[side][1]) and tmp != 4:
                self.cube.move_D()
                self.logs.append('move_D')
                bottom_color = self.cube.cube_sides['D'][check_piece[side][0]][check_piece[side][1]]
                tmp += 1
            if (bottom_color == side_color[side][0]):
                self.step_3_rot_left(side)
            elif (bottom_color == side_color[side][1]):
                self.step_3_rot_right(side)

    def step_3_rotate_bottom(self, ext:bool, ext_2:bool):
        sides = ['L', 'F', 'R', 'B', 'B', 'R', 'F', 'L']
        for side in sides:
            mid_color = self.cube.cube_sides[side][1][1]
            need_color = self.cube.cube_sides[side][2][1]
            tmp = 0
            while (need_color != mid_color) and tmp != 4:
                self.cube.move_D()
                self.logs.append('move_D')
                tmp += 1
                need_color = self.cube.cube_sides[side][2][1]
            if (mid_color == need_color):
                self.step_3_rotation(side, ext, ext_2)
            elif (ext_2 == True):
                self.step_3_rotation(side, ext, ext_2)

    def step_3_check(self):
        sides = ['L', 'F', 'R', 'B']
        if self.check_step_2() == 0:
            return 0
        for side in sides:
            left_piece = self.cube.cube_sides[side][1][0]
            right_piece = self.cube.cube_sides[side][1][2]
            mid_piece = self.cube.cube_sides[side][1][1]
            if (left_piece != mid_piece or right_piece != mid_piece):
                return 0
        return 1

    def step_3(self, flag: bool):
        self.step_3_rotate_bottom(False, False)
        tmp = 0
        while (self.step_3_check() == 0):
            if (tmp == 4):
                self.step_3_rotate_bottom(True, True)
            if (self.step_3_check() == 1):
                break
            self.step_3_rotate_bottom(True, False)
            if (self.step_3_check() == 1):
                break
            self.step_3_rotate_bottom(False, False)
            if (self.step_3_check() == 1):
                break
            tmp += 1

        if (flag == True):
            print('STEP 3 complete')
            self.cube.display_cube()
    
    def step_4_OLL_check_position(self):
        sides = ['L', 'F', 'R', 'B']
        bottom = self.cube.cube_sides['D']
        ret_list = ''
        tmp = 1

        for i in bottom:
            for j in i:
                if (j == 'Y'):
                    ret_list += str(tmp) + ' '
                tmp += 1

        for side in sides:
            bottom_side = self.cube.cube_sides[side][2]
            tmp = 0
            for piece in bottom_side:
                if (piece == 'Y'):
                    ret_list += side + str(tmp) + ' '
                tmp += 1
        return (ret_list[:-1])

    def step_4_check_top(self):
        bottom = self.cube.cube_sides['D']
        for j in bottom:
            for i in j:
                if (i != 'Y'):
                    return 0
        return 1

    def upper_down_translation(self, movelist):
        ret_list = []
        for move in movelist:
            ret_list.append(self.rev_tranlation[move])
        return ret_list

    def step_4_OLL_rotation(self):
        for i in range(16):
            pattern = self.step_4_OLL_check_position()
            if (pattern == "2 4 5 6 7 8 9 B0 B2"):          # Глаза: R2 D' R | U2 R' D | R U2 R
                movelist = ['move_R', 'move_R', 'move_D', 'move_D', 'move_D', 'move_R',
                            'move_U', 'move_U', 'move_R', 'move_R', 'move_R', 'move_D',
                            'move_R', 'move_U', 'move_U', 'move_R']
                movelist = self.upper_down_translation(movelist)
                # print('Глаза')
                self.cube.execute_movelist(movelist)
                self.logs += movelist
            elif (pattern == "2 4 5 6 7 8 9 L0 R2"):        # Уши: R U R D | R' U' | R D' R2
                movelist = ['move_R', 'move_U', 'move_R', 'move_D',
                            'move_R', 'move_R', 'move_R', 'move_U', 'move_U', 'move_U',
                            'move_R', 'move_D', 'move_D', 'move_D', 'move_R', 'move_R']
                movelist = self.upper_down_translation(movelist)
                # print('Уши')
                self.cube.execute_movelist(movelist)
                self.logs += movelist
            elif (pattern == "1 2 4 5 6 8 9 R0 B2"):        # Восьмерка: R2 D' | R U' R' | D R U R
                movelist = ['move_R', 'move_R', 'move_D', 'move_D', 'move_D',
                            'move_R', 'move_U', 'move_U', 'move_U', 'move_R', 'move_R', 'move_R',
                            'move_D', 'move_R', 'move_U', 'move_R']
                movelist = self.upper_down_translation(movelist)
                # print('Восьмерка')
                self.cube.execute_movelist(movelist)
                self.logs += movelist
            elif (pattern == "2 4 5 6 8 L0 L2 R0 R2"):      # Двойные глаза: R U R' | U R U' | R' U R | U2 R'
                movelist = ['move_R', 'move_U', 'move_R', 'move_R', 'move_R',
                            'move_U', 'move_R', 'move_U', 'move_U', 'move_U',
                            'move_R', 'move_R', 'move_R', 'move_U', 'move_R',
                            'move_U', 'move_U', 'move_R', 'move_R', 'move_R']
                # print('Двойные')
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
            elif (pattern == "2 4 5 6 8 F0 R0 R2 B2"):      # Вертолет: R U2 R2 | U' R2 | U' R2 | U2 R
                movelist = ['move_R', 'move_U', 'move_U', 'move_R', 'move_R',
                            'move_U', 'move_U', 'move_U', 'move_R', 'move_R',
                            'move_U', 'move_U', 'move_U', 'move_R', 'move_R',
                            'move_U', 'move_U', 'move_R']
                # print('Вертолет')
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
            elif (pattern == "2 4 5 6 7 8 L0 F0 B0"):       # Рыбки_1: R U R' | U R U2 R'
                movelist = ['move_R', 'move_U', 'move_R', 'move_R', 'move_R',
                            'move_U', 'move_R', 'move_U', 'move_U', 'move_R', 'move_R', 'move_R']
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                # print('Рыбки_1')
                self.logs += movelist
            elif (pattern == "2 4 5 6 8 9 F2 R2 B2"):       # Рыбки_2: L' U' L | U' L' | U2 L
                movelist = ['move_L', 'move_L', 'move_L', 'move_U', 'move_U', 'move_U', 'move_L',
                            'move_U', 'move_U', 'move_U', 'move_L', 'move_L', 'move_L',
                            'move_U', 'move_U', 'move_L']
                movelist = self.upper_down_translation(movelist)
                # print('Рыбки_2')
                self.cube.execute_movelist(movelist)
                self.logs += movelist
            elif (pattern == "5 L0 L1 L2 F1 R0 R1 R2 B1"):  # Точки_1: R U2 R2 | F R F' | U2 R' F | R F'
                movelist = ['move_R', 'move_U', 'move_U', 'move_R', 'move_R',
                            'move_F', 'move_R', 'move_F', 'move_F', 'move_F',
                            'move_U', 'move_U', 'move_R', 'move_R', 'move_R', 'move_F',
                            'move_R', 'move_F', 'move_F', 'move_F']
                # print('Точки_1')
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
            elif (pattern == "5 7 L0 L1 F0 F1 R1 B1 B2"):   # Запятые_1: y2 L U F U' F' L' F R U R' U' F'
                movelist = self.cube.parse_moveset("L U F U' F' L' F R U R' U' F'")
                movelist = self.translate_movelist_by_side('B', movelist)
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                # print('Запятые_1')
                self.logs += movelist
            elif (pattern == "5 9 L1 F1 F2 R1 R2 B1 B2"):   # Запятые_2: y F U R U' R' F' R' F' U' F U R
                movelist = self.cube.parse_moveset("F U R U' R' F' R' F' U' F U R")
                movelist = self.translate_movelist_by_side('L', movelist)
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                # print('Запятые_2')
                self.logs += movelist
            elif (pattern == "1 3 5 L1 L2 F1 R0 R1 B1"):    # Микки_маус_1: R' U2 F R U R' U' F2 U2 F R
                movelist = self.cube.parse_moveset("R' U2 F R U R' U' F2 U2 F R")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
                # print('Микки_маус_1')
            elif (pattern == "1 3 5 L1 F0 F1 F2 R1 B1"):    # Микки_маус_2: y2 F R' F' R U2 R' U' F' U F R2 U' R'
                movelist = self.cube.parse_moveset("F R' F' R U2 R' U' F' U F R2 U' R'")
                movelist = self.translate_movelist_by_side('B', movelist)
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                # print('Микки_маус_2')
                self.logs += movelist
            elif (pattern == "1 5 9 L1 F1 R0 R1 B1 B2"):    # Диагональ: R U R' U R' F R F' U2 R' F R F'
                movelist = self.cube.parse_moveset("R U R' U R' F R F' U2 R' F R F'")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
                # print('Диагональ')
            elif (pattern == "4 5 6 L0 L2 F1 F2 B0 B1"):    # Палки_1: F U R U' R' U R U' R' F'
                movelist = self.cube.parse_moveset("F U R U' R' U R U' R' F'")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
                # print('Палки_1')
            elif (pattern == "4 5 6 L0 L2 F1 R0 R2 B1"):    # Палки_2: R' F R F' U2 R U' R' U y' R' U2 R
                movelist = self.cube.parse_moveset("R' F R F' U2 R U' R' U")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
                # print('Палки_2')
                movelist = self.cube.parse_moveset("R' U2 R")
                movelist = self.translate_movelist_by_side('R', movelist)
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
            elif (pattern == "4 5 6 L2 F1 R0 B0 B1 B2"):    # Палки_3: y R U R' U R U' B U' B' R'
                movelist = self.cube.parse_moveset("R U R' U R U' B U' B' R'")
                movelist = self.translate_movelist_by_side('L', movelist)
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                # print('Палки_3')
                self.logs += movelist
            elif (pattern == "4 5 6 F0 F1 F2 B0 B1 B2"):    # Палки_4: R' F R U R U' R2 F' R2 U' R' U R U R'
                movelist = self.cube.parse_moveset("R' F R U R U' R2 F' R2 U' R' U R U R'")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
                # print('Палки_4')
            elif (pattern == "3 4 5 6 L2 F1 F2 R2 B1"):     # Буква_Г_1: y2 R' F R U R' U' F' R U' R' U2 R
                movelist = self.cube.parse_moveset("R' F R U R' U' F' R U' R' U2 R")
                movelist = self.translate_movelist_by_side('B', movelist)
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                # print('Буква_Г_1')
                self.logs += movelist
            elif (pattern == "3 4 5 6 F0 F1 R0 B0 B1"):     # Буква_Г_2: y2 F U R U2 R' U' R U R' F'
                movelist = self.cube.parse_moveset("F U R U2 R' U' R U R' F'")
                movelist = self.translate_movelist_by_side('B', movelist)
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                # print('Буква_Г_2')
                self.logs += movelist
            elif (pattern == "1 4 5 6 L2 F1 F2 B1 B2"):     # Буква_Г_3: y2 R' F R U R' F' R F U' F'
                movelist = self.cube.parse_moveset("R' F R U R' F' R F U' F'")
                movelist = self.translate_movelist_by_side('B', movelist)
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                # print('Буква_Г_3')
                self.logs += movelist
            elif (pattern == "3 4 5 6 9 F1 R0 R2 B1"):      # Буква_Т_1: F R U R' U' F'
                movelist = self.cube.parse_moveset("F R U R' U' F'")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
                # print('Буква_Т_1')
            elif (pattern == "3 4 5 6 9 F1 F2 B0 B1"):      # Буква_Т_2: R U R' U' R' F R F'
                movelist = self.cube.parse_moveset("R U R' U' R' F R F'")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
                # print('Буква_Т_2')
            elif (pattern == "4 5 6 7 9 L0 F1 R2 B1"):      # Cкобки_1: R U R2 U' R' F R U R U' F'
                movelist = self.cube.parse_moveset("R U R2 U' R' F R U R U' F'")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
                # print('Cкобки_1')
            elif (pattern == "4 5 6 7 9 F1 B0 B1 B2"):      # Cкобки_2: y R' U' R' F R F' U R
                movelist = self.cube.parse_moveset("R' U' R' F R F' U R")
                movelist = self.translate_movelist_by_side('L', movelist)
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                # print('Cкобки_2')
                self.logs += movelist
            elif (pattern == "1 4 5 6 9 F1 R0 B1 B2"):      # Пропеллеры_1: R' F R U R' U' F' U R
                movelist = self.cube.parse_moveset("R' F R U R' U' F' U R")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
                # print('Пропеллеры_1')
            elif (pattern == "1 4 5 6 9 L2 F1 B0 B1"):      # Пропеллеры_2: L F' L' U' L U F U' L'
                movelist = self.cube.parse_moveset("L F' L' U' L U F U' L'")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
                # print('Пропеллеры_2')
            elif (pattern == "2 5 6 L2 F1 R0 R1 B0 B2"):    # Стелсы_1: y' F R U R' U' R U R' U' F'
                movelist = self.cube.parse_moveset("F R U R' U' R U R' U' F'")
                movelist = self.translate_movelist_by_side('R', movelist)
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                # print('Стелсы_1')
                self.logs += movelist
            elif (pattern == "2 5 6 L0 L2 F1 F2 R1 B0"):    # Стелсы_2: F' L' U' L U L' U' L U F
                movelist = self.cube.parse_moveset("F' L' U' L U L' U' L U F")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
                # print('Стелсы_2')
            elif (pattern == "2 5 6 F0 F1 F2 R1 B0 B2"):    # Стелсы_3: y' F R U R' U' R U' R' U R U R' F'
                movelist = self.cube.parse_moveset("F R U R' U' R U' R' U R U R' F'")
                movelist = self.translate_movelist_by_side('R', movelist)
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                # print('Стелсы_3')
                self.logs += movelist
            elif (pattern == "2 5 6 F0 F1 R0 R1 R2 B2"):    # Стелсы_4: y R' U2 R U R' U R F R U R' U' F'
                movelist = self.cube.parse_moveset("R' U2 R U R' U R F R U R' U' F'")
                movelist = self.translate_movelist_by_side('L', movelist)
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                # print('Стелсы_4')
                self.logs += movelist
            elif (pattern == "2 5 6 L0 F0 F1 F2 R1 R2"):    # Стелсы_5: R U2 R' U' R U' R' F R U R' U' F'
                movelist = self.cube.parse_moveset("R U2 R' U' R U' R' F R U R' U' F'")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
                # print('Стелсы_5')
            elif (pattern == "2 5 6 7 L0 F0 F1 R1 B0"):     # Рюмки_1: y R U R' U F' U F U' R U2 R'
                movelist = self.cube.parse_moveset("R U R' U F' U F U' R U2 R'")
                movelist = self.translate_movelist_by_side('L', movelist)
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                # print('Рюмки_1')
                self.logs += movelist
            elif (pattern == "2 4 5 9 L1 F1 F2 R2 B2"):     # Рюмки_2: R U R' U' R' F R2 U R' U' F'
                movelist = self.cube.parse_moveset("R U R' U' R' F R2 U R' U' F'")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
                # print('Рюмки_2')
            elif (pattern == "2 4 5 7 L0 L1 F0 F1 B0"):     # Молнии_1: F R' F' R U2 R U2 R'
                movelist = self.cube.parse_moveset("F R' F' R U2 R U2 R'")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
                # print('Молнии_1')
            elif (pattern == "2 5 6 9 F1 F2 R1 R2 B2"):     # Молнии_2: R U2 R' U2 R' F R F'
                movelist = self.cube.parse_moveset("R U2 R' U2 R' F R F'")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
                # print('Молнии_2')
            elif (pattern == "2 4 5 7 L1 L2 F1 R2 B2"):     # Молнии_3: y2 F R U R' U' F' U F R U R' U' F'
                movelist = self.cube.parse_moveset("F R U R' U' F' U F R U R' U' F'")
                movelist = self.translate_movelist_by_side('B', movelist)
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                # print('Молнии_3')
                self.logs += movelist
            elif (pattern == "1 4 5 7 8 L0 L1 L2 B1"):      # Мягкие_знаки_1: B' U' R' U R B
                movelist = self.cube.parse_moveset("B' U' R' U R B")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
                # print('Мягкие_знаки_1')
            elif (pattern == "3 5 6 8 9 R0 R1 R2 B1"):      # Мягкие_знаки_2: y F U R' F R F' U' F'
                movelist = self.cube.parse_moveset("F U R' F R F' U' F'")
                movelist = self.translate_movelist_by_side('L', movelist)
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                # print('Мягкие_знаки_2')
                self.logs += movelist
            elif (pattern == "1 4 5 7 8 L1 F0 B1 B2"):      # Мягкие_знаки_3: R' F R U R' U' F2 U F R
                movelist = self.cube.parse_moveset("R' F R U R' U' F2 U F R")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
                # print('Мягкие_знаки_3')
            elif (pattern == "3 5 6 8 9 F2 R1 B0 B1"):      # Мягкие_знаки_4: R U B' U' R' U R B R'
                movelist = self.cube.parse_moveset("R U B' U' R' U R B R'")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
                # print('Мягкие_знаки_4')
            elif (pattern == "2 3 4 5 7 L1 L2 F1 B0"):      # Буквы_М_1: R U R' U R U' R' U' R' F R F'
                movelist = self.cube.parse_moveset("R U R' U R U' R' U' R' F R F'")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
                # print('Буквы_М_1')
            elif (pattern == "1 2 5 6 9 F1 R0 R1 B2"):      # Буквы_М_2: y' R U R2' F' U' F U R2 U2' R'
                movelist = self.cube.parse_moveset("R U R2' F' U' F U R2 U2' R'")
                movelist = self.translate_movelist_by_side('R', movelist)
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                # print('Буквы_М_2')
                self.logs += movelist
            elif (pattern == "1 2 4 5 9 L1 F1 R0 B2"):      # Галстуки_1: y R' U' F R' F' R2 U' R' U2 R
                movelist = self.cube.parse_moveset("R' U' F R' F' R2 U' R' U2 R")
                movelist = self.translate_movelist_by_side('L', movelist)
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                # print('Галстуки_1')
                self.logs += movelist
            elif (pattern == "1 2 4 5 9 L0 L1 F1 F2"):      # Галстуки_2: F R U' R' U' R U R' F'
                movelist = self.cube.parse_moveset("F R U' R' U' R U R' F'")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
                # print('Галстуки_2')
            elif (pattern == "1 3 5 6 8 F0 F2 R1 B1"):       # Петухи_1: R U' R' U2 R U B U' B' U' R'
                movelist = self.cube.parse_moveset("R U' R' U2 R U B U' B' U' R'")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
                # print('Петухи_1')
            elif (pattern == "1 3 4 5 8 L0 L1 F1 F2"):       # Петухи_2: R' U' R U' R' U2 R F R U R' U' F'
                movelist = self.cube.parse_moveset("R' U' R U' R' U2 R F R U R' U' F'")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
                # print('Петухи_2')
            elif (pattern == "1 3 5 6 8 L2 R0 R2 B1"):       # Петухи_3: R2' U R' B' R U' R2' U R B R'
                movelist = self.cube.parse_moveset("R2' U R' B' R U' R2' U R B R'")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
                # print('Петухи_3')
            elif (pattern == "1 3 4 5 8 L1 L2 R0 B1"):       # Петухи_4: y R U R' U' R U' R' F' U' F R U R'
                movelist = self.cube.parse_moveset("R U R' U' R U' R' F' U' F R U R'")
                movelist = self.translate_movelist_by_side('L', movelist)
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                # print('Петухи_4')
                self.logs += movelist
            else:
                self.cube.move_D()
                self.logs.append('move_D')

    def step_4_OLL(self, flag: bool):
        self.step_4_OLL_rotation()
        if (self.step_4_check_top() != 1):
            self.step_4(flag)
            self.step_5(flag)
            self.step_6(flag)

        if (flag == True):
            print('STEP 4 OLL complete')
            self.cube.display_cube()

    def translate_movelist(self, movelist : list):
        ret_list = []
        i = 0
        fin = len(movelist)
        while i < fin:
            j = 0
            num_of_repeats = 0
            move_to_find = movelist[i]
            if (fin - i > 3):
                for j in range(4):
                    if move_to_find == movelist[j + i]:
                        num_of_repeats += 1
                    else:
                        break
            if (num_of_repeats == 3):
                ret_list.append('rev_' + movelist[i])
                i += 2
            elif (num_of_repeats == 4):
                i += 3
            else:
                ret_list.append(movelist[i])
            i += 1
        return ret_list

    def step_4_check(self):
        sides = ['F', 'L', 'B', 'R']
        check_piece = {'L':[1, 0], 'F':[0, 1], 'R':[1, 2], 'B':[2, 1]}
        broken_list = copy(sides)
        ret_colors = {}

        for side in sides:
            mid_piece = self.cube.cube_sides[side][1][1]
            bottom_piece = self.cube.cube_sides[side][2][1]
            down_piece = self.cube.cube_sides['D'][check_piece[side][0]][check_piece[side][1]]
            ret_colors[side] = [bottom_piece, down_piece]
            if (bottom_piece == mid_piece and down_piece == 'Y') or (bottom_piece == 'Y' and down_piece == mid_piece):
                broken_list.remove(side)
        return broken_list, ret_colors
    
    def step_4_do_all_work(self, side):
        movelist = ['move_D', 'move_F', 'move_L', 'move_D', 'move_L', 'move_L', 'move_L', 'move_D',
                    'move_D', 'move_D', 'move_F', 'move_F', 'move_F']
        trans_movelist = self.translate_movelist_by_side(side, movelist)
        self.cube.execute_movelist(trans_movelist)
        self.logs += trans_movelist

    def step_4_move_piece(self, broken_list, ret_colors):
        if len(broken_list) == 2:
            if ('F' in broken_list and 'B' in broken_list) or ('R' in broken_list and 'L' in broken_list):
                if ('F' in broken_list):
                    mid_side = 'R'
                else:
                    mid_side = 'F'
                self.step_4_do_all_work(broken_list[0])
                self.step_4_do_all_work(mid_side)
                self.step_4_do_all_work(broken_list[0])
            else:
                if ('F' in broken_list and 'R' in broken_list):
                    self.step_4_do_all_work('F')
                else:
                    self.step_4_do_all_work(broken_list[1])
        else:
            if ret_colors['B'][0] == 'Y':
                back_piece = ret_colors['B'][1]
            else:
                back_piece = ret_colors['B'][0]
            if (back_piece == 'O'):
                self.step_4_do_all_work('B')
            else:
                self.step_4_do_all_work('R')

    def step_4_rotate(self):
        while (True):
            bottom_piece = self.cube.cube_sides['F'][2][1]
            down_piece = self.cube.cube_sides['D'][0][1]
            if (bottom_piece == 'G' and down_piece == 'Y') or (bottom_piece == 'Y' and down_piece == 'G'):
                break
            self.cube.move_D()
            self.logs.append('move_D')

    def step_4(self, flag:bool):
        self.step_4_rotate()

        broken_list, ret_colors = self.step_4_check()
        while (len(broken_list) != 0):
            self.step_4_move_piece(broken_list, ret_colors)
            broken_list, ret_colors = self.step_4_check()
        if (flag == True):
            print('STEP 4 complete')
            self.cube.display_cube()

    def step_5_create_yellow_cross(self, cross):
        if sum(cross) == 0:
            movelist = ['move_F', 'move_D', 'move_L', 'move_D', 'move_D', 'move_D',
                        'move_L', 'move_L', 'move_L', 'move_F', 'move_F', 'move_F']
            self.cube.execute_movelist(movelist)
            self.logs += movelist
        else:
            tmp_state = self.step_5_check_cross()
            while (True):
                if tmp_state == [1, 0, 1, 0] or tmp_state == [0, 0, 1, 1]:
                    break
                self.cube.move_D()
                self.logs.append('move_D')
                tmp_state = self.step_5_check_cross()
            
            if (tmp_state == [1, 0, 1, 0]):
                movelist = ['move_F', 'move_D', 'move_L', 'move_D', 'move_D', 'move_D',
                            'move_L', 'move_L', 'move_L', 'move_F', 'move_F', 'move_F']
                self.cube.execute_movelist(movelist)
                self.logs += movelist
            elif (tmp_state == [0, 0, 1, 1]):
                movelist = ['move_F', 'move_L', 'move_D', 'move_L', 'move_L', 'move_L',
                            'move_D', 'move_D', 'move_D', 'move_F', 'move_F', 'move_F']
                self.cube.execute_movelist(movelist)
                self.logs += movelist

    def step_5_check_cross(self):
        check_piece = [[0, 1], [2, 1], [1, 0], [1, 2]]
        ret_list = []

        for i in check_piece:
            if self.cube.cube_sides['D'][i[0]][i[1]] == 'Y':
                ret_list.append(1)
            else:
                ret_list.append(0)
        return ret_list

    def step_5(self, flag:bool):
        cross_state = self.step_5_check_cross()
        while (cross_state != [1, 1, 1, 1]):
            self.step_5_create_yellow_cross(cross_state)
            cross_state = self.step_5_check_cross()

        if (flag == True):
            print('STEP 5 complete')
            self.cube.display_cube()
    
    def upper_down_translation(self, movelist):
        ret_list = []
        for move in movelist:
            ret_list.append(self.rev_tranlation[move])
        return ret_list

    def step_6_create_yellow_cross(self, cross):
        if (cross == [0, 0, 1, 1] and self.cube.cube_sides['F'][2][0] == 'Y' and self.cube.cube_sides['F'][2][2] == 'Y'):
            movelist = ['move_R', 'move_R', 'move_D', 'move_R', 'move_R', 'move_R',
                        'move_U', 'move_U', 'move_R', 'move_D', 'move_D', 'move_D', 'move_R',
                        'move_R', 'move_R', 'move_U', 'move_U', 'move_R', 'move_R', 'move_R' ]
            movelist = self.upper_down_translation(movelist)
            self.cube.execute_movelist(movelist)
            self.logs += movelist
        elif (cross == [1, 0, 1 ,0] and self.cube.cube_sides['F'][2][2] == 'Y' and self.cube.cube_sides['B'][2][0] == 'Y'):
            movelist = ['move_R', 'move_R', 'move_R', 'move_F', 'move_F', 'move_F',
                        'move_L', 'move_F', 'move_R', 'move_F', 'move_F', 'move_F',
                        'move_L', 'move_L', 'move_L', 'move_F']
            movelist = self.upper_down_translation(movelist)
            self.cube.execute_movelist(movelist)
            self.logs += movelist
        elif (cross == [1, 0, 0, 1] and self.cube.cube_sides['B'][2][2] == 'Y' and self.cube.cube_sides['R'][2][0] == 'Y'):
            movelist = ['move_R', 'move_R', 'move_R', 'move_F', 'move_F', 'move_F',
                        'move_L', 'move_L', 'move_L', 'move_F', 'move_R', 'move_F',
                        'move_F', 'move_F','move_L', 'move_F' ]
            movelist = self.upper_down_translation(movelist)
            self.cube.execute_movelist(movelist)
            self.logs += movelist
        elif (cross == [0, 0, 1, 0] and self.cube.cube_sides['F'][2][0] == 'Y' and 
                (self.cube.cube_sides['L'][2][0] == 'Y' or self.cube.cube_sides['R'][2][0] == 'Y') and self.cube.cube_sides['B'][2][0] == 'Y'):
            movelist = ['move_R', 'move_U', 'move_R', 'move_R', 'move_R', 'move_U',
                        'move_R', 'move_U', 'move_U', 'move_R', 'move_R', 'move_R' ]
            movelist = self.upper_down_translation(movelist)
            self.cube.execute_movelist(movelist)
            self.logs += movelist
        elif (cross == [0, 1, 0, 0] and (self.cube.cube_sides['F'][2][2] == 'Y' or self.cube.cube_sides['B'][2][2] == 'Y') and 
                self.cube.cube_sides['R'][2][2] == 'Y' and self.cube.cube_sides['L'][2][2] == 'Y'):
            movelist = ['move_R', 'move_U', 'move_U', 'move_R', 'move_R', 'move_R',
                        'move_U', 'move_U', 'move_U', 'move_R', 'move_U', 'move_U',
                        'move_U', 'move_R', 'move_R', 'move_R']
            movelist = self.upper_down_translation(movelist)
            self.cube.execute_movelist(movelist)
            self.logs += movelist
        elif (cross == [0, 0, 0, 0]):
            if (self.cube.cube_sides['F'][2][0] == 'Y' and self.cube.cube_sides['F'][2][2] == 'Y' and 
            self.cube.cube_sides['B'][2][0] == 'Y' and self.cube.cube_sides['B'][2][2] == 'Y'):
                movelist = ['move_R', 'move_U', 'move_U', 'move_R', 'move_R', 'move_R',
                            'move_U', 'move_U', 'move_U', 'move_R', 'move_U', 'move_R',
                            'move_R', 'move_R', 'move_U', 'move_U', 'move_U', 'move_R',
                            'move_U', 'move_U', 'move_U', 'move_R', 'move_R', 'move_R' ]
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
            elif (self.cube.cube_sides['F'][2][0] == 'Y' and self.cube.cube_sides['B'][2][2] == 'Y' and 
            self.cube.cube_sides['R'][2][0] == 'Y' and self.cube.cube_sides['R'][2][2] == 'Y'):
                movelist = ['move_R', 'move_U', 'move_U', 'move_R', 'move_R', 'move_U',
                            'move_U', 'move_U', 'move_R', 'move_R', 'move_U', 'move_U',
                            'move_U', 'move_R', 'move_R', 'move_U', 'move_U', 'move_R' ]
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
            else:
                self.cube.move_D()
                self.logs.append('move_D')
        else:
            self.cube.move_D()
            self.logs.append('move_D')

    def step_6_check_cross(self):
        check_piece = [[0, 0], [0, 2], [2, 0], [2, 2]]
        ret_list = []

        for i in check_piece:
            if self.cube.cube_sides['D'][i[0]][i[1]] == 'Y':
                ret_list.append(1)
            else:
                ret_list.append(0)
        return ret_list

    def step_6(self, flag:bool):
        cross_state = self.step_6_check_cross()
        while cross_state != [1, 1, 1, 1]:
            self.step_6_create_yellow_cross(cross_state)
            cross_state = self.step_6_check_cross()

        if (flag == True):
            print('STEP 6 complete')
            self.cube.display_cube()

    def is_cube_solved(self):
        sides = ['L', 'F', 'R', 'B', 'U', 'D']
        cube_side = self.cube.cube_sides
        for side in sides:
            if (cube_side[side][1][1] == cube_side[side][0][0] == cube_side[side][0][1] == cube_side[side][0][2] and
                cube_side[side][1][1] == cube_side[side][1][0] == cube_side[side][1][2] and
                cube_side[side][1][1] == cube_side[side][2][0] == cube_side[side][2][1] == cube_side[side][2][2] ):
                pass
            else:
                return 0
        return 1
    
    def step_5_PLL_parse_slice(self):
        sides = ['L', 'F', 'R', 'B']
        ret_str = ''
        for side in sides:
            check_side = self.cube.cube_sides[side][2]
            for i in check_side:
                ret_str += str(i)
            ret_str += ' '
        return ret_str[:-1]

    def step_5_PLL_patter_transfer(self, pattern):
        tmp = ['O', 'G', 'R', 'B', 'O']
        ret_list = []
        ret_list.append(pattern)
        for i in range(4):
            ret_pattern = ''
            for letter in ret_list[-1]:
                if letter in tmp:
                    i = tmp.index(letter)
                    ret_pattern += tmp[i + 1]
                else:
                    ret_pattern += letter
            ret_list.append(ret_pattern)
        return ret_list

# U U R U U B D D U F R L B R U R L U U L R F R L D L L R U F R F F L B L D R U L

    def step_5_PLL_rotation(self): 
        for i in range(16):
            pattern = self.step_5_PLL_parse_slice()
            if (pattern in self.step_5_PLL_patter_transfer('RGB ORR BBO GOG')):      # Треугольники углов_1: y' R U R' U' R' F R U R' U' R' F' R U R2 U' R'
                # print('Треугольники углов_1')
                movelist = self.cube.parse_moveset("R U R' U' R' F R U R' U' R' F' R U R2 U' R'")
                movelist = self.translate_movelist_by_side('R', movelist)
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
            elif (pattern in self.step_5_PLL_patter_transfer('GRG RBB OOR BGO')):    # Треугольники углов_2: y' R U R2 U' R' F R U R U' R' F' R U R U' R'
                # print('Треугольники углов_2')
                movelist = self.cube.parse_moveset("R U R2 U' R' F R U R U' R' F' R U R U' R'")
                movelist = self.translate_movelist_by_side('R', movelist)
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
            if (pattern in self.step_5_PLL_patter_transfer('GOB OGR BRG RBO')):   # Терминатор: R' U2 R' D' R U R' D R U' R' D' R U2 R' D R2
                # print('Терминатор')
                movelist = self.cube.parse_moveset("R' U2 R' D' R U R' D R U' R' D' R U2 R' D R2")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
            elif (pattern in self.step_5_PLL_patter_transfer('GRG RGR BOB OBO')):   # Саночки: y' R' U' R U' R U R U' R' U R U R2 U' R' U2
                # print('Саночки')
                movelist = self.cube.parse_moveset("R U R2 U' R' F R U R U' R' F' R U R U' R'")
                movelist = self.translate_movelist_by_side('R', movelist)
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
            elif (pattern in self.step_5_PLL_patter_transfer('BGB OBO GOG RRR')):   # Треугольники сторон_1: R U' R U R U R U' R' U' R2
                # print('Треугольники сторон_1')
                movelist = self.cube.parse_moveset("R U' R U R U R U' R' U' R2")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
            elif (pattern in self.step_5_PLL_patter_transfer('BOB OGO GBG RRR')):   # Треугольники сторон_2: R2 U R U R' U' R' U' R' U R'
                # print('Треугольники сторон_2')
                movelist = self.cube.parse_moveset("R2 U R U R' U' R' U' R' U R'")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
            elif (pattern in self.step_5_PLL_patter_transfer('RRO GGR BBB OOG')):   # Лямбды_1: R U2 R' U' R U2 L' U R' U' L
                # print('Лямбды_1')
                movelist = self.cube.parse_moveset("R U2 R' U' R U2 L' U R' U' L")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
            elif (pattern in self.step_5_PLL_patter_transfer('ORR BOO GGG RBB')):   # Лямбды_2: U' R' U L' U2 R U' R' U2 R L
                # print('Лямбды_2')
                movelist = self.cube.parse_moveset("U' R' U L' U2 R U' R' U2 R L")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
            elif (pattern in self.step_5_PLL_patter_transfer('OGR RGR BBO GOB')):   # Cемерки_1: U R2 F R U R U' R' F' R U2 R' U2 R
                # print('Cемерки_1')
                movelist = self.cube.parse_moveset("U R2 F R U R U' R' F' R U2 R' U2 R")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
            elif (pattern in self.step_5_PLL_patter_transfer('RBB OGO GOR BRG')):   # Cемерки_2: L U2 L' U2 L F' L' U' L U L F L2 U
                # print('Cемерки_2')
                movelist = self.cube.parse_moveset("L U2 L' U2 L F' L' U' L U L F L2 U")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
            elif (pattern in self.step_5_PLL_patter_transfer('RBO GRR BGB OOG')):   # Буква Т: R U R' U' R' F R2 U' R' U' R U R' F'
                # print('Буква Т')
                movelist = self.cube.parse_moveset("R U R' U' R' F R2 U' R' U' R U R' F'")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
            elif (pattern in self.step_5_PLL_patter_transfer('GGB ORR BOG RBO')):   # Копье: F R U' R' U' R U R' F' R U R' U' R' F R F'
                # print('Копье')
                movelist = self.cube.parse_moveset("F R U' R' U' R U R' F' R U R' U' R' F R F'")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
            elif (pattern in self.step_5_PLL_patter_transfer('GOB OBG RRR BGO')):   # Параллельный перенос: U' R' U R U' R2 F' U' F U R F R' F' R2
                # print('Параллельный переноc')
                movelist = self.cube.parse_moveset("U' R' U R U' R2 F' U' F U R F R' F' R2")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
            elif (pattern in self.step_5_PLL_patter_transfer('GOB ORR BBG RGO')):   # Летающая тарелка: R' U2 R U2 L U' R' U L' U L U' R U L'
                # print('Летающая тарелка')
                movelist = self.cube.parse_moveset("R' U2 R U2 L U' R' U L' U L U' R U L'")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
            elif (pattern in self.step_5_PLL_patter_transfer('BBG RRO GGB OOR')):   # Буквы X_1: R U R' U R U R' F' R U R' U' R' F R2 U' R' U2 R U' R'
                # print('Буквы X_1')
                movelist = self.cube.parse_moveset("R U R' U R U R' F' R U R' U' R' F R2 U' R' U2 R U' R'")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
            elif (pattern in self.step_5_PLL_patter_transfer('GBB ORR BGG ROO')):   # Буквы X_2: R' U R U' R' F' U' F R U R' F R' F' R U' R
                # print('Буквы X_2')
                movelist = self.cube.parse_moveset("R' U R U' R' F' U' F R U R' F R' F' R U' R")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
            elif (pattern in self.step_5_PLL_patter_transfer('GOG RBB OGR BRO')):   # Восьмерки_1: R2' F2 R U2 R U2' R' F R U R' U' R' F R2
                # print('Восьмерки_1')
                movelist = self.cube.parse_moveset("R2 F2 R U2 R U2 R' F R U R' U' R' F R2")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
            elif (pattern in self.step_5_PLL_patter_transfer('BGO GBB ORG ROR')):   # Восьмерки_2: R2' F' R U R U' R' F' R U2' R' U2' R' F2 R2
                # print('Восьмерки_2')
                movelist = self.cube.parse_moveset("R2 F' R U R U' R' F' R U2 R' U2 R' F2 R2")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
            elif (pattern in self.step_5_PLL_patter_transfer('RBO GGR BOB ORG')):   # Восьмерки_3: L2 F2 L' U2 L' U2 L F' L' U' L U L F' L2
                # print('Восьмерки_3')
                movelist = self.cube.parse_moveset("L2 F2 L' U2 L' U2 L F' L' U' L U L F' L2")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
            elif (pattern in self.step_5_PLL_patter_transfer('BRO GGB OBG ROR')):   # Восьмерки_4: U' D R' U' R U D' R2 U R' U R U' R U' R2
                # print('Восьмерки_4')
                movelist = self.cube.parse_moveset("U' D R' U' R U D' R2 U R' U R U' R U' R2")
                movelist = self.upper_down_translation(movelist)
                self.cube.execute_movelist(movelist)
                self.logs += movelist
            else:
                self.cube.move_D()
                self.logs.append('move_D')

    def step_5_PLL_check_state(self):
        sides = ['L', 'F', 'R', 'B']
        for side in sides:
            check_side = self.cube.cube_sides[side][2]
            if (check_side[1] != check_side[0]) or (check_side[1] != check_side[2]):
                return 0
        return 1

    def step_5_PLL(self, flag: bool):
        if (self.step_5_PLL_check_state() == 0):
            self.step_5_PLL_rotation()

        if (self.step_5_PLL_check_state() == 1):
            while self.cube.cube_sides['F'][2][1] != self.cube.cube_sides['F'][1][1]:
                self.cube.move_D()
                self.logs.append('move_D')
        
        if (flag == True):
            print('STEP 5 PPL complete')
            self.cube.display_cube()
