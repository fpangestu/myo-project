from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.gridlayout import GridLayout
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import random
import numpy as np

x1 = np.arange(200)
y1 = [random.uniform(-100, 100) for i in range(len(x1))]
fig1, ax1 = plt.subplots()
ax1.plot(x1, y1)
for line_y in [-100, 0, 100]:
    ax1.axhline(line_y, color='gray', linestyle='--', alpha=0.5)
ax1.set_ylim(-150, 150)

x2 = np.arange(200)
y2 = [random.uniform(-500, 500) for i in range(len(x2))]
fig2, ax2 = plt.subplots()
for line_y in [-500, 0, 500]:
    ax2.axhline(line_y, color='gray', linestyle='--', alpha=0.5)
ax2.plot(x2, y2)
ax2.set_ylim(-750, 750)

x3 = np.arange(200)
y3 = [random.uniform(-5, 5) for i in range(len(x3))]
fig3, ax3 = plt.subplots()
for line_y in [-2.5, 0, 2.5]:
    ax3.axhline(line_y, color='gray', linestyle='--', alpha=0.5)
ax3.plot(x3, y3)
ax3.set_ylim(-5, 5)

x4 = np.arange(200)
y4 = [random.uniform(-1, 1) for i in range(len(x4))]
fig4, ax4 = plt.subplots()
for line_y in [-0.5, 0, 0.5]:
    ax4.axhline(line_y, color='gray', linestyle='--', alpha=0.5)
ax4.plot(x4, y4)
ax4.set_ylim(-1, 1)

class View(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        box = self.ids.box0
        box.add_widget(FigureCanvasKivyAgg(fig1))
        box = self.ids.box1
        box.add_widget(FigureCanvasKivyAgg(fig2))
        box = self.ids.box2
        box.add_widget(FigureCanvasKivyAgg(fig3))
        box = self.ids.box3
        box.add_widget(FigureCanvasKivyAgg(fig4))
        box = self.ids.box4
        box.add_widget(FigureCanvasKivyAgg(fig1))
        box = self.ids.box5
        box.add_widget(FigureCanvasKivyAgg(fig1))
        box = self.ids.box6
        box.add_widget(FigureCanvasKivyAgg(fig1))
        box = self.ids.box7
        box.add_widget(FigureCanvasKivyAgg(fig1))

        # self.ids.name_label.text = f'Hello {name}!'

        # box = self.ids.boxgyro
        # box.add_widget(FigureCanvasKivyAgg(fig2))
        # box = self.ids.boxacc
        # box.add_widget(FigureCanvasKivyAgg(fig3))
        # box = self.ids.boxori
        # box.add_widget(FigureCanvasKivyAgg(fig4))


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        Builder.load_file("view.kv")
        return View()

MainApp().run()
