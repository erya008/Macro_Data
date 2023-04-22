import pandas as pd
import numpy as np
import cufflinks as cf
import macro_func

# 导入需要的包
cf.set_config_file(offline=True,theme='white',dimensions=(550,350),colorscale='plotly')

# 生成固定资产投资单月值的序列：名义值
investment_series = macro_func.cusum_mtm_series('M0000272,M0000273','2002-02-01')
investment_series = macro_func.seasonal_adj(investment_series)
investment_series = np.log(investment_series)
investment_series = macro_func.trend_trace(investment_series,'固定资产投资','2018-01','2019-12')

# 生成固定资产投资单月值的序列：实际值
investment_series = macro_func.cusum_mtm_series('M0000272,M0000273','2002-02-01')
ppi_index = macro_func.value_yty_adj('M5567965,M0001227','2002-03')
investment_series = investment_series.join(ppi_index)
investment_series.iloc[:,0] = np.array(investment_series.iloc[:,0])/np.array(investment_series.iloc[:,1])
investment_series = macro_func.seasonal_adj(investment_series.iloc[:,0].to_frame())
investment_series = np.log(investment_series)
investment_series = macro_func.trend_trace(investment_series,'固定资产投资实际值','2018-01','2019-12')


# 固定资产投资的官方环比增速
investment_mtm = macro_func.get_data('M0061572','2011-01','','edb')
investment_mtm = investment_mtm.drop(index=investment_mtm[abs(investment_mtm['M0061572'])>1].index)
macro_func.plot_seasonal(investment_mtm)

# 固定资产投资的当月同比
investment_yty = macro_func.cusum_mtm('M0000272,M0000273','2010-01-01','')
investment_yty.join(macro_func.get_data('M0001227','2010-01-01','','edb'))['2013':].iplot(title='固定资产投资的月度同比（蓝）、PPI（橙）',legend=False,kind='spread')
investment_yty = macro_func.two_average(investment_yty)
macro_func.plot_seasonal(investment_yty,tl='的当月同比-两年平均')

# 生成固定资产投资：第一产业：单月值的序列：名义值
investment_first_series = macro_func.cusum_mtm_series('M0000276,M0000277','2002-02-01')
investment_first_series = macro_func.seasonal_adj(investment_first_series)
investment_first_series = np.log(investment_first_series)
investment_first_series = macro_func.trend_trace(investment_first_series,'固定资产投资：第一产业','2018-01','2019-12')

# 固定资产投资-第一产业的当月同比
investment_first_yty = macro_func.cusum_mtm('M0000276,M0000277','2010-01-01','')
investment_first_yty = macro_func.two_average(investment_first_yty)
investment_first_yty = investment_first_yty.drop(index=investment_first_yty[abs(investment_first_yty['M0000276'])>40].index)
macro_func.plot_seasonal(investment_first_yty,tl='的当月同比')


# 生成固定资产投资：第二产业：单月值的序列：名义值
investment_second_series = macro_func.cusum_mtm_series('M0000278,M0000279','2002-02-01')
investment_second_series = macro_func.seasonal_adj(investment_second_series)
investment_second_series = np.log(investment_second_series)
investment_second_series = macro_func.trend_trace(investment_second_series,'固定资产投资：第二产业','2018-01','2019-12')

# 固定资产投资-第二产业的当月同比
investment_second_yty = macro_func.cusum_mtm('M0000278,M0000279','2010-01-01','')
investment_second_yty = macro_func.two_average(investment_second_yty)
investment_second_yty.join(macro_func.export_average(macro_func.two_average(macro_func.get_data('M0000607','2006-01-01','','edb')))).iplot(title='第二产业固定资产投资的月度同比（蓝）、出口增速（橙）',legend=False)
macro_func.plot_seasonal(investment_second_yty,tl='的当月同比')


# # 生成固定资产投资：第三产业：单月值的序列：名义值
# investment_third_series = macro_func.cusum_mtm_series('M0000280,M0000281','2002-02-01')
# investment_third_series = macro_func.seasonal_adj(investment_third_series)
# investment_third_series = np.log(investment_third_series)
# investment_third_series = macro_func.trend_trace(investment_third_series,'固定资产投资：第三产业','2018-01','2019-12')

# 固定资产投资-第三产业的当月同比
investment_third_yty = macro_func.cusum_mtm('M0000280,M0000281','2010-01-01','')
investment_third_yty = macro_func.two_average(investment_third_yty)
macro_func.plot_seasonal(investment_third_yty,tl='的当月同比')


# 生成固定资产投资：房地产业：单月值的序列：名义值
investment_house_series = macro_func.cusum_mtm_series('S0029656,S0029657','2002-02-01')
investment_house_series = macro_func.seasonal_adj(investment_house_series)
investment_house_series = np.log(investment_house_series)
investment_house_series = macro_func.trend_trace(investment_house_series,'固定资产投资：房地产业','2018-01','2019-12')

# 固定资产投资-房地产业的当月同比
investment_house_yty = macro_func.cusum_mtm('S0029656,S0029657','2010-01-01','')
investment_house_yty = macro_func.two_average(investment_house_yty)
macro_func.plot_seasonal(investment_house_yty,tl='的当月同比')


# 生成固定资产投资：民间投资：单月值的序列：名义值
investment_private_series = macro_func.cusum_mtm_series('M5438207,M5438208','2005-01-01')
investment_private_series = macro_func.seasonal_adj(investment_private_series)
investment_private_series = np.log(investment_private_series)
investment_private_series = macro_func.trend_trace(investment_private_series,'固定资产投资：民间投资','2018-01','2019-12')

# 固定资产投资-民间投资的当月同比
investment_private_yty = macro_func.cusum_mtm('M5438207,M5438208','2010-01-01','')
investment_private_yty = macro_func.two_average(investment_private_yty)
macro_func.plot_seasonal(investment_private_yty,tl='的当月同比')


# 固定资产投资-采矿业投资的当月同比
investment_mining_yty = macro_func.cusum_mtm_1('M0000342,M0000343')
investment_mining_yty = macro_func.two_average(investment_mining_yty)
macro_func.plot_seasonal(investment_mining_yty,k=3,tl='的当月同比')


# 生成固定资产投资：制造业：单月值的序列：名义值
investment_manufacturing_series = macro_func.cusum_mtm_1_series('M0000356,M0000357')
investment_manufacturing_series = macro_func.seasonal_adj(investment_manufacturing_series)
investment_manufacturing_series = np.log(investment_manufacturing_series)
investment_manufacturing_series = macro_func.trend_trace(investment_manufacturing_series,'固定资产投资：制造业投资','2018-01','2019-12', plot_start='2017-01')

# 固定资产投资-制造业投资的当月同比
investment_manufacturing_yty = macro_func.cusum_mtm_1('M0000356,M0000357')
investment_manufacturing_yty = macro_func.two_average(investment_manufacturing_yty)
investment_manufacturing_yty.join(macro_func.export_average(macro_func.two_average(macro_func.get_data('M0000607','2006-01-01','','edb'))))['2018':].iplot(title='制造业固定资产投资的月度同比（蓝）、出口增速（橙）',legend=False)
macro_func.plot_seasonal(investment_manufacturing_yty,k=3,tl='的当月同比')


# 生成固定资产投资：基建：单月值的序列：名义值
investment_infrastructure_series = macro_func.cusum_mtm_1_series('M5440434,M5440435')
investment_infrastructure_series = macro_func.seasonal_adj(investment_infrastructure_series)
investment_infrastructure_series = np.log(investment_infrastructure_series)
investment_infrastructure_series = macro_func.trend_trace(investment_infrastructure_series,'固定资产投资：基建投资','2018-01','2019-12', plot_start='2017-01')

# 固定资产投资-基础设施建设投资的当月同比
investment_infrastructure_yty = macro_func.cusum_mtm_1('M5440434,M5440435')
investment_infrastructure_yty = macro_func.two_average(investment_infrastructure_yty)
macro_func.plot_seasonal(investment_infrastructure_yty,k=3,tl='的当月同比')

# 固定资产投资-电力热力燃气等公共事业投资的当月同比
investment_utility_yty = macro_func.cusum_mtm_1('M0000418,M0000419')
investment_utility_yty = macro_func.two_average(investment_utility_yty)
macro_func.plot_seasonal(investment_utility_yty,k=3,tl='的当月同比')

# 固定资产投资-交运仓储投资的当月同比
investment_transport_yty = macro_func.cusum_mtm_1('M0000428,M0000429')
investment_transport_yty = macro_func.two_average(investment_transport_yty)
macro_func.plot_seasonal(investment_transport_yty,k=3,tl='的当月同比')

# 固定资产投资-水利环境投资的当月同比
investment_environment_yty = macro_func.cusum_mtm_1('M0000454,M0000455')
investment_environment_yty = macro_func.two_average(investment_environment_yty)
macro_func.plot_seasonal(investment_environment_yty,k=3,tl='的当月同比')

# # 重点行业的固定资产投资累计同比的季节性
# industry_investment_yty = macro_func.get_data('M0000339,M0000343,M0000357,M0000359,M0000361,M0000367,M0000385,M0000387,M0000399,M0000401,M0000403,M0000405,M0068555,M0000407,M0000409,M0000411,M0000419,M0000429,M0000431,M0000433,M0000455,M0000457,M0000461,M0000465,M0000467,M0000471','2015-01-01','','edb')
# industry_investment_yty = macro_func.two_average(industry_investment_yty)
# for i in industry_investment_yty.columns[0:7]:
#     macro_func.plot_seasonal(industry_investment_yty[[i]],tl='累计同比的季节性')
# for i in industry_investment_yty.columns[7:14]:
#     macro_func.plot_seasonal(industry_investment_yty[[i]],tl='累计同比的季节性')
# for i in industry_investment_yty.columns[14:21]:
#     macro_func.plot_seasonal(industry_investment_yty[[i]],tl='累计同比的季节性')
# for i in industry_investment_yty.columns[21:]:
#     macro_func.plot_seasonal(industry_investment_yty[[i]],tl='累计同比的季节性')

# # 固定资产投资-农副食品加工业的当月同比
# investment_processing_food_yty = macro_func.cusum_mtm_1('M0000358,M0000359')
# investment_processing_food_yty = macro_func.two_average(investment_processing_food_yty)
# investment_processing_food_yty.join(macro_func.two_average(macro_func.get_data('M0000032','2006-01-01','','edb')))['2018':].iplot(title='农副食品加工业投资的月度同比（蓝）、工业增加值（橙）',secondary_y='M0000032',legend=False)
# macro_func.plot_seasonal(investment_processing_food_yty,k=3,tl='的当月同比')

# # 固定资产投资-食品制造业的当月同比
# investment_manufacture_food_yty = macro_func.cusum_mtm_1('M0000360,M0000361')
# investment_manufacture_food_yty = macro_func.two_average(investment_manufacture_food_yty)
# investment_manufacture_food_yty.join(macro_func.two_average(macro_func.get_data('M0000034','2006-01-01','','edb')))['2018':].iplot(title='食品制造业投资的月度同比（蓝）、工业增加值（橙）',secondary_y='M0000034',legend=False)
# macro_func.plot_seasonal(investment_manufacture_food_yty,k=3,tl='的当月同比')

# # 固定资产投资-纺织业的当月同比
# investment_textile_yty = macro_func.cusum_mtm_1('M0000366,M0000367')
# investment_textile_yty = macro_func.two_average(investment_textile_yty)
# investment_textile_yty.join(macro_func.two_average(macro_func.get_data('M0000040','2006-01-01','','edb')))['2018':].iplot(title='纺织业投资的月度同比（蓝）、工业增加值（橙）',secondary_y='M0000040',legend=False)
# macro_func.plot_seasonal(investment_textile_yty,k=3,tl='的当月同比')

# # 固定资产投资-化学制品制造业的当月同比
# investment_chemical_yty = macro_func.cusum_mtm_1('M0000384,M0000385')
# investment_chemical_yty = macro_func.two_average(investment_chemical_yty)
# investment_chemical_yty.join(macro_func.two_average(macro_func.get_data('M0000058','2006-01-01','','edb')))['2018':].iplot(title='化学制品制造业投资的月度同比（蓝）、工业增加值（橙）',secondary_y='M0000058',legend=False)
# macro_func.plot_seasonal(investment_chemical_yty,k=3,tl='的当月同比')

# # 固定资产投资-医药制造业的当月同比
# investment_medicine_yty = macro_func.cusum_mtm_1('M0000386,M0000387')
# investment_medicine_yty = macro_func.two_average(investment_medicine_yty)
# investment_medicine_yty.join(macro_func.two_average(macro_func.get_data('M0000060','2006-01-01','','edb')))['2018':].iplot(title='医药制造业投资的月度同比（蓝）、工业增加值（橙）',secondary_y='M0000060',legend=False)
# macro_func.plot_seasonal(investment_medicine_yty,k=3,tl='的当月同比')

# # 固定资产投资-有色金属冶炼业的当月同比
# investment_non_ferrous_yty = macro_func.cusum_mtm_1('M0000398,M0000399')
# investment_non_ferrous_yty = macro_func.two_average(investment_non_ferrous_yty)
# investment_non_ferrous_yty.join(macro_func.two_average(macro_func.get_data('M0000072','2006-01-01','','edb')))['2018':].iplot(title='有色金属冶炼业投资的月度同比（蓝）、工业增加值（橙）',secondary_y='M0000072',legend=False)
# macro_func.plot_seasonal(investment_non_ferrous_yty,k=3,tl='的当月同比')

# # 固定资产投资-金属制品业的当月同比
# investment_metal_yty = macro_func.cusum_mtm_1('M0000400,M0000401')
# investment_metal_yty = macro_func.two_average(investment_metal_yty)
# investment_metal_yty.join(macro_func.two_average(macro_func.get_data('M0000074','2006-01-01','','edb')))['2018':].iplot(title='金属制品业投资的月度同比（蓝）、工业增加值（橙）',secondary_y='M0000074',legend=False)
# macro_func.plot_seasonal(investment_metal_yty,k=3,tl='的当月同比')

# # 固定资产投资-通用设备制造业的当月同比
# investment_general_purpose_yty = macro_func.cusum_mtm_1('M0000402,M0000403')
# investment_general_purpose_yty = macro_func.two_average(investment_general_purpose_yty)
# investment_general_purpose_yty.join(macro_func.two_average(macro_func.get_data('M0000076','2006-01-01','','edb')))['2018':].iplot(title='通用设备制造业投资的月度同比（蓝）、工业增加值（橙）',secondary_y='M0000076',legend=False)
# macro_func.plot_seasonal(investment_general_purpose_yty,k=3,tl='的当月同比')

# # 固定资产投资-专用设备制造业的当月同比
# investment_special_purpose_yty = macro_func.cusum_mtm_1('M0000404,M0000405')
# investment_special_purpose_yty = macro_func.two_average(investment_special_purpose_yty)
# investment_special_purpose_yty.join(macro_func.two_average(macro_func.get_data('M0000078','2006-01-01','','edb')))['2018':].iplot(title='专用设备制造业投资的月度同比（蓝）、工业增加值（橙）',secondary_y='M0000078',legend=False)
# macro_func.plot_seasonal(investment_special_purpose_yty,k=3,tl='的当月同比')

# # 固定资产投资-汽车制造业的当月同比
# investment_vehicle_yty = macro_func.cusum_mtm_1('M0068554,M0068555')
# investment_vehicle_yty = macro_func.two_average(investment_vehicle_yty)
# investment_vehicle_yty.join(macro_func.two_average(macro_func.get_data('M0068071','2006-01-01','','edb')))['2018':].iplot(title='汽车制造业投资的月度同比（蓝）、工业增加值（橙）',secondary_y='M0068071',legend=False)
# macro_func.plot_seasonal(investment_vehicle_yty,k=3,tl='的当月同比')

# # 固定资产投资-铁路船舶制造业的当月同比
# investment_train_yty = macro_func.cusum_mtm_1('M0000406,M0000407')
# investment_train_yty = macro_func.two_average(investment_train_yty)
# investment_train_yty.join(macro_func.two_average(macro_func.get_data('M0000080','2006-01-01','','edb')))['2018':].iplot(title='铁路船舶制造业投资的月度同比（蓝）、工业增加值（橙）',secondary_y='M0000080',legend=False)
# macro_func.plot_seasonal(investment_train_yty,k=3,tl='的当月同比')

# # 固定资产投资-电气机械制造业的当月同比
# investment_electrical_machinery_yty = macro_func.cusum_mtm_1('M0000408,M0000409')
# investment_electrical_machinery_yty = macro_func.two_average(investment_electrical_machinery_yty)
# investment_electrical_machinery_yty.join(macro_func.two_average(macro_func.get_data('M0000082','2006-01-01','','edb')))['2018':].iplot(title='电气机械制造业投资的月度同比（蓝）、工业增加值（橙）',secondary_y='M0000082',legend=False)
# macro_func.plot_seasonal(investment_electrical_machinery_yty,k=3,tl='的当月同比')

# # 固定资产投资-计算机通信制造业的当月同比
# investment_computer_yty = macro_func.cusum_mtm_1('M0000410,M0000411')
# investment_computer_yty = macro_func.two_average(investment_computer_yty)
# investment_computer_yty.join(macro_func.two_average(macro_func.get_data('M0000084','2006-01-01','','edb')))['2018':].iplot(title='计算机通信制造业投资的月度同比（蓝）、工业增加值（橙）',secondary_y='M0000084',legend=False)
# macro_func.plot_seasonal(investment_computer_yty,k=3,tl='的当月同比')








