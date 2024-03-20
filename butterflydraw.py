import json
import math
import os
import queue
import threading

from dataqueue import data_queue
import tkinter as tk
from tkinter import font

# from hudinjector import TestHUD

blue = "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"
purple = "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"

RED = 0
BLUE = 1
FULL = 0
NOTFULL = 1
X = 0
Y = 1


class ButterflyDraw:
    angle = math.pi / 3
    point1 = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]

    center = None
    radius = None

    colors = [['', ''], ['', '']]

    def init_FlowerDraw(self, center, radius):
        self.center = center
        self.radius = radius
        for i in range(6):
            the_angle = i * self.angle
            self.point1[i][X] = center[X] + radius * math.cos(the_angle)
            self.point1[i][Y] = center[Y] + radius * math.sin(the_angle)

        self.colors[RED][FULL] = '#f88dff'
        self.colors[RED][NOTFULL] = '#a75fff'
        self.colors[BLUE][FULL] = '#6aaffc'
        self.colors[BLUE][NOTFULL] = '#0277fa'

        self.blue = tk.PhotoImage(data=blue)
        self.purple = tk.PhotoImage(data=purple)

    def draw_circle(self, canvas, color_flag, full_flag):
        canvas.create_oval(self.center[0] - 8, self.center[1] - 8, self.center[0] + 8, self.center[1] + 8,
                           fill=self.colors[color_flag][full_flag])

    def draw_flower(self, canvas, petal_num, color_flag, full_flag):
        for i in range(petal_num):
            x1 = self.point1[i][X]
            y1 = self.point1[i][Y]

            canvas.create_image(x1,y1,image = self.blue if color_flag == BLUE else self.purple)

def update_gui_from_queue(root, canvas, butterfly_draw: ButterflyDraw, last_data):
    try:
        # 非阻塞地从队列中获取数据
        data = data_queue.get_nowait()
        # data = 6

        if last_data != data:
            last_data = data
            # 使用队列中的数据更新GUI
            num = data % 10
            color_flag = RED if data >= 10 else BLUE
            full_flag = FULL if num == 6 else NOTFULL

            canvas.delete("all")
            butterfly_draw.draw_flower(canvas, num, color_flag, full_flag)
            butterfly_draw.draw_circle(canvas, color_flag, full_flag)

        # 清除队列中的数据标记为已处理
        data_queue.task_done()
    except queue.Empty:
        # 队列为空，没有新数据
        pass
    # 100毫秒后再次调用自身进行更新
    root.after(100, update_gui_from_queue, root, canvas, butterfly_draw, last_data)


def draw_overlay():
    root = tk.Tk()
    root.title("Namarya Butterfly HUD")

    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()

    f = open(os.path.split(os.path.realpath(__file__))[0] + '\\config.json', 'r')
    res = json.loads(f.read())
    f.close()

    size_rate = res["size"]
    radius_rate = res["radius"]

    size_base = 0.2775 * size_rate
    canvas_size = size_base * screenheight
    # size_base = 0.5

    # 创建一个Canvas用于绘制花瓣
    canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg='black',
                       highlightthickness=0)
    canvas.pack()



    # 设置花瓣的中心点和半径
    center = (canvas_size / 2, canvas_size / 2)
    radius = canvas_size / 4 * radius_rate
    
    butterfly_draw = ButterflyDraw()
    butterfly_draw.init_FlowerDraw(center, radius)

    # 设置窗口的默认位置
    x = int(screenwidth * 0.55)  # 设置窗口左上角的X坐标为屏幕宽度的55%
    y = int(screenheight * 0.60)  # 设置窗口左上角的Y坐标为屏幕高度的60%
    root.geometry(f"+{x}+{y}")

    def on_drag(event):
        # 计算鼠标移动的偏移量
        offset_x = event.x_root - root._drag_start_x
        offset_y = event.y_root - root._drag_start_y
        # 移动窗口
        root.geometry(f'+{root._start_x + offset_x}+{root._start_y + offset_y}')

    def start_drag(event):
        # 记录拖动开始时鼠标的位置和窗口的位置
        root._drag_start_x = event.x_root
        root._drag_start_y = event.y_root
        root._start_x = root.winfo_x()
        root._start_y = root.winfo_y()

    root._drag_start_x = None
    root._drag_start_y = None
    root._start_x = None
    root._start_y = None
    canvas.bind('<Button-1>', start_drag)  # 鼠标左键按下事件
    canvas.bind('<B1-Motion>', on_drag)  # 鼠标拖动事件（左键按下的情况下移动）

    root.overrideredirect(True)
    # screenwidth = root.winfo_screenwidth() // 2 + 300
    # screenheight = root.winfo_screenheight() // 4 * 3
    # root.geometry(f"+{screenwidth}+{screenheight}")
    root.lift()
    root.wm_attributes("-topmost", True)
    root.wm_attributes("-transparentcolor", "black")

    # 启动周期性的GUI更新函数
    root.after(100, update_gui_from_queue, root, canvas, butterfly_draw, None)

    # 启动tkinter mainloop
    root.mainloop()


# draw_overlay()
