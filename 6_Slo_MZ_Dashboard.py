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
			"name": "SLO_분석",
			"shared": false,
			"owner": "Dynatrace",
			"preset": true
		},
		"tiles": [
			{
				"name": "_성공율_분석",
				"tileType": "DATA_EXPLORER",
				"configured": true,
				"bounds": {
					"top": 38,
					"left": 0,
					"width": 456,
					"height": 646
				},
				"tileFilter": {
				"managementZone": {
					"id": "4602628388230493397",
					"name": "MANAGEMENTZONE"
					}
				},
				"customName": "Data explorer results",
				"queries": [
					{
						"id": "A",
						"timeAggregation": "DEFAULT",
						"splitBy": [],
						"metricSelector": "(100)*(builtin:service.errors.fivexx.successCount:splitBy(\\\"dt.entity.service\\\"))/(builtin:service.requestCount.server:splitBy(\\\"dt.entity.service\\\"))",
						"enabled": true
					}
				],
				"visualConfig": {
					"type": "TABLE",
					"global": {
					  "hideLegend": false
					},
					"rules": [
						{
							"matcher": "A:",
							"properties": {
							  "color": "DEFAULT",
							  "seriesType": "LINE"
							},
							"seriesOverrides": []
						}
					],
					"axes": {
						"xAxis": {
							"displayName": "",
							"visible": true
						},
						"yAxes": []
					},
					"heatmapSettings": {},
					"tableSettings": {
						"isThresholdBackgroundAppliedToCell": false
					},
					"graphChartSettings": {
						"connectNulls": false
					}
				}
			},
			{
				"name": "PRD MS-VW_응답시간_분석",
				"tileType": "DATA_EXPLORER",
				"configured": true,
				"bounds": {
					"top": 38,
					"left": 456,
					"width": 456,
					"height": 646
				},
				"tileFilter": {
					"managementZone": {
						"id": "4602628388230493397",
						"name": "MANAGEMENTZONE"
					}
				},
				"customName": "Data explorer results",
				"queries": [
					{
						"id": "A",
						"timeAggregation": "DEFAULT",
						"metricSelector": "(100)*((calc:service.slo_fast_PRD-MS-VW_requests:splitBy(\\\"dt.entity.service\\\"))/(builtin:service.requestCount.server:splitBy(\\\"dt.entity.service\\\")))",
						"enabled": true
					}
				],
				"visualConfig": {
					"type": "TABLE",
					"global": {
						"hideLegend": false
					},
					"rules": [
						{
							"matcher": "A:",
							"properties": {
								"color": "DEFAULT"
								},
							"seriesOverrides": []
						}
					],
					"axes": {
						"xAxis": {
							"visible": true
						},
						"yAxes": []
					},
					"heatmapSettings": {},
					"tableSettings": {
						"isThresholdBackgroundAppliedToCell": false
					},
					"graphChartSettings": {
						"connectNulls": false
					}
				},
				"queriesSettings": {
					"resolution": ""
				}
			},
			{
				"name": "_응답시간_트랜잭션 건수",
				"tileType": "DATA_EXPLORER",
				"configured": true,
				"bounds": {
					"top": 38,
					"left": 912,
					"width": 456,
					"height": 646
				},
				"tileFilter": {
					"managementZone": {
					"id": "4602628388230493397",
					"name": "MANAGEMENTZONE"
					}
				},
				"customName": "Data explorer results",
				"queries": [
					{
						"id": "B",
						"timeAggregation": "DEFAULT",
						"metricSelector": "builtin:service.requestCount.server:splitBy(\\\"dt.entity.service\\\")",
						"enabled": true
					}
				],
				"visualConfig": {
					"type": "TABLE",
					"global": {
						"hideLegend": false
					},
					"rules": [
						{
							"matcher": "B:",
							"properties": {
								"color": "DEFAULT"
							},
							"seriesOverrides": []
						}
					],
					"axes": {
						"xAxis": {
							"visible": true
						},
						"yAxes": []
					},
					"heatmapSettings": {},
					"tableSettings": {
						"isThresholdBackgroundAppliedToCell": false
						},
					"graphChartSettings": {
						"connectNulls": false
					}
				},
				"queriesSettings": {
					"resolution": ""
				}
			},
			{
				"name": "성공율 SLO  Trend",
				"tileType": "DATA_EXPLORER",
				"configured": true,
				"bounds": {
					"top": 684,
					"left": 0,
					"width": 684,
					"height": 266
				},
				"tileFilter": {
					"managementZone": {
						"id": "4602628388230493397",
						"name": "MANAGEMENTZONE"
					}
				},
				"customName": "Data explorer results",
				"queries": [
					{
						"id": "A",
						"timeAggregation": "DEFAULT",
						"metricSelector": "(100)*(builtin:service.errors.fivexx.successCount:splitBy())/(builtin:service.requestCount.server:splitBy())",
						"enabled": true
					}
				],
				"visualConfig": {
					"type": "GRAPH_CHART",
					"global": {
						"hideLegend": false
					},
					"rules": [
						{
							"matcher": "A:",
							"properties": {
							"color": "DEFAULT",
								"seriesType": "AREA"
							},
							"seriesOverrides": []
						}
					],
					"axes": {
						"xAxis": {
							"displayName": "",
							"visible": true
						},
						"yAxes": [
							{
								"displayName": "",
								"visible": true,
								"min": "0",
								"max": "100",
								"position": "LEFT",
								"queryIds": [
									"A"
								],
								"defaultAxis": true
							}
						]
					},
					"heatmapSettings": {},
					"tableSettings": {
						"isThresholdBackgroundAppliedToCell": false
					},
					"graphChartSettings": {
						"connectNulls": false
					}
				},
				"queriesSettings": {
					"resolution": ""
				}
			},
			{
				"name": "성능 SLO Trend",
				"tileType": "DATA_EXPLORER",
				"configured": true,
				"bounds": {
					"top": 684,
					"left": 684,
					"width": 684,
					"height": 266
				},
				"tileFilter": {
					"managementZone": {
						"id": "4602628388230493397",
						"name": "MANAGEMENTZONE"
					}
				},
				"customName": "Data explorer results",
				"queries": [
					{
						"id": "A",
						"timeAggregation": "DEFAULT",
						"metricSelector": "(100)*((calc:service.slo_fast_PRD-MS-VW_requests:splitBy())/(builtin:service.requestCount.server:splitBy()))",
						"enabled": true
					}
				],
				"visualConfig": {
					"type": "GRAPH_CHART",
					"global": {
						"hideLegend": false
					},
					"rules": [
						{
							"matcher": "A:",
							"properties": {
								"color": "DEFAULT",
								"seriesType": "AREA"
							},
							"seriesOverrides": []
						}
					],
					"axes": {
						"xAxis": {
							"displayName": "",
							"visible": true
						},
						"yAxes": [
							{
								"displayName": "",
								"visible": true,
								"min": "0",
								"max": "100",
								"position": "LEFT",
								"queryIds": [
									"A"
								],
								"defaultAxis": true
							}
						]
					},
					"heatmapSettings": {},
					"tableSettings": {
						"isThresholdBackgroundAppliedToCell": false
					},
					"graphChartSettings": {
						"connectNulls": false
					}
				},
				"queriesSettings": {
					"resolution": ""
				}
			},
					{
				"name": "Markdown",
				"tileType": "MARKDOWN",
				"configured": true,
				"bounds": {
					"top": 38,
					"left": 1368,
					"width": 304,
					"height": 152
				},
				"tileFilter": {},
				"markdown": "🔙 [SLO 현황](#dashboard;id=6a96a9da-7576-4b03-98db-85370d5504c2)"
			},
			{
				"name": "Markdown",
				"tileType": "MARKDOWN",
				"configured": true,
				"bounds": {
					"top": 0,
					"left": 0,
					"width": 1368,
					"height": 38
				},
				"tileFilter": {},
				"markdown": "#### 서비스 상세 분석을 하시려면 테이블 내 서비스 이름을 클릭하세요."
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

# SLO 생성을 위해 사용할 JSON 형태의 Body를 구성하고 사용자 정의 값 할당
rstCondition = config.get("calcm", "rstCondition")

# 대상 서비스 그룹을 실행시 매개변수에서 받아옴
arg = sys.argv[1]
metricName = arg.replace(" ", "-")

# Management Zone ID 가져오기
apiUrl = "/api/config/v1/managementZones"
r_json = dtapiget(apiUrl)
mzID = ""
for data in r_json["values"]:
	entityId = data["id"]
	entityName = data["name"]
	if arg == entityName:
		 mzID = entityId
if mzID == "":
	print("== Failed!!!")
	print('==manazement zone을 찾을 수 없습니다!!! %s' % arg)
	sys.exit()


# 매개변수에서 받은 서비스 이름을 JSON에 반영
jsonObj = createJsonObj()
jsonObj["dashboardMetadata"]["name"] = arg + "_" + rstCondition + "_SLO_분석"
jsonObj["tiles"][0]["name"] = arg + "_성공율_분석"
jsonObj["tiles"][0]["tileFilter"]["managementZone"]["id"] = mzID
jsonObj["tiles"][0]["tileFilter"]["managementZone"]["name"] = arg
jsonObj["tiles"][1]["name"] = arg + "_응답시간_분석"
jsonObj["tiles"][1]["tileFilter"]["managementZone"]["id"] = mzID
jsonObj["tiles"][1]["tileFilter"]["managementZone"]["name"] = arg
jsonObj["tiles"][1]["queries"][0]["metricSelector"] = "(100)*((calc:service.slo_fast_" + metricName + "_" + rstCondition + "_requests:splitBy(\"dt.entity.service\"))/(builtin:service.requestCount.server:splitBy(\"dt.entity.service\")))"
jsonObj["tiles"][2]["name"] = arg + "_트랜잭션_건수"
jsonObj["tiles"][2]["tileFilter"]["managementZone"]["id"] = mzID
jsonObj["tiles"][2]["tileFilter"]["managementZone"]["name"] = arg
jsonObj["tiles"][3]["tileFilter"]["managementZone"]["id"] = mzID
jsonObj["tiles"][3]["tileFilter"]["managementZone"]["name"] = arg
jsonObj["tiles"][4]["tileFilter"]["managementZone"]["id"] = mzID
jsonObj["tiles"][4]["tileFilter"]["managementZone"]["name"] = arg
jsonObj["tiles"][4]["queries"][0]["metricSelector"] = "(100)*((calc:service.slo_fast_" + metricName + "_" + rstCondition + "_requests:splitBy())/(builtin:service.requestCount.server:splitBy()))"

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
