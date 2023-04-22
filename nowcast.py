import pandas as pd
import numpy as np
import cufflinks as cf
import macro_func

# 导入需要的包
cf.set_config_file(offline=True,theme='white',dimensions=(550,350),colorscale='plotly')

datafile = "C:\\Users\\wanzh\\OneDrive\\宏观经济预测专题\\NowCast\\许老师课题"

# 官方环比数据-价格数据和PMI
cpi_ppi = macro_func.get_data('M0000705,M0061581,M0049160,M0065959,M0017126,M0000138','1999-12-01','','edb')
cpi_ppi.columns = ['cpi','cpiexfood','ppi','rpi','pmi','pmi_cx']
cpi_ppi.to_excel(r'{}\\cpi_ppi.xls'.format(datafile))

# GDP数据环比
gdp = macro_func.value_yty_adj('M5567889,M0039354','1999-12-01')
gdp = gdp.resample('Q').last()
gdp = macro_func.seasonal_adj(gdp,fq='Q')
gdp.columns = ['gdp']
gdp = gdp.pct_change()*100
gdp.to_excel(r'{}\\gdp.xls'.format(datafile))

# 工业增加值环比
iv = macro_func.get_data('M0061571','2011-01-01','','edb')
iv.columns = ['iv']
iv.to_excel(r'{}\\iv.xls'.format(datafile))

# 社会消费品零售
consumption = macro_func.value_yty_adj('M0001439,M0001440','2002-03')
consumption = macro_func.na_fill_jan(consumption)
consumption = macro_func.cusum_m(consumption)
cpi_index = macro_func.value_yty_adj('M5567964,M0000612','2002-03')
consumption = consumption.join(cpi_index)
consumption.iloc[:,0] = np.array(consumption.iloc[:,0])/np.array(consumption.iloc[:,1])
consumption = macro_func.seasonal_adj(consumption.iloc[:,0].to_frame())
consumption.columns = ['consumption']
consumption = consumption.pct_change()*100
consumption.to_excel(r'{}\\consumption.xls'.format(datafile))

# M0、M1、M2的处理
M = macro_func.get_data('M0001380,M0001382,M0001384','1999-12-01','','edb')
for i in M.columns.values:
    M[i] = macro_func.seasonal_adj(M[[i]])
M.columns = ['M0','M','M2']
M = M.pct_change()*100
M.to_excel(r'{}\\M.xls'.format(datafile))

# 进出口和FDI的处理
trade = macro_func.get_data('M0000606,M0000608,M0009870','2002-10-01','','edb')
trade = macro_func.fill_index(trade)
for i in trade.columns.values:
    trade[i] = macro_func.na_fill_na(trade[[i]])  
    trade[i] = macro_func.seasonal_adj(trade[[i]])  
trade.columns = ['export','import','fdi']
trade = trade.pct_change()*100
trade.to_excel(r'{}\\trade.xls'.format(datafile))

# 固定资产投资的处理
investment = macro_func.cusum_mtm_series('M0000272,M0000273','2002-02')
ppi_index = macro_func.value_yty_adj('M5567965,M0001227','2002-03')
investment = investment.join(ppi_index)
investment.iloc[:,0] = np.array(investment.iloc[:,0])/np.array(investment.iloc[:,1])
investment = macro_func.seasonal_adj(investment.iloc[:,0].to_frame())
investment.columns = ['investment']
investment = investment.pct_change()*100
investment.to_excel(r'{}\\invest.xls'.format(datafile))

# 财政收支的处理
fiscal = macro_func.get_data('M0024054,M0024055','1999-12-01','','edb')
fiscal = macro_func.fill_index(fiscal)
for i in fiscal.columns.values:
    fiscal[i] = macro_func.na_fill_na(fiscal[[i]])
    fiscal[i] = macro_func.seasonal_adj(fiscal[[i]])
fiscal.columns = ['revenue','expenditure']
fiscal = fiscal.pct_change(1)*100
fiscal.to_excel(r'{}\\fiscal.xls'.format(datafile))

# 房价的处理
house_price = macro_func.get_data('S2707426','1999-12-01','','edb')
house_price.columns = ['house_price']
house_price.to_excel(r'{}\\house_price.xls'.format(datafile))

# 新增社融的处理
sfi = macro_func.get_data('M5206730','2002-01-01','','edb')
sfi = macro_func.fill_index(sfi)
sfi = macro_func.na_fill_na(sfi)
sfi = macro_func.seasonal_adj(sfi)
sfi.columns = ['sfi']
sfi = sfi.pct_change()*100
sfi.to_excel(r'{}\\sfi.xls'.format(datafile))

# 汽车产量的处理
car = macro_func.get_data('S0105523','2000-01-01','','edb')
car = macro_func.fill_index(car)
car = macro_func.na_fill_na(car)
car = macro_func.seasonal_adj(car)
car.columns = ['car']
car = car.pct_change()*100
car.to_excel(r'{}\\car.xls'.format(datafile))

# 人民币名义汇率指数
exchange = macro_func.get_data('M0000210','2000-01-01','','edb')
exchange.columns = ['exchange']
exchange = exchange.pct_change()*100
exchange.to_excel(r'{}\\exchange.xls'.format(datafile))

# 几个行业数据的处理
industry = macro_func.get_data('S0027012,S0027378,S0036012','1999-12-01','','edb')
industry = macro_func.fill_index(industry)
for i in industry.columns.values:
    industry[i] = macro_func.na_fill_na(industry[[i]])  
    industry[i] = macro_func.seasonal_adj(industry[[i]])  
industry.columns = ['power','iron','freight']
industry = industry.pct_change(1)*100
industry.to_excel(r'{}\\industry.xls'.format(datafile))

# 记得把数据剪切到data文件夹下
# 合并数据
import os
files = os.listdir(datafile)
files

data_list = []
for f in files:
    if os.path.splitext(f)[1] == '.xls':
        data_list.append(datafile+ '\\' + f)
    else:
        pass
data_list


df = pd.read_excel(data_list[0],index_col=0)
for i in range(1, len(data_list)):
    df_i = pd.read_excel(data_list[i],index_col=0)
    df = df.join(df_i,how='outer').drop_duplicates()
df = df.resample('MS').mean()
df.to_excel(datafile +'\\data_merge.xls')