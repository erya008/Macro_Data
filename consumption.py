import pandas as pd
import numpy as np
import cufflinks as cf
import macro_func

# 导入需要的包
cf.set_config_file(offline=True,theme='white',dimensions=(550,350),colorscale='plotly')

# 社会消费品零售总额的当月同比
consumption_yty = macro_func.get_data('M0001428,M0061657,M0061658,M0061659,M0061660,M6451628,M5201391,M5201395,M5201399,M5405526','2015-01-01','','edb')
consumption_yty_twoyear = macro_func.two_average(consumption_yty)
consumption_yty_twoyear[['M0001428','M0061659','M0061660']].iplot(title='社零消费增速，两年平均：整体（蓝）、商品（橙）、餐饮（绿）',legend=False)
for i in consumption_yty_twoyear:
    macro_func.plot_seasonal(consumption_yty_twoyear[[i]])

consumption_yty_threeyear = macro_func.three_average(consumption_yty)
consumption_yty_threeyear[['M0001428','M0061659','M0061660']].iplot(title='社零消费增速，三年平均：整体（蓝）、商品（橙）、餐饮（绿）',legend=False)

# 实物商品网上零售额
goods_online = macro_func.cusum_mtm('M5540105,M5540106','2015-02','')
macro_func.plot_seasonal(goods_online,tl='的单月同比')

# M0001439：社会消费品零售总额：累计值
consumption_series = macro_func.get_data('M0001439','2000-01','','edb')
consumption_series = macro_func.na_fill_jan(consumption_series)
consumption_series = macro_func.cusum_m(consumption_series)
consumption_series = macro_func.seasonal_adj(consumption_series)
consumption_series = np.log(consumption_series)
consumption_series = macro_func.trend_trace(consumption_series,'社会消费品零售','2018-01','2019-12')

# M0061663：社会消费品零售总额：商品零售：累计值
goods_series = macro_func.get_data('M0061663','2000-01','','edb')
goods_series = macro_func.na_fill_jan(goods_series)
goods_series = macro_func.cusum_m(goods_series)
goods_series = macro_func.seasonal_adj(goods_series)
goods_series = np.log(goods_series)
goods_series = macro_func.trend_trace(goods_series,'商品零售','2018-01','2019-12')

# M0061664：社会消费品零售总额：餐饮收入：累计值
foods_series = macro_func.get_data('M0061664','2000-01','','edb')
foods_series = macro_func.na_fill_jan(foods_series)
foods_series = macro_func.cusum_m(foods_series)
foods_series = macro_func.seasonal_adj(foods_series)
foods_series = np.log(foods_series)
foods_series = macro_func.trend_trace(foods_series,'餐饮收入','2018-01','2019-12')

# 社会消费品零售总额的环比
consumption_mtm =macro_func.get_data('M0061573','2015-01-01','','edb')
consumption_mtm.drop(index=consumption_mtm[abs(consumption_mtm['M0061573'])>4].index, inplace=True)
macro_func.plot_seasonal(consumption_mtm)

# 限额以上与限额以下企业消费品零售对比
consumption_below_yty = macro_func.get_data('M0001427,M5201390','2015-01-01','','edb')
consumption_below_yty.eval(
    '''
    consumption_below = M0001427 - M5201390
    ''',
    inplace=True
)
consumption_below_yty = macro_func.fill_index(consumption_below_yty)
consumption_below_yty = consumption_below_yty.pct_change(12,fill_method=None)*100
consumption_below_yty = macro_func.two_average(consumption_below_yty)
for i in consumption_below_yty:
    macro_func.plot_seasonal(consumption_below_yty[[i]])

# 限额以上重点商品零售增速
main_goods_yty = macro_func.get_data('M0073698,M0073701,M0073702,M0001456,M0001464,M0001465,M0001460,M0001461,M0073705,M0001458,M0001462,M0001466,M0001468,M0001467,M0001463','2015-01-01','','edb')
main_goods_yty = macro_func.two_average(main_goods_yty)
for i in main_goods_yty:
    macro_func.plot_seasonal(main_goods_yty[[i]])

# 服务业观察指标
service_sales = macro_func.get_data('S6604459,S6604460,S0036001,S0036011,S0036002,S0036003,S0036004,S0118855','2015-01-01','','edb')
for i in service_sales:
    macro_func.plot_seasonal(service_sales[[i]])

# 农民工就业和收入
farmers = macro_func.get_data('M5405763,M5405765','2015-01-01','','edb')
farmers.loc['2021-03'] = (np.sqrt(np.array(1+farmers.loc['2020-03']/100)*np.array(1+farmers.loc['2021-03']/100))-1)*100
farmers.loc['2021-06'] = (np.sqrt(np.array(1+farmers.loc['2020-06']/100)*np.array(1+farmers.loc['2021-06']/100))-1)*100
farmers.loc['2021-09'] = (np.sqrt(np.array(1+farmers.loc['2020-09']/100)*np.array(1+farmers.loc['2021-09']/100))-1)*100
farmers.loc['2021-12'] = (np.sqrt(np.array(1+farmers.loc['2020-12']/100)*np.array(1+farmers.loc['2021-12']/100))-1)*100
farmers.loc['2020-03'] = np.nan
farmers.loc['2020-06'] = np.nan
for i in farmers:
    macro_func.plot_seasonal(farmers[[i]])

# 城乡储户问卷调查
depositor_survey = macro_func.get_data('M0007437,M0007438,M5207465,M5207466,M0007443,M0007448,M0007446,M5530629','2015-01-01','','edb')
for i in depositor_survey:
    macro_func.plot_seasonal(depositor_survey[[i]])

# 城镇调查失业率
unemployment_rate = macro_func.get_data('M5650805,M5650806,M7082071,M6179512','2015-01-01','','edb')
for i in unemployment_rate.columns:
    macro_func.plot_seasonal(unemployment_rate[[i]])

# 就业人员平均工作时间
per_worktime = macro_func.get_data('M5650810', '2018-06', '', 'edb')
macro_func.plot_seasonal(per_worktime)

# 新增城镇就业和PMI就业
labor = macro_func.get_data('M5480389,M0017136,M5207830,M5207836,M5207843','2015-01-01','','edb')
labor[['M5480389']] = macro_func.cusum_m(labor[['M5480389']])
for i in labor.columns:
    macro_func.plot_seasonal(labor[[i]])

# 城镇居民人均收入和支出
income_expenditure = macro_func.get_data('M0012989,M0012992','2015-01-01','','edb')
income_expenditure.loc['2021-03'] = (np.sqrt(np.array(1+income_expenditure.loc['2020-03']/100)*np.array(1+income_expenditure.loc['2021-03']/100))-1)*100
income_expenditure.loc['2021-06'] = (np.sqrt(np.array(1+income_expenditure.loc['2020-06']/100)*np.array(1+income_expenditure.loc['2021-06']/100))-1)*100
income_expenditure.loc['2021-09'] = (np.sqrt(np.array(1+income_expenditure.loc['2020-09']/100)*np.array(1+income_expenditure.loc['2021-09']/100))-1)*100
income_expenditure.loc['2021-12'] = (np.sqrt(np.array(1+income_expenditure.loc['2020-12']/100)*np.array(1+income_expenditure.loc['2021-12']/100))-1)*100
income_expenditure.loc['2020-03'] = np.nan
income_expenditure.loc['2020-06'] = np.nan
for i in income_expenditure.columns:
    macro_func.plot_seasonal(income_expenditure[[i]])

# 城镇居民人均支出与可支配收入的比例
expenditure_rate = macro_func.get_data('M0012988,M0012991','2015-01-01','','edb')
expenditure_rate['expenditure_rate'] = expenditure_rate['M0012991']*100/expenditure_rate['M0012988']
macro_func.plot_seasonal(expenditure_rate[['expenditure_rate']])