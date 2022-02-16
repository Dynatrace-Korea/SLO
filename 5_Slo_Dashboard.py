import sys
import configparser
import argparse
import datetime, time
import requests
import json
import sys
from requests import api
from requests.api import request

# 완성된 Full Url과 header를 생성해 줌
def createFullUrl(apiUrl, tenantID, APIToken):
    if "/e/" in tenantID:
        url = tenantID + apiUrl
        if not url.startswith("https://"):
            url = "https://" + url
    else:
        url = f"https://{tenantID}.live.dynatrace.com" + apiUrl
    headers = {'accept': "application/json", "Authorization": "Api-Token " + APIToken}
    return url, headers

# 해당 API Url을 이용해 GET 방식으로 호출한 후 결과를 반환
def dtapiget(apiUrl):
    global tenantID
    global APIToken
    url, headers = createFullUrl(apiUrl, tenantID, APIToken)
    response = requests.get(url, headers = headers)
    r_json = response.json()
    return r_json

# SLO Dashboard 생성을 위해 사용할 JSON 형태의 Body를 구성
def createJsonObj():
    requestBody = '''{
		"dashboardMetadata": {
			"name": "SLO 현황2",
			"shared": false,
			"owner": "Dynatrace",
			"preset": true
		},
		"tiles": [
			{
			  "name": "Back-end SLO",
			  "tileType": "HEADER",
			  "configured": true,
			  "bounds": {
				"top": 0,
				"left": 0,
				"width": 304,
				"height": 38
			  },
			  "tileFilter": {}
			},
			{
				"name": "Markdown",
				"tileType": "MARKDOWN",
				"configured": true,
				"bounds": {
					"top": 38,
					"left": 1216,
					"width": 304,
					"height": 608
				  },
				"tileFilter": {
				"timeframe": "yesterday"
				},
				"markdown": "___\\n## 🔍  Links\\n***\\n- [SLO](ui/slo)\\n"
			},
			{
				"name": "성공율_SLO",
				"tileType": "SLO",
				"configured": true,
				"bounds": {
					"top": 114,
					"left": 0,
					"width": 304,
					"height": 114
				},
				"tileFilter": {
					"timeframe": "-1d to -1m"
				},
				"assignedEntities": [
					""
				]
			},
			{
				"name": "성능_SLO",
				"tileType": "SLO",
				"configured": true,
				"bounds": {
					"top": 228,
					"left": 0,
					"width": 304,
					"height": 114
				},
				"tileFilter": {
				"timeframe": "-1d to -1m"
				},
				"assignedEntities": [
					""
				]
			},
			{
				"name": "Markdown",
				"tileType": "MARKDOWN",
				"configured": true,
				"bounds": {
					"top": 38,
					"left": 0,
					"width": 304,
					"height": 76
				},
				"tileFilter": {
					"timeframe": "-1d"
				},
				"markdown": "___\\n🔍 [SLO](#dashboard;id=)\\n___"
			},
			{
				"name": "Markdown",
				"tileType": "MARKDOWN",
				"configured": true,
				"bounds": {
					"top": 0,
					"left": 304,
					"width": 1216,
					"height": 38
				},
				"tileFilter": {},
				"markdown": "#### SLO 상세 분석을 하시려면 돋보기 🔍 옆에 있는 SLO 대상 이름을 클릭하세요."
			}
		]
    }'''
    jsonObj = json.loads(requestBody)
    return jsonObj


################################################ 메인 작업 수행 ###############################################

# 대상 환경(Tenant or Environment) 정보를 설정 파일에서 가져옴
config = configparser.RawConfigParser()
config.read('./dtenv.properties', encoding='utf-8')
section = "tenant"
tenantID = config.get(section, "tenantID")
APIToken = config.get(section, "APIToken")

# 매개변수에서 받은 서비스 이름을 JSON에 반영
jsonObj = createJsonObj()

# SLO dashboard 생성
apiUrl = "/api/config/v1/dashboards"
url, headers = createFullUrl(apiUrl, tenantID, APIToken)
response = requests.post(url, json=jsonObj, headers = headers)
if response.status_code == 201:
    print("== Success!")
else:
    print("== Failed!!!")
    print("-- 응답코드: %d" % response.status_code)
    print("-- 에러내용 --")
    print(response.text)
