import datetime
import random
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk

import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from dateutil.relativedelta import relativedelta
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkintermapview import TkinterMapView

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import telepot
from telepot.loop import MessageLoop
import time

import Product
import Store

W_WIDTH = 1100
W_HEIGHT = 800

product_dic = Product.LoadAllProduct()
store_dic = Store.LoadAllStore()

p_unit_code_dic = Product.LoadUnitDivCode()  # 상품 단위 구분 코드 (병, 캔, 컵, 개...)
p_total_code_dic = Product.LoadTotalDivCode()  # 상품 소분류 코드 (살충제, 세탁세제...)
s_area_code = Store.LoadAreaCode()  # 업체 업태 코드 (편의점, 백화점...)
s_area_detail_code = Store.LoadAreaDetailCode()  # 업체 지역 코드 (서울, 광주...)


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
            # self.new_canvas.itemconfig("new_canvas", fill='white')
        elif self.show_mod == 'white':
            self.show_mod = 'black'
            self.dark_mod_button['image'] = self.dark_mod_on_image
            self.canvas.itemconfig("subtitle", fill='white')
            self.canvas.itemconfig("title_line", fill='white')
            self.canvas.itemconfig("title", fill='white')
            self.canvas.itemconfig("background", fill='black')
            # self.new_canvas.itemconfig("new_canvas", fill='black')

    def Send_Mail(self):
        query = self.text.get("1.0", "end-1c")  # 첫 번째 줄의 첫 번째 문자부터 마지막 줄의 마지막 문자까지의 텍스트 가져오기

        # Split the query into lines
        lines = query.split('\n')

        # The first line is the recipient's email
        recipient_email = lines[0].strip()

        # The rest of the lines are the email body
        body = '\n'.join(lines[1:]).strip()

        # Example usage
        sender_email = 'yan38829@gmail.com'
        sender_password = 'skjlqxiojfchseke'
        subject = '오늘 할 일 - 장 보기 메모!'

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = subject

        # Add body to email
        message.attach(MIMEText(body, 'plain'))

        try:
            # Connect to the Gmail SMTP server
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()  # Can be omitted

            # Login to the server
            server.login(sender_email, sender_password)

            # Send email
            server.sendmail(sender_email, recipient_email, message.as_string())

            # Quit the server
            server.quit()

            print("Mail 전송 완료! : ", body)
        except Exception as e:
            print(f'Failed to send email : {e}')

    def find_valid_day(self, goodInspectDay):
        while True:
            result = Product.CalAveragePrice(goodInspectDay, '246')
            if result != 0:
                # print(goodInspectDay)
                return goodInspectDay
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

                p_two_weeks_ago = Product.CalAveragePrice(self.two_weeks_ago, product.goodId)
                p_a_year_ago = Product.CalAveragePrice(self.a_year_ago, product.goodId)

                temp.append(goodName)  # 상품명
                temp.append(product.goodBaseCnt + p_unit_code_dic[product.goodUnitDivCode])  # 상품단위

                temp.append(p_this_week)
                temp.append(p_two_weeks_ago)
                temp.append(p_a_year_ago)

                table_data.append(temp.copy())
                # print(table_data)
                temp.clear()

                if len(graph_data) == 0:
                    p_a_month_ago = Product.CalAveragePrice(self.a_month_ago, product.goodId)
                    p_two_months_ago = Product.CalAveragePrice(self.two_months_ago, product.goodId)
                    p_three_months_ago = Product.CalAveragePrice(self.three_months_ago, product.goodId)
                    p_four_months_ago = Product.CalAveragePrice(self.four_months_ago, product.goodId)
                    p_five_months_ago = Product.CalAveragePrice(self.five_months_ago, product.goodId)

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

        frame = self.notebook.nametowidget(selected_tab)
        for widget in frame.winfo_children():
            widget.destroy()

        # 특정 스타일 이름을 사용하여 Treeview 스타일 설정
        style = ttk.Style()
        style.configure("Custom.Treeview", rowheight=40)  # 특정 스타일 이름으로 행 높이 설정

        # 표 추가
        tree = ttk.Treeview(frame, columns=("상품", "단위", "금주", "2주전", "1년전"), show='headings', style="Custom.Treeview")
        tree.heading("상품", text="상품")
        tree.heading("단위", text="단위")
        tree.heading("금주", text="금주")
        tree.heading("2주전", text="2주전")
        tree.heading("1년전", text="1년전")

        for good, unit, this, two, year in data["table"]:
            tree.insert("", "end", values=(good, unit, this, two, year))
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 표의 너비 조정
        tree.column("상품", width=200)
        tree.column("단위", width=100)
        tree.column("금주", width=100)
        tree.column("2주전", width=100)
        tree.column("1년전", width=100)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 그래프 프레임 추가
        self.graph_frame = ttk.Frame(frame)
        self.graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 행 클릭 이벤트 바인딩
        tree.bind("<ButtonRelease-1>", self.on_row_click)

        # 첫 번째 행 선택하여 그래프 생성
        if tree.get_children():
            first_item = tree.get_children()[0]
            item_values = tree.item(first_item, "values")
            product_name = item_values[0]
            print(f"First product: {product_name}")

            product = product_dic[product_name]
            self.create_graph(product.goodId)

    def on_row_click(self, event):
        selected_item = event.widget.selection()
        if selected_item:
            item_values = event.widget.item(selected_item[0], "values")
            product_name = item_values[0]
            print(f"Selected product: {product_name}")

            product = product_dic[product_name]
            self.create_graph(product.goodId)

    def create_graph(self, goodId):
        # 기존 figure 닫기
        if hasattr(self, 'fig'):
            plt.close(self.fig)

        p_this_week = Product.CalAveragePrice(self.this_week, goodId)
        p_a_month_ago = Product.CalAveragePrice(self.a_month_ago, goodId)
        p_two_months_ago = Product.CalAveragePrice(self.two_months_ago, goodId)
        p_three_months_ago = Product.CalAveragePrice(self.three_months_ago, goodId)
        p_four_months_ago = Product.CalAveragePrice(self.four_months_ago, goodId)
        p_five_months_ago = Product.CalAveragePrice(self.five_months_ago, goodId)

        self.graph_data = [p_five_months_ago, p_four_months_ago, p_three_months_ago, p_two_months_ago, p_a_month_ago,
                           p_this_week]

        # 기존 그래프 위젯 제거
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        # 새 그래프 생성
        self.fig, self.ax = plt.subplots(figsize=(10, 6))  # 그래프 크기 설정
        self.ax.plot(self.graph_data, marker='o')
        self.ax.set_xticks(range(len(self.labels)))
        self.ax.set_xticklabels(self.labels, fontproperties="Malgun Gothic")
        self.ax.set_title('월간 그래프', fontproperties="Malgun Gothic")
        self.fig.subplots_adjust(left=0.15)
        self.graph_canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.graph_canvas.draw()
        self.graph_canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def search_location(self, event=None):
        if not self.search_in_progress:
            self.search_in_progress = True

            address = self.map_entry.get("1.0", "end-1c")
            self.search_marker = self.map_widget.set_address(address, marker=True)
            if self.search_marker is False:
                # address was invalid (return value is False)
                self.search_marker = None
            self.search_in_progress = False

    def update_item_local(self, event):
        selected_category = self.category_combobox_local.get()
        selected_key = self.category_map_local.get(selected_category)

        if selected_key:
            new_items = {v: k for k, v in p_total_code_dic.items() if
                         int(k) // 1000 == int(selected_key) // 1000 and int(k) % 1000 != 0}
            self.items_map_local = new_items
            self.item_combobox_local['values'] = list(new_items.keys())
            self.item_combobox_local.set("품목 선택")
            self.product_combobox_local.set("상품 선택")
            self.product_combobox_local['values'] = []

    def update_product_local(self, event):
        selected_item = self.item_combobox_local.get()
        selected_key = self.items_map_local.get(selected_item)

        if selected_key:
            new_products = {product.goodName: product.goodId for product in product_dic.values() if
                            product.goodSmlclsCode == selected_key}
            self.products_map_local = new_products
            self.product_combobox_local['values'] = list(new_products.keys())
            self.product_combobox_local.set("상품 선택")

    def update_items_goods(self, event):
        selected_category = self.category_combobox_goods.get()
        selected_key = self.category_map_local.get(selected_category)

        if selected_key:
            new_items = {v: k for k, v in p_total_code_dic.items() if
                         int(k) // 1000 == int(selected_key) // 1000 and int(k) % 1000 != 0}
            item_values = list(new_items.keys())
            self.item_map_goods = new_items
            self.item_combobox_goods['values'] = item_values
            self.item_combobox_goods.set("품목 선택")
            self.product_combobox_goods.set("상품 선택")
            self.product_combobox_goods['values'] = []
        else:
            self.item_combobox_goods.set("품목 선택")
            self.product_combobox_goods.set("상품 선택")
            self.item_combobox_goods['values'] = []
            self.product_combobox_goods['values'] = []

    def update_products_goods(self, event=None):
        selected_item = self.item_combobox_goods.get()
        selected_key = self.item_map_goods.get(selected_item)

        if selected_key:
            new_products = {product.goodName: product.goodId for product in product_dic.values() if
                            product.goodSmlclsCode == selected_key}
            product_values = list(new_products.keys())
            self.product_map_goods = new_products
            self.product_combobox_goods['values'] = product_values
            self.product_combobox_goods.set("상품 선택")
        else:
            self.product_combobox_goods.set("상품 선택")
            self.product_combobox_goods['values'] = []

    def update_stores_goods(self, event=None):
        selected_area = self.area_combobox_goods.get()
        if selected_area == "전체":
            self.store_combobox_goods['values'] = ["전체"]
            self.store_combobox_goods.set("전체")
            return

        selected_area_code = self.area_map_local.get(selected_area)

        selected_entp_types = [entp for entp, var in self.entp_vars_goods.items() if var.get()]
        selected_entp_codes = [code for code, entp in s_area_code.items() if entp in selected_entp_types]

        if selected_area_code:
            store_names = ["전체"] + [store.entpName for store in store_dic.values() if
                                    store.entpAreaCode == selected_area_code and store.entpTypeCode in selected_entp_codes]
        else:
            store_names = ["전체"] + [store.entpName for store in store_dic.values() if
                                    store.entpTypeCode in selected_entp_codes]

        self.store_combobox_goods['values'] = store_names
        self.store_combobox_goods.set("전체")

    def search_lowest_price_store(self):
        selected_area = self.area_combobox_local.get()
        selected_product = self.product_combobox_local.get()

        area_key = self.area_map_local.get(selected_area)
        product_key = self.products_map_local.get(selected_product)

        stores_by_price = {}

        for key, store in store_dic.items():
            if store.entpAreaCode == area_key:
                good_price_info = Product.getProductPriceInfoSvc(self.this_week, key, product_key)
                if good_price_info != 0:
                    stores_by_price[key] = good_price_info

        sorted_stores_by_price = dict(sorted(stores_by_price.items(), key=lambda item: int(item[1].goodPrice)))

        # 검색 결과를 출력할 프레임 생성
        if self.results_frame_local is not None:
            self.results_frame_local.destroy()

        self.results_frame_local = ttk.Frame(self.window)
        self.results_frame_local.place(x=295 + 75, y=575, width=315, height=212)

        # Treeview 생성
        style = ttk.Style()
        style.configure("Treeview", rowheight=30)  # 특정 스타일 이름으로 행 높이 설정

        columns = ("store_name", "price")
        self.results_tree_local = ttk.Treeview(self.results_frame_local, columns=columns, show='headings', height=3)
        self.results_tree_local.heading("store_name", text="매장")
        self.results_tree_local.heading("price", text="가격")

        # Treeview 열 너비 설정
        self.results_tree_local.column("store_name", width=150)
        self.results_tree_local.column("price", width=150)

        # Treeview에 정렬된 결과 추가
        for store_id, price_info in sorted_stores_by_price.items():
            store_name = store_dic[store_id].entpName
            price_with_unit = f"{price_info.goodPrice}원"
            self.results_tree_local.insert("", "end", values=(store_name, price_with_unit))

        self.results_tree_local.pack(fill=tk.BOTH, expand=True)

        # 행 클릭 이벤트 바인딩
        self.results_tree_local.bind("<ButtonRelease-1>", self.on_store_row_click_local)

    def on_store_row_click_local(self, event):
        if not self.search_in_progress:
            self.search_in_progress = True

            selected_item = event.widget.selection()
            address = None
            store_name = None
            if selected_item:
                item_values = event.widget.item(selected_item[0], "values")
                store_name = item_values[0]
                # store_dic에서 선택된 매장의 주소와 우편번호를 가져옴
                for store_id, store in store_dic.items():
                    if store.entpName == store_name:
                        address = store.roadAddrBasic
                        print(address)
                        break

            if address:
                # 지도에 마커 설정
                self.search_marker = self.map_widget_local.set_address(address, marker=True)
                if self.search_marker:
                    self.search_marker.set_text(store_name)
            self.map_widget_local.set_zoom(10)  # 줌 레벨

            self.search_in_progress = False

    def search_product_price_info(self):
        # 체크된 업태들의 코드 가져오기
        selected_entp_types = [entp for entp, var in self.entp_vars_goods.items() if var.get()]
        if not selected_entp_types:
            print("업태가 선택되지 않았습니다.")
            return
        selected_entp_codes = [code for code, entp in s_area_code.items() if entp in selected_entp_types]
        if not selected_entp_codes:
            selected_entp_codes = [0]  # 아무것도 체크되지 않은 경우 0으로 설정

        # 지역 코드 가져오기
        selected_area = self.area_combobox_goods.get()
        area_key = self.area_map_local.get(selected_area, 0)

        # 품목군 코드 가져오기
        selected_category = self.category_combobox_goods.get()
        category_key = self.category_map_local.get(selected_category, 0)
        if not selected_category or selected_category == "품목군 선택":
            print("품목군이 선택되지 않았습니다.")
            return

        # 품목 코드 가져오기
        selected_item = self.item_combobox_goods.get()
        item_key = self.item_map_goods.get(selected_item, 0)
        if not selected_item or selected_item == "품목 선택":
            print("품목이 선택되지 않았습니다.")
            return

        # 상품 코드 가져오기
        selected_product = self.product_combobox_goods.get()
        product_key = self.product_map_goods.get(selected_product, 0)
        if not selected_product or selected_product == "상품 선택":
            print("상품이 선택되지 않았습니다.")
            return

        # 판매점 entpId 가져오기
        selected_store = self.store_combobox_goods.get()
        store_key = next((key for key, store in store_dic.items() if store.entpName == selected_store), 0)

        # 새로운 창 생성
        new_window = tk.Toplevel(self.window)
        new_window.title("오늘 할 일 : 장보기")
        new_window.geometry("1100x800")

        # 제목 라벨
        title_label = tk.Label(new_window, text="생필품 가격 정보", font=("와구리체 TTF", 18))
        title_label.pack(pady=(10, 0))

        # 선 그리기
        title_line = tk.Frame(new_window, height=2, bg='black', bd=0, width=1100 - 560)
        title_line.pack(fill=tk.X, padx=20, pady=10)

        # Notebook 생성
        notebook = ttk.Notebook(new_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20)

        # 전체 탭 생성
        all_tab_frame = ttk.Frame(notebook)
        notebook.add(all_tab_frame, text="전체")

        # 데이터 리스트 생성
        data_list = self.add_product_info_to_tab(all_tab_frame, selected_entp_codes, product_key, area_key, store_key,
                                                 ['전체'])

        # 각 업태별로 탭 생성
        for entp_type, entp_code in zip(selected_entp_types, selected_entp_codes):
            tab_frame = ttk.Frame(notebook)
            notebook.add(tab_frame, text=entp_type)

            # 각 탭 내용
            self.add_product_info_to_tab(tab_frame, [entp_code], product_key, area_key, store_key, [entp_type],
                                         data_list)

    def add_product_info_to_tab(self, tab_frame, selected_entp_codes, product_key, area_key, store_key, entp_types,
                                data_list=None):
        print(f"Creating tab for entp_types: {entp_types}, selected_entp_codes: {selected_entp_codes}")

        if '전체' in entp_types:
            return self.add_product_section(tab_frame, selected_entp_codes, product_key, area_key, store_key,
                                            entp_types)
        else:
            self.add_product_section(tab_frame, selected_entp_codes, product_key, area_key, store_key, entp_types,
                                     data_list)

    def add_product_section(self, scrollable_canvas_frame, selected_entp_codes, product_key, area_key, store_key,
                            entp_types, data_list=None):
        # 상품명 라벨
        product_name = next((name for name, product in product_dic.items() if product.goodId == product_key), "상품명")

        # 데이터 추가를 위한 임시 저장소
        data_added = False

        # Treeview 생성
        columns = ("지역", "판매점", "상품명", "가격")
        results_tree = ttk.Treeview(scrollable_canvas_frame, columns=columns, show='headings')
        results_tree.heading("지역", text="지역")
        results_tree.heading("판매점", text="판매점")
        results_tree.heading("상품명", text="상품명")
        results_tree.heading("가격", text="가격")

        # Treeview 열 너비 설정
        results_tree.column("지역", width=200)
        results_tree.column("판매점", width=200)
        results_tree.column("상품명", width=200)
        results_tree.column("가격", width=100)

        # 데이터 개수를 세기 위한 변수
        data_count = 0

        if data_list is None:
            data_list = []
            # 데이터 추가
            for store_id, store in store_dic.items():
                if store.entpTypeCode in selected_entp_codes and (area_key == 0 or store.entpAreaCode == area_key) and (
                        store_key == 0 or store_id == store_key):
                    good_price_info = Product.getProductPriceInfoSvc(self.this_week, store_id, product_key)
                    if good_price_info != 0:
                        data_list.append({
                            "area": s_area_detail_code[store.entpAreaCode],
                            "store_name": store.entpName,
                            "product_name": product_name,
                            "price": f"{good_price_info.goodPrice}원",
                            "entp_type_code": store.entpTypeCode
                        })
                        results_tree.insert("", "end", values=(
                        s_area_detail_code[store.entpAreaCode], store.entpName, product_name,
                        f"{good_price_info.goodPrice}원"))
                        data_count += 1
                        data_added = True
        else:
            for data in data_list:
                if data["entp_type_code"] in selected_entp_codes:
                    results_tree.insert("", "end",
                                        values=(data["area"], data["store_name"], data["product_name"], data["price"]))
                    data_count += 1
                    data_added = True

        # 데이터가 추가된 경우에만 라벨과 Treeview를 출력
        if data_added:
            # 행 높이를 설정
            results_tree.configure(height=data_count)

            product_label = tk.Label(scrollable_canvas_frame, text=product_name, font=("와구리체 TTF", 14), anchor="w",
                                     justify="left")
            product_label.pack(fill=tk.X, padx=10, pady=10)
            results_tree.pack(fill=tk.BOTH, expand=True)

        return data_list

    def toggle_all_checkboxes(self, *args):
        all_checked = self.entp_vars_goods["전체"].get()
        for entp in self.entp_types_goods:
            if entp != "전체":
                self.entp_vars_goods[entp].set(all_checked)
        self.update_stores_goods()

    def Telebot_handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if content_type == 'text':
            command = msg['text']

            if command == '/start':
                self.bot.sendMessage(chat_id, "안녕하세요! 어무니가 장 봐오라고 하셨군요! 제가 어느 정도가 평균 가격인지 알려드릴게요. 상품의 이름을 적어주세용! +^+")
            elif command == '/help':
                self.bot.sendMessage(chat_id, "상품 이름을 검색하면 평균 가격을 알려드릴게요!")
            else:
                if command in product_dic:
                    price = Product.CalAveragePrice(self.this_week, product_dic[command].goodId)
                    self.bot.sendMessage(chat_id, f'이 정도 가격에 구매하면 등짝을 지킬 수 있어요!  :  {price}원')
                else:
                    self.bot.sendMessage(chat_id, f'그런 상품은 없는데...')

    def start_telegram_bot(self):
        # 메시지 루프를 별도 스레드에서 실행
        message_loop_thread = threading.Thread(target=self.run)
        message_loop_thread.daemon = True
        message_loop_thread.start()

    def run(self):
        MessageLoop(self.bot, self.Telebot_handle).run_forever()

    def __init__(self):
        window = tk.Tk()
        window.title('오늘 할 일 : 장보기')

        # self.today = datetime.date.today().strftime('%Y%m%d')
        self.today = '20220805'

        self.this_week = self.find_valid_day(get_last_friday(self.today))
        self.two_weeks_ago = self.find_valid_day(get_weeks_earlier(self.today, 2))
        self.a_year_ago = self.find_valid_day(get_last_friday(get_one_year_earlier(self.today)))

        self.a_month_ago = self.find_valid_day(get_last_friday(get_months_earlier(self.today, 1)))
        self.two_months_ago = self.find_valid_day(get_last_friday(get_months_earlier(self.today, 2)))
        self.three_months_ago = self.find_valid_day(get_last_friday(get_months_earlier(self.today, 3)))
        self.four_months_ago = self.find_valid_day(get_last_friday(get_months_earlier(self.today, 4)))
        self.five_months_ago = self.find_valid_day(get_last_friday(get_months_earlier(self.today, 5)))

        # print(self.a_month_ago, self.two_months_ago, self.three_months_ago, self.four_months_ago, self.five_months_ago)

        self.labels = [get_previous_month(self.today[4] + self.today[5], 5) + "월",
                       get_previous_month(self.today[4] + self.today[5], 4) + "월",
                       get_previous_month(self.today[4] + self.today[5], 3) + "월",
                       get_previous_month(self.today[4] + self.today[5], 2) + "월",
                       get_previous_month(self.today[4] + self.today[5], 1) + "월",
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
        self.canvas.create_text(W_WIDTH / 2, 35, tags="title", text='오늘 할 일 : 장보기', font=Title_font)

        if random.randint(0, 1) == 0:
            self.canvas.create_text(W_WIDTH / 2, 75, tags="subtitle",
                                    text='엄마가 시킨 심부름 : ' + self.words[random.randint(0, len(self.words) - 1)] \
                                         + ', ' + self.words[random.randint(0, len(self.words) - 1)],
                                    font=Subtitle_font)
        else:
            self.canvas.create_text(W_WIDTH / 2, 75, tags="subtitle",
                                    text='엄마가 시킨 심부름 : ' + self.words[random.randint(0, len(self.words) - 1)] \
                                         + ', ' + self.words[random.randint(0, len(self.words) - 1)] + ', ' +
                                         self.words[random.randint(0, len(self.words) - 1)], font=Subtitle_font)

        ### 상품 검색창 ###

        self.text = tk.Text(window, width=25, height=6)  # 너비와 높이를 지정할 수 있음
        self.text.place(x=W_WIDTH - 250, y=15)

        search_button_image = Image.open("img/search_cat.png")
        search_button_image = ImageTk.PhotoImage(search_button_image)
        search_button = tk.Button(window, image=search_button_image, command=self.Send_Mail)
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
                  foreground=[("selected", "#000080"), ("!selected", "#808080")],
                  # 폰트 색상을 남색으로 설정, # 선택되지 않은 탭의 글꼴 색상을 회색으로 설정
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
        self.canvas.create_window(W_WIDTH // 2, 280, window=self.notebook, width=W_WIDTH - 40, height=W_HEIGHT // 3)

        # 주간 가격정보 제목 추가
        weekly_price_label = tk.Label(window, text="주간 가격정보", font=("와구리체 TTF", 16), anchor="w")
        self.canvas.create_window(20, 115, anchor="nw", window=weekly_price_label)

        self.search_marker = None
        self.search_in_progress = False

        ### 내 지역 최저가 매장 ###

        self.results_frame_local = None
        self.area_map_local = {v: k for k, v in s_area_detail_code.items() if int(k) % 100000 == 0}
        self.category_map_local = {v: k for k, v in p_total_code_dic.items() if
                                   int(k) % 1000 == 0 and int(k) % 10000 != 0}
        self.items_map_local = {}
        self.products_map_local = {}

        filter_frame_local = tk.Frame(self.canvas)
        self.canvas.create_window(273 + 75, W_HEIGHT // 3 + 155, anchor="nw", window=filter_frame_local)

        # 스타일 설정
        style.configure('TCombobox', padding=5, relief='flat', background='white')
        style.configure('TButton', padding=(5, 3), relief='solid', borderwidth=1, background='#ececec')

        # 제목 라벨
        title_label_local = tk.Label(filter_frame_local, text="내 지역 최저가 매장", font=("와구리체 TTF", 16))
        title_label_local.grid(row=0, column=0, columnspan=2, padx=20, pady=5, sticky="w")

        # 지역 콤보박스
        area_values_local = list(self.area_map_local.keys())
        self.area_combobox_local = ttk.Combobox(filter_frame_local, values=area_values_local, style='TCombobox',
                                                width=18)
        self.area_combobox_local.set("지역 선택")
        self.area_combobox_local.grid(row=1, column=0, padx=(20, 5), pady=5, sticky="ew")

        # 품목군 콤보박스
        self.category_combobox_local = ttk.Combobox(filter_frame_local, values=list(self.category_map_local.keys()),
                                                    style='TCombobox', width=18)
        self.category_combobox_local.set("품목군 선택")
        self.category_combobox_local.grid(row=1, column=1, padx=(5, 20), pady=5, sticky="ew")

        # 품목 콤보박스
        self.item_combobox_local = ttk.Combobox(filter_frame_local, values=[], style='TCombobox', width=18)  # 초기에는 빈 값
        self.item_combobox_local.set("품목 선택")
        self.item_combobox_local.grid(row=2, column=0, padx=(20, 5), pady=5, sticky="ew")

        # 품목군 선택 이벤트 바인딩
        self.category_combobox_local.bind("<<ComboboxSelected>>", self.update_item_local)
        # 품목 선택 이벤트 바인딩
        self.item_combobox_local.bind("<<ComboboxSelected>>", self.update_product_local)

        # 상품 콤보박스
        self.product_combobox_local = ttk.Combobox(filter_frame_local, values=[], style='TCombobox',
                                                   width=18)  # 초기에는 빈 값
        self.product_combobox_local.set("상품 선택")
        self.product_combobox_local.grid(row=2, column=1, padx=(5, 20), pady=5, sticky="ew")

        # 검색 버튼
        self.search_button_local = ttk.Button(filter_frame_local, text="검색", command=self.search_lowest_price_store,
                                              style='TButton', width=15)
        self.search_button_local.grid(row=3, column=0, columnspan=2, padx=20, pady=5, sticky="ew")

        # 각 열의 가중치를 동일하게 설정하여 너비를 맞춤
        filter_frame_local.grid_columnconfigure(0, weight=1)
        filter_frame_local.grid_columnconfigure(1, weight=1)

        ### Treeview 초기화 및 추가 ###

        style.configure("Treeview", rowheight=30)  # 행 높이 설정

        self.results_frame_local = ttk.Frame(window)
        self.results_frame_local.place(x=295 + 75, y=575, width=315, height=212)

        columns = ("store_name", "price")
        self.results_tree_local = ttk.Treeview(self.results_frame_local, columns=columns, show='headings', height=3)
        self.results_tree_local.heading("store_name", text="매장")
        self.results_tree_local.heading("price", text="가격")

        # Treeview 열 너비 설정
        self.results_tree_local.column("store_name", width=150)
        self.results_tree_local.column("price", width=150)

        # Treeview 위젯을 프레임에 추가
        self.results_tree_local.pack(fill=tk.BOTH, expand=True)

        ### 지도 ###

        self.map_widget_local = TkinterMapView(window, width=355 + 25, height=365, corner_radius=0)
        self.map_widget_local.place(x=625 + 75, y=W_HEIGHT // 3 + 155)

        # 초기 지도 위치 설정 (위도, 경도 및 줌 레벨)
        self.map_widget_local.set_zoom(10)  # 줌 레벨

        ### 생필품 가격 정보 조회 ###

        self.item_map_goods = {}
        self.product_map_goods = {}

        filter_frame_goods = tk.Frame(self.canvas)
        self.canvas.create_window(20, W_HEIGHT // 3 + 155, anchor="nw", window=filter_frame_goods)

        # 스타일 설정
        style.configure('TCombobox', padding=5, relief='flat', background='white')
        style.configure('TButton', padding=(5, 3), relief='solid', borderwidth=1, background='#ececec')

        # 제목 라벨
        title_label_goods = tk.Label(filter_frame_goods, text="생필품 가격 정보", font=("와구리체 TTF", 16))
        title_label_goods.grid(row=0, column=0, columnspan=5, padx=5, pady=5, sticky="w")

        # 업태 체크박스들
        entp_label_goods = tk.Label(filter_frame_goods, text="업태", font=("와구리체 TTF", 12))
        entp_label_goods.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.entp_types_goods = ["편의점", "백화점", "대형마트", "슈퍼마켓", "전체"]
        self.entp_vars_goods = {entp: tk.BooleanVar() for entp in self.entp_types_goods}
        checkbox_frame1_goods = tk.Frame(filter_frame_goods)
        checkbox_frame1_goods.grid(row=1, column=1, columnspan=4, padx=5, pady=5, sticky="w")

        checkbox_frame2_goods = tk.Frame(filter_frame_goods)
        checkbox_frame2_goods.grid(row=2, column=1, columnspan=4, padx=5, pady=5, sticky="w")

        # 첫 번째 행 체크박스
        for i, entp in enumerate(self.entp_types_goods[:3]):
            chk = tk.Checkbutton(checkbox_frame1_goods, text=entp, variable=self.entp_vars_goods[entp],
                                 command=self.update_stores_goods)
            chk.pack(side=tk.LEFT, padx=10)  # 간격을 동일하게 설정

        # 두 번째 행 체크박스
        for i, entp in enumerate(self.entp_types_goods[3:]):
            chk = tk.Checkbutton(checkbox_frame2_goods, text=entp, variable=self.entp_vars_goods[entp],
                                 command=self.update_stores_goods)
            chk.pack(side=tk.LEFT, padx=10)  # 간격을 동일하게 설정

        # 전체 체크박스에 대한 이벤트 처리
        self.entp_vars_goods["전체"].trace_add("write", self.toggle_all_checkboxes)



        # 지역 콤보박스
        area_label_goods = tk.Label(filter_frame_goods, text="지역", font=("와구리체 TTF", 12))
        area_label_goods.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        area_values_goods = ["전체"] + list(self.area_map_local.keys())
        self.area_combobox_goods = ttk.Combobox(filter_frame_goods, values=area_values_goods, style='TCombobox',
                                                width=15)
        self.area_combobox_goods.set("전체")
        self.area_combobox_goods.grid(row=3, column=1, padx=5, pady=5, sticky="ew", columnspan=4)

        # 판매점 콤보박스
        store_label_goods = tk.Label(filter_frame_goods, text="판매점", font=("와구리체 TTF", 12))
        store_label_goods.grid(row=4, column=0, padx=5, pady=5, sticky="w")

        self.store_combobox_goods = ttk.Combobox(filter_frame_goods, values=["전체"], style='TCombobox', width=15)
        self.store_combobox_goods.set("전체")
        self.store_combobox_goods.grid(row=4, column=1, padx=5, pady=5, sticky="ew", columnspan=4)

        # 품목군 콤보박스
        category_label_goods = tk.Label(filter_frame_goods, text="품목군", font=("와구리체 TTF", 12))
        category_label_goods.grid(row=5, column=0, padx=5, pady=5, sticky="w")

        self.category_combobox_goods = ttk.Combobox(filter_frame_goods, values=list(self.category_map_local.keys()),
                                                    style='TCombobox', width=15)
        self.category_combobox_goods.set("품목군 선택")
        self.category_combobox_goods.grid(row=5, column=1, padx=5, pady=5, sticky="ew", columnspan=4)

        # 품목 콤보박스
        item_label_goods = tk.Label(filter_frame_goods, text="품목", font=("와구리체 TTF", 12))
        item_label_goods.grid(row=6, column=0, padx=5, pady=5, sticky="w")

        self.item_combobox_goods = ttk.Combobox(filter_frame_goods, values=["전체"], style='TCombobox', width=15)
        self.item_combobox_goods.set("품목 선택")
        self.item_combobox_goods.grid(row=6, column=1, padx=5, pady=5, sticky="ew", columnspan=4)

        # 상품 콤보박스
        product_label_goods = tk.Label(filter_frame_goods, text="상품", font=("와구리체 TTF", 12))
        product_label_goods.grid(row=7, column=0, padx=5, pady=5, sticky="w")

        self.product_combobox_goods = ttk.Combobox(filter_frame_goods, values=["전체"], style='TCombobox', width=15)
        self.product_combobox_goods.set("상품 선택")
        self.product_combobox_goods.grid(row=7, column=1, padx=5, pady=5, sticky="ew", columnspan=4)


        # # 조회 버튼을 품목 콤보박스 오른쪽에 배치하고 높이를 늘림
        # inquiry_image = Image.open("img/inquiry_cat.png")
        # inquiry_image = ImageTk.PhotoImage(inquiry_image)
        # self.search_button_goods = tk.Button(filter_frame_goods, image=inquiry_image, command=self.search_product_price_info, width=10)
        # self.search_button_goods.image = inquiry_image  # 이미지가 가비지 컬렉션되지 않도록 참조를 유지
        #
        # self.search_button_goods.grid(row=7, column=0, columnspan=5, padx=5, pady=5, sticky="ew")  # 전체 행을 덮도록 설정

        # 상품 조회 버튼
        self.search_button_goods = ttk.Button(filter_frame_goods, text="조회", command=self.search_product_price_info,
                                              style='TButton', width=10)
        self.search_button_goods.grid(row=8, column=0, columnspan=5, padx=5, pady=5, sticky="ew",
                                      ipady=20)  # 전체 행을 덮도록 설정

        # 각 열의 가중치를 동일하게 설정하여 너비를 맞춤
        filter_frame_goods.grid_columnconfigure(0, weight=1)
        filter_frame_goods.grid_columnconfigure(1, weight=1)
        filter_frame_goods.grid_columnconfigure(2, weight=1)
        filter_frame_goods.grid_columnconfigure(3, weight=1)
        filter_frame_goods.grid_columnconfigure(4, weight=1)

        # 품목군 선택 이벤트 바인딩
        self.category_combobox_goods.bind("<<ComboboxSelected>>", self.update_items_goods)
        self.item_combobox_goods.bind("<<ComboboxSelected>>", self.update_products_goods)

        # 지역 선택 이벤트 바인딩
        self.area_combobox_goods.bind("<<ComboboxSelected>>", self.update_stores_goods)

        # 창 닫기 이벤트 처리++++++++++++++++
        window.protocol("WM_DELETE_WINDOW", self.on_closing)

        TOKEN = '7214401654:AAGdAoPpFFksphZBmJp854c31yLRMAgmXSU'

        # Create a bot instance
        self.bot = telepot.Bot(TOKEN)

        # Start the message loop
        MessageLoop(self.bot, self.Telebot_handle).run_as_thread()


        ### 메인 루프 ###
        self.window = window
        window.mainloop()


if __name__ == "__main__":
    app = MainGUI()
