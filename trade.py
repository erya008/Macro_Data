import pandas as pd
import numpy as np
import cufflinks as cf
import macro_func

# 导入需要的包
cf.set_config_file(offline=True,theme='white',dimensions=(550,350),colorscale='plotly')

# 进出口、贸易顺差和FDI金额的季节性比较
trade_volume = macro_func.get_data('M0000604,M0000606,M0000608,M0000610,M0007453,M0054766,M0096210,M0009870','2010-01-01','','edb')
for i in trade_volume:
    macro_func.plot_seasonal(trade_volume[[i]])

# 进出口、贸易顺差和FDI金额的季节性比较-累计值，适用于1-2月
trade_volume_ytd = macro_func.get_data('M0043603,M0043623,M0043639,M0096210,M0041769,U8414400,M0009880','2010-01-01','','edb')
for i in trade_volume_ytd:
    macro_func.plot_seasonal(trade_volume_ytd[[i]])

# 出口金额的趋势比较
trade_export = macro_func.get_data('M0043623','2010-01-01','','edb')
trade_export = macro_func.na_fill_jan(trade_export) # 累计值填充1月缺失值
trade_export = macro_func.cusum_m(trade_export)
# macro_func.plot_seasonal(trade_export, tl='的当月值')
trade_export = trade_export.iloc[:,0].to_frame()
trade_export = macro_func.seasonal_adj(trade_export)
trade_export = np.log(trade_export)
trade_export = macro_func.trend_trace(trade_export,'出口金额','2018-01','2019-12')

# 进口金额的趋势比较
trade_import = macro_func.get_data('M0043639','2010-01-01','','edb')
trade_import = macro_func.na_fill_jan(trade_import) # 累计值填充1月缺失值
trade_import = macro_func.cusum_m(trade_import)
# macro_func.plot_seasonal(trade_import, tl='的当月值')
trade_import = trade_import.iloc[:,0].to_frame()
trade_import = macro_func.seasonal_adj(trade_import)
trade_import = np.log(trade_import)
trade_import = macro_func.trend_trace(trade_import,'进口金额','2018-01','2019-12')

# 进出口金额和FDI的同比增速
trade_yoy = macro_func.get_data('M0000605,M0000607,M0000609,M0007454,M0009871','2010-01-01','','edb')
trade_yoy = macro_func.two_average(trade_yoy)
for i in trade_yoy:
    macro_func.plot_seasonal(trade_yoy[[i]])

# 进出口金额和FDI的同比增速-累计同比，适用于1-2月
trade_yoy_ytd = macro_func.get_data('M0043657,M0043677,M0043693,M0041770,M0009881','2010-01-01','','edb')
trade_yoy_ytd = macro_func.two_average(trade_yoy_ytd)
for i in trade_yoy_ytd:
    macro_func.plot_seasonal(trade_yoy_ytd[[i]])

# 进出口金额和FDI的同比增速-人民币计价
trade_yoy_rmb = macro_func.get_data('M5469146,M5469147,M5469148','2010-01-01','','edb')
trade_yoy_rmb = macro_func.two_average(trade_yoy_rmb)
for i in trade_yoy_rmb:
    macro_func.plot_seasonal(trade_yoy_rmb[[i]])

# 进出口金额和FDI的同比增速-人民币计价-累计同比，适用于1-2月
trade_yoy_rmb_ytd = macro_func.get_data('M5469149,M5469150,M5469151','2010-01-01','','edb')
trade_yoy_rmb_ytd = macro_func.two_average(trade_yoy_rmb_ytd)
for i in trade_yoy_rmb_ytd:
    macro_func.plot_seasonal(trade_yoy_rmb_ytd[[i]])

# 国际收支平衡表-经常项目金额
current_account = macro_func.get_data('M5540070,M5481116,M5540067,M5540082','2015-01-01','','edb')
for i in current_account:
    macro_func.plot_seasonal(current_account[[i]])

# 美国消费数据环比
us_sales_mtm = macro_func.get_data('G1109265,G1109322,G1109312','2015-01-01','','edb')
for i in us_sales_mtm:
    macro_func.plot_seasonal(us_sales_mtm[[i]])

# 美国消费数据指数_现价
us_sales_index = macro_func.get_data('G1120772,G1120784,G1120796','2015-01-01','','edb')
us_sales_index = us_sales_index/us_sales_index.loc['2020-01'].values
us_sales_index['2019':].iplot(title='现价：耐用品（蓝）、非耐用品（橙）、服务（绿）',legend=False)

# 美国消费数据指数_不变价
us_sales_index = macro_func.get_data('G1120773,G1120785,G1120797','2015-01-01','','edb')
us_sales_index = us_sales_index/us_sales_index.loc['2020-01'].values
us_sales_index['2019':].iplot(title='不变价：耐用品（蓝）、非耐用品（橙）、服务（绿）',legend=False)

# 中国出口和美国零售
export_ussales = macro_func.get_data('M0056659,G1109245','2011-07-01','','edb')
export_ussales = macro_func.two_average(export_ussales)
export_ussales.iplot(title='中国出口（蓝）、美国零售（橙）',secondary_y='G1109245',legend=False)

# 欧盟零售销售_工业生产指数
eu_sales_index = macro_func.get_data('G0900641,G0900612','2015-01-01','','edb')
eu_sales_index.iplot(title='欧盟：零售销售（蓝）、工业生产（橙）',legend=False)

# 人民币汇率和美元指数
exchange = macro_func.get_data('M0067855,M0000271','2015-01-01','','edb')
exchange.iplot(title='人民币汇率（蓝）、美元指数（橙）',secondary_y='M0000271',legend=False,kind='ratio')

# 外汇储备的变动
foreign_reserve = macro_func.get_data('M0010049,M0001681','2011-01-01','','edb')
foreign_reserve.iplot(title='外汇储备（蓝）、外汇占款（橙）',secondary_y='M0001681',legend=False)
foreign_reserve = foreign_reserve.diff()
for i in foreign_reserve:
    macro_func.plot_seasonal(foreign_reserve[[i]])

# 外汇市场交易：美元计价（月）
fx_trade = macro_func.get_data('M5525771,M5525772,M5525773,M5525774,M5525775','2012-01','','edb')
for i in fx_trade.columns:
    macro_func.plot_seasonal(fx_trade[[i]])

# 美欧隔夜息差与美元汇率
spread_dxy = macro_func.get_data('G0001699,G0000902,G0000891,G0008068,M0000271','2001-01','','edb')
spread_dxy.eval(
    '''
    US_EU_1D_spread = G0001699-G0000902
    US_EU_10Y_spread = G0000891-G0008068
    ''',
    inplace = True
)
spread_dxy[['US_EU_1D_spread','M0000271']]['2015-01':].iplot(secondary_y='M0000271',title='美欧隔夜息差（蓝）、美元指数（橙、右轴）',legend=False,dimensions=(600,380),theme='white')
spread_dxy[['US_EU_10Y_spread','M0000271']]['2015-01':].iplot(secondary_y='M0000271',title='美德10年国债息差（蓝）、美元指数（橙、右轴）',legend=False,dimensions=(600,380),theme='white')

# 美国通胀预期与美元汇率
inflation_dxy = macro_func.get_data('G0000889,G0000891,G0005426,G0005428,M0000271','2001-01','','edb')
inflation_dxy.eval(
    '''
    inflation_5y = G0000889-G0005426
    inflation_10y = G0000891-G0005428
    ''',
    inplace = True
)
inflation_dxy[['inflation_5y','inflation_10y','M0000271']]['2019-01':].iplot(secondary_y='M0000271',title='美国通胀预期：5年国债（蓝）10年国债（橙）、美元指数（绿、右轴）',legend=False,dimensions=(600,380),theme='white')
