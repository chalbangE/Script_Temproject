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

    response = requests.get(url)  # API 호출 및 응답 받기
    # print(response.text)
    root = ET.fromstring(response.text)  # XML 응답 파싱

    products_map = {}  # goodId를 키로 갖는 Product들의 맵

    for item in root.iter("item"):
        temp = Product(
            goodId=item.findtext("goodId"),                     # 상품아이디
            goodName=item.findtext("goodName"),                 # 상품명
            goodUnitDivCode=item.findtext("goodUnitDivCode"),   # 상품단위구분코드
            goodBaseCnt=item.findtext("goodBaseCnt"),           # 상품단위량
            goodSmlclsCode=item.findtext("goodSmlclsCode"),     # 상품소분류코드
            detailMean=item.findtext("detailMean"),             # 상품설명상세
            goodTotalCnt=item.findtext("goodTotalCnt"),         # 상품용량
            goodTotalDivCode=item.findtext("goodTotalDivCode")  # 상품용량구분코드
        )

        if temp.goodName:
            products_map[temp.goodName] = temp

    return products_map


# 상품 단위 구분 코드, 상품 용량 구분 코드
def LoadUnitDivCode():
    url = 'http://openapi.price.go.kr/openApiImpl/ProductPriceInfoService/getStandardInfoSvc.do'
    service_key = "bgABaHDCI6aMWSF9LIrvGAVSXbmEl193MNFLDhw+ndhs2/+TJ+PIq9J2DUn12Ei05O7fTEuSWxePGK8a7qfD0A=="

    code_map = {}

    queryParams = {'serviceKey': service_key, 'classCode': 'UT'}
    response = requests.get(url, params=queryParams)
    root = ET.fromstring(response.text)

    for item in root.iter("iros.openapi.service.vo.stdInfoVO"):
        code_map[item.findtext("code")] = item.findtext("codeName")

    return code_map


# 상품 소분류 코드
def LoadTotalDivCode():
    url = 'http://openapi.price.go.kr/openApiImpl/ProductPriceInfoService/getStandardInfoSvc.do'
    service_key = "bgABaHDCI6aMWSF9LIrvGAVSXbmEl193MNFLDhw+ndhs2/+TJ+PIq9J2DUn12Ei05O7fTEuSWxePGK8a7qfD0A=="

    code_map = {}

    queryParams = {'serviceKey': service_key, 'classCode': 'AL'}
    response = requests.get(url, params=queryParams)
    root = ET.fromstring(response.text)

    for item in root.iter("iros.openapi.service.vo.stdInfoVO"):
        code_map[item.findtext("code")] = item.findtext("codeName")

    return code_map

def CalAveragePrice(goodInspectDay=None, goodId=None):
    url = 'http://openapi.price.go.kr/openApiImpl/ProductPriceInfoService/getProductPriceInfoSvc.do'
    service_key = "bgABaHDCI6aMWSF9LIrvGAVSXbmEl193MNFLDhw+ndhs2/+TJ+PIq9J2DUn12Ei05O7fTEuSWxePGK8a7qfD0A=="

    queryParams = {'serviceKey': service_key, 'goodInspectDay': goodInspectDay, 'entpId': None, 'goodId': goodId}

    response = requests.get(url, params=queryParams)
    # print(response.text)

    root = ET.fromstring(response.text)

    # print(goodInspectDay, goodId)

    price = []
    for item in root.iter("iros.openapi.service.vo.goodPriceVO"):
        price.append(int(item.findtext("goodPrice")))

    if len(price) == 0:
        return 0
    else:
        return sum(price) // len(price)

# print(CalAveragePrice("20220729", "168"))