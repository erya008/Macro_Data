import os
# from matplotlib.cbook import flatten
import pandas as pd
import numpy as np
from datetime import datetime
import cufflinks as cf
from statsmodels.tsa.x13 import x13_arima_analysis
from scipy.interpolate import interp1d
from sklearn import linear_model
from WindPy import w
from wotan import flatten
from scipy import signal
from statsmodels.tsa.arima.model import ARIMA

# from fredapi import Fred
# fred = Fred(api_key='014e29301e011aa7d9e1e1d8051bbd4e')
# M2NS = fred.get_series('M2NS')

cf.set_config_file(offline=True,theme='white',dimensions=(550,350),colorscale='plotly')

# 从WIND接口取数的函数，tickers是代码，start是起始时间
# end是结束时间，一般用空值，代表最新
# method：edb，宏观数据库，wsd，价格序列
# 数据初始化时即填充日期序列
def get_data(tickers, start, end, method):
    w.start()

    if method == 'edb':
        _data = w.edb(tickers, start, end, "Fill=Blank")
        _data = pd.DataFrame(np.array(_data.Data).T, columns=_data.Codes, index=_data.Times)
    elif method == 'wsd':
        _data = w.wsd(tickers, "close", start, end, "")
        _data = pd.DataFrame(np.array(_data.Data).T, columns=_data.Codes, index=_data.Times)
    else:
        print("You may input the wrong arguments.")
    # w.close()

    _data.index = pd.to_datetime(_data.index, format="%Y-%m-%d")
    return _data

# 把时间序列转换成按月度排列的季节性序列
def trans_seasonal(data, k):
    data['year'] = data.index.year
    data['month'] = data.index.month
    _col = data.columns.values[0]
    _data = data.pivot_table(index='month', columns='year', values=_col)
    _data['历史平均'] = np.mean(_data.iloc[:, -(k+1):-1], axis=1)
    # print('季节性重排后的数据是：', f'{config(data)}')
    return _data.iloc[:, -(k+2):]

# 把月度排列的季节性序列做成图 
def plot_seasonal(data, k=4, tl=''):
    _data = trans_seasonal(data, k)
    _data.iplot(mode='lines+markers',title=config(data)[0]+tl,symbol='triangle-up',size=6,width=1,dash='dash')

# 计算历史上90%、75%、50%、25%、10%分位数
def pct_compute(data):
    _data = []
    _data.append(data.quantile(0.9).values[0])
    _data.append(data.quantile(0.75).values[0])
    _data.append(data.quantile(0.5).values[0])
    _data.append(data.quantile(0.25).values[0])
    _data.append(data.quantile(0.1).values[0])
    print(f'{config(data)}的分位数是：',[float('%.3f' %x) for x in _data])
    return _data

# 做分位数图
def pct_plot(data,tl=''):
    _pct = pct_compute(data)
    data.iplot(title=config(data)[0]+tl,hline=[dict(y=i,color=j,dash='dash') for i,j in zip(_pct,['orange','pink','gray','violet','green'])])

# 将Wind代码转换成语义，用于作图
def config(data):
    # _data是一个DataFrame，第1列：WindID是索引列
    _data = pd.read_csv('mapping.csv',index_col=0)
    # _config是一个Series，astype转换成文本类型
    _config = _data['SeriesID'].astype(str)
    # _col0是待处理数据的列名(变量名)
    _col0 = data.columns.values
    # 增加一个待处理数据变量名的判断，避免作图错误
    _col = _config[_col0].values
    return _col

# # 将Wind代码转换成语义，用于作图
# def config(data):
#     # _data是一个DataFrame，第1列：WindID是索引列
#     _data = pd.read_csv('mapping.csv',index_col=0)
#     # _config是一个Series，astype转换成文本类型
#     _config = _data['SeriesID'].astype(str)
#     # _col0是待处理数据的列名(变量名)
#     _col0 = data.columns.values
#     # 增加一个待处理数据变量名的判断，避免作图错误
#     if _col0 in _config.index.values :
#         _col = _config[_col0].values
#         return _col
#     else :
#         return ' '

# 补齐完整的日期索引
def fill_index(data):
    _start = data.index[0].strftime('%Y-%m-%d')
    _end = data.index[-1].strftime('%Y-%m-%d')
    _w = pd.date_range(_start, _end, freq='M')
    _data = data.reindex(_w)
    _data.index = pd.to_datetime(_data.index, format="%Y-%m-%d")
    return _data

# 查找并显示缺失值
def na_check(data):
    for _columnname in data.columns:
        if data[_columnname].count() != len(data):
            _loc = data[data[_columnname].isnull().values==True].index.strftime('%Y-%m-%d').tolist()
            for i in _loc:
                print('变量："{}"的位置："{}"有缺失值'.format(_columnname,i))
        else:
            print('变量："{}"不存在缺失值'.format(_columnname))

# 适用于单月缺失填补，用scipy包的interpolate函数，使用三阶样条函数法
def na_fill_na(data):
    _data = fill_index(data)
    _data = _data.reset_index()
    _x = np.array(_data[_data.iloc[:,1].notnull()].index)
    _y = np.array(_data[_data.iloc[:,1].notnull()].iloc[:,1])
    _xnew = np.array(_data.index)

    f = interp1d(_x, _y, kind='cubic', fill_value="extrapolate")

    _data = pd.DataFrame(f(_xnew), index=data.index, columns=data.columns)
    return _data

# 适用于单月值序列中1-2月是累计值的缺失填补，用过去三个月补充1月缺失值，用1-2月累计数据，减去1月的补充缺失值
def na_fill_cusum(data):
    _data = fill_index(data)
    _data = _data.reset_index()
    _na_index = _data[_data.isnull().values==True].index.tolist()
    for i in _na_index:
        _data.iloc[i,1]=_data.iloc[i-3:i,1].mean()
        _data.iloc[i+1,1]=_data.iloc[i+1,1]-_data.iloc[i,1]
    _data = _data.set_index('index', "%Y-%m-%d")
    return _data

# 适用于累计值累计同比序列中1月的填补，用1-2月累计数据的一半，作为1月值
# 用1-2月累计同比，作为1月同比
def na_fill_total(data):

    _data = fill_index(data)
    _data = _data.reset_index()
    _na_index = _data[_data.isnull().values==True].index.tolist()
    for i in _na_index:
        _data.iloc[i,1]=_data.iloc[i+1,1]/2
        _data.iloc[i,2]=_data.iloc[i+1,2]
    _data = _data.set_index('index', "%Y-%m-%d")
    return _data

# 适用于累计值序列中，1月缺失值的填补，用1-2月累计数据的一半，作为1月值
# 填充1月缺失值后，可以再用差分转换成当月值
def na_fill_jan(data):

    _data = fill_index(data)
    _data = _data.reset_index()
    _na_index = _data[_data.isnull().values==True].index.tolist()
    for i in _na_index:
        _data.iloc[i,1]=_data.iloc[i+1,1]/2
    _data = _data.set_index('index', "%Y-%m-%d")
    return _data

# 累计值通过差分转换成当月值
# 1月值保持不变，年内做差分
def cusum_m(data):
    _data = fill_index(data)
    _data['month'] = _data.index.month
    for i in range(len(_data)-1,0,-1):
        if _data.iloc[i]['month'] > 1:
            _data.iloc[i] = _data.iloc[i] - _data.iloc[i-1]
    _data = _data.drop('month',axis=1)
    return _data

# 累计值通过差分转换成当季值
# 3月值保持不变，年内按季度做差分，并保留季度值
def cusum_q(data):
    _data = fill_index(data)
    _data['month'] = _data.index.month
    while _data.iloc[0].month != 3:
        _data.drop(_data.head(1).index, inplace=True)
    while _data.iloc[-1].month % 3 != 0:
        _data.drop(_data.tail(1).index, inplace=True)
    _data = _data.resample('Q').last()
    for i in range(len(_data)-1,0,-1):
        if _data.iloc[i]['month'] > 3:
            _data.iloc[i] = _data.iloc[i] - _data.iloc[i-1]
    _data = _data.drop('month',axis=1)
    return _data

path_sa = os.getcwd() # 获取当前文件夹地址
# 把生成的春节数据dat文件转换成DataFrame格式
def gel_hol(name):
    with open('{}\\hol_files\\{}.dat'.format(path_sa, name), 'r') as f:
        _data = f.readlines()
    
    _data = pd.DataFrame(_data)
    _holiday = pd.DataFrame()
    _data = _data[0].str.split(' ', expand=True)
    _holiday['hol'] = _data[4]
    _holiday.index = pd.date_range('1901-01-31','2050-12-31',freq='M')
    
    return _holiday

# 调用Python的X-13模块做季节性调整
# fq='M'是月度序列，fq='Q'是季度序列
# mode=是春节调整的模式
def seasonal_adj(data, log=None, fq='M', mode='hol_save_7_14'):
    path = '{}\\x13as.exe'.format(path_sa)
    hol = gel_hol(mode)
    if fq == 'M':
        _sa = x13_arima_analysis(data, log=log, x12path=path, freq=fq, exog=hol)
    elif fq == 'Q':
        _sa = x13_arima_analysis(data, log=log, x12path=path, freq=fq)

    _result_seasonal = _sa.seasadj.to_frame()
    _name = data.columns[0]
    _result_seasonal.rename(columns={'seasadj': _name}, inplace=True)
    return _result_seasonal

# 获得X-13季节性调整的季调因子
# 季调因子是自己使用原始序列和季调后序列计算
# 增加log选项，0是加法模型，1是乘法模型
def seasonal_adj_factor(data, log=0, fq='M', mode='hol_save_7_14'):
    _result_seasonal = seasonal_adj(data, log=log, fq=fq, mode=mode)
    if log == 0:
        _result_factor = data - _result_seasonal
    elif log == 1:
        _result_factor = data/_result_seasonal
    else:
        print('You may input the wrong log option')
    _result_factor.columns = [_result_factor.columns[0]+'_factor']
    return _result_factor

# 把同时有累计值和累计同比的指标的累计同比折算成当月同比
# tickers中包含两个指标，第一个指标是累计值，第二个是累计增速
def cusum_mtm(tickers, start, end):
    _data = get_data(tickers, start, end, method='edb')
    _data = na_fill_total(_data)
    _data['new'] = np.nan

    for i in range(12,len(_data)):
        _data.iloc[i,2] = _data.iloc[i-12,0] * (1+_data.iloc[i,1]/100)
    _data = cusum_m(_data)
    _data.iloc[:,0] = (_data.iloc[:,2]/_data.shift(12).iloc[:,0]-1)*100
    return _data.iloc[:,0].to_frame()


# 把同时有累计值和累计同比的指标，折算出当月值
# tickers中包含两个指标，第一个指标是累计值，第二个是累计增速
def cusum_mtm_series(tickers, start, base=2019):
    # 获取并填充序列
    _data = get_data(tickers, start, '', method='edb')
    _data = na_fill_total(_data)
    _data['new'] = np.nan

    # 折算当月同比
    for i in range(12,len(_data)):
        _data.iloc[i,2] = _data.iloc[i-12,0] * (1+_data.iloc[i,1]/100)
    _data = cusum_m(_data)
    _data.iloc[:,1] = (_data.iloc[:,2]/_data.shift(12).iloc[:,0]-1)*100
    _data.iloc[:,0] = _data.iloc[:,2]
    _data.drop(['new'], axis=1, inplace=True)

    _data['year'] = _data.index.year
    _data = _data.reset_index()
    # 提取基期的index
    _index = _data[_data.year==base].index.tolist()

    _data['new'] = np.nan

    # 将第四列作为新数据，根据2019年当月值和折算的当月同比，生成月度值
    for i in _index:
        _data.iloc[i,4] = _data.iloc[i,1]

    for j in range(0,_index[0]//12+1): # 注意+1
        for i in _index:
            if i-12*(j+1) >= 0: # 增加一个是否为负的判断
                _data.iloc[i-12*(j+1),4] = _data.iloc[i-12*j,4] / (1 + _data.iloc[i-12*j,2]/100) # 注意计算公式
    
    for j in range(0,(len(_data)-_index[-1])//12+1): # 注意+1
        for i in _index:
            if i+12*(j+1) <= len(_data)-1: # 增加一个是否超限的判断
                _data.iloc[i+12*(j+1),4] = _data.iloc[i+12*j,4] * (1 + _data.iloc[i+12*(j+1),2]/100) # 注意计算公式
        
    _data = _data.set_index('index')
    _data.index = pd.to_datetime(_data.index, format="%Y-%m-%d")
    # 更换列名，用当月值的列名代替
    _name = _data.columns[0]
    _data.rename(columns={'new': _name}, inplace=True)
    # 去掉第0行，因为第0行是缺失值，影响季节性调整
    _data.drop(index=_data.index[0], inplace=True)
    return _data.iloc[:,3].to_frame()

# 把只到2017年累计值的投资数据，以及累计同比折算成当月同比
# tickers中包含两个指标，第一个指标是累计值，第二个是累计增速
# 数据起始时间写死为2016年12月
# 各年的1月增速缺失值，手动写死，新的一年记得添加
def cusum_mtm_1(tickers):
    _data = get_data(tickers, start='2016-12-01', end='', method='edb')
    _data = fill_index(_data)
    _data['2017-01'].iloc[0,0] = _data['2017-02'].iloc[0,0]/2
    _data['2017-01'].iloc[0,1] = _data['2017-02'].iloc[0,1]
    _data['2018-01'].iloc[0,1] = _data['2018-02'].iloc[0,1]
    _data['2019-01'].iloc[0,1] = _data['2019-02'].iloc[0,1]
    _data['2020-01'].iloc[0,1] = _data['2020-02'].iloc[0,1]
    _data['2021-01'].iloc[0,1] = _data['2021-02'].iloc[0,1]
    _data['2022-01'].iloc[0,1] = _data['2022-02'].iloc[0,1]
    _data['2023-01'].iloc[0,1] = _data['2023-02'].iloc[0,1]
    for i in range(12,len(_data)):
        _data.iloc[i,0] = _data.iloc[i-12,0] * (1+_data.iloc[i,1]/100)
    _data = cusum_m(_data)
    _data.iloc[:,0] = _data.iloc[:,0].pct_change(12,fill_method=None)*100
    return _data.iloc[:,0].to_frame()

# 把只到2017年累计值的投资数据，以及累计同比折算出当月绝对值
# tickers中包含两个指标，第一个指标是累计值，第二个是累计增速
# 数据起始时间写死为2016年12月
# 各年的1月增速缺失值，手动写死，新的一年记得添加
def cusum_mtm_1_series(tickers):
    _data = get_data(tickers, start='2016-12-01', end='', method='edb')
    _data = fill_index(_data)
    _data['2017-01'].iloc[0,0] = _data['2017-02'].iloc[0,0]/2
    _data['2017-01'].iloc[0,1] = _data['2017-02'].iloc[0,1]
    _data['2018-01'].iloc[0,1] = _data['2018-02'].iloc[0,1]
    _data['2019-01'].iloc[0,1] = _data['2019-02'].iloc[0,1]
    _data['2020-01'].iloc[0,1] = _data['2020-02'].iloc[0,1]
    _data['2021-01'].iloc[0,1] = _data['2021-02'].iloc[0,1]
    _data['2022-01'].iloc[0,1] = _data['2022-02'].iloc[0,1]
    _data['2023-01'].iloc[0,1] = _data['2023-02'].iloc[0,1]
    for i in range(12,len(_data)):
        _data.iloc[i,0] = _data.iloc[i-12,0] * (1+_data.iloc[i,1]/100)
    _data = cusum_m(_data)
    return _data.iloc[:,0].to_frame()

# 最新的年份放在前面
# 计算两年平均增速，基数效应已经写死，2020年7月后的同比增速不再剔除
def two_average(data):
    _data = data.copy()
    _data.loc['2021-01'] = (np.sqrt(np.array(1+_data.loc['2020-01']/100)*np.array(1+_data.loc['2021-01']/100))-1)*100
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

# 最新的年份放在前面
# 计算三年平均增速，基数效应已经写死，2020年7月后的同比增速不再剔除
def three_average(data):
    _data = data.copy()
    _data.loc['2022-01'] = (np.cbrt(np.array(1+_data.loc['2020-01']/100)*np.array(1+_data.loc['2021-01']/100)*np.array(1+_data.loc['2022-01']/100))-1)*100
    _data.loc['2022-02'] = (np.cbrt(np.array(1+_data.loc['2020-02']/100)*np.array(1+_data.loc['2021-02']/100)*np.array(1+_data.loc['2022-02']/100))-1)*100
    _data.loc['2022-03'] = (np.cbrt(np.array(1+_data.loc['2020-03']/100)*np.array(1+_data.loc['2021-03']/100)*np.array(1+_data.loc['2022-03']/100))-1)*100
    _data.loc['2022-04'] = (np.cbrt(np.array(1+_data.loc['2020-04']/100)*np.array(1+_data.loc['2021-04']/100)*np.array(1+_data.loc['2022-04']/100))-1)*100
    _data.loc['2021-01'] = (np.sqrt(np.array(1+_data.loc['2020-01']/100)*np.array(1+_data.loc['2021-01']/100))-1)*100
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


# 计算出口的两年平均增速，消除尖刺，尖刺已写死
def export_average(data):
    data.loc['2019-02'] = (np.sqrt(np.array(1+data.loc['2018-02']/100)*np.array(1+data.loc['2019-02']/100))-1)*100
    data.loc['2018-02'] = data.loc['2019-02']
    data.loc['2016-02'] = (np.sqrt(np.array(1+data.loc['2015-02']/100)*np.array(1+data.loc['2016-02']/100))-1)*100
    data.loc['2015-02'] = (np.sqrt(np.array(1+data.loc['2014-02']/100)*np.array(1+data.loc['2015-02']/100))-1)*100
    data.loc['2014-02'] = (np.sqrt(np.array(1+data.loc['2013-02']/100)*np.array(1+data.loc['2014-02']/100))-1)*100
    return(data)

# # 去趋势，取log做差分
# def de_trend(data):
#     data = fill_index(data)
#     data = np.log(data).diff()
#     return data

# 利用同比构造定基指数
def base_index_construct(tickers,start,base=2016):
    
    # tickers，两个数据，左侧是定基指数，右侧是当月同比
    _data = get_data(tickers,start,'','edb')
    # 补齐时间索引
    _data = fill_index(_data)
    _data['year'] = _data.index.year
    _data = _data.reset_index()
    _index = _data[_data.year==base].index.tolist()

    for j in range(0,_index[0]//12):
        for i in _index:
            _data.iloc[i-12*(j+1),1] = _data.iloc[i-12*j,1] / (1+_data.iloc[i-12*j,2]/100)

    for j in range(0,(len(_data)-_index[-1])//12+1): # 注意+1
        for i in _index:
            if i+12*(j+1) <= len(_data)-1: # 增加一个是否超限的判断
                _data.iloc[i+12*(j+1),1] = _data.iloc[i+12*j,1] * (1 + _data.iloc[i+12*(j+1),2]/100) # 注意计算公式   

    _data = _data.set_index('index')
    _data = _data.drop('year',axis=1)
    return _data

# 数据清理流程
def data_clean(data,method='na',fq='M', mode='hol_save_7_14'):
    _data = fill_index(data)
    if method == 'na':
        _data = na_fill_na(_data)
    else :
        _data = na_fill_cusum(_data)
    _data = seasonal_adj(_data,fq,mode)
    return _data

# 通过官方同比数据，调整绝对值
def value_yty_adj(tickers, start, base=2019):
    # tickers，两个数据，左侧是当月值，右侧是当月同比
    _data = get_data(tickers,start,'','edb')
    # 补齐时间索引
    _data = fill_index(_data)
    _data['year'] = _data.index.year
    _data = _data.reset_index()
    # 提取基期的index
    _index = _data[_data.year==base].index.tolist()

    _data['new'] = np.nan

    # 将第四列作为新数据
    for i in _index:
        _data.iloc[i,4] = _data.iloc[i,1]

    for j in range(0,_index[0]//12+1): # 注意+1
        for i in _index:
            if i-12*(j+1) >= 0: # 增加一个是否为负的判断
                _data.iloc[i-12*(j+1),4] = _data.iloc[i-12*j,4] / (1 + _data.iloc[i-12*j,2]/100) # 注意计算公式
    
    for j in range(0,(len(_data)-_index[-1])//12+1): # 注意+1
        for i in _index:
            if i+12*(j+1) <= len(_data)-1: # 增加一个是否超限的判断
                _data.iloc[i+12*(j+1),4] = _data.iloc[i+12*j,4] * (1 + _data.iloc[i+12*(j+1),2]/100) # 注意计算公式
        
    _data = _data.set_index('index')
    _data.index = pd.to_datetime(_data.index, format="%Y-%m-%d")
    # 更换列名，用当月值的列名代替
    _name = _data.columns[0]
    _data.rename(columns={'new': _name}, inplace=True)
    return _data.iloc[:,3].to_frame()

# 根据疫情前的样本期外推趋势，并与疫情后走势对标
# data是季调后数据，tl是数据名称，sample_start是样本期起点，sample_end是样本期终点
# plot_start是作图的起点
def trend_trace(data, tl, sample_start, sample_end, plot_start='2015'):
    ols = linear_model.LinearRegression()

    _sample = data[sample_start:sample_end].copy()
    _x = np.array((_sample.index - datetime.strptime('190001','%Y%m')).days.values).reshape(-1,1)
    _y = np.array(_sample.iloc[:,0]).reshape(-1,1)

    ols.fit(_x,_y)

    _x_ = np.array((data.index - datetime.strptime('190001','%Y%m')).days.values).reshape(-1,1)
    data['trend'] = ols.predict(_x_)
    # data['diff'] = data.iloc[:,0] - data.iloc[:,1]

    data[plot_start:].iplot(title=tl+'：走势（蓝）、疫情前趋势（橙）',dash=['solid','dash'], kind='spread', legend=False)
    return data

# 生成宏观经济数据的季度数据，根据模式不同，可以生成绝对值、同比、环比
# 生成的是名义值
# tickers，两个数据，左侧是绝对值，右侧是同比
# 对于本函数而言，绝对值和同比，都要选择累计值和累计同比的tickers
# 基期是2019年
# start是样本起始期
def econ_q_n(tickers, start, econ_base=2019, mode='nominal'):
    _data = value_yty_adj(tickers,start,base=econ_base)
    _data = cusum_q(_data)
    _data = seasonal_adj(_data, fq='Q')

    if mode == 'nominal':
        return _data
    elif mode == 'yty':
        return _data.pct_change(4)*100
    elif mode == 'qtq':
        return _data.pct_change()*100
    else:
        print("You may input the wrong arguments.")

# 生成宏观经济数据的季度数据，根据模式不同，可以生成绝对值、同比、环比
# 生成的是经价格平减后的实际值
# tickers，四个数据，左侧是目标变量的绝对值和同比，右侧是价格指数的定基值和同比
# 对于本函数而言，目标变量的绝对值和同比，都要选择累计值和累计同比的tickers
# 对于本函数而言，价格指数的定基值和同比，都要选择当月值和当月同比的tickers
# 基期是2019年
# start是样本起始期
def econ_q_r(tickers, start, econ_base=2019, mode='real'):
    _data_value = value_yty_adj(tickers[:17],start,base=econ_base)
    _data_value = cusum_q(_data_value)

    _data_price = value_yty_adj(tickers[18:],start,base=econ_base)
    _data_price = _data_price.resample('Q').mean() # 做季度平均

    _data = _data_value.join(_data_price)

    # 做价格平减
    _data.iloc[:,0] = np.array(_data.iloc[:,0])/np.array(_data.iloc[:,1])
    
    # 最后做季节性调整
    _data = seasonal_adj(_data.iloc[:,0].to_frame(), fq='Q')
    
    if mode == 'real':
        return _data
    elif mode == 'yty':
        return _data.pct_change(4)*100
    elif mode == 'qtq':
        return _data.pct_change()*100
    else:
        print("You may input the wrong arguments.")

# 剔除数据极端值
# 按照百分位法，对百分位排序高于max和低于min的数据，进行调整
# np.clip将数组中的元素限制在min, max之间
# 大于max的就使得它等于max，小于min,的就使得它等于min
def winsor_percentile(data, min=0.025, max=0.975):
    _q = data.quantile([min, max])
    return np.clip(data, _q.iloc[0], _q.iloc[1], axis=1)

# 使用bi_weight方法去趋势
def bi_weight(data, window=24, result='flatten'):
    _data = np.array(data)[:,0]
    _obs = np.linspace(0, _data.shape[0]-1, num=_data.shape[0])
    flatten_lc, trend_lc = flatten(
        _obs,   # Array of time values
        _data,   # Array of flux values
        method='biweight',
        window_length=window,   # The length of the filter window in units of `time`
        return_trend=True,   # Return trend and flattened light curve
    )
    if result == 'flatten':
        return pd.DataFrame(flatten_lc, index=data.index, columns=data.columns)
    elif result == 'trend':
        return pd.DataFrame(trend_lc, index=data.index, columns=data.columns)
    else:
        print("You may input the wrong arguments.")

# 使用线性方法去趋势
def de_trend(data):
    _data = np.array(data)[:,0]
    _data = signal.detrend(data)
    return pd.DataFrame(_data, index=data.index, columns=data.columns)

# 0-1标准化
def normalization(data):
    return (data - np.mean(data,axis=0))/np.std(data,axis=0)

# 去均值
def de_mean(data):
    return (data - np.mean(data,axis=0))

# 主成分分析，默认取第1主成分，n设置主成分的个数
def pca_n(data, n=1):
    _data = normalization(data) # 将数据标准化为零均值-单位标准差
    _data = np.array(_data) # 将数据转化为数组
    _covMat = np.cov(_data.T)  # 求协方差矩阵
    _eigValue, _eigVec = np.linalg.eig(_covMat) # 求协方差矩阵的特征值和特征向量
    _eigValInd = np.argsort(-_eigValue)
    # 返回特征值由大到小排序的下标，下标越小，特征值越大，比如0代表最大的特征值
    # 排第x的值n，是原序列中的第n个
    # 举例：array([0, 1, 2, 3, 7, 5, 6, 4], dtype=int64)
    # 最大的（排第1）是原序列的第0个。。。第5大（排第5个）是原序列的第7个
    _eigVec = _eigVec[:,_eigValInd] # 根据特征值的大小，重新排列特征向量的顺序
    _selectVec = np.matrix(_eigVec.T[:n]) # 因为[:n]表示前n行，因此之前需要转置处理（选择前n个大的特征值）
    _finalData = np.dot(_data, _selectVec.T) # 再转置回来
    return pd.DataFrame(_finalData, index=data.index)

# 调用ARIMA模型做拟合和预测
# 最终输出结果是合并原序列和预测序列的单一序列
# order = (p,d,q)
# seasonal_order = (P,D,Q,s)
# s是periodicity，frequency of series，月度数据为12，季度数据为4
def arima_forecast(data, forecast_n, order, seasonal_order):
    _model = ARIMA(data, order=order, seasonal_order=seasonal_order).fit()
    _result = _model.forecast(forecast_n).to_frame()
    _result.columns = data.columns
    return data.append(_result)


# 自动选择ARIMA的阶数
# 先安装pmdarima包
# pip install pmdarima --user
# 最终输出结果是合并原序列和预测序列的单一序列

# 导入auto_arima模型

# import pmdarima as pm

# m=12，frequency of series
# seasonal=True，Has Seasonality
# model.predict的结果是Ndarray
# 需要先生成预测时间段的时间Index
# 再转换成DataFrame，再合并

# from pandas.tseries.offsets import Day, MonthEnd

# def auto_arima_forecast(data, forecast_n, m=12, seasonal=True):
#     _model = pm.auto_arima(data, m=m, seasonal=seasonal)
#     print(_model.summary())
#     _result = _model.predict(forecast_n)
#     _index = pd.date_range(start=(data.index[-1]+MonthEnd()),periods=forecast_n,freq='M')
#     _result = pd.DataFrame(_result, columns=data.columns, index=_index)
#     return data.append(_result)



# 环比转成同比
# 大概原理是先取对数，把连乘变成连加
# 然后用.rolling().sum()实现连加
# 最后再用取指数还原
# 区分月度数据和季度数据，M和Q
# 可以处理DataFrame格式，不仅限于Series格式
def mom_yoy(data, periodicity):
    if periodicity == 'M':
        return ((np.exp(np.log((1+data/100)).rolling(12).sum()))-1)*100
    elif periodicity == 'Q':
        return ((np.exp(np.log((1+data/100)).rolling(4).sum()))-1)*100
    else:
        print("You may input the wrong periodicity arguments.")


# 格兰杰因果检验
# 导入grangercausalitytests命令
# 最大滞后期12期
# grangercausalitytests：检验第二列是否是第一列的格兰杰原因(第二列导致第一列)
# 结果显示格兰杰因果检验的p值，如果p值小于0.05，则行变量_x是列变量_y的格兰杰原因
# 即当p值小于0.05时，意味着行变量_x导致列变量_y
# 最后一行的转置.T主要是为了理解方便

from statsmodels.tsa.stattools import grangercausalitytests
maxlag=12
test = 'ssr_chi2test'

def grangers_causation_matrix(data, variables, test='ssr_chi2test', verbose=False):    
    """Check Granger Causality of all possible combinations of the Time series.
    The rows are the response variable, columns are predictors. The values in the table 
    are the P-Values. P-Values lesser than the significance level (0.05), implies 
    the Null Hypothesis that the coefficients of the corresponding past values is 
    zero, that is, the X does not cause Y can be rejected.

    data      : pandas dataframe containing the time series variables
    variables : list containing names of the time series variables.
    """
    df = pd.DataFrame(np.zeros((len(variables), len(variables))), columns=variables, index=variables)
    for c in df.columns:
        for r in df.index:
            test_result = grangercausalitytests(data[[r, c]], maxlag=maxlag, verbose=False)
            # test_result针对每一个滞后阶数lag，都生成一个检验结果，序号从1到12
            # 而range(maxlag)是0-11，所以需要i+1获得检验结果
            # 获得检验的P值
            p_values = [round(test_result[i+1][0][test][1],4) for i in range(maxlag)]
            # 如果verbose=True，则打印详细检验结果
            if verbose: print(f'Y = {r}, X = {c}, P Values = {p_values}')
            # 取最小的格兰杰因果检验P值
            min_p_value = np.min(p_values)
            df.loc[r, c] = min_p_value
    df.columns = [var + '_x' for var in variables]
    df.index = [var + '_y' for var in variables]
    return df.T


# 协整检验
# 导入coint_johansen命令
# coint_johansen(endog, det_order, k_ar_diff)
# Parameters
# endog : array_like (nobs_tot x neqs)
#     Data to test
# det_order : int
#     * -1 - no deterministic terms
#     * 0 - constant term
#     * 1 - linear trend
# k_ar_diff : int, nonnegative
#     Number of lagged differences in the model.
# 输出结果是<statsmodels.tsa.vector_ar.vecm.JohansenTestResult at 0x1fa6094ae20>
# 最终输出结果：True就是有协整关系，False就是没有协整关系

from statsmodels.tsa.vector_ar.vecm import coint_johansen

def cointegration_test(df, alpha=0.05): 
    """Perform Johanson's Cointegration Test and Report Summary"""
    out = coint_johansen(df, -1, 5)
    d = {'0.90':0, '0.95':1, '0.99':2}
    # lr1: Trace statistic
    traces = out.lr1
    # cvt: Critical values (90%, 95%, 99%) of trace statistic
    cvts = out.cvt[:, d[str(1-alpha)]]
    # str: 将指定的值转换为字符串
    # str.ljust: 返回一个原字符串左对齐,并使用空格填充至指定长度的新字符串
    # 也可以选择其他填充，比如'0'
    # 如果指定的长度小于原字符串的长度则返回原字符串
    def adjust(val, length= 6): return str(val).ljust(length)


    # Summary
    print('Name   ::  Test Stat > C(95%)    =>   Signif  \n', '--'*20)
    for col, trace, cvt in zip(df.columns, traces, cvts):
        print(adjust(col), ':: ', adjust(round(trace,2), 9), ">", adjust(cvt, 8), ' =>  ' , trace > cvt)


# 平稳性检验
# 导入adfuller命令
# adfuller只能处理1维数据
# adfuller的输出结果
# 第1个是检验统计量
# 第2个是显著性P值
# 第3个是滞后阶数
# 第4个是样本量
# 第5个是检验临界值
# (-1.2779550432118798,
#  0.6391966001730578,
#  12,
#  133,
#  {'1%': -3.480500383888377,
#   '5%': -2.8835279559405045,
#   '10%': -2.578495716547007},
#  158.95865874127225)

from statsmodels.tsa.stattools import adfuller

def adfuller_test(series, signif=0.05, name='', verbose=False):
    """Perform ADFuller to test for Stationarity of given series and print report"""
    r = adfuller(series, autolag='AIC')
    output = {'test_statistic':round(r[0], 4), 'pvalue':round(r[1], 4), 'n_lags':round(r[2], 4), 'n_obs':r[3]}
    p_value = output['pvalue'] 
    def adjust(val, length= 6): return str(val).ljust(length)

    # Print Summary
    print(f'    Augmented Dickey-Fuller Test on "{name}"', "\n   ", '-'*47)
    print(f' Null Hypothesis: Data has unit root. Non-Stationary.')
    print(f' Significance Level    = {signif}')
    print(f' Test Statistic        = {output["test_statistic"]}')
    print(f' No. Lags Chosen       = {output["n_lags"]}')

    for key,val in r[4].items():
        print(f' Critical value {adjust(key)} = {round(val, 3)}')

    if p_value <= signif:
        print(f" => P-Value = {p_value}. Rejecting Null Hypothesis.")
        print(f" => Series is Stationary.")
    else:
        print(f" => P-Value = {p_value}. Weak evidence to reject the Null Hypothesis.")
        print(f" => Series is Non-Stationary.")  


# VAR模型预测
# 导入VARMAX命令
# exog是VAR模型的外生变量
# order是VAR(p, q)的阶数
# trend='c'是A(t)的数学形式
# n_forecast是预测外的期数

# 导入包
import statsmodels.api as sm

def var_forecast(df, exog=None, order=(1, 0), trend='c', n_forecast=20):
    # 拟合模型
    _orgmod = sm.tsa.VARMAX(df, exog=exog, order=order, trend=trend)
    # 估计模型
    _fitMod = _orgmod.fit(maxiter=1000, disp=False)
    # 打印结果
    print(_fitMod.summary())
    # 预测样本
    # VAR(p, q)，样本期用-p期的样本
    _forecast_input = df[-order[0]:]
    # 预测
    _fc = _fitMod.forecast(y=_forecast_input, steps=n_forecast)
    # 合并数据
    return df.append(_fc)


# 把差分序列还原
# 适用于1次差分后的数据
# 使用cumsum()函数累加做差分还原
# 注意：df_train和df_forecast，可以通过样本期选择来指定
# 举例：result = invert_transformation(df[:'2022-02'],df_diff_f['2022-03':])

def invert_transformation(df_train, df_forecast):
    """Revert back the differencing to get the forecast to original scale."""
    df_fc = df_forecast.copy()
    columns = df_train.columns
    for col in columns:        
        # Roll back 1st Diff
        df_fc[str(col)] = df_train[col].iloc[-1] + df_fc[str(col)].cumsum()
    return df_train.append(df_fc)

# 提取某些时间点前后的数据
# 只能提取单列的样本
# data是数据列
# index_array是目标时间点列表，比如["2015-08-11","2014-01-30"]
# first_n和last_n是时间点前后的数据区间
def event_study_reindex(data, index_array, first_n=60, last_n=60):
    _result = pd.DataFrame()
    # 重置index，便于获取目标日期位置
    _data = data.reset_index()
    for i in index_array:
        # 获取目标日期位置
        _index = _data[_data['index']==i].index.values[0]
        # 提取目标数据
        temp_data = _data.iloc[_index-first_n:_index+last_n+1,:]
        # 丢弃原来的日期index
        temp_data.drop(['index'], axis=1, inplace=True)
        # 生成计数变量
        temp_data['number'] = list(range(-first_n,last_n+1))
        # 将计数变量作为新index
        temp_data=temp_data.set_index(['number'])
        # 重命名
        temp_data.columns=[i]
        _result = _result.join(temp_data, how='outer')
    
    return _result










