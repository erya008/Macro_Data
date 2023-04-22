import pandas as pd
import numpy as np
import cufflinks as cf
import macro_func

# 导入需要的包
cf.set_config_file(offline=True,theme='white',dimensions=(550,350),colorscale='plotly')

# 做货币总量投放的图
money_aggregate_yty = macro_func.get_data('M0001383,M0001385,M5525763,M0009970,M5525766,M5525767,M5525769,M6179510','2010-01-01','','edb')
money_aggregate_yty_two_year = macro_func.two_average(money_aggregate_yty)

# 做货币总量投放的同比季节性图
for i in money_aggregate_yty.columns:
    macro_func.plot_seasonal(money_aggregate_yty[[i]])
    macro_func.plot_seasonal(money_aggregate_yty_two_year[[i]],tl='两年平均增速')

money_aggregate_yty.columns=['M1','M2','社融','贷款','委托贷款','信托贷款','企业债券','政府债券']
money_aggregate_yty_two_year.columns=['M1','M2','社融','贷款','委托贷款','信托贷款','企业债券','政府债券']
money_aggregate_yty['2018':].iplot(subplots=True,legend=False,subplot_titles=True,shape=(1,8),title='主要金融数据的存量增速',dimensions=(1400,400))
money_aggregate_yty_two_year['2018':].iplot(subplots=True,legend=False,subplot_titles=True,shape=(1,8),title='主要金融数据的存量增速（两年平均）',dimensions=(1400,400))

# 做货币总量投放的环比季节性图
money_aggregate = macro_func.get_data('M5525755,M5525756,M5525758,M5525759,M5525760,M5525761,M5525762,M6179494','2010-01-01','','edb')
money_aggregate_mtm = money_aggregate.pct_change()*100
for i in money_aggregate_mtm.columns:
    macro_func.plot_seasonal(money_aggregate_mtm[[i]],tl='的环比')

# 社融与M2缺口与10年国债
tsf_aggregate = macro_func.get_data('M0001385,M5525763','2010-01-01','','edb')
tsf_aggregate['tsf_m2'] = tsf_aggregate['M5525763']-tsf_aggregate['M0001385']
gb_10Y = macro_func.get_data('M1001654','2010-01-01','','edb')
gb_10Y = gb_10Y.resample('M').mean()
tsf_aggregate = tsf_aggregate.join(gb_10Y,how='outer')
tsf_aggregate.fillna(method='ffill', inplace=True)
tsf_aggregate[['tsf_m2','M1001654']].iplot(title='社融与M2增速之差（蓝）与国债收益率（橙）',secondary_y='M1001654',legend=False,size=3)

# 做超储率的季节性图
Excess_RRR = macro_func.get_data('M0010096','2001-01','','edb')
macro_func.plot_seasonal(Excess_RRR, 4)

# 做资金面的图
fund_rates = macro_func.get_data('M0220162,M0220163,M0041653,M0041371,M0017142,M0017143,M0017145,M0329545,M1001654','2010-01-01','','edb')
fund_rates[['M0041371']] = fund_rates[['M0041371']].fillna(method='ffill')
fund_rates[['M0329545']] = fund_rates[['M0329545']].fillna(method='ffill')
fund_rates.columns=['DR001','DR007','R007','OMO7D','shibor3M','shibor6M','shibor1Y','MLF1Y','GB10Y']

print(fund_rates.tail(),end='\n\n')

fund_rates[['DR001','DR007','R007','OMO7D']]['2020':].iplot(title='DR007和R007')
fund_rates[['shibor3M','shibor6M','shibor1Y','MLF1Y']]['2020':].iplot(title='3个月、6个月和1年期SHIBOR')

fund_rates.eval(
    '''
    DR007_DR001_spread = DR007-DR001
    R007_DR007_spread = R007-DR007
    DR007_OMO7D_spread = DR007-OMO7D
    shibor1Y_DR007_spread = shibor1Y-DR007
    shibor1Y_MLF1Y_spread = shibor1Y-MLF1Y
    GB10Y_OMO7D_spread = GB10Y-OMO7D
    ''',
    inplace=True
)
macro_func.pct_plot(fund_rates[['DR007_DR001_spread']]['2016':])
macro_func.pct_plot(fund_rates[['R007_DR007_spread']]['2016':])
macro_func.pct_plot(fund_rates[['DR007_OMO7D_spread']]['2016':])
macro_func.pct_plot(fund_rates[['shibor1Y_DR007_spread']]['2016':])
macro_func.pct_plot(fund_rates[['shibor1Y_MLF1Y_spread']]['2016':])
macro_func.pct_plot(fund_rates[['GB10Y_OMO7D_spread']]['2016':])
macro_func.plot_seasonal(fund_rates[['DR001']].resample('M').mean(),3,tl='的季节性')
macro_func.plot_seasonal(fund_rates[['DR007']].resample('M').mean(),3,tl='的季节性')
macro_func.plot_seasonal(fund_rates[['R007']].resample('M').mean(),3,tl='的季节性')
macro_func.plot_seasonal(fund_rates[['shibor1Y']].resample('M').mean(),3,tl='的季节性')

# 做贷款利率的季节性图
Lending_rate = macro_func.get_data('M0058003','2013-10','','edb')
macro_func.plot_seasonal(Lending_rate, 3)

# # 一般贷款利率和新增企业中长期贷款的季调比较
# lending = macro_func.get_data('M0058003,M0057877','2008-10','','edb')
# lending = lending.resample('Q').mean().fillna(method='ffill')
# for i in lending.columns:
#     lending[[i]]=macro_func.seasonal_adj(lending[[i]],fq='Q')
# lending.columns = macro_func.config(lending)
# lending.iplot(secondary_y=['企业长贷'],title='季调后的贷款利率与新增贷款-企业贷款',legend={'orientation':'h','x':0.2,'y':-0.1})

# # 个人住房贷款利率和新增居民中长期贷款的季调比较
# lending = macro_func.get_data('M0058005,M0057875','2008-10','','edb')
# lending = lending.resample('Q').mean().fillna(method='ffill')
# for i in lending.columns:
#     lending[[i]]=macro_func.seasonal_adj(lending[[i]],fq='Q')
# lending.columns = macro_func.config(lending)
# lending.iplot(secondary_y=['居民长贷'],title='季调后的贷款利率与新增贷款-居民贷款',legend={'orientation':'h','x':0.2,'y':-0.1})

# # 票据融资利率和新增票据融资的季调比较
# lending = macro_func.get_data('M0058004,M0048260','2008-10','','edb')
# lending = lending.resample('Q').mean().fillna(method='ffill')
# for i in lending.columns:
#     lending[[i]]=macro_func.seasonal_adj(lending[[i]],fq='Q')
# lending.columns = macro_func.config(lending)
# lending.iplot(secondary_y=['票据融资'],title='季调后的贷款利率与新增贷款-票据融资',legend={'orientation':'h','x':0.2,'y':-0.1})

# 做新增社融数据的季节性图
tsf = macro_func.get_data('M5206730,M5206731,M0048260,M0057874,M0057875,M0057876,M0057877,M5540101,M5206733,M5206734,M5206735,M5206736,M5206737,M6179492,M6094226,M6094227','2013-10','','edb')
for i in tsf.columns:
    macro_func.plot_seasonal(tsf[[i]])

# # 新增社融数据的季调后数据
# tsf = macro_func.get_data('M5206730,M5206731,M0048260,M0057874,M0057875,M0057876,M0057877,M5206733,M5206734,M5206735,M5206736,M5206737','2009-01','','edb')
# for i in tsf.columns:
#     tsf[[i]]=macro_func.seasonal_adj(tsf[[i]],fq='M')
# gb_bond = macro_func.get_data('M6179492','2017-01','','edb')
# gb_bond[['M6179492']]=macro_func.seasonal_adj(gb_bond[['M6179492']],fq='M')
# for i in tsf.columns:
#     macro_func.plot_seasonal(tsf[[i]],tl='_季调')
# macro_func.plot_seasonal(gb_bond,tl='_季调')

# 做M0、M1、M2的月环比的季节性图
M = macro_func.get_data('M0001380,M0001382,M0001384','2013-10','','edb')
M = M - M.shift(1)
for i in M.columns:
    macro_func.plot_seasonal(M[[i]],tl='的月环比变动')

# 做新增存款的季节性图
deposit = macro_func.get_data('M0009942,M0009943,M0057879,M0009945,M5540102','2013-10','','edb')
for i in deposit.columns:
    macro_func.plot_seasonal(deposit[[i]])

# 做结构性存款的变动图
stru_deposit = macro_func.get_data('M0062889,M0252073,M0062897,M0252083','2013-10','','edb')
stru_deposit.columns = macro_func.config(stru_deposit)
stru_deposit['2019':].iplot(subplots=True,shared_yaxes=True,subplot_titles=True,legend=False,title='结构性存款的变动',dimensions=(1000,400))

# 做股票指数估值水平的图
# 取沪深300的市盈率-wind计算
from WindPy import w
w.start()
hs300 = w.wsd("000300.SH", "pe_ttm", "2012-01-01", "", "")
hs300 = pd.DataFrame(np.array(hs300.Data).T, columns=hs300.Codes, index=hs300.Times)

valuation = macro_func.get_data('M1001654,M0332214,M0330956,M0330172,M0020209','2012-01-01','','edb')
valuation = valuation.join(hs300)

valuation.eval(
    '''
    value_kc50 = 100/M0332214
    value_zz500 = 100/M0330956
    value_hs300 = 100/M0330172
    ''',
    inplace=True
)
valuation['value_hs300_wind'] = 100/valuation['000300.SH']
valuation['value_rela'] = valuation['value_hs300_wind']/valuation['M1001654']
# valuation.columns = macro_func.config(valuation)
valuation[['value_hs300_wind','M1001654']]['2011-07':].iplot(kind='ratio',title='沪深300股息率（蓝）与10年期国债（橙）的估值比较',legend=False)
macro_func.pct_plot(valuation[['value_rela']])
valuation[['value_hs300_wind','M0020209']].iplot(secondary_y='M0020209',title='沪深300的股息率（蓝）与指数（橙）',legend=False)
macro_func.pct_plot(valuation[['000300.SH']])

# 国债的发行与到期数据
def convert_data(raw):
    """
    把Wind数据转换成DataFrame格式
    
    :raw: WindData
        待转换的Wind数据
    """
    # 把列表数据转换成DataFrame格式
    data = pd.DataFrame(np.array(raw.Data),
                        index=raw.Fields,
                        columns=raw.Codes).T
    data = data.iloc[:,[0, 2, 4, 5]] # 选择需要的数据
    data.columns = ['date', 'gb_IssueAmount', 'gb_MaturityAmount', 'gb_NetIssue'] # 重命名列
    data = data.set_index('date') # 设置时间索引
    data = data.astype(float)
    return data

def get_wind_param(start='2010-01-01', bondid='a101020100000000'):
    base = f"startdate={start};" \
           f"frequency=monthly;" \
           f"maingrade=all;" \
           f"zxgrade=all;" \
           f"datetype=startdate;" \
           f"type=default;" \
           f"bondtype=default;" \
           f"bondid={bondid}"
    return base

from WindPy import w
# 启动WinPy接口
w.start()
# 提取国债的发行与到期数据
param = get_wind_param(start='2014-01-01', bondid='a101020100000000')
raw = w.wset("bondissuanceandmaturity", param)
data = convert_data(raw)    # 转换为DataFrame并提取关键列
for i in data.columns:
    macro_func.plot_seasonal(data[[i]],3)

# 地方债的发行与到期数据
def convert_data(raw):
    """
    把Wind数据转换成DataFrame格式
    
    :raw: WindData
        待转换的Wind数据
    """
    # 把列表数据转换成DataFrame格式
    data = pd.DataFrame(np.array(raw.Data),
                        index=raw.Fields,
                        columns=raw.Codes).T
    data = data.iloc[:,[0, 2, 4, 5]] # 选择需要的数据
    data.columns = ['date', 'lgb_IssueAmount', 'lgb_MaturityAmount', 'lgb_NetIssue'] # 重命名列
    data = data.set_index('date') # 设置时间索引
    data = data.astype(float)
    return data

def get_wind_param(start='2010-01-01', bondid='a101020200000000'):
    base = f"startdate={start};" \
           f"frequency=monthly;" \
           f"maingrade=all;" \
           f"zxgrade=all;" \
           f"datetype=startdate;" \
           f"type=default;" \
           f"bondtype=default;" \
           f"bondid={bondid}"
    return base

from WindPy import w
# 启动WinPy接口
w.start()
# 提取国债的发行与到期数据
param = get_wind_param(start='2014-01-01', bondid='a101020200000000')
raw = w.wset("bondissuanceandmaturity", param)
data = convert_data(raw)    # 转换为DataFrame并提取关键列
for i in data.columns:
    macro_func.plot_seasonal(data[[i]],3)

# 同业存单的发行与到期数据
def convert_data(raw):
    """
    把Wind数据转换成DataFrame格式
    
    :raw: WindData
        待转换的Wind数据
    """
    # 把列表数据转换成DataFrame格式
    data = pd.DataFrame(np.array(raw.Data),
                        index=raw.Fields,
                        columns=raw.Codes).T
    data = data.iloc[:,[0, 2, 4, 5]] # 选择需要的数据
    data.columns = ['date', 'cd_IssueAmount', 'cd_MaturityAmount', 'cd_NetIssue'] # 重命名列
    data = data.set_index('date') # 设置时间索引
    data = data.astype(float)
    return data

def get_wind_param(start='2010-01-01', bondid='a101020100000000'):
    base = f"startdate={start};" \
           f"frequency=monthly;" \
           f"maingrade=all;" \
           f"zxgrade=all;" \
           f"datetype=startdate;" \
           f"type=default;" \
           f"bondtype=default;" \
           f"bondid={bondid}"
    return base

from WindPy import w
# 启动WinPy接口
w.start()
# 提取同业存单的发行与到期数据
param = get_wind_param(start='2014-01-01', bondid='1000011872000000')
raw = w.wset("bondissuanceandmaturity", param)
data = convert_data(raw)    # 转换为DataFrame并提取关键列
for i in data.columns:
    macro_func.plot_seasonal(data[[i]],3)

