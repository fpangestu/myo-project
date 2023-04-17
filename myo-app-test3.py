import numpy as np

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.gridlayout import GridLayout
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import random
import threading
import time
from kivy.clock import Clock

x1 = np.arange(10)
y1 = [random.uniform(-100, 100) for i in range(len(x1))]

def data():
    data.a = None
    data.fig = None

data()

plt.plot(x,y)
plt.ylabel("Y axis")
plt.xlabel("X axis")

def gen_rand_int(intput):
    return random.randint(20,50)

data.fig = Figure(figsize=(5,4), dpi=100)
data.a = data.fig.add_subplot()
data.a.plot(x)
run_thread = True

def animate():
    while run_thread:
        data.a.clear()
        n_list = list(map(gen_rand_int, [0]*5))
        data.a.plot(n_list)
        time.sleep(0.1)
        # print("animate")

calcThread = threading.Thread(target=animate)
calcThread.start()

class View(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        box = self.ids.box0
        box.add_widget(FigureCanvasKivyAgg(fig1))
        box = self.ids.box1
        box.add_widget(FigureCanvasKivyAgg(fig1))
        box = self.ids.box2
        box.add_widget(FigureCanvasKivyAgg(fig1))
        box = self.ids.box3
        box.add_widget(FigureCanvasKivyAgg(fig1))
        box = self.ids.box4
        box.add_widget(FigureCanvasKivyAgg(fig1))
        box = self.ids.box5
        box.add_widget(FigureCanvasKivyAgg(fig1))
        box = self.ids.box6
        box.add_widget(FigureCanvasKivyAgg(fig1))
        box = self.ids.box7
        box.add_widget(FigureCanvasKivyAgg(fig1))
        box = self.ids.boxgyro
        box.add_widget(FigureCanvasKivyAgg(fig2))
        box = self.ids.boxacc
        box.add_widget(FigureCanvasKivyAgg(fig3))
        box = self.ids.boxori
        box.add_widget(FigureCanvasKivyAgg(fig4))
        
        
        Clock.schedule_interval(self.timer, 0.005)

    
    def timer(self, dt):
        canvas = FigureCanvasKivyAgg(data.fig)
        self.box.clear_widgets()
        self.box.add_widget(canvas)
        print("timer")


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        Builder.load_file('view.kv')
        return View()
    
    
try:
    MainApp().run()
except:
    run_thread = False
    print("Keyboard interrupt")