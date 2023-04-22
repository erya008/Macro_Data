import pandas as pd
import numpy as np
from datetime import datetime
import cufflinks as cf
from pandas.core import base
from statsmodels.tsa.x13 import x13_arima_analysis
from scipy.interpolate import interp1d
from sklearn import linear_model
from WindPy import w

cf.set_config_file(offline=True,theme='white',dimensions=(550,350),colorscale='plotly')

# 将Wind代码转换成语义
def config(data):
    _data = pd.read_csv('mapping.csv',index_col=0)
    _config = _data['SeriesID'].astype(str)
    _col = _config[data].values
    return _col


w.start()

# 此处修改 date=xxx 的时间，最新查询时间
new_time = '2021-09-12'
# 此处修改 date=xxx 的时间，最新报告期
report_time = '2021-06-30'

# 提取全部A股的wind代码
code = w.wset("sectorconstituent","date={};sectorid=a001010100000000;field=wind_code,sec_name".format(new_time))
code = ','.join(code.Data[0])

# 测试用，以防提取超限
code = code[:19]

# 提取证券简称等基础信息
base_data = w.wss(code, "sec_name,stm_issuingdate,mkt,nature1,corpscale,industry_csrc12_n,industry_sw,industry_gics","rptDate={};tradeDate={};industryType=1".format(report_time,new_time))
base_data = pd.DataFrame(np.array(base_data.Data).T, columns=base_data.Fields, index=base_data.Codes)

# 当新的报表期时，更新report的时间列表
report = ['2018-03-31','2018-06-30','2018-09-30','2018-12-31','2019-03-31','2019-06-30','2019-09-30','2019-12-31','2020-03-31','2020-06-30','2020-09-30','2020-12-31','2021-03-31','2021-06-30']
# 当需要新的变量时，更新indicators的变量列表，记得更新config文件
indicators = ['tot_oper_rev,np_belongto_parcomsh,roe_ttm2']

# 提取各报告期的财务数据并合并
for i in report:
    _data = w.wss(code, indicators,"unit=1;rptDate={};rptType=1".format(report))
    _data = pd.DataFrame(np.array(_data.Data).T, columns=[ k + '_' + report for k in config(_data.Fields)], index=_data.Codes)
    base_data = base_data.join(_data)


