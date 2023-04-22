import pandas as pd
import numpy as np
import cufflinks as cf
import macro_func

# 导入需要的包
cf.set_config_file(offline=True,theme='white',dimensions=(550,350),colorscale='plotly')

# 提取PMI的数据
pmi = macro_func.get_data('M0017126,M0017127,M0017128,M0017129,M0017131,M0017132,M0017133,M5766711,M0017134,M0017135,M0017136,M0017137,M5207790','2013-10','','edb')
pmi.eval(
    '''
    domestic_demand = M0017128 - M0017129
    production_order = M0017127 - M0017128
    raw_prices = M0017134 - M5766711
    ''',
    inplace=True
)

# # 对PMI各分项做季调
# pmi_sa = pmi.dropna(axis=1,how='any') # 剔除缺失值
# for i in pmi_sa.columns:
#     pmi_sa[[i]] = macro_func.seasonal_adj(pmi_sa[[i]])

# 做PMI的季节性图
pmi.drop(index=pmi[pmi['M0017126']<40].index, inplace=True)
for i in pmi.columns:
    macro_func.plot_seasonal(pmi[[i]])

# # 做季调后PMI的走势图
# pmi_sa.drop(index=pmi_sa[pmi_sa['M0017126']<40].index, inplace=True)
# for i in pmi_sa.columns:
#     pmi_sa[[i]].iplot(title=macro_func.config(pmi_sa[[i]])[0]+'_季调后')
#     # macro_func.plot_seasonal(pmi_sa[[i]], tl='_季调后')

# pmi_yty = pmi.rolling(12).mean()
# print('PMI的年同比折算')
# for i in pmi_yty.columns:
#     macro_func.plot_seasonal(pmi_yty[[i]],tl='的同比')

# 做大中小企业PMI的季节性图
pmi_size = macro_func.get_data('M5206738,M5206739,M5206740','2015-01-01','','edb')
pmi_size.eval(
    '''
    big_small = M5206738 - M5206740
    ''',
    inplace=True
)
pmi_size.drop(index=pmi_size[pmi_size['M5206738']<40].index, inplace=True)
for i in pmi_size.columns:
    macro_func.plot_seasonal(pmi_size[[i]])

# 做非制造业PMI的季节性图
pmi_non_manufacturing = macro_func.get_data('M0048236,M0048237,M0048238,M0048239,M0048240,M0068606,M5207830,M0088875,M0088876,M0088877','2013-10','','edb')
pmi_non_manufacturing.drop(index=pmi_non_manufacturing[pmi_non_manufacturing['M0048236']<40].index, inplace=True)
for i in pmi_non_manufacturing.columns:
    macro_func.plot_seasonal(pmi_non_manufacturing[[i]])

# 做建筑业PMI的季节性图
pmi_construction = macro_func.get_data('M5207831,M5207832,M5207833,M5207837,M5207834,M5207835,M5207836','2013-10','','edb')
pmi_construction.drop(index=pmi_construction[pmi_construction['M5207831']<40].index, inplace=True)
for i in pmi_construction.columns:
    macro_func.plot_seasonal(pmi_construction[[i]])

# 做服务业PMI的季节性图
pmi_service = macro_func.get_data('M5207838,M5207839,M5207840,M5207844,M5207841,M5207842,M5207843','2013-10','','edb')
pmi_service.drop(index=pmi_service[pmi_service['M5207838']<40].index, inplace=True)
for i in pmi_service.columns:
    macro_func.plot_seasonal(pmi_service[[i]])

# BCI:中国企业经营状况指数
bci = macro_func.get_data('M5786898,M5786899,M5786900,M5786901,M5786902,M5786903,M5786904,M5786905,M5786906,M5786907,M5786908,M5786909','2015-01-01','','edb')
for i in bci.columns:
    macro_func.plot_seasonal(bci[[i]])

# 美国消费数据环比
us_sales_mtm = macro_func.get_data('G1109265,G1109322,G1109312','2015-01-01','','edb')
for i in us_sales_mtm:
    macro_func.plot_seasonal(us_sales_mtm[[i]])

# 美国PMI数据
pmi_us = macro_func.get_data('G0002323,G0008345,G0008346,G0008347,G0008348,G0008349,G0008350,G0008351,G0008352,G0008353,G0008354','2015-01-01','','edb')
for i in pmi_us.columns:
    macro_func.plot_seasonal(pmi_us[[i]])