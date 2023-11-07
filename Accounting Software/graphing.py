import matplotlib
import customtkinter

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.figure import Figure

window = customtkinter.CTk()
window.geometry("1280x800")
frame = customtkinter.CTkFrame(window)
frame.place(relwidth=1, relheight=1, relx=0,rely=0)

figure = Figure(figsize=(11, 11), dpi=100)
a = figure.add_subplot(111)
a.plot([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],[0, 10, 45, 30, 70, 50, 100,130, 200, 400, 450])

canvas = FigureCanvasTkAgg(figure, frame)
canvas._tkcanvas.place(relwidth=0.5,relheight=0.5,relx=0.05,rely=0.05)

window.mainloop()