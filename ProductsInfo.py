import requests
import xml.etree.ElementTree as ET
import tkinter

# API 호출을 위한 URL 및 인증키 설정
url = 'http://openapi.price.go.kr/openApiImpl/ProductPriceInfoService/getProductInfoSvc.do?ServiceKey=bgABaHDCI6aMWSF9LIrvGAVSXbmEl193MNFLDhw%2Bndhs2%2F%2BTJ%2BPIq9J2DUn12Ei05O7fTEuSWxePGK8a7qfD0A%3D%3D'
# 공공데이터포털에서 발급받은 디코딩되지 않은 인증키 입력
service_key = "bgABaHDCI6aMWSF9LIrvGAVSXbmEl193MNFLDhw+ndhs2/+TJ+PIq9J2DUn12Ei05O7fTEuSWxePGK8a7qfD0A=="

# Tkinter 윈도우 생성 및 설정
window = tkinter.Tk()
window.title("전체 상품 정보")
frame = tkinter.Frame(window)
frame.pack()

# 표 헤더 설정
header = ["ID", "이름", "단위량", "상세정보", "용량"]
for i, col_name in enumerate(header):
    label = tkinter.Label(frame, text=col_name, font=("Helvetica", 14, "bold"))
    label.grid(row=0, column=i)

# API 요청 파라미터 설정
queryParams = {'serviceKey': service_key}

# API 호출 및 응답 받기
response = requests.get(url, params=queryParams)
print(response.text)

# XML 응답 파싱
root = ET.fromstring(response.text)

# XML 데이터를 반복하면서 표에 데이터 추가
row_count = 1
for item in root.iter("item"):
    goodId = item.findtext("goodId")
    goodName = item.findtext("goodName")
    goodBaseCnt = item.findtext("goodBaseCnt")
    detailMean = item.findtext("detailMean")
    goodTotalCnt = item.findtext("goodTotalCnt")

    data = [goodId, goodName, goodBaseCnt, detailMean, goodTotalCnt]
    for i, value in enumerate(data):
        label = tkinter.Label(frame, text=value, font=("Helvetica", 12))
        label.grid(row=row_count, column=i)

    row_count += 1

# Tkinter 메인 루프 실행
window.mainloop()