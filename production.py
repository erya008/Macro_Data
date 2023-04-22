from os import getpid
import pandas as pd
import numpy as np
import cufflinks as cf
import macro_func

# 导入需要的包
cf.set_config_file(offline=True,theme='white',dimensions=(550,350),colorscale='plotly')

# # 主要需求指标概览
# main_demand = macro_func.get_data('M0000545,M5767203,M0000612,M0001227,M0000607,M0000609,M0001428,M0061659,M0061660,M0000273,S0029657,M0000357,M5440435,M5531328','2016-01-01','','edb')
# main_demand.columns = macro_func.config(main_demand)
# main_demand.to_csv(r'C:\Users\wanzh\OneDrive\金阳宏观\课题\两年平均增速/main_demand_raw_data.csv',encoding='utf_8_sig')
# main_demand = macro_func.two_average(main_demand)
# main_demand.to_csv(r'C:\Users\wanzh\OneDrive\金阳宏观\课题\两年平均增速/main_demand_two_year_average.csv',encoding='utf_8_sig')
# main_demand_q = main_demand.resample('Q').mean().fillna(method='ffill')
# main_demand_q.to_csv(r'C:\Users\wanzh\OneDrive\金阳宏观\课题\两年平均增速/main_demand_q.csv',encoding='utf_8_sig')

# GDP同比数据
gdp_yty = macro_func.get_data('M0039354,M5567901,M5567902,M5567903','2005-01-01','','edb')
gdp_yty['2019':].iplot(title='GDP（蓝）、第一产业（橙）、第二产业（绿）、第三产业（红）',kind='bar',legend=False)
gdp_yty.loc['2021-03'] = (np.sqrt(np.array(1+gdp_yty.loc['2020-03']/100)*np.array(1+gdp_yty.loc['2021-03']/100))-1)*100
gdp_yty.loc['2021-06'] = (np.sqrt(np.array(1+gdp_yty.loc['2020-06']/100)*np.array(1+gdp_yty.loc['2021-06']/100))-1)*100
gdp_yty.loc['2021-09'] = (np.sqrt(np.array(1+gdp_yty.loc['2020-09']/100)*np.array(1+gdp_yty.loc['2021-09']/100))-1)*100
gdp_yty.loc['2021-12'] = (np.sqrt(np.array(1+gdp_yty.loc['2020-12']/100)*np.array(1+gdp_yty.loc['2021-12']/100))-1)*100
gdp_yty.loc['2020-03'] = np.nan
gdp_yty.loc['2020-06'] = np.nan
gdp_yty['2019':].iplot(title='GDP（蓝）、第一产业（橙）、第二产业（绿）、第三产业（红）',kind='bar',legend=False)

# 分行业的GDP同比数据
gdp_industry_yty = macro_func.get_data('M5567904,M5567905,M5784264,M5567906,M5567907,M5567908,M5567909,M5567910,M5567911,M5784265,M5784266,M5567912','2015-01-01','','edb')
gdp_industry_yty.loc['2021-03'] = (np.sqrt(np.array(1+gdp_industry_yty.loc['2020-03']/100)*np.array(1+gdp_industry_yty.loc['2021-03']/100))-1)*100
gdp_industry_yty.loc['2021-06'] = (np.sqrt(np.array(1+gdp_industry_yty.loc['2020-06']/100)*np.array(1+gdp_industry_yty.loc['2021-06']/100))-1)*100
gdp_industry_yty.loc['2021-09'] = (np.sqrt(np.array(1+gdp_industry_yty.loc['2020-09']/100)*np.array(1+gdp_industry_yty.loc['2021-09']/100))-1)*100
gdp_industry_yty.loc['2021-12'] = (np.sqrt(np.array(1+gdp_industry_yty.loc['2020-12']/100)*np.array(1+gdp_industry_yty.loc['2021-12']/100))-1)*100
gdp_industry_yty.loc['2020-03'] = np.nan
gdp_industry_yty.loc['2020-06'] = np.nan
for i in gdp_industry_yty.columns:
    macro_func.plot_seasonal(gdp_industry_yty[[i]])

# GDP环比数据
gdp_qtq = macro_func.get_data('M0061567','2010-01-01','','edb')
macro_func.plot_seasonal(gdp_qtq)

# 服务业生产指数
service_production = macro_func.get_data('M5767203','2011-01-01','','edb')
service_production = macro_func.two_average(service_production)
macro_func.plot_seasonal(service_production)

# 服务业生产指数-累计同比，适用于1-2月
service_production_ytd = macro_func.get_data('M6001405','2011-01-01','','edb')
service_production_ytd = macro_func.two_average(service_production_ytd)
macro_func.plot_seasonal(service_production_ytd)

# 工业增加值的疫情前后趋势对比
iv_series = macro_func.value_yty_adj('M5567963,M0000545','2000-01')
iv_series = macro_func.seasonal_adj(iv_series)
iv_series = np.log(iv_series)
iv_series = macro_func.trend_trace(iv_series,'工业增加值','2018-01','2019-12')

# 工业增加值的同比
iv_yty = macro_func.get_data('M0000545,M0096211,M0096212,M0096213,M0330955,M6512871,M0000548,M0000551,M0000552,M0000553','2013-01-01','','edb')
iv_yty = macro_func.two_average(iv_yty)
for i in iv_yty:
    macro_func.plot_seasonal(iv_yty[[i]])

# 工业增加值的累计同比-适用于1-2月
iv_yty_ytd = macro_func.get_data('M0000011,M0096214,M0096215,M0096216,M0330930,M0330931,M0000014,M0000017,M0000018,M0000019','2013-01-01','','edb')
iv_yty_ytd = macro_func.two_average(iv_yty_ytd)
for i in iv_yty_ytd:
    macro_func.plot_seasonal(iv_yty_ytd[[i]])

# 工业增加值的环比
iv_mtm = macro_func.get_data('M0061571','2011-01-01','','edb')
iv_mtm = iv_mtm.drop(index=iv_mtm[abs(iv_mtm['M0061571'])>10].index)
macro_func.plot_seasonal(iv_mtm)

# 工业增加值的分行业同比
iv_industry_yty = macro_func.get_data('M0000032,M0000034,M0000040,M0000058,M0000060,M0068077,M0000068,M0000070,M0000072,M0000074,M0000076,M0000078,M0068071,M0000080,M0000082,M0000084,M0000092','2013-01-01','','edb')
iv_industry_yty = macro_func.two_average(iv_industry_yty)
for i in iv_industry_yty:
    macro_func.plot_seasonal(iv_industry_yty[[i]])

# 工业增加值的分行业累计同比-适用于1-2月
iv_industry_ytd = macro_func.get_data('M0000033,M0000035,M0000041,M0000059,M0000061,M0068078,M0000069,M0000071,M0000073,M0000075,M0000077,M0000079,M0068072,M0000081,M0000083,M0000085,M0000093','2013-01-01','','edb')
iv_industry_ytd = macro_func.two_average(iv_industry_ytd)
for i in iv_industry_ytd:
    macro_func.plot_seasonal(iv_industry_ytd[[i]])

# 主要工业产品产量
products_yty = macro_func.get_data('S0027100,S0027160,S0027703,S0027711,S0027375,S0027552,S0027564,S0243302,S0243303,S0243304,S0028195,S0243306,S0028183,S0026990,S0026998,S0073099,S0027013','2015-01-01','','edb')
products_yty = macro_func.two_average(products_yty)
for i in products_yty.columns:
    macro_func.plot_seasonal(products_yty[[i]])

# 主要工业产品产量-累计同比，适用于1-2月
products_ytd = macro_func.get_data('S0027102,S0027162,S0027705,S0027713,S0027377,S0027554,S0027566,S0243312,S0243313,S0243314,S0028197,S0243316,S0028185,S0026992,S0027000,S0073169,S0027015','2015-01-01','','edb')
products_ytd = macro_func.two_average(products_ytd)
for i in products_ytd.columns:
    macro_func.plot_seasonal(products_ytd[[i]])

# 2021年之前没有1月数据，所以单写一个函数
def two_average_new(data):
    _data = data.copy()
    _data.loc['2021-02'] = (np.sqrt(np.array(1+_data.loc['2020-02']/100)*np.array(1+_data.loc['2021-02']/100))-1)*100
    _data.loc['2021-03'] = (np.sqrt(np.array(1+_data.loc['2020-03']/100)*np.array(1+_data.loc['2021-03']/100))-1)*100
    _data.loc['2021-04'] = (np.sqrt(np.array(1+_data.loc['2020-04']/100)*np.array(1+_data.loc['2021-04']/100))-1)*100
    _data.loc['2021-05'] = (np.sqrt(np.array(1+_data.loc['2020-05']/100)*np.array(1+_data.loc['2021-05']/100))-1)*100
    _data.loc['2021-06'] = (np.sqrt(np.array(1+_data.loc['2020-06']/100)*np.array(1+_data.loc['2021-06']/100))-1)*100
    _data.loc['2021-07'] = (np.sqrt(np.array(1+_data.loc['2020-07']/100)*np.array(1+_data.loc['2021-07']/100))-1)*100
    _data.loc['2021-08'] = (np.sqrt(np.array(1+_data.loc['2020-08']/100)*np.array(1+_data.loc['2021-08']/100))-1)*100
    _data.loc['2021-09'] = (np.sqrt(np.array(1+_data.loc['2020-09']/100)*np.array(1+_data.loc['2021-09']/100))-1)*100
    _data.loc['2021-10'] = (np.sqrt(np.array(1+_data.loc['2020-10']/100)*np.array(1+_data.loc['2021-10']/100))-1)*100
    _data.loc['2021-11'] = (np.sqrt(np.array(1+_data.loc['2020-11']/100)*np.array(1+_data.loc['2021-11']/100))-1)*100
    _data.loc['2021-12'] = (np.sqrt(np.array(1+_data.loc['2020-12']/100)*np.array(1+_data.loc['2021-12']/100))-1)*100
    _data.loc['2020-01'] = np.nan
    _data.loc['2020-02'] = np.nan
    _data.loc['2020-03'] = np.nan
    _data.loc['2020-04'] = np.nan
    _data.loc['2020-05'] = np.nan
    _data.loc['2020-06'] = np.nan
    return(_data)

# 用电量同比和环比
electricity_yty = macro_func.get_data('S5100122,S5100124,S5100125,S5100126','2015-01-01','','edb')
electricity_yty = two_average_new(electricity_yty)
for i in electricity_yty.columns:
    macro_func.plot_seasonal(electricity_yty[[i]])
electricity_mtm = macro_func.get_data('S5100223,S5100226,S5100227','2015-01-01','','edb')
for i in electricity_mtm.columns:
    macro_func.plot_seasonal(electricity_mtm[[i]])

# 原煤产量的趋势比较
# 原始数据一定要做季节性调整，然后取对数
# 根据疫情前的样本期外推趋势，并与疫情后走势对标
# data是季调后数据，tl是数据名称，sample_start是样本期起点，sample_end是样本期终点
# plot_start是作图的起点
# 原煤产量在1月和2月缺失值，需要先填补缺失值
# 在填补缺失值之前，要先手动补充缺失的月份，否则会报错
coal = macro_func.get_data('S0026989','2010-01-01','','edb')
coal = macro_func.fill_index(coal)
coal = macro_func.na_fill_na(coal)
coal = macro_func.seasonal_adj(coal)
coal = np.log(coal)
coal = macro_func.trend_trace(coal,'产量：原煤','2018-01','2019-12')
# trend_trace(data, tl, sample_start, sample_end, plot_start='2015')

# 发电量产量的趋势比较
# 原始数据一定要做季节性调整，然后取对数
# 根据疫情前的样本期外推趋势，并与疫情后走势对标
# data是季调后数据，tl是数据名称，sample_start是样本期起点，sample_end是样本期终点
# plot_start是作图的起点
# 发电量在1月和2月缺失值，需要先填补缺失值
# 在填补缺失值之前，要先手动补充缺失的月份，否则会报错
electricity = macro_func.get_data('S0027012','2010-01-01','','edb')
electricity = macro_func.fill_index(electricity)
electricity = macro_func.na_fill_na(electricity)
electricity = macro_func.seasonal_adj(electricity)
electricity = np.log(electricity)
electricity = macro_func.trend_trace(electricity,'产量：发电量','2018-01','2019-12')
# trend_trace(data, tl, sample_start, sample_end, plot_start='2015')

# 粗钢产量的趋势比较
# 原始数据一定要做季节性调整，然后取对数
# 根据疫情前的样本期外推趋势，并与疫情后走势对标
# data是季调后数据，tl是数据名称，sample_start是样本期起点，sample_end是样本期终点
# plot_start是作图的起点
# 粗钢在1月和2月缺失值，需要先填补缺失值
# 在填补缺失值之前，要先手动补充缺失的月份，否则会报错
steel = macro_func.get_data('S0027374','2010-01-01','','edb')
steel = macro_func.fill_index(steel)
steel = macro_func.na_fill_na(steel)
steel = macro_func.seasonal_adj(steel)
steel = np.log(steel)
steel = macro_func.trend_trace(steel,'产量：粗钢','2018-01','2019-12')
# trend_trace(data, tl, sample_start, sample_end, plot_start='2015')

# 高频工业生产指标
products_rate = macro_func.get_data('C1925068,S6124651,S6124650,S5449386,S5417017,S5446174,Z0381034,D1081308,S5123779,S0247603','2013-10','','edb')
products_rate = products_rate.resample('M').mean()
for i in products_rate:
    macro_func.plot_seasonal(products_rate[[i]])