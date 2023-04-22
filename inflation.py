import pandas as pd
import numpy as np
import cufflinks as cf
import macro_func

# 导入需要的包
cf.set_config_file(offline=True,theme='white',dimensions=(550,350),colorscale='plotly')

# CPI及主要分项的环比
cpi_mtm = macro_func.get_data('M0000705,M0000706,M0061581,M0085934,M0061583,M0061585,M0327907,M0068107,M0000708,M0000713,M0068121,M0068122,M0000711,M0327927,M0068116,M0068118,M0068171,M0000712,M0068172,M0068119,M0000710','2010-01-01','','edb')
for i in cpi_mtm.columns:
    macro_func.plot_seasonal(cpi_mtm[[i]])

# PPI及主要分项的环比
ppi_mtm = macro_func.get_data('M0049160,M0066329,M0066330,M0066331,M0066332,M0096793,M0096794,M0096811,M0096812,M0096815,M0096816,M0096817,M0066333,M0066334,M0066335,M0066336,M0066337','2010-01-01','','edb')
for i in ppi_mtm.columns[0:8]:
    macro_func.plot_seasonal(ppi_mtm[[i]])
for i in ppi_mtm.columns[8:]:
    macro_func.plot_seasonal(ppi_mtm[[i]])

# 农产品价格高频环比
agricultural_hf = macro_func.get_data('S0000236,S0248945,S5065106,S5065109,S5065110,S5065111,S5065112','2015-01-01','','edb')
agricultural_hf = agricultural_hf.resample('M').mean().pct_change()*100
for i in agricultural_hf.columns:
    macro_func.plot_seasonal(agricultural_hf[[i]],tl='的环比')

# 工业品价格高频环比
industrial_hf = macro_func.get_data('S0000274,S0105897,S0031525,S0182141,S0181379,S0181380,S0029751,S0029755,S0181383,S0186244,S0033227,S5704696,S0033272,S0033155,S5914515,S5319531,S5914179','2017-01-01','','edb')
industrial_hf = industrial_hf.resample('M').mean().pct_change()*100
for i in industrial_hf.columns:
    macro_func.plot_seasonal(industrial_hf[[i]],tl='的环比')

# 大宗商品进口数量的环比
goods_import = macro_func.get_data('M0041529,M0041571,S0027235,S0117475,S0027490,S0106255,S0027639,S0106267,S0027654,S0027959,S0173743','2017-01-01','','edb')
goods_import = goods_import.pct_change()*100
for i in goods_import.columns:
    macro_func.plot_seasonal(goods_import[[i]],tl='的环比')

# 大宗商品进口数量的同比
goods_import = macro_func.get_data('M0041529,M0041571,S0027235,S0117475,S0027490,S0106255,S0027639,S0106267,S0027654,S0027959,S0173743','2017-01-01','','edb')
goods_import = goods_import.pct_change(12)*100
for i in goods_import.columns:
    macro_func.plot_seasonal(goods_import[[i]],tl='的同比')

# CPI及主要分项的同比
cpi_yty = macro_func.get_data('M0000612,M0001022,M0000616,M0000613,M0085932,M0000614,M0000615,M0327903,M0000628,M0000650,M0000630,M0000637,M0000644,M0000633','2010-01-01','','edb')
for i in cpi_yty.columns:
    macro_func.plot_seasonal(cpi_yty[[i]])

# 生猪存栏和猪肉价格同比
pig = macro_func.get_data('M0044542,S0109325,S0109324','2008-07-01','','edb')
pig = pig.fillna(method='ffill')
pig.iplot(title='CPI猪肉同比（蓝）、生猪存栏（橙）、生猪出栏（绿）',legend=False,secondary_y=['S0109325','S0109324'])

# M1增速和PPI同比
M1 = macro_func.get_data('M0001383,M0001227','2015-01-01','','edb')
M1.iplot(title='M1同比（蓝，领先8个月）与PPI（橙，右轴）',legend=False,secondary_y='M0001227')

# 资金利率与通胀
shibor = macro_func.get_data('M0017142,M0000613,M0001227','2006-01-01','','edb')
shibor = shibor.resample('M').mean()
shibor.iplot(title='3个月SHIBOR（蓝）与CPI非食品（橙）、PPI（绿，右轴）',legend=False,secondary_y='M0001227')

