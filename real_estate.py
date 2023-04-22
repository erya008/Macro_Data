import pandas as pd
import numpy as np
import cufflinks as cf
import macro_func

# 导入需要的包
cf.set_config_file(offline=True,theme='white',dimensions=(550,350),colorscale='plotly')

# 房屋施工面积的当月同比
floor_space_under_construction = macro_func.cusum_mtm('S0029668,S0073290','2010-01-01','')
floor_space_under_construction = macro_func.two_average(floor_space_under_construction)
macro_func.plot_seasonal(floor_space_under_construction,tl='的当月同比')

# 房屋新开工面积的当月同比
floor_space_started = macro_func.cusum_mtm('S0029669,S0073293','2010-01-01','')
floor_space_started = macro_func.two_average(floor_space_started)
macro_func.plot_seasonal(floor_space_started,tl='的当月同比')

# 房屋竣工面积的当月同比
floor_space_completed = macro_func.cusum_mtm('S0029670,S0073297','2010-01-01','')
floor_space_completed = macro_func.two_average(floor_space_completed)
macro_func.plot_seasonal(floor_space_completed,tl='的当月同比')

# 本年购置土地面积的当月同比
land_space_purchased = macro_func.cusum_mtm('S0029666,S0073288','2010-01-01','')
land_space_purchased = macro_func.two_average(land_space_purchased)
macro_func.plot_seasonal(land_space_purchased,tl='的当月同比')

# 本年土地成交价款的当月同比
transaction_value_land = macro_func.cusum_mtm('S0073282,S0073285','2010-01-01','')
transaction_value_land = macro_func.two_average(transaction_value_land)
macro_func.plot_seasonal(transaction_value_land,tl='的当月同比')

# 商品房销售面积的当月同比
sales_floor = macro_func.cusum_mtm('S0029658,S0073300','2010-01-01','')
sales_floor = macro_func.two_average(sales_floor)
macro_func.plot_seasonal(sales_floor,tl='的当月同比')

# 商品房销售金额的当月同比
sales_value = macro_func.cusum_mtm('S0029659,S0049591','2010-01-01','')
sales_value = macro_func.two_average(sales_value)
macro_func.plot_seasonal(sales_value,tl='的当月同比')

# 房地产开发资金来源:合计的当月同比
total_funds = macro_func.cusum_mtm('S0029646,S0073244','2010-01-01','')
total_funds = macro_func.two_average(total_funds)
# total_funds['2016-07':].iplot(title='房地产开发资金来源：当月同比')
macro_func.plot_seasonal(total_funds,tl='的当月同比')

# 国内贷款的当月同比
domestic_loans = macro_func.cusum_mtm('S0029648,S0073245','2010-01-01','')
domestic_loans = macro_func.two_average(domestic_loans)
macro_func.plot_seasonal(domestic_loans,tl='的当月同比')

# 自筹资金的当月同比
self_raising_funds = macro_func.cusum_mtm('S0029652,S0073250','2010-01-01','')
self_raising_funds = macro_func.two_average(self_raising_funds)
macro_func.plot_seasonal(self_raising_funds,tl='的当月同比')

# 其他资金的当月同比
other_funds = macro_func.cusum_mtm('S0029654,S0073252','2010-01-01','')
other_funds = macro_func.two_average(other_funds)
macro_func.plot_seasonal(other_funds,tl='的当月同比')

# 定金及预付款的当月同比
bargain_funds = macro_func.cusum_mtm('S0029655,S0073253','2010-01-01','')
bargain_funds = macro_func.two_average(bargain_funds)
macro_func.plot_seasonal(bargain_funds,tl='的当月同比')

# 个人按揭贷款的当月同比
mortgage_loan = macro_func.cusum_mtm('S0073241,S0073254','2010-01-01','')
mortgage_loan = macro_func.two_average(mortgage_loan)
macro_func.plot_seasonal(mortgage_loan,tl='的当月同比')

# # 各项应付款的当月同比
# payment_payable = macro_func.cusum_mtm('S0073242,S0073255','2010-01-01','')
# payment_payable = macro_func.two_average(payment_payable)
# macro_func.plot_seasonal(payment_payable,tl='的当月同比')

# 房地产价格指数
house_price_yty = macro_func.get_data('S2704485,S2707445,S2707446,S2707447','2012-01-01','','edb')
house_price_yty.columns = macro_func.config(house_price_yty)
house_price_yty.iplot(title='百城住宅价格指数：同比',legend={'orientation':'h','x':0,'y':-0.1})
house_price_mtm = macro_func.get_data('S2700453,S2707442,S2707443,S2707444','2012-01-01','','edb')
for i in house_price_mtm.columns:
    macro_func.plot_seasonal(house_price_mtm[[i]],3)