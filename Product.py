import xml.etree.ElementTree as ET

import requests


class Product:
    def __init__(self, goodId=None, goodName=None, goodUnitDivCode=None, goodBaseCnt=None, goodSmlclsCode=None,
                 detailMean=None, goodTotalCnt=None, goodTotalDivCode=None):
        self.goodId = goodId
        self.goodName = goodName
        self.goodUnitDivCode = goodUnitDivCode
        self.goodBaseCnt = goodBaseCnt
        self.goodSmlclsCode = goodSmlclsCode
        self.detailMean = detailMean
        self.goodTotalCnt = goodTotalCnt
        self.goodTotalDivCode = goodTotalDivCode

    def __str__(self):
        return f"Product(goodId={self.goodId}, goodName={self.goodName}, goodUnitDivCode={self.goodUnitDivCode}, goodBaseCnt={self.goodBaseCnt}, goodSmlclsCode={self.goodSmlclsCode}, detailMean={self.detailMean}, goodTotalCnt={self.goodTotalCnt}, goodTotalDivCode={self.goodTotalDivCode})"


def LoadAllProduct():
    url = 'http://openapi.price.go.kr/openApiImpl/ProductPriceInfoService/getProductInfoSvc.do?ServiceKey=bgABaHDCI6aMWSF9LIrvGAVSXbmEl193MNFLDhw%2Bndhs2%2F%2BTJ%2BPIq9J2DUn12Ei05O7fTEuSWxePGK8a7qfD0A%3D%3D'
    service_key = "bgABaHDCI6aMWSF9LIrvGAVSXbmEl193MNFLDhw+ndhs2/+TJ+PIq9J2DUn12Ei05O7fTEuSWxePGK8a7qfD0A=="

    queryParams = {'serviceKey': service_key}  # API 요청 파라미터 설정
    response = requests.get(url, params=queryParams)  # API 호출 및 응답 받기
    # print(response.text)
    root = ET.fromstring(response.text)  # XML 응답 파싱

    products_map = {}  # goodId를 키로 갖는 Product들의 맵

    for item in root.iter("item"):
        temp = Product(
            goodId=item.findtext("goodId"),
            goodName=item.findtext("goodName"),
            goodUnitDivCode=item.findtext("goodUnitDivCode"),
            goodBaseCnt=item.findtext("goodBaseCnt"),
            goodSmlclsCode=item.findtext("goodSmlclsCode"),
            detailMean=item.findtext("detailMean"),
            goodTotalCnt=item.findtext("goodTotalCnt"),
            goodTotalDivCode=item.findtext("goodTotalDivCode")
        )

        if temp.goodId:
            products_map[temp.goodId] = temp

    return products_map


# LoadAllProduct 함수를 호출하여 products_map을 가져오기
products_map = LoadAllProduct()

# 맵 출력
# for goodId, product in products_map.items():
#     print(product)
