from tkinter import *
import tkinter.font as tkFont
import random
import Product
import Store
from PIL import Image, ImageTk

W_WIDTH = 1000
W_HEIGHT = 800

product_dic = Product.LoadAllProduct()
store_dic = Store.LoadAllStore()

p_unit_code_dic = Product.LoadUnitDivCode()         # 상품 단위 구분 코드 (병, 캔, 컵, 개...)
p_total_code_dic = Product.LoadTotalDivCode()       # 상품 소분류 코드 (살충제, 세탁세제...)
s_area_code = Store.LoadAreaCode()                  # 업체 업태 코드 (편의점, 백화점...)
s_area_detail_code = Store.LoadAreaDetailCode()     # 업체 지역 코드 (서울, 광주...)


class GIF:
    def __init__(self, window, x, y, width, height):
        self.gif = Image.open("gif/cat2.gif")
        self.gif_frames = []

        for frame in range(0, self.gif.n_frames):
            self.gif.seek(frame)
            self.gif_frames.append(ImageTk.PhotoImage(self.gif.copy()))

        self.label = Label(window)
        self.label.place(x=x, y=y, width=width, height=height)  # 원하는 위치와 크기로 설정

    def update_label(self, frame):
        gif_frame = self.gif_frames[frame]
        self.label.config(image=gif_frame)
        self.label.image = gif_frame

    def animate(self, window, current_frame=0):
        frame_count = len(self.gif_frames)
        self.update_label(current_frame)
        current_frame = (current_frame + 1) % frame_count
        window.after(100, lambda: self.animate(window, current_frame))

class MainGUI:
    def Dark_mod_button_click(self):
        if self.show_mod == 'black':
            self.show_mod = 'white'
            self.dark_mod_button['image'] = self.dark_mod_off_image
            self.canvas.itemconfig("subtitle", fill='black')
            self.canvas.itemconfig("title_line", fill='black')
            self.canvas.itemconfig("title", fill='black')
            self.canvas.itemconfig("background", fill='white')
        elif self.show_mod == 'white':
            self.show_mod = 'black'
            self.dark_mod_button['image'] = self.dark_mod_on_image
            self.canvas.itemconfig("subtitle", fill='white')
            self.canvas.itemconfig("title_line", fill='white')
            self.canvas.itemconfig("title", fill='white')
            self.canvas.itemconfig("background", fill='black')

    def __init__(self):
        window = Tk()
        window.title('오늘 할 일 : 장 보기')

        Title_font = tkFont.Font(family="와구리체 TTF", size=30)
        Subtitle_font = tkFont.Font(family="UhBee Seulvely", size=15)

        try:
            with open('list.txt', 'r', encoding='utf-8') as fp:
                self.words = fp.read().split()
        except UnicodeDecodeError as e:
            print(f"파일 못 열었다... {e}")

        self.canvas = Canvas(window, bg='white', width=W_WIDTH, height=W_HEIGHT)
        self.canvas.pack()
        self.canvas.create_rectangle(0, 0, W_WIDTH, W_HEIGHT, tags="background")
        self.canvas.create_line(280, 100, W_WIDTH - 280, 100, tags="title_line")
        self.canvas.create_text(W_WIDTH / 2, 35, tags="title", text='오늘 할 일 : 장 보기', font=Title_font)


        if random.randint(0, 1) == 0:
            self.canvas.create_text(W_WIDTH / 2, 75, tags="subtitle", text='엄마가 시킨 심부름 : ' + self.words[random.randint(0, len(self.words) - 1)]\
                            + ', '+ self.words[random.randint(0, len(self.words) - 1)], font=Subtitle_font)
        else:
            self.canvas.create_text(W_WIDTH / 2, 75, tags="subtitle", text='엄마가 시킨 심부름 : ' + self.words[random.randint(0, len(self.words) - 1)]\
                            + ', '+ self.words[random.randint(0, len(self.words) - 1)] + ', '+ self.words[random.randint(0, len(self.words) - 1)], font=Subtitle_font)

        self.show_mod = 'white'
        # 다크모드 이미지 로드
        self.dark_mod_on_image = Image.open("img/white_cat.jpg")
        self.dark_mod_off_image = Image.open("img/black_cat.jpg")

        # 이미지를 Tkinter로 변환
        self.dark_mod_on_image = ImageTk.PhotoImage(self.dark_mod_on_image)
        self.dark_mod_off_image = ImageTk.PhotoImage(self.dark_mod_off_image)

        # 버튼 생성 및 이미지 설정
        self.dark_mod_button = Button(window, image=self.dark_mod_off_image, command=self.Dark_mod_button_click)
        self.dark_mod_button.place(x=180, y=15)

        gif_instance = GIF(window, x=20, y=20, width=147, height=80)
        gif_instance.animate(window)

        window.mainloop()



MainGUI()