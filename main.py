import solver
import cube
import argparse
import sys

def save_list_to_file(listname : list, filename : str):
    f = open(filename, 'w')
    for move in listname:
        f.write(move + '\n')
    f.close

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('flag', help='флаг ввода ("manual" ручной, "random" рандомная генерация)')
    parser.add_argument('show', help='флаг вывода ("full" полный поэтапный вывод, "min" только ходы)')
    args = parser.parse_args()

    my_cube = cube.Cube()
    if (args.flag == 'manual'):
        movelist = my_cube.parse_moveset(input('Введите последовательность:\n'))
    elif (args.flag == 'random'):
        movelist = my_cube.random_start(int(input('Введите число движений для рандомайзера:\n')))
    else:
        print('Неизвестный флаг: ', args.flag)
        exit(0)
    
    if (args.show == 'full'):
        show_flag = True
    elif (args.show == 'min'):
        show_flag = False
    else:
        print('Неизвестный флаг: ', args.show)
        exit(0)
    my_cube.execute_movelist(movelist)
    if (show_flag == True):
        print('CUBE CREATED')
        my_cube.display_cube()
    my_solver = solver.Solver(my_cube)
    my_solver.step_1(show_flag)
    my_solver.step_2(show_flag)
    my_solver.step_3(show_flag)
    my_solver.step_4_OLL(show_flag)
    my_solver.step_5_PLL(show_flag)
    initial_moves = my_solver.translate_movelist(movelist)
    solving_moves = my_solver.translate_movelist(my_solver.logs)
    save_list_to_file(initial_moves, 'Initial.txt')
    save_list_to_file(solving_moves, 'Solving.txt')
    if (show_flag == False):
        for move in solving_moves:
            print(move)
    print('Number moves to solve this cube: ', len(solving_moves))

if __name__ == '__main__':
    sys.exit(main())