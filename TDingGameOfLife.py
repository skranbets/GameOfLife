import turtle
import tkinter
import random
from tkinter import messagebox as ms
import time
import Errors
from Grid import Grid

t = turtle.Turtle()
wn = turtle.Screen()
t.hideturtle()
wn.setup(900, 900)
t.speed(0)
wn.tracer(0, 0)

sleep_time = 0.5
current_grid = []
game_active = False


def set_up():
    global current_grid
    temp_num = int(wn.numinput("Size of Grid", "Please the size of the grid in the Universe ( ? x ? ) "))
    current_grid = Grid(temp_num)


def draw_board():
    wn.setup(current_grid.grid_size * current_grid.box + 8, current_grid.grid_size * current_grid.box + 8)
    for i in range(current_grid.grid_size):
        for j in range(current_grid.grid_size):
            if current_grid.grid_list[i][j] == 0:
                draw_box(-3 - (current_grid.grid_size * current_grid.box / 2) + j * current_grid.box,
                         3 + (current_grid.grid_size * current_grid.box / 2) - i * current_grid.box, False)
            elif current_grid.grid_list[i][j] == 1:
                current_grid.grid_list[i][j] = 0
                draw_box(-3 - (current_grid.grid_size * current_grid.box / 2) + j * current_grid.box,
                         3 + (current_grid.grid_size * current_grid.box / 2) - i * current_grid.box, True)

    t.penup()


def draw_box(x, y, is_filled):
    x = int(x)
    y = int(y)
    t.begin_fill()
    t.pencolor("black")
    if is_filled:
        box_num = (round(x / current_grid.box) + round((current_grid.grid_size / 2) + 0.1) +
                   ((round((0 - y) / current_grid.box) + round((current_grid.grid_size / 2) + 0.1)) * len(
                       current_grid.grid_list)))
        box_counter = 0
        t.penup()
        for i in range(len(current_grid.grid_list)):
            for j in range(len(current_grid.grid_list[i])):
                if box_counter == box_num:
                    if current_grid.grid_list[i][j] == 0:
                        current_grid.grid_list[i][j] = 1
                        t.fillcolor("black")
                    elif current_grid.grid_list[i][j] == 1:
                        current_grid.grid_list[i][j] = 0
                        t.pencolor("black")
                        t.fillcolor("white")

                box_counter = box_counter + 1
    else:
        t.fillcolor("white")

    t.penup()
    t.goto(x, y)
    t.pendown()
    t.forward(current_grid.box)
    t.right(90)
    t.forward(current_grid.box)
    t.right(90)
    t.forward(current_grid.box)
    t.right(90)
    t.forward(current_grid.box)
    t.right(90)
    t.end_fill()




def color_box(x, y):
    if -(current_grid.grid_size * current_grid.box + 8) / 2 <= x <= (
            current_grid.grid_size * current_grid.box + 8) / 2 and -(
            current_grid.grid_size * current_grid.box + 8) / 2 <= y <= (
            current_grid.grid_size * current_grid.box + 8) / 2:
        if current_grid.grid_size % 2 != 0:
            x_prime = -3 + ((x + current_grid.box / 2) // current_grid.box) * current_grid.box
            x_prime -= current_grid.box / 2
            y_prime = 3 + ((y + current_grid.box / 2) // current_grid.box) * current_grid.box
            y_prime += current_grid.box / 2
        else:
            x_prime = -3 + (x // current_grid.box) * current_grid.box
            y_prime = 3 + (y // current_grid.box) * current_grid.box + current_grid.box
        t.penup()
        t.pencolor("black")
        draw_box(x_prime, y_prime, True)
    wn.update()


def quit_it():
    pause_game()
    exit(0)


def generate_random():
    pause_game()
    size_uni = current_grid.grid_size * current_grid.grid_size
    count_filled = 0
    for h in range(current_grid.grid_size):
        for g in range(current_grid.grid_size):
            if current_grid.grid_list[h][g] == 1:
                count_filled = count_filled + 1
    num_to_be_filled = int(size_uni * 4 / 10) - count_filled
    fill_list = []

    for i in range(num_to_be_filled):
        temp_num = random.randint(1, size_uni)
        while temp_num in fill_list:
            temp_num = random.randint(1, size_uni)
        fill_list.append(temp_num)
    for j in range(current_grid.grid_size):
        for k in range(current_grid.grid_size):
            grid_index = j * len(current_grid.grid_list[0]) + k + 1
            if grid_index in fill_list:
                if current_grid.grid_list[k][j] == 0:
                    draw_box(-3 - (current_grid.grid_size * current_grid.box / 2) + j * current_grid.box,
                             3 + (current_grid.grid_size * current_grid.box / 2) - k * current_grid.box,
                             True)


def read_file():
    pause_game()
    global current_grid
    new_grid = []
    file_name = wn.textinput("File Name", "Enter the file name")
    try:
        row_num = -1
        life_file = open(f"./lifeFiles/{file_name}.life", "r")
        for line in life_file:
            line = line.strip()
            if row_num == -1:
                row_num = len(line)
            if row_num != len(line):
                raise Errors.NotRectangle
            col_list = []
            for digit in line:
                if digit != "0" and digit != "1":
                    raise Errors.InvalidFile
                else:
                    col_list.append(int(digit))

            new_grid.append(col_list)
        life_file.close()
        if len(new_grid) != len(new_grid[0]):
            raise Errors.NotSquare

        current_grid.new_grid(new_grid)
        t.pencolor("black")
        draw_board()

    except FileNotFoundError:
        ms.showinfo("File Not Found", "The file was not found.")
    except Errors.InvalidFile:
        ms.showinfo("Invalid File", "The file contains invalid data ( not 1 or 0 )")
    except Errors.NotSquare:
        ms.showinfo("Invalid File", "The life file is not a square")
    except Errors.NotRectangle:
        ms.showinfo("Invalid File", "The life file is not a rectangle")




def start_game():
    global game_active
    game_active = True

    while game_active:
        next_gen()
        time.sleep(sleep_time)
        wn.listen()


def pause_game():
    global game_active
    game_active = False


def next_gen():
    to_be_filled_cord = []
    for i in range(current_grid.grid_size):
        for j in range(current_grid.grid_size):
            neighbor_counter = 0
            if i == 0:
                if current_grid.grid_list[i + 1][j]:
                    neighbor_counter = neighbor_counter + 1
                if j == 0:
                    if current_grid.grid_list[i + 1][j + 1]:
                        neighbor_counter = neighbor_counter + 1
                    if current_grid.grid_list[i][j + 1]:
                        neighbor_counter = neighbor_counter + 1
                elif j == current_grid.grid_size - 1:
                    if current_grid.grid_list[i + 1][j - 1]:
                        neighbor_counter = neighbor_counter + 1
                    if current_grid.grid_list[i][j - 1]:
                        neighbor_counter = neighbor_counter + 1
                else:
                    if current_grid.grid_list[i + 1][j + 1]:
                        neighbor_counter = neighbor_counter + 1
                    if current_grid.grid_list[i][j + 1]:
                        neighbor_counter = neighbor_counter + 1
                    if current_grid.grid_list[i + 1][j - 1]:
                        neighbor_counter = neighbor_counter + 1
                    if current_grid.grid_list[i][j - 1]:
                        neighbor_counter = neighbor_counter + 1
            elif i == current_grid.grid_size - 1:
                if current_grid.grid_list[i - 1][j]:
                    neighbor_counter = neighbor_counter + 1
                if j == 0:
                    if current_grid.grid_list[i - 1][j + 1]:
                        neighbor_counter = neighbor_counter + 1
                    if current_grid.grid_list[i][j + 1]:
                        neighbor_counter = neighbor_counter + 1
                elif j == current_grid.grid_size - 1:
                    if current_grid.grid_list[i - 1][j - 1]:
                        neighbor_counter = neighbor_counter + 1
                    if current_grid.grid_list[i][j - 1]:
                        neighbor_counter = neighbor_counter + 1
                else:
                    if current_grid.grid_list[i - 1][j + 1]:
                        neighbor_counter = neighbor_counter + 1
                    if current_grid.grid_list[i][j + 1]:
                        neighbor_counter = neighbor_counter + 1
                    if current_grid.grid_list[i - 1][j - 1]:
                        neighbor_counter = neighbor_counter + 1
                    if current_grid.grid_list[i][j - 1]:
                        neighbor_counter = neighbor_counter + 1
            else:
                if current_grid.grid_list[i + 1][j]:
                    neighbor_counter = neighbor_counter + 1
                if current_grid.grid_list[i - 1][j]:
                    neighbor_counter = neighbor_counter + 1
                if j == 0:
                    if current_grid.grid_list[i - 1][j + 1]:
                        neighbor_counter = neighbor_counter + 1
                    if current_grid.grid_list[i][j + 1]:
                        neighbor_counter = neighbor_counter + 1
                    if current_grid.grid_list[i + 1][j + 1]:
                        neighbor_counter = neighbor_counter + 1
                elif j == current_grid.grid_size - 1:
                    if current_grid.grid_list[i - 1][j - 1]:
                        neighbor_counter = neighbor_counter + 1
                    if current_grid.grid_list[i][j - 1]:
                        neighbor_counter = neighbor_counter + 1
                    if current_grid.grid_list[i + 1][j - 1]:
                        neighbor_counter = neighbor_counter + 1
                else:
                    if current_grid.grid_list[i - 1][j - 1]:
                        neighbor_counter = neighbor_counter + 1
                    if current_grid.grid_list[i][j - 1]:
                        neighbor_counter = neighbor_counter + 1
                    if current_grid.grid_list[i + 1][j - 1]:
                        neighbor_counter = neighbor_counter + 1
                    if current_grid.grid_list[i - 1][j + 1]:
                        neighbor_counter = neighbor_counter + 1
                    if current_grid.grid_list[i][j + 1]:
                        neighbor_counter = neighbor_counter + 1
                    if current_grid.grid_list[i + 1][j + 1]:
                        neighbor_counter = neighbor_counter + 1

            if current_grid.grid_list[i][j] == 0:
                if neighbor_counter == 3:
                    to_be_filled_cord.append([i, j])
            elif current_grid.grid_list[i][j] == 1:
                if neighbor_counter < 2:
                    to_be_filled_cord.append([i, j])
                elif neighbor_counter > 3:
                    to_be_filled_cord.append([i, j])

    for x in range(len(to_be_filled_cord)):
        num_1 = to_be_filled_cord[x][0]
        num_2 = to_be_filled_cord[x][1]
        draw_box(-3 - (current_grid.grid_size * current_grid.box / 2) + num_2 * current_grid.box,
                 3 + (current_grid.grid_size * current_grid.box / 2) - num_1 * current_grid.box,
                 True)
    wn.update()


def speed_slowest():
    global sleep_time
    sleep_time = 2


def speed_slow():
    global sleep_time
    sleep_time = 1.5


def speed_normal():
    global sleep_time
    sleep_time = 1


def speed_fast():
    global sleep_time
    sleep_time = 0.5


def speed_fastest():
    global sleep_time
    sleep_time = 0.1


def main():
    set_up()
    draw_board()
    wn.onclick(color_box)
    t.ondrag(color_box)
    wn.onkey(read_file, "f")
    wn.onkey(quit_it, "q")
    wn.onkey(generate_random, "r")
    wn.onkey(start_game, "s")
    wn.onkey(pause_game, "p")
    wn.onkey(next_gen, "Right")
    wn.onkey(speed_fastest, "5")
    wn.onkey(speed_fast, "4")
    wn.onkey(speed_normal, "3")
    wn.onkey(speed_slow, "2")
    wn.onkey(speed_slowest, "1")
    wn.listen()
    tkinter.mainloop()


if __name__ == "__main__":
    main()
