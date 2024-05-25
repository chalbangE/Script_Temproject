from tkinter import *
import tkinter.font as tkFont
import random
import Product
import Store

W_WIDTH = 1000
W_HEIGHT = 800

product_dic = Product.LoadAllProduct()
store_dic = Store.LoadAllStore()

p_unit_code_dic = Product.LoadUnitDivCode()         # 상품 단위 구분 코드 (병, 캔, 컵, 개...)
p_total_code_dic = Product.LoadTotalDivCode()       # 상품 소분류 코드 (살충제, 세탁세제...)
s_area_code = Store.LoadAreaCode()                  # 업체 업태 코드 (편의점, 백화점...)
s_area_detail_code = Store.LoadAreaDetailCode()     # 업체 지역 코드 (서울, 광주...)


class MainGUI:
    def __init__(self):
        window = Tk()
        window.title('오늘 할 일 : 장 보기')

        Title_font = tkFont.Font(family="와구리체 TTF", size=25)
        Subtitle_font = tkFont.Font(family="UhBee Seulvely", size=15)

        try:
            with open('list.txt', 'r', encoding='utf-8') as fp:
                self.words = fp.read().split()
        except UnicodeDecodeError as e:
            print(f"파일 못 열었다... {e}")

        self.canvas = Canvas(window,bg='white',width=W_WIDTH,height=W_HEIGHT)
        self.canvas.pack()
        self.canvas.create_line(280, 80, W_WIDTH - 280, 80, tags="shape")
        self.canvas.create_text(W_WIDTH / 2, 25, text='오늘 할 일 : 장 보기', font=Title_font)

        if random.randint(0, 1) == 0:
            self.canvas.create_text(W_WIDTH / 2, 60, text='엄마가 시킨 심부름 : ' + self.words[random.randint(0, len(self.words) - 1)]
                                                          + ', '+ self.words[random.randint(0, len(self.words) - 1)], font=Subtitle_font)
        else:
            self.canvas.create_text(W_WIDTH / 2, 60, text='엄마가 시킨 심부름 : ' + self.words[random.randint(0, len(self.words) - 1)]
                                                          + ', '+ self.words[random.randint(0, len(self.words) - 1)] + ', '+ self.words[random.randint(0, len(self.words) - 1)], font=Subtitle_font)

        window.mainloop()

MainGUI()