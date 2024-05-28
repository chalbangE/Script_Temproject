import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import random
import Product
import Store
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
from dateutil.relativedelta import relativedelta

W_WIDTH = 1000
W_HEIGHT = 800

product_dic = Product.LoadAllProduct()
store_dic = Store.LoadAllStore()

p_unit_code_dic = Product.LoadUnitDivCode()         # 상품 단위 구분 코드 (병, 캔, 컵, 개...)
p_total_code_dic = Product.LoadTotalDivCode()       # 상품 소분류 코드 (살충제, 세탁세제...)
s_area_code = Store.LoadAreaCode()                  # 업체 업태 코드 (편의점, 백화점...)
s_area_detail_code = Store.LoadAreaDetailCode()     # 업체 지역 코드 (서울, 광주...)


def get_previous_month(month_str, cnt):
    month = int(month_str)
    previous_month = (month - cnt - 1) % 12 + 1
    return f"{previous_month:02d}"

def get_last_friday(date_str):
    input_date = datetime.datetime.strptime(date_str, '%Y%m%d')
    input_weekday = input_date.weekday()
    days_since_friday = (input_weekday - 4) % 7
    if input_weekday == 4:  # 금요일이면
        return input_date.strftime('%Y%m%d')
    last_friday = input_date - datetime.timedelta(days=days_since_friday)
    return last_friday.strftime('%Y%m%d')


def get_weeks_earlier(date_str, cnt):
    input_date = datetime.datetime.strptime(date_str, '%Y%m%d')
    weeks_earlier = input_date - datetime.timedelta(weeks=cnt)
    return weeks_earlier.strftime('%Y%m%d')


def get_one_year_earlier(date_str):
    input_date = datetime.datetime.strptime(date_str, '%Y%m%d')
    try:
        one_year_earlier = input_date.replace(year=input_date.year - 1)
    except ValueError:
        one_year_earlier = input_date.replace(year=input_date.year - 1, day=28)
    return one_year_earlier.strftime('%Y%m%d')


def get_months_earlier(date_str, cnt):
    input_date = datetime.datetime.strptime(date_str, '%Y%m%d')
    months_earlier = input_date - relativedelta(months=cnt)
    return months_earlier.strftime('%Y%m%d')


def print_product_info(goodid):
    print('goodid', product_dic[goodid].goodId)
    print('goodName', product_dic[goodid].goodName)
    print('goodUnitDivCode', product_dic[goodid].goodUnitDivCode)
    print('goodBaseCnt', product_dic[goodid].goodBaseCnt)
    print('goodSmlclsCode', product_dic[goodid].goodSmlclsCode)
    print('detailMean', product_dic[goodid].detailMean)
    print('goodTotalCnt', product_dic[goodid].goodTotalCnt)
    print('goodTotalDivCode', product_dic[goodid].goodTotalDivCode)

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

    def CalAveragePrice(self, goodInspectDay, goodId):
        cnt = 0
        while True:
            result = Product.CalAveragePrice(goodInspectDay, goodId)
            if result != 0:
                return result
            cnt += 1
            goodInspectDay = get_weeks_earlier(goodInspectDay, 1)

    def load_weekly_price_info(self, tab_text):
        tab_dic = {
            "곡물가공품": "030201000",
            "축산물": "030101000",
            "수산물": "030103000",
            "채소류": "030102000",
            "양념•소스류": "030204000",
            "과자•빙과류": "030205000",
            "차•음료•주류": "030206000",
            "위생용품": "030301000"
        }
        table_data = []
        graph_data = []
        product_cnt = 0
        temp = []

        for goodName, product in product_dic.items():
            if int(product.goodSmlclsCode) // 1000 * 1000 == int(tab_dic[tab_text]):
                p_this_week = Product.CalAveragePrice(self.this_week, product.goodId)

                # print(self.this_week, product.goodId)
                if p_this_week == 0:
                    continue
                product_cnt += 1
                if product_cnt == 6:
                    break
                # print_product_info(goodName)

                p_two_weeks_ago = self.CalAveragePrice(self.two_weeks_ago, product.goodId)
                p_a_year_ago = self.CalAveragePrice(self.a_year_ago, product.goodId)

                temp.append(goodName)                                                 # 상품명
                temp.append(product.goodBaseCnt + p_unit_code_dic[product.goodUnitDivCode])   # 상품단위

                temp.append(p_this_week)
                temp.append(p_two_weeks_ago)
                temp.append(p_a_year_ago)

                table_data.append(temp.copy())
                # print(table_data)
                temp.clear()

                p_a_month_ago = self.CalAveragePrice(self.a_month_ago, product.goodId)
                p_two_months_ago = self.CalAveragePrice(self.two_months_ago, product.goodId)
                p_three_months_ago = self.CalAveragePrice(self.three_months_ago, product.goodId)
                p_four_months_ago = self.CalAveragePrice(self.four_months_ago, product.goodId)
                p_five_months_ago = self.CalAveragePrice(self.five_months_ago, product.goodId)

                temp.append(p_five_months_ago)
                temp.append(p_four_months_ago)
                temp.append(p_three_months_ago)
                temp.append(p_two_months_ago)
                temp.append(p_a_month_ago)
                temp.append(p_this_week)

                graph_data.append(temp.copy())
                # print(graph_data)
                temp.clear()

        # print({"table": table_data, "graph": graph_data})
        return {"table": table_data, "graph": graph_data}

    def on_tab_change(self, event):
        selected_tab = event.widget.select()
        tab_text = self.notebook.tab(selected_tab, "text")
        data = self.load_weekly_price_info(tab_text)
        # print(tab_text)

        frame = self.notebook.nametowidget(selected_tab)
        for widget in frame.winfo_children():
            widget.destroy()

        # 표 추가
        tree = ttk.Treeview(frame, columns=("상품", "단위", "금주", "2주전", "1년전"), show='headings')
        tree.heading("상품", text="상품")
        tree.heading("단위", text="단위")
        tree.heading("금주", text="금주")
        tree.heading("2주전", text="2주전")
        tree.heading("1년전", text="1년전")
        # print(data["table"])
        for good, unit, this, two, year in data["table"]:
            tree.insert("", "end", values=(good, unit, this, two, year))
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 표의 너비 조정
        tree.column("상품", width=200)  # "Item" 열의 너비 설정
        tree.column("단위", width=100)  # "Value" 열의 너비 설정
        tree.column("금주", width=100)  # "Value" 열의 너비 설정
        tree.column("2주전", width=100)  # "Value" 열의 너비 설정
        tree.column("1년전", width=100)  # "Value" 열의 너비 설정
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 그래프 추가
        fig, ax = plt.subplots()
        print(data["graph"][0])
        ax.plot(data["graph"][0], marker='o')
        ax.set_xticks(range(len(self.labels)))
        ax.set_xticklabels(self.labels, fontproperties="Malgun Gothic")
        ax.set_title('월간 그래프', fontproperties="Malgun Gothic")
        graph_canvas = FigureCanvasTkAgg(fig, master=frame)
        graph_canvas.draw()
        graph_canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def __init__(self):
        window = tk.Tk()
        window.title('오늘 할 일 : 장 보기')

        # self.today = datetime.date.today().strftime('%Y%m%d')
        self.today = '20220805'

        self.this_week = get_last_friday(self.today)
        self.two_weeks_ago = get_weeks_earlier(self.today, 2)
        self.a_year_ago = get_last_friday(get_one_year_earlier(self.today))

        self.a_month_ago = get_last_friday(get_months_earlier(self.today, 1))
        self.two_months_ago = get_last_friday(get_months_earlier(self.today, 2))
        self.three_months_ago = get_last_friday(get_months_earlier(self.today, 3))
        self.four_months_ago = get_last_friday(get_months_earlier(self.today, 4))
        self.five_months_ago = get_last_friday(get_months_earlier(self.today, 5))

        print(self.a_month_ago, self.two_months_ago, self.three_months_ago, self.four_months_ago, self.five_months_ago)

        self.labels = [get_previous_month(self.today[4]+self.today[5], 5)+"월",
                       get_previous_month(self.today[4]+self.today[5], 4)+"월",
                       get_previous_month(self.today[4]+self.today[5], 3)+"월",
                       get_previous_month(self.today[4]+self.today[5], 2)+"월",
                       get_previous_month(self.today[4]+self.today[5], 1)+"월",
                       "현재"]

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
        self.category_contents = {
            "곡물가공품": {"table": [["A", 1], ["B", 2], ["C", 3]], "graph": [1, 2, 3], "labels": self.labels},
            "축산물": {"table": [], "graph": [], "labels": self.labels},
            "수산물": {"table": [], "graph": [], "labels": self.labels},
            "채소류": {"table": [], "graph": [], "labels": self.labels},
            "양념•소스류": {"table": [], "graph": [], "labels": self.labels},
            "과자•빙과류": {"table": [], "graph": [], "labels": self.labels},
            "차•음료•주류": {"table": [], "graph": [], "labels": self.labels},
            "위생용품": {"table": [], "graph": [], "labels": self.labels}
        }

        # 스타일 설정
        style = ttk.Style()
        style.configure("TNotebook.Tab", borderwidth=1, padding=[5, 2])
        style.map("TNotebook.Tab",
                  foreground=[("selected", "#000080"), ("!selected", "#808080")],  # 폰트 색상을 남색으로 설정, # 선택되지 않은 탭의 글꼴 색상을 회색으로 설정
                  font=[("selected", Basic_font), ("!selected", Basic_font)])

        style.configure("Treeview", rowheight=40)  # 행 높이 설정

        # 노트북 위젯 생성
        self.notebook = ttk.Notebook(window)
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

        # 각 카테고리에 대한 탭과 프레임 생성
        for category, data in self.category_contents.items():
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=category)

        # Notebook을 Canvas에 추가
        self.canvas.create_window(W_WIDTH // 2, 250, window=self.notebook, width=W_WIDTH - 40, height=W_HEIGHT // 3)

        # 창 닫기 이벤트 처리
        window.protocol("WM_DELETE_WINDOW", self.on_closing)

        ### 메인 루프 ###
        self.window = window
        window.mainloop()


if __name__ == "__main__":
    app = MainGUI()