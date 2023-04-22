import requests
import pandas as pd
import cufflinks as cf

# 取US COMTRADE数据的函数接口
def comtrade_data(**params):
    r = requests.get("http://comtrade.un.org/api/get", params=params)
    return pd.DataFrame(r.json()['dataset'])

Iron_ores = comtrade_data(r="156",px="HS",ps="ALL",p="36",rg='1',cc='2601',type='C',freq="A")
Iron_ores[['yr','TradeValue']].iplot(x='yr',y='TradeValue',kind='bar',title='中国自澳大利亚进口铁矿石金额')

import json
response = requests.get("https://comtrade.un.org/Data/cache/reporterAreas.json")
areas = json.loads(response.text) # dict 结构
areas = areas['results'] # list 结构，每个元素是一个字典
# 比如areas[1]是第二个元素，areas[1]['id']是4，areas[1]['text']是Afghanist
country_list = []
for i in range(0, len(areas)):
    country_list.append(areas[i]['text'])
# 移除Faeroe Isds
country_list.remove('Faeroe Isds')
country_list.remove('Greece')

# 官网地址: https://comtrade.un.org/data/
# 参考报告: https://zhuanlan.zhihu.com/p/337467250
# r 是 reporting area
# px 是 classification
# ps 是 time period
# p 是 parter area
# rg 是 trade regime / trade flow
# cc 是 classification code
# type 是 trade data type
# freq 是 data set frequency

data = pd.DataFrame()
# 如果是all，则是全部国家
for j in ['202201','202202','202203']:
    for i in country_list[1:3]:
        print(i)
        _data = comtrade_data(r=i,px="HS",ps=j,p="World",rg='Export',cc='AG2',type='C',freq="M")
        print(_data)
        data = data.append(_data)
