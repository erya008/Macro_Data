import pandas as pd
import numpy as np
import cufflinks as cf
import macro_func

# 导入需要的包
cf.set_config_file(offline=True,theme='white',dimensions=(550,350),colorscale='plotly')

# # 公共财政收支增速的季节性
# public_finance = macro_func.get_data('M0024063,M0024064','2015-01-01','','edb')
# public_finance = macro_func.two_average(public_finance)
# for i in public_finance.columns:
#     macro_func.plot_seasonal(public_finance[[i]],tl='两年平均增速')

# 公共财政收入的季节性
public_finance_revenue = macro_func.cusum_mtm('M0046168,M0046169','2015-01-01','')
public_finance_revenue = macro_func.two_average(public_finance_revenue)
macro_func.plot_seasonal(public_finance_revenue,tl='的单月值的增速')

# 公共财政支出的季节性
public_finance_expentiture = macro_func.cusum_mtm('M0046166,M0046167','2015-01-01','')
public_finance_expentiture = macro_func.two_average(public_finance_expentiture)
macro_func.plot_seasonal(public_finance_expentiture,tl='的单月值的增速')

# 政府性基金收入的季节性
government_managed_funds_revenue = macro_func.cusum_mtm('M0096879,M0096883','2010-01-01','')
government_managed_funds_revenue = macro_func.two_average(government_managed_funds_revenue)
macro_func.plot_seasonal(government_managed_funds_revenue,tl='的单月值的增速')

# 政府性基金支出的季节性
government_managed_funds_expentiture = macro_func.cusum_mtm('M0096887,M0096891','2010-01-01','')
government_managed_funds_expentiture = macro_func.two_average(government_managed_funds_expentiture)
macro_func.plot_seasonal(government_managed_funds_expentiture,tl='的单月值的增速')

# 公共财政收入各科目增速的季节性
public_finance_revenue = macro_func.get_data('M0024065,M0046079,M0046080,M0046084,M0046085,M0046081,M0046089,M0046087,M0075965,M6823407,M6823408,M0046086,M0325657,M0075969,M0046088,M0325658,M0075973','2015-01-01','','edb')
public_finance_revenue = macro_func.two_average(public_finance_revenue)
# for i in public_finance_revenue.columns:
#     public_finance_revenue.drop(index=public_finance_revenue[abs(public_finance_revenue[i])>50].index,inplace=True)
for i in public_finance_revenue.columns:
    macro_func.plot_seasonal(public_finance_revenue[[i]],tl='两年平均增速')

# 公共财政支出各科目增速的季节性
public_finance_expentiture = macro_func.get_data('M0046132,M0046133,M6823411,M0046135,M6823412,M0046137,M0046138,M0046139,M0046140','2015-01-01','','edb')
public_finance_expentiture = macro_func.two_average(public_finance_expentiture)
# for i in public_finance_expentiture.columns:
#     public_finance_expentiture.drop(index=public_finance_expentiture[abs(public_finance_expentiture[i])>50].index,inplace=True)
for i in public_finance_expentiture.columns:
    macro_func.plot_seasonal(public_finance_expentiture[[i]],tl='两年平均增速')