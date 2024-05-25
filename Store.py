import xml.etree.ElementTree as ET

import requests


class Store:
    def __init__(self, entpId=None, entpName=None, entpTypeCode=None, entpAreaCode=None, areaDetailCode=None,
                 entpTelno=None, postNo=None, plmkAddrBasic=None, plmkAddrDetail=None, roadAddrBasic=None,
                 roadAddrDetail=None, xMapCoord=None, yMapCoord=None):
        self.entpId = entpId
        self.entpName = entpName
        self.entpTypeCode = entpTypeCode
        self.entpAreaCode = entpAreaCode
        self.areaDetailCode = areaDetailCode
        self.entpTelno = entpTelno
        self.postNo = postNo
        self.plmkAddrBasic = plmkAddrBasic
        self.plmkAddrDetail = plmkAddrDetail
        self.roadAddrBasic = roadAddrBasic
        self.roadAddrDetail = roadAddrDetail
        self.xMapCoord = xMapCoord
        self.yMapCoord = yMapCoord

    def __str__(self):
        return f"Product(entpId={self.entpId}, entpName={self.entpName}, entpTypeCode={self.entpTypeCode}, entpAreaCode={self.entpAreaCode}, areaDetailCode={self.areaDetailCode}, entpTelno={self.entpTelno}, postNo={self.postNo})"


def LoadAllStore():
    url = 'http://openapi.price.go.kr/openApiImpl/ProductPriceInfoService/getStoreInfoSvc.do?ServiceKey=bgABaHDCI6aMWSF9LIrvGAVSXbmEl193MNFLDhw%2Bndhs2%2F%2BTJ%2BPIq9J2DUn12Ei05O7fTEuSWxePGK8a7qfD0A%3D%3D'

    response = requests.get(url)  # API 호출 및 응답 받기
    # print(response.text)
    root = ET.fromstring(response.text)  # XML 응답 파싱

    stores_map = {}  # goodId를 키로 갖는 Product들의 맵

    for item in root.iter("iros.openapi.service.vo.entpInfoVO"):
        temp = Store(
            entpId=item.findtext("entpId"),
            entpName=item.findtext("entpName"),
            entpTypeCode=item.findtext("entpTypeCode"),
            entpAreaCode=item.findtext("entpAreaCode"),
            areaDetailCode=item.findtext("areaDetailCode"),
            entpTelno=item.findtext("entpTelno"),
            postNo=item.findtext("postNo"),
            plmkAddrBasic=item.findtext("plmkAddrBasic"),
            plmkAddrDetail=item.findtext("plmkAddrDetail"),
            roadAddrBasic=item.findtext("roadAddrBasic"),
            roadAddrDetail=item.findtext("roadAddrDetail"),
            xMapCoord=item.findtext("xMapCoord"),
            yMapCoord=item.findtext("yMapCoord")
        )

        if temp.entpName:
            stores_map[temp.entpName] = temp

    return stores_map


# 업체 업태 코드
def LoadAreaCode():
    url = 'http://openapi.price.go.kr/openApiImpl/ProductPriceInfoService/getStandardInfoSvc.do'
    service_key = "bgABaHDCI6aMWSF9LIrvGAVSXbmEl193MNFLDhw+ndhs2/+TJ+PIq9J2DUn12Ei05O7fTEuSWxePGK8a7qfD0A=="

    code_map = {}

    queryParams = {'serviceKey': service_key, 'classCode': 'BU'}
    response = requests.get(url, params=queryParams)
    root = ET.fromstring(response.text)

    for item in root.iter("iros.openapi.service.vo.stdInfoVO"):
        code_map[item.findtext("code")] = item.findtext("codeName")

    return code_map


# 업체 지역 코드
def LoadAreaDetailCode():
    url = 'http://openapi.price.go.kr/openApiImpl/ProductPriceInfoService/getStandardInfoSvc.do'
    service_key = "bgABaHDCI6aMWSF9LIrvGAVSXbmEl193MNFLDhw+ndhs2/+TJ+PIq9J2DUn12Ei05O7fTEuSWxePGK8a7qfD0A=="

    code_map = {}

    queryParams = {'serviceKey': service_key, 'classCode': 'AR'}
    response = requests.get(url, params=queryParams)
    root = ET.fromstring(response.text)

    for item in root.iter("iros.openapi.service.vo.stdInfoVO"):
        code_map[item.findtext("code")] = item.findtext("codeName")

    return code_map
