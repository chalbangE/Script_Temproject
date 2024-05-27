import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import random
import Product
import Store
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

        self.label = tk.Label(window)
        self.label.place(x=x, y=y, width=width, height=height)  # 원하는 위치와 크기로 설정

        self.animation_id = None

    def update_label(self, frame):
        gif_frame = self.gif_frames[frame]
        self.label.config(image=gif_frame)
        self.label.image = gif_frame

    def animate(self, window, current_frame=0):
        frame_count = len(self.gif_frames)
        self.update_label(current_frame)
        current_frame = (current_frame + 1) % frame_count
        self.animation_id = window.after(100, lambda: self.animate(window, current_frame))

    def stop_animation(self, window):
        if self.animation_id is not None:
            window.after_cancel(self.animation_id)
            self.animation_id = None


class MainGUI:
    def on_closing(self):
        self.gif_instance.stop_animation(self.window)
        self.window.destroy()

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

    def search(self):
        query = self.text.get("1.0", "end-1c")  # 첫 번째 줄의 첫 번째 문자부터 마지막 줄의 마지막 문자까지의 텍스트 가져오기
        print("검색어:", query)


    def __init__(self):
        window = tk.Tk()
        window.title('오늘 할 일 : 장 보기')

        ### 타이틀 ###
        Title_font = tkFont.Font(family="와구리체 TTF", size=30)
        Subtitle_font = tkFont.Font(family="UhBee Seulvely", size=15)
        Basic_font = tkFont.Font(family="SUITE", size=12)

        try:
            with open('list.txt', 'r', encoding='utf-8') as fp:
                self.words = fp.read().split()
        except UnicodeDecodeError as e:
            print(f"파일 못 열었다... {e}")

        self.canvas = tk.Canvas(window, bg='white', width=W_WIDTH, height=W_HEIGHT)
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

        ### 상품 검색창 ###
        self.text = tk.Text(window, width=25, height=6)  # 너비와 높이를 지정할 수 있음
        self.text.place(x=W_WIDTH - 250, y=15)

        search_button_image = Image.open("img/search_cat.jpg")
        search_button_image = ImageTk.PhotoImage(search_button_image)
        search_button = tk.Button(window, image=search_button_image, command=self.search)
        search_button.place(x=W_WIDTH - 100, y=15)


        ### 테마 ###
        self.show_mod = 'white'

        # 다크모드 이미지 로드
        self.dark_mod_on_image = Image.open("img/white_cat.jpg")
        self.dark_mod_off_image = Image.open("img/black_cat.jpg")

        # 이미지를 Tkinter로 변환
        self.dark_mod_on_image = ImageTk.PhotoImage(self.dark_mod_on_image)
        self.dark_mod_off_image = ImageTk.PhotoImage(self.dark_mod_off_image)

        # 버튼 생성 및 이미지 설정
        self.dark_mod_button = tk.Button(window, image=self.dark_mod_off_image, command=self.Dark_mod_button_click)
        self.dark_mod_button.place(x=180, y=15)

        self.gif_instance = GIF(window, x=20, y=20, width=147, height=80)
        self.gif_instance.animate(window)

        ### 주간 가격정보 ###
        category_contents = {
            "곡물가공품": {"table": [["A", 1], ["B", 2], ["C", 3]], "graph": [1, 2, 3]},
            "축산물": {"table": [["X", 10], ["Y", 20], ["Z", 30]], "graph": [10, 20, 30]},
            "수산물": {"table": [["M", 100], ["N", 200], ["O", 300]], "graph": [100, 200, 300]},
            "채소류": {"table": [["I", 5], ["J", 15], ["K", 25]], "graph": [5, 15, 25]},
            "양념•소스류": {"table": [["M", 100], ["N", 200], ["O", 300]], "graph": [100, 200, 300]},
            "과자•빙과류": {"table": [["M", 100], ["N", 200], ["O", 300]], "graph": [100, 200, 300]},
            "차•음료•주류": {"table": [["M", 100], ["N", 200], ["O", 300]], "graph": [100, 200, 300]},
            "위생용품": {"table": [["M", 100], ["N", 200], ["O", 300]], "graph": [100, 200, 300]}
        }
        # 스타일 설정
        style = ttk.Style()
        style.configure("TNotebook.Tab", borderwidth=1, padding=[5, 2])
        style.map("TNotebook.Tab",
                  background=[("selected", "#f0f0f0")],
                  foreground=[("selected", "#000080"), ("!selected", "#808080")],  # 폰트 색상을 남색으로 설정, # 선택되지 않은 탭의 글꼴 색상을 회색으로 설정
                  font=[("selected", Basic_font), ("!selected", Basic_font)])

        # 노트북 위젯 생성
        notebook = ttk.Notebook(window)

        # 각 카테고리에 대한 탭과 프레임 생성
        for category, data in category_contents.items():
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=category)

            # 표 추가
            tree = ttk.Treeview(frame, columns=("Item", "Value"), show='headings')
            tree.heading("Item", text="Item")
            tree.heading("Value", text="Value")
            for item, value in data["table"]:
                tree.insert("", "end", values=(item, value))
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # 그래프 추가
            fig, ax = plt.subplots()
            ax.plot(data["graph"], marker='o')
            graph_canvas = FigureCanvasTkAgg(fig, master=frame)
            graph_canvas.draw()
            graph_canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Notebook을 Canvas에 추가
        self.canvas.create_window(W_WIDTH // 2, 250, window=notebook, width=W_WIDTH, height=W_HEIGHT // 3)

        # 창 닫기 이벤트 처리
        window.protocol("WM_DELETE_WINDOW", self.on_closing)

        ### 메인 루프 ###
        self.window = window
        window.mainloop()


if __name__ == "__main__":
    app = MainGUI()