from tkinter import *
import tkinter.font as tkFont
import random
import os

W_WIDTH = 1000
W_HEIGHT = 800

class MainGUI:
    def __init__(self):
        window = Tk()
        window.title('오늘 할 일 : 장 보기')

        Title_font_path = os.path.join("font", "font\woguri.ttf")
        Subtitle_font_path = os.path.join("font", "font\Subtitle.ttf")
        if os.path.exists(Title_font_path):
            window.tk.call("font", "create", "WaguriFont", "-family", "와구리체 TTF", "-size", 20, "-file", Title_font_path)
        if os.path.exists(Subtitle_font_path):
            window.tk.call("font", "create", "SeulvelyFont", "-family", "UhBee Seulvely", "-size", 15, "-file", Subtitle_font_path)

        Title_font = tkFont.Font(family="와구리체 TTF", size=20)
        Subtitle_font = tkFont.Font(family="UhBee Seulvely", size=15)
        # print(tkFont.families())

        try:
            with open('list.txt', 'r', encoding='utf-8') as fp:
                self.words = fp.read().split()
        except UnicodeDecodeError as e:
            print(f"파일 못 열었다... {e}")

        self.canvas = Canvas(window,bg='white',width=W_WIDTH,height=W_HEIGHT)
        self.canvas.pack()
        self.canvas.create_line(280, 80, W_WIDTH - 280, 80, tags="shape")
        self.canvas.create_text(W_WIDTH / 2, 20, text='오늘 할 일 : 장 보기', font=Title_font)

        if random.randint(0, 1) == 0:
            self.canvas.create_text(W_WIDTH / 2, 55, text='엄마가 시킨 심부름 : ' + self.words[random.randint(0, len(self.words) - 1)]
                                                          + ', '+ self.words[random.randint(0, len(self.words) - 1)], font=Subtitle_font)
        else:
            self.canvas.create_text(W_WIDTH / 2, 55, text='엄마가 시킨 심부름 : ' + self.words[random.randint(0, len(self.words) - 1)]
                                                          + ', '+ self.words[random.randint(0, len(self.words) - 1)] + ', '+ self.words[random.randint(0, len(self.words) - 1)], font=Subtitle_font)

        window.mainloop()

MainGUI()