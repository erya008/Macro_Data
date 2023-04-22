import pandas as pd
import numpy as np
import cufflinks as cf
import macro_func

# 导入需要的包
cf.set_config_file(offline=True,theme='white',dimensions=(550,350),colorscale='plotly')

# 工业企业营业收入的当月同比
revenue_yty = macro_func.value_yty_adj('M5767811,M5767812','2017-01-01')
revenue_yty = macro_func.cusum_m(revenue_yty)
revenue_yty = revenue_yty.pct_change(12)*100
revenue_yty = macro_func.two_average(revenue_yty)
revenue_yty.drop(revenue_yty.head(13).index, inplace=True)
macro_func.plot_seasonal(revenue_yty,tl='的当月同比')

# 工业企业利润总额的当月同比
profit_yty = macro_func.value_yty_adj('M0000556,M0000557','2017-01-01')
profit_yty = macro_func.cusum_m(profit_yty)
profit_yty = profit_yty.pct_change(12)*100
profit_yty = macro_func.two_average(profit_yty)
profit_yty.drop(profit_yty.head(13).index, inplace=True)
macro_func.plot_seasonal(profit_yty,tl='的当月同比')

# 工业企业营业成本的当月同比
cost_yty = macro_func.value_yty_adj('M5767813,M5767814','2017-01-01')
cost_yty = macro_func.cusum_m(cost_yty)
cost_yty = cost_yty.pct_change(12)*100
cost_yty = macro_func.two_average(cost_yty)
cost_yty.drop(cost_yty.head(13).index, inplace=True)
macro_func.plot_seasonal(cost_yty,tl='的当月同比')

# 制造业利润总额的当月同比
manufacturing_profit_yty = macro_func.cusum_mtm('S0206718,S0206721','2010-01-01','')
manufacturing_profit_yty = macro_func.two_average(manufacturing_profit_yty)
macro_func.plot_seasonal(manufacturing_profit_yty,tl='的当月同比')

# 电力热力燃气利润总额的当月同比
utility_profit_yty = macro_func.cusum_mtm('S0206719,S0206722','2010-01-01','')
utility_profit_yty = macro_func.two_average(utility_profit_yty)
macro_func.plot_seasonal(utility_profit_yty,tl='的当月同比')

# 工业企业产成品存货的累计同比
stock_yty = macro_func.get_data('M0000561','2010-01-01','', 'edb')
stock_yty = macro_func.two_average(stock_yty)
macro_func.plot_seasonal(stock_yty)

# # 分行业的利润增速季节性比较
# industry_profit_yty = macro_func.get_data('S0001668,S0002550,S0003684,S0004314,S0004482,S0005616,S0005784,S0006414,S0007002,S0007254,S0007632,S0007926,S0008850,S0009102,S0010866,S0011202,S0168314,S0012546,S0014184,S0014394,S0014898,S0016242,S0017964,S0020694,S0020442,S0021744,S0023214,S0024390,S0025566,S0026322,S0168356,S0026448,S0026784,S0026826','2016-01-01','','edb')
# industry_profit_yty = macro_func.two_average(industry_profit_yty)
# for i in industry_profit_yty.columns[0:10]:
#     macro_func.plot_seasonal(industry_profit_yty[[i]])
# for i in industry_profit_yty.columns[10:20]:
#     macro_func.plot_seasonal(industry_profit_yty[[i]])
# for i in industry_profit_yty.columns[20:30]:
#     macro_func.plot_seasonal(industry_profit_yty[[i]])
# for i in industry_profit_yty.columns[30:]:
#     macro_func.plot_seasonal(industry_profit_yty[[i]])

# 最新一个月数据更新慢，two_average函数容易报错

# # 工业企业管理费用的当月同比
# supervision_cost_yty = macro_func.cusum_mtm('M0044687,M0044688','2010-01-01','')
# supervision_cost_yty = macro_func.two_average(supervision_cost_yty)
# macro_func.plot_seasonal(supervision_cost_yty,tl='的当月同比')

# # 工业企业销售费用的当月同比
# distribution_cost_yty = macro_func.cusum_mtm('M0044689,M0044690','2010-01-01','')
# distribution_cost_yty = macro_func.two_average(distribution_cost_yty)
# macro_func.plot_seasonal(distribution_cost_yty,tl='的当月同比')

# # 工业企业财务费用的当月同比
# finance_cost_yty = macro_func.cusum_mtm('M0044685,M0044686','2010-01-01','')
# finance_cost_yty = macro_func.two_average(finance_cost_yty)
# macro_func.plot_seasonal(finance_cost_yty,tl='的当月同比')

# # 工业企业利息费用的当月同比
# interest_cost_yty = macro_func.cusum_mtm('M0044702,M0044703','2010-01-01','')
# interest_cost_yty = macro_func.two_average(interest_cost_yty)
# macro_func.plot_seasonal(interest_cost_yty,tl='的当月同比')