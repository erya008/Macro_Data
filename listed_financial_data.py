import pandas as pd
import numpy as np
import cufflinks as cf
import macro_func

# 导入需要的包
cf.set_config_file(offline=True,theme='white',dimensions=(550,350),colorscale='plotly')

# 设定数据默认路径
data_path=r'C:\Users\wanzh\OneDrive\金阳宏观\交办课题\零容忍政策\财务数据'

# 读取excel原始数据
data=pd.read_excel(io=f'{data_path}\\上市公司财务数据.xlsx')
data=data[:-2] # 最后两行是Wind注释，删除

# 变量重命名，便于后续统一替换
# 变量名基于Wind命名规则
data.columns=['trade_code','sec_code','corpscale','industry_nc','industry_sw_2021','industry_gics','tot_oper_rev_2016','tot_oper_rev_2017','tot_oper_rev_2018','tot_oper_rev_2019','tot_oper_rev_2019q3','tot_oper_rev_2020q3','tot_oper_rev_2021q3',
'np_belongto_parcomsh_2016','np_belongto_parcomsh_2017','np_belongto_parcomsh_2018','np_belongto_parcomsh_2019','np_belongto_parcomsh_2019q3','np_belongto_parcomsh_2020q3','np_belongto_parcomsh_2021q3',
'employee_2016','employee_2017','employee_2018','employee_2019','employee_2019q3','employee_2020q3','employee_2021q3']

# 设置证券代码为索引列
data.set_index('trade_code',inplace=True)

# 计算上市A股整体数据
result_all = pd.ExcelWriter(f'{data_path}\\result_all.xlsx')

all_revenue_year=data[data[['tot_oper_rev_2016','tot_oper_rev_2017','tot_oper_rev_2018','tot_oper_rev_2019']].notna()]
all_revenue_year=all_revenue_year[['tot_oper_rev_2016','tot_oper_rev_2017','tot_oper_rev_2018','tot_oper_rev_2019']]
all_revenue_year.loc['sum']=all_revenue_year.apply(lambda x: x.sum())
all_revenue_year.loc[['sum']].to_excel(result_all,'revenue_year')
all_revenue_quarter=data[data[['tot_oper_rev_2019q3','tot_oper_rev_2020q3','tot_oper_rev_2021q3']].notna()]
all_revenue_quarter=all_revenue_quarter[['tot_oper_rev_2019q3','tot_oper_rev_2020q3','tot_oper_rev_2021q3']]
all_revenue_quarter.loc['sum']=all_revenue_quarter.apply(lambda x: x.sum())
all_revenue_quarter.loc[['sum']].to_excel(result_all,'revenue_quarter')

all_profit_year=data[data[['np_belongto_parcomsh_2016','np_belongto_parcomsh_2017','np_belongto_parcomsh_2018','np_belongto_parcomsh_2019']].notna()]
all_profit_year=all_profit_year[['np_belongto_parcomsh_2016','np_belongto_parcomsh_2017','np_belongto_parcomsh_2018','np_belongto_parcomsh_2019']]
all_profit_year.loc['sum']=all_profit_year.apply(lambda x: x.sum())
all_profit_year.loc[['sum']].to_excel(result_all,'profit_year')
all_profit_quarter=data[data[['np_belongto_parcomsh_2019q3','np_belongto_parcomsh_2020q3','np_belongto_parcomsh_2021q3']].notna()]
all_profit_quarter=all_profit_quarter[['np_belongto_parcomsh_2019q3','np_belongto_parcomsh_2020q3','np_belongto_parcomsh_2021q3']]
all_profit_quarter.loc['sum']=all_profit_quarter.apply(lambda x: x.sum())
all_profit_quarter.loc[['sum']].to_excel(result_all,'profit_quarter')

all_labor_year=data[data[['employee_2016','employee_2017','employee_2018','employee_2019']].notna()]
all_labor_year=all_labor_year[['employee_2016','employee_2017','employee_2018','employee_2019']]
all_labor_year.loc['sum']=all_labor_year.apply(lambda x: x.sum())
all_labor_year.loc[['sum']].to_excel(result_all,'labor_year')
all_labor_quarter=data[data[['employee_2019q3','employee_2020q3','employee_2021q3']].notna()]
all_labor_quarter=all_labor_quarter[['employee_2019q3','employee_2020q3','employee_2021q3']]
all_labor_quarter.loc['sum']=all_labor_quarter.apply(lambda x: x.sum())
all_labor_quarter.loc[['sum']].to_excel(result_all,'labor_quarter')

result_all.save()


# 获得申万行业列表
industry_sw_21=data['industry_sw_2021'].unique()

# 营业总收入结果表
# 生成带列名的空DataFrame
revenue_year=pd.DataFrame(columns=['tot_oper_rev_2016','tot_oper_rev_2017','tot_oper_rev_2018','tot_oper_rev_2019'])
revenue_quarter=pd.DataFrame(columns=['tot_oper_rev_2019q3','tot_oper_rev_2020q3','tot_oper_rev_2021q3'])
for i in industry_sw_21: # 针对每个申万行业做循环
    revenue=data[data['industry_sw_2021']==i]
    _revenue_year=revenue[revenue[['tot_oper_rev_2016','tot_oper_rev_2017','tot_oper_rev_2018','tot_oper_rev_2019']].notna()] # 提取2016、2017、2018、2019年非空的数据
    _revenue_year=_revenue_year[['tot_oper_rev_2016','tot_oper_rev_2017','tot_oper_rev_2018','tot_oper_rev_2019']]
    _revenue_year.loc[i]=_revenue_year.apply(lambda x: x.sum()) # 对列求和
    revenue_year=revenue_year.append(_revenue_year.loc[[i]]) # 合并各行业数据
    
    _revenue_quarter=revenue[revenue[['tot_oper_rev_2019q3','tot_oper_rev_2020q3','tot_oper_rev_2021q3']].notna()]
    _revenue_quarter=_revenue_quarter[['tot_oper_rev_2019q3','tot_oper_rev_2020q3','tot_oper_rev_2021q3']]
    _revenue_quarter.loc[i]=_revenue_quarter.apply(lambda x: x.sum())
    revenue_quarter=revenue_quarter.append(_revenue_quarter.loc[[i]])
    
# 输出结果
result_revenue_sw = pd.ExcelWriter(f'{data_path}\\result_revenue_sw.xlsx')
revenue_year.to_excel(result_revenue_sw,'year')
revenue_quarter.to_excel(result_revenue_sw,'quarter')
result_revenue_sw.save()

# 归母净利润结果表
# 生成带列名的空DataFrame
profit_year=pd.DataFrame(columns=['np_belongto_parcomsh_2016','np_belongto_parcomsh_2017','np_belongto_parcomsh_2018','np_belongto_parcomsh_2019'])
profit_quarter=pd.DataFrame(columns=['np_belongto_parcomsh_2019q3','np_belongto_parcomsh_2020q3','np_belongto_parcomsh_2021q3'])
for i in industry_sw_21: # 针对每个申万行业做循环
    profit=data[data['industry_sw_2021']==i]
    _profit_year=profit[profit[['np_belongto_parcomsh_2016','np_belongto_parcomsh_2017','np_belongto_parcomsh_2018','np_belongto_parcomsh_2019']].notna()] # 提取2016、2017、2018、2019年非空的数据
    _profit_year=_profit_year[['np_belongto_parcomsh_2016','np_belongto_parcomsh_2017','np_belongto_parcomsh_2018','np_belongto_parcomsh_2019']]
    _profit_year.loc[i]=_profit_year.apply(lambda x: x.sum()) # 对列求和
    profit_year=profit_year.append(_profit_year.loc[[i]]) # 合并各行业数据
    
    _profit_quarter=profit[profit[['np_belongto_parcomsh_2019q3','np_belongto_parcomsh_2020q3','np_belongto_parcomsh_2021q3']].notna()]
    _profit_quarter=_profit_quarter[['np_belongto_parcomsh_2019q3','np_belongto_parcomsh_2020q3','np_belongto_parcomsh_2021q3']]
    _profit_quarter.loc[i]=_profit_quarter.apply(lambda x: x.sum())
    profit_quarter=profit_quarter.append(_profit_quarter.loc[[i]])
    
# 输出结果
result_profit_sw = pd.ExcelWriter(f'{data_path}\\result_profit_sw.xlsx')
profit_year.to_excel(result_profit_sw,'year')
profit_quarter.to_excel(result_profit_sw,'quarter')
result_profit_sw.save()

# 员工总数结果表
# 生成带列名的空DataFrame
labor_year=pd.DataFrame(columns=['employee_2016','employee_2017','employee_2018','employee_2019'])
labor_quarter=pd.DataFrame(columns=['employee_2019q3','employee_2020q3','employee_2021q3'])
for i in industry_sw_21: # 针对每个申万行业做循环
    labor=data[data['industry_sw_2021']==i]
    _labor_year=labor[labor[['employee_2016','employee_2017','employee_2018','employee_2019']].notna()] # 提取2016、2017、2018、2019年非空的数据
    _labor_year=_labor_year[['employee_2016','employee_2017','employee_2018','employee_2019']]
    _labor_year.loc[i]=_labor_year.apply(lambda x: x.sum()) # 对列求和
    labor_year=labor_year.append(_labor_year.loc[[i]]) # 合并各行业数据
    
    _labor_quarter=labor[labor[['employee_2019q3','employee_2020q3','employee_2021q3']].notna()]
    _labor_quarter=_labor_quarter[['employee_2019q3','employee_2020q3','employee_2021q3']]
    _labor_quarter.loc[i]=_labor_quarter.apply(lambda x: x.sum())
    labor_quarter=labor_quarter.append(_labor_quarter.loc[[i]])
    
# 输出结果
result_labor_sw = pd.ExcelWriter(f'{data_path}\\result_labor_sw.xlsx')
labor_year.to_excel(result_labor_sw,'year')
labor_quarter.to_excel(result_labor_sw,'quarter')
result_labor_sw.save()


# 获得国民经济行业列表
industry_nc=data['industry_nc'].unique()

# 营业总收入结果表
# 生成带列名的空DataFrame
revenue_year=pd.DataFrame(columns=['tot_oper_rev_2016','tot_oper_rev_2017','tot_oper_rev_2018','tot_oper_rev_2019'])
revenue_quarter=pd.DataFrame(columns=['tot_oper_rev_2019q3','tot_oper_rev_2020q3','tot_oper_rev_2021q3'])
for i in industry_nc: # 针对每个申万行业做循环
    revenue=data[data['industry_nc']==i]
    _revenue_year=revenue[revenue[['tot_oper_rev_2016','tot_oper_rev_2017','tot_oper_rev_2018','tot_oper_rev_2019']].notna()] # 提取2016、2017、2018、2019年非空的数据
    _revenue_year=_revenue_year[['tot_oper_rev_2016','tot_oper_rev_2017','tot_oper_rev_2018','tot_oper_rev_2019']]
    _revenue_year.loc[i]=_revenue_year.apply(lambda x: x.sum()) # 对列求和
    revenue_year=revenue_year.append(_revenue_year.loc[[i]]) # 合并各行业数据
    
    _revenue_quarter=revenue[revenue[['tot_oper_rev_2019q3','tot_oper_rev_2020q3','tot_oper_rev_2021q3']].notna()]
    _revenue_quarter=_revenue_quarter[['tot_oper_rev_2019q3','tot_oper_rev_2020q3','tot_oper_rev_2021q3']]
    _revenue_quarter.loc[i]=_revenue_quarter.apply(lambda x: x.sum())
    revenue_quarter=revenue_quarter.append(_revenue_quarter.loc[[i]])
    
# 输出结果
result_revenue_nc = pd.ExcelWriter(f'{data_path}\\result_revenue_nc.xlsx')
revenue_year.to_excel(result_revenue_nc,'year')
revenue_quarter.to_excel(result_revenue_nc,'quarter')
result_revenue_nc.save()

# 归母净利润结果表
# 生成带列名的空DataFrame
profit_year=pd.DataFrame(columns=['np_belongto_parcomsh_2016','np_belongto_parcomsh_2017','np_belongto_parcomsh_2018','np_belongto_parcomsh_2019'])
profit_quarter=pd.DataFrame(columns=['np_belongto_parcomsh_2019q3','np_belongto_parcomsh_2020q3','np_belongto_parcomsh_2021q3'])
for i in industry_nc: # 针对每个申万行业做循环
    profit=data[data['industry_nc']==i]
    _profit_year=profit[profit[['np_belongto_parcomsh_2016','np_belongto_parcomsh_2017','np_belongto_parcomsh_2018','np_belongto_parcomsh_2019']].notna()] # 提取2016、2017、2018、2019年非空的数据
    _profit_year=_profit_year[['np_belongto_parcomsh_2016','np_belongto_parcomsh_2017','np_belongto_parcomsh_2018','np_belongto_parcomsh_2019']]
    _profit_year.loc[i]=_profit_year.apply(lambda x: x.sum()) # 对列求和
    profit_year=profit_year.append(_profit_year.loc[[i]]) # 合并各行业数据
    
    _profit_quarter=profit[profit[['np_belongto_parcomsh_2019q3','np_belongto_parcomsh_2020q3','np_belongto_parcomsh_2021q3']].notna()]
    _profit_quarter=_profit_quarter[['np_belongto_parcomsh_2019q3','np_belongto_parcomsh_2020q3','np_belongto_parcomsh_2021q3']]
    _profit_quarter.loc[i]=_profit_quarter.apply(lambda x: x.sum())
    profit_quarter=profit_quarter.append(_profit_quarter.loc[[i]])
    
# 输出结果
result_profit_nc = pd.ExcelWriter(f'{data_path}\\result_profit_nc.xlsx')
profit_year.to_excel(result_profit_nc,'year')
profit_quarter.to_excel(result_profit_nc,'quarter')
result_profit_nc.save()

# 员工总数结果表
# 生成带列名的空DataFrame
labor_year=pd.DataFrame(columns=['employee_2016','employee_2017','employee_2018','employee_2019'])
labor_quarter=pd.DataFrame(columns=['employee_2019q3','employee_2020q3','employee_2021q3'])
for i in industry_nc: # 针对每个申万行业做循环
    labor=data[data['industry_nc']==i]
    _labor_year=labor[labor[['employee_2016','employee_2017','employee_2018','employee_2019']].notna()] # 提取2016、2017、2018、2019年非空的数据
    _labor_year=_labor_year[['employee_2016','employee_2017','employee_2018','employee_2019']]
    _labor_year.loc[i]=_labor_year.apply(lambda x: x.sum()) # 对列求和
    labor_year=labor_year.append(_labor_year.loc[[i]]) # 合并各行业数据
    
    _labor_quarter=labor[labor[['employee_2019q3','employee_2020q3','employee_2021q3']].notna()]
    _labor_quarter=_labor_quarter[['employee_2019q3','employee_2020q3','employee_2021q3']]
    _labor_quarter.loc[i]=_labor_quarter.apply(lambda x: x.sum())
    labor_quarter=labor_quarter.append(_labor_quarter.loc[[i]])
    
# 输出结果
result_labor_nc = pd.ExcelWriter(f'{data_path}\\result_labor_nc.xlsx')
labor_year.to_excel(result_labor_nc,'year')
labor_quarter.to_excel(result_labor_nc,'quarter')
result_labor_nc.save()

# 获得企业规模列表
scale=data['corpscale'].unique()

# 营业总收入结果表
# 生成带列名的空DataFrame
revenue_year=pd.DataFrame(columns=['tot_oper_rev_2016','tot_oper_rev_2017','tot_oper_rev_2018','tot_oper_rev_2019'])
revenue_quarter=pd.DataFrame(columns=['tot_oper_rev_2019q3','tot_oper_rev_2020q3','tot_oper_rev_2021q3'])
for i in scale: # 针对每个申万行业做循环
    revenue=data[data['corpscale']==i]
    _revenue_year=revenue[revenue[['tot_oper_rev_2016','tot_oper_rev_2017','tot_oper_rev_2018','tot_oper_rev_2019']].notna()] # 提取2016、2017、2018、2019年非空的数据
    _revenue_year=_revenue_year[['tot_oper_rev_2016','tot_oper_rev_2017','tot_oper_rev_2018','tot_oper_rev_2019']]
    _revenue_year.loc[i]=_revenue_year.apply(lambda x: x.sum()) # 对列求和
    revenue_year=revenue_year.append(_revenue_year.loc[[i]]) # 合并各行业数据
    
    _revenue_quarter=revenue[revenue[['tot_oper_rev_2019q3','tot_oper_rev_2020q3','tot_oper_rev_2021q3']].notna()]
    _revenue_quarter=_revenue_quarter[['tot_oper_rev_2019q3','tot_oper_rev_2020q3','tot_oper_rev_2021q3']]
    _revenue_quarter.loc[i]=_revenue_quarter.apply(lambda x: x.sum())
    revenue_quarter=revenue_quarter.append(_revenue_quarter.loc[[i]])
    
# 输出结果
result_revenue_scale = pd.ExcelWriter(f'{data_path}\\result_revenue_scale.xlsx')
revenue_year.to_excel(result_revenue_scale,'year')
revenue_quarter.to_excel(result_revenue_scale,'quarter')
result_revenue_scale.save()

