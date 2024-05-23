from tkinter import *

class MainGUI:
    def __init__(self):
        window = Tk()
        window.title('오늘 할 일 : 장 보기')
        self.canvas = Canvas(window,bg='white',width=1000,height=800)
        self.canvas.pack()

        window.mainloop()

MainGUI()