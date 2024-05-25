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
            goodId=item.findtext("goodId"),
            goodName=item.findtext("goodName"),
            goodUnitDivCode=item.findtext("goodUnitDivCode"),
            goodBaseCnt=item.findtext("goodBaseCnt"),
            goodSmlclsCode=item.findtext("goodSmlclsCode"),
            detailMean=item.findtext("detailMean"),
            goodTotalCnt=item.findtext("goodTotalCnt"),
            goodTotalDivCode=item.findtext("goodTotalDivCode")
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
