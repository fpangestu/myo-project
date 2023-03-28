import tkinter as tk
import tkinter.ttk as ttk           # themed widgets
from PIL import ImageTk, Image

window = tk.Tk()

frame1 = tk.Frame(
    master = window,
    relief = tk.RAISED,
    borderwidth = 1
)

frame2 = tk.Frame(
    master = window,
    relief = tk.RAISED,
    borderwidth = 1
)

frame1.grid(row=1, column=1, padx=5, pady=5)
image = Image.open("img/myo.png")
tk_image = ImageTk.PhotoImage(image)
label = tk.Label(window, image=tk_image)

frame2.grid(row=1, column=2, padx=5, pady=5)
label2 = tk.Label(master=frame2, text=f"Row {1}\nColumn {2}")


label.pack()
label2.pack()

window.mainloop()