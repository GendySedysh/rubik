from mimetypes import init
import argparse
from pickle import TRUE
import pygame
import time
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

vertices = (
    ( 1, -1, -1), ( 1,  1, -1), (-1,  1, -1), (-1, -1, -1),
    ( 1, -1,  1), ( 1,  1,  1), (-1, -1,  1), (-1,  1,  1)
)
edges = ((0,1),(0,3),(0,4),(2,1),(2,3),(2,7),(6,3),(6,4),(6,7),(5,1),(5,4),(5,7))
surfaces = ((0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4), (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6))
colors = ((1, 0, 0), (0, 1, 0), (1, 0.5, 0), (0, 0, 1), (1, 1, 0), (1, 1, 1))

class Cube():
    def __init__(self, id, N, scale):
        self.N = N
        self.scale = scale
        self.init_i = [*id]
        self.current_i = [*id]
        self.rot = [[1 if i==j else 0 for i in range(3)] for j in range(3)]

    def isAffected(self, axis, slice, dir):
        return self.current_i[axis] == slice

    def update(self, axis, slice, dir):

        if not self.isAffected(axis, slice, dir):
            return

        i, j = (axis+1) % 3, (axis+2) % 3
        for k in range(3):
            self.rot[k][i], self.rot[k][j] = -self.rot[k][j]*dir, self.rot[k][i]*dir

        self.current_i[i], self.current_i[j] = (
            self.current_i[j] if dir < 0 else self.N - 1 - self.current_i[j],
            self.current_i[i] if dir > 0 else self.N - 1 - self.current_i[i] )

    def transformMat(self):
        scaleA = [[s*self.scale for s in a] for a in self.rot]  
        scaleT = [(p-(self.N-1)/2)*2.1*self.scale for p in self.current_i] 
        return [*scaleA[0], 0, *scaleA[1], 0, *scaleA[2], 0, *scaleT, 1]

    def draw(self, col, surf, vert, animate, angle, axis, slice, dir):

        glPushMatrix()
        if animate and self.isAffected(axis, slice, dir):
            glRotatef( angle*dir, *[1 if i==axis else 0 for i in range(3)] )
        glMultMatrixf( self.transformMat() )

        glBegin(GL_QUADS)
        for i in range(len(surf)):
            glColor3fv(colors[i])
            for j in surf[i]:
                glVertex3fv(vertices[j])
        glEnd()

        glPopMatrix()

class EntireCube():
    def __init__(self, N, scale):
        self.N = N
        cr = range(self.N)
        self.cubes = [Cube((x, y, z), self.N, scale) for x in cr for y in cr for z in cr]

    def mainloop(self, init_moves, solution_moves):

        rot_cube_map  = { K_UP: (-1, 0), K_DOWN: (1, 0), K_LEFT: (0, -1), K_RIGHT: (0, 1)}
        rot_slice_map = {
            K_1: (0, 0, 1), K_2: (0, 1, 1), K_3: (0, 2, 1), K_4: (1, 0, 1), K_5: (1, 1, 1),
            K_6: (1, 2, 1), K_7: (2, 0, 1), K_8: (2, 1, 1), K_9: (2, 2, 1),
            K_F1: (0, 0, -1), K_F2: (0, 1, -1), K_F3: (0, 2, -1), K_F4: (1, 0, -1), K_F5: (1, 1, -1),
            K_F6: (1, 2, -1), K_F7: (2, 0, -1), K_F8: (2, 1, -1), K_F9: (2, 2, -1),
        }  

        ang_x, ang_y, rot_cube = 150, 150, (0, 0)
        animate, animate_ang, animate_speed = False, 0, 5
        action = (0, 0, 0)

        tmp = 0
        tmp_2 = 0
        end_tmp = len(init_moves)
        end_tmp_2 = len(solution_moves)
        # MAINLOOP
        while True:
            if tmp < end_tmp:
                if not animate and init_moves[tmp] in rot_slice_map:
                    animate, action = True, rot_slice_map[init_moves[tmp]]
                    tmp += 1
            elif tmp == end_tmp:
                for i in range(5):
                    print('CUBE CREATED')
                pygame.time.wait(1500)
                tmp += 1
            elif tmp > end_tmp and tmp_2 < end_tmp_2:
                if not animate and solution_moves[tmp_2] in rot_slice_map:
                    animate, action = True, rot_slice_map[solution_moves[tmp_2]]
                    tmp_2 += 1
            elif tmp_2 == end_tmp_2:
                for i in range(5):
                    print('CUBE SOLVED')
                tmp_2 += 1
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == KEYDOWN:
                        if event.key in rot_cube_map:
                            rot_cube = rot_cube_map[event.key]
                        if not animate and event.key in rot_slice_map:
                            animate, action = True, rot_slice_map[event.key]
                    if event.type == KEYUP:
                        if event.key in rot_cube_map:
                            rot_cube = (0, 0)

            ang_x += rot_cube[0]*2
            ang_y += rot_cube[1]*2

            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            glTranslatef(0, 0, -40)
            glRotatef(ang_y, 0, 1, 0)
            glRotatef(ang_x, 1, 0, 0)

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

            if animate:
                if animate_ang >= 90:
                    for cube in self.cubes:
                        cube.update(*action)
                    animate, animate_ang = False, 0

            for cube in self.cubes:
                cube.draw(colors, surfaces, vertices, animate, animate_ang, *action)
            if animate:
                animate_ang += animate_speed

            pygame.display.flip()
            pygame.time.wait(10)

def translate_movelist(movelist):
    translation = { 'move_D': K_F6, 'move_U': K_4, 'move_B': K_F3, 'move_F': K_1, 'move_L': K_F9, 'move_R': K_7,
                    'rev_move_D': K_6, 'rev_move_U': K_F4, 'rev_move_B': K_3,
                    'rev_move_F': K_F1, 'rev_move_L': K_9, 'rev_move_R': K_F7 }

    ret_list = []
    for move in movelist:
        ret_list.append(translation[move])
    return ret_list

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('init_file', help='Файл со списком действий закручивающими куб')
    parser.add_argument('solution_file', help='Файл со списком действий решающими куб')
    args = parser.parse_args()

    init_path = args.init_file
    solution_path = args.solution_file

    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glEnable(GL_DEPTH_TEST) 

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    NewEntireCube = EntireCube(3, 1.5)

    with open(init_path) as f:
        init_moves = f.read().splitlines()
    init_moves = translate_movelist(init_moves)
    with open(solution_path) as f:
        solution_moves = f.read().splitlines()
    solution_moves = translate_movelist(solution_moves)
    NewEntireCube.mainloop(init_moves, solution_moves)

if __name__ == '__main__':
    main()
    pygame.quit()
    quit()