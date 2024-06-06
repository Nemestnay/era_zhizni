import random
from tkinter import *
from tkinter import messagebox
import time

tk = Tk()
app_running = True


# задание размеров окна с учетом меню, количества клеток
size_canvas_x = 600
size_canvas_y = 600
s_x = s_y =15 # размер игрового поля
step_x = size_canvas_x // s_x  # шаг по горизонтали
step_y = size_canvas_y // s_y  # шаг по вертикали
size_canvas_x = step_x * s_x
size_canvas_y = step_y * s_y
menu_x = 280
list_ids = []

#создание таблицы отображающей текущее положение живых клеток(1)  и мертвых(0)
tekushai_tablica = [[0 for i in range(s_y)] for j in range(s_x)]
stop = False


#функция выхода из игры
def on_closing():
    global app_running
    if messagebox.askokcancel("Выход из игры", "Хотите выйти из игры?"):
        app_running = False
        tk.destroy()


# описание и созднаие начального окна
tk.protocol("WM_DELETE_WINDOW", on_closing)
tk.title("Эра жизни")
tk.resizable(0, 0)
#tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=size_canvas_x + menu_x, height=size_canvas_y, bd=0, highlightthickness=0)
canvas.create_rectangle(0, 0, size_canvas_x, size_canvas_y, fill="white")
canvas.pack()
tk.update()


#клетки поля
def draw_table():
    for i in range(0, s_x + 1):
        canvas.create_line(step_x * i, 0, step_x * i, size_canvas_y)
    for i in range(0, s_y + 1):
        canvas.create_line(0, step_y * i, size_canvas_x, step_y * i)


draw_table()


#"обнуляет" таблицу текущих значений
def button_begin_again():
    global list_ids
    for el in list_ids:
        canvas.delete(el)
    list_ids = []
    global tekushai_tablica
    tekushai_tablica = [[0 for i in range(s_y)] for j in range(s_x)]


#одна итерация игры
def button_one_step():
    global tekushai_tablica
    #создание и заполнение массива, хранящего количество живых соседей у каждой клетки
    tablica_count = [[0 for i in range(s_y)] for j in range(s_x)]
    for j in range(s_x):
        for i in range(s_y):
            if (j > 0) and (i > 0) and (j < s_x - 1) and (i < s_y - 1):
                tablica_count[j][i] += tekushai_tablica[j-1][i-1] + tekushai_tablica[j-1][i] + tekushai_tablica[j - 1][i+1] + \
                                       tekushai_tablica[j][i-1] + tekushai_tablica[j][i+1] + tekushai_tablica[j+1][i-1] + \
                                       tekushai_tablica[j+1][i] + tekushai_tablica[j+1][i+1]
            if (j == 0) and (i > 0) and (i < s_y - 1):
                tablica_count[j][i] += tekushai_tablica[j][i-1] + tekushai_tablica[j][i+1] + tekushai_tablica[j+1][i-1] + \
                                       tekushai_tablica[j+1][i] + tekushai_tablica[j+1][i+1]
            if (j > 0) and (i == 0) and (j < s_x - 1):
                tablica_count[j][i] += tekushai_tablica[j-1][i] + tekushai_tablica[j - 1][i+1] + tekushai_tablica[j][i+1] + \
                                       tekushai_tablica[j+1][i] + tekushai_tablica[j+1][i+1]
            if (i > 0) and (j == s_x - 1) and (i < s_y - 1):
                tablica_count[j][i] += tekushai_tablica[j-1][i-1] + tekushai_tablica[j-1][i] + tekushai_tablica[j - 1][i+1] + \
                                       tekushai_tablica[j][i-1] + tekushai_tablica[j][i+1]
            if (j > 0) and (j < s_x - 1) and (i == s_y - 1):
                tablica_count[j][i] += tekushai_tablica[j-1][i-1] + tekushai_tablica[j-1][i] + \
                                       tekushai_tablica[j][i-1] + tekushai_tablica[j+1][i-1] + \
                                       tekushai_tablica[j+1][i]
            if (j == s_x - 1) and (i == s_y - 1):
                tablica_count[j][i] += tekushai_tablica[j-1][i-1] + tekushai_tablica[j-1][i] + tekushai_tablica[j][i-1]
            if (i == 0) and (j == s_x - 1):
                tablica_count[j][i] += tekushai_tablica[j-1][i] + tekushai_tablica[j - 1][i+1] + tekushai_tablica[j][i+1]
            if (j == 0) and (i == s_y - 1):
                tablica_count[j][i] += tekushai_tablica[j][i-1] + tekushai_tablica[j+1][i-1] + tekushai_tablica[j+1][i]
            if (j == 0) and (i == 0):
                tablica_count[j][i] += tekushai_tablica[j][i+1] + tekushai_tablica[j+1][i] + tekushai_tablica[j+1][i+1]
    sledushai_tablica = tekushai_tablica
    nalichie_razlichiy = False

    for j in range(s_x):
        for i in range(s_y):
            if tekushai_tablica[j][i] == 0 and tablica_count[j][i] == 3:
                sledushai_tablica[j][i] = 1
                nalichie_razlichiy = True
            if tekushai_tablica[j][i] == 1 and (tablica_count[j][i] < 2 or tablica_count[j][i] > 3):
                sledushai_tablica[j][i] = 0
                nalichie_razlichiy = True
    global stop
    if not nalichie_razlichiy:
        stop = True
    tekushai_tablica = sledushai_tablica
    global list_ids
    for el in list_ids:
        canvas.delete(el)
    list_ids = []
    for j in range(s_x):
        for i in range(s_y):
            if tekushai_tablica[j][i] == 1:
                draw_point_to_black(j, i)


#запускает 100 итерации игры и имеет возможность завершить их досрочно
def button_to_start():
    global stop
    stop = False
    iter = 100
    while not stop and iter != 0:
        button_one_step()
        time.sleep(0.1)
        tk.update_idletasks()
        iter -= 1


b0 = Button(tk, text="Начать заново!", command=button_begin_again)
b0.place(x=size_canvas_x + 20, y=30)

b1 = Button(tk, text="Один шаг", command=button_one_step)
b1.place(x=size_canvas_x+20, y=70)

b2 = Button(tk, text="Старт!", command=button_to_start)
b2.place(x=size_canvas_x+20, y=110)


#заливка клетки рандомным цветом
def draw_point_to_random(x, y):
    massivchik = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
    str = "#"
    for i in range(6):
        str += massivchik[random.randint(0, 15)]
    id1 = canvas.create_rectangle(x * step_x, y * step_y, x * step_x + step_x, y * step_y + step_y, fill=str)
    list_ids.append(id1)


#заливка клетки черным цветом
def draw_point_to_black(x, y):
    id1 = canvas.create_rectangle(x * step_x, y * step_y, x * step_x + step_x, y * step_y + step_y, fill="black")
    list_ids.append(id1)


#описание нажатий мышки
def add_to_all(event):
    _type = 0  #ЛКМ
    if event.num == 3:
        _type = 1  #ПКМ
    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()
    ip_x = mouse_x // step_x
    ip_y = mouse_y // step_y
    if ip_x < s_x and ip_y < s_y:
        if tekushai_tablica[ip_x][ip_y] == 0:
            tekushai_tablica[ip_x][ip_y] = 1
            draw_point_to_black(ip_x, ip_y)


canvas.bind_all("<Button-1>", add_to_all)  #ЛКМ
canvas.bind_all("<Button-3>", add_to_all)  #ПКМ


while app_running:
    if app_running:
        tk.update_idletasks()
        tk.update()
    time.sleep(0.005)
