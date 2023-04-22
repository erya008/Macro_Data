# 当然可以。Tushare是一个开源的Python财经数据接口库，
# 它可以帮助用户获取股票、基金、期货等金融数据，并且提供了很多数据处理和分析的工具。
# 如果你想使用tushare库，首先需要在你的Python环境中安装它。
# 你可以使用pip命令来安装：pip install tushare。
# 安装完成后，你需要在tushare官网上注册账号，并获取你的token，这个token是用来验证你的身份的。
# 获取到token后，你就可以开始使用tushare库了。
# 使用tushare库获取数据非常简单，只需要调用相应的函数，传入相应的参数即可。
# 比如，如果你想获取某只股票的历史价格数据，你可以调用tushare提供的get_hist_data函数，传入股票代码和时间范围等参数即可。
# 你可以在tushare官网上查看所有的函数和参数，以及它们的用法。
# tushare库的数据参数可以在官方文档中查看，官方文档提供了详细的API接口说明和参数说明。
# 你可以在tushare官网上找到文档，或者在Python中使用help(tushare)命令来查看。
# 在文档中，你可以找到每个函数的输入参数和输出结果的详细说明，以及参数的默认值和可选值等信息。
# 此外，tushare官网还提供了很多使用示例和教程，可以帮助你更好地理解如何使用tushare库获取和处理金融数据。
# 在Python中使用tushare库，首先需要安装tushare库，可以使用pip命令安装：`pip install tushare`。
# 然后，你需要在tushare官网上注册账号，并获取你的token。
# 获取到token后，你可以在Python中使用如下代码来调用tushare库，并传入你的token：


import tushare as ts

# 设置token
ts.set_token('your_token_here')

# 初始化pro接口
pro = ts.pro_api()

# 调用接口函数
data = pro.xxx(params)


# 其中，`set_token()`函数用于设置你的token，`pro_api()`函数用于初始化tushare的pro接口，`xxx()`是具体的接口函数名称，`params`参数是对应接口函数需要传入的参数。请将上述代码中的 `your_token_here` 替换为你自己的token即可。



# 根据股票和债券的比例7：3，建立一个投资组合，按照股票和债券的比例，分别买入股票和债券，然后计算投资组合的年化收益率和年化波动率，每个月调仓一次
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import tushare as ts
import statsmodels.api as sm
import statsmodels.formula.api as smf

# 从tushare获取股票数据
def get_stock_data(stock_code, start_date, end_date):

    df = ts.get_k_data(stock_code, start=start_date, end=end_date)
    df = df.set_index('date')
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    df = df[['close']]
    df.columns = [stock_code]
    return df

# 从tushare获取债券数据
def get_bond_data(bond_code, start_date, end_date):

    df = ts.get_k_data(bond_code, start=start_date, end=end_date)
    df = df.set_index('date')
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    df = df[['close']]
    df.columns = [bond_code]
    return df

# 计算股票和债券的年化收益率
def get_annualized_return(df):
    
        df = df.sort_index()
        df = df.pct_change()
        df = df.dropna()
        df = df + 1
        df = df.cumprod()
        df = df.iloc[-1]
        df = df ** (252 / len(df)) - 1
        return df

# 计算股票和债券的年化波动率
def get_annualized_volatility(df):
        
            df = df.sort_index()
            df = df.pct_change()
            df = df.dropna()
            df = df.std() * np.sqrt(252)
            return df

# 计算股票和债券的夏普比率
def get_sharpe_ratio(df):
        
            df = df.sort_index()
            df = df.pct_change()
            df = df.dropna()
            df = df.mean() / df.std() * np.sqrt(252)
            return df

# 计算股票和债券的最大回撤
def get_max_drawdown(df):
            
                df = df.sort_index()
                df = df.pct_change()
                df = df.dropna()
                df = (1 + df).cumprod()
                df = df / df.cummax() - 1
                df = df.min()
                return df

# 计算股票和债券的协方差
def get_covariance(df):

    df = df.sort_index()
    df = df.pct_change()
    df = df.dropna()
    df = df.cov()
    return df

# 计算股票和债券的相关系数
def get_correlation(df):
            
        df = df.sort_index()
        df = df.pct_change()
        df = df.dropna()
        df = df.corr()
        return df

# 计算股票和债券的协方差矩阵
def get_covariance_matrix(df):
                
                df = df.sort_index()
                df = df.pct_change()
                df = df.dropna()
                df = df.cov()
                return df

# 计算股票和债券的相关系数矩阵
def get_correlation_matrix(df):
        
        df = df.sort_index()
        df = df.pct_change()
        df = df.dropna()
        df = df.corr()
        return df

# 计算股票和债券的协方差矩阵的逆矩阵
def get_inverse_covariance_matrix(df):
        
        df = df.sort_index()
        df = df.pct_change()
        df = df.dropna()
        df = df.cov()
        df = np.linalg.inv(df)
        return df

# 绘制投资组合的投资收益率和投资波动率的折线图
def plot_portfolio(df):
                
                df = df.sort_index()
                df = df.pct_change()
                df = df.dropna()
                df = df + 1
                df = df.cumprod()
                df.plot()
                plt.show()

# 绘制投资组合的夏普比率的折线图
def plot_sharpe_ratio(df):
            
            df = df.sort_index()
            df = df.pct_change()
            df = df.dropna()
            df = df.mean() / df.std() * np.sqrt(252)
            df.plot()
            plt.show()

# 绘制投资组合的最大回撤的折线图
def plot_max_drawdown(df):
                
                df = df.sort_index()
                df = df.pct_change()
                df = df.dropna()
                df = (1 + df).cumprod()
                df = df / df.cummax() - 1
                df = df.min()
                df.plot()
                plt.show()


import pandas as pd

def fill_monthly_data(df):
    """
    将DataFrame中缺失的1月和2月的单月数据补全为累计数据的1月和2月的数据

    参数：
    df：pandas.DataFrame，需要进行填充操作的DataFrame，时间索引为'yyyy-mm'格式，有单月数据列和累计数据列

    返回：
    无返回，直接对原DataFrame进行修改
    """
    df.index = pd.to_datetime(df.index)

    years = df.index.year.unique()
    months = df.index.month.unique()

    for year in years:
        for month in months:
            month_data = df.loc[f'{year}-{month:02}']
            cumulative_data = month_data['累计数据']
            if month in [1, 2]:
                month_data['单月数据'] = cumulative_data
            else:
                month_data['单月数据'].fillna(method='ffill', inplace=True)


# 我有一个DataFrame数据，有很多年，index是月份，时间index的格式是yyyy-mm，一列是加总数据，其他列是各分项数据，我希望计算各分项对加总数据的同比拉动作用，并输出累计柱状图

import pandas as pd
import matplotlib.pyplot as plt

def calculate_contribution(df):
    """
    计算各分项对加总数据的同比拉动作用，并输出累计柱状图

    参数：
    df：pandas.DataFrame，需要进行计算的DataFrame，时间索引为'yyyy-mm'格式，有加总数据列和各分项数据列

    返回：
    无返回，直接输出累计柱状图
    """
    df.index = pd.to_datetime(df.index)

    years = df.index.year.unique()
    months = df.index.month.unique()

    contribution = pd.DataFrame(columns=df.columns[1:])
    for year in years:
        for month in months:
            month_data = df.loc[f'{year}-{month:02}']
            if month == 1:
                last_year_data = df.loc[f'{year-1}-12']
            else:
                last_year_data = df.loc[f'{year}-{month-1:02}']

            if not last_year_data.empty:
                contribution.loc[f'{year}-{month:02}'] = (month_data.iloc[:, 1:] / last_year_data.iloc[:, 1:] - 1).sum()
    
    cumulative_contribution = contribution.cumsum()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    cumulative_contribution.plot(kind='bar', ax=ax)
    ax.set(title='各分项对加总数据的同比拉动作用累计柱状图', xlabel='时间', ylabel='同比拉动作用')
    plt.show()






# 例如，单月数据是这样的：
# 3月  100
# 4月  200
# 5月  300
# 6月  400
# 7月  500
# 8月  600
# 9月  700
# 10月 800
# 11月 900
# 12月 1000
# 累计数据是这样的：
# 1月  100
# 2月  200
# 3月  300
# 4月  500
# 5月  800
# 6月  1200
# 7月  1700
# 8月  2300
# 9月  3000
# 10月 3800
# 11月 4700
# 12月 5700
# 我希望把单月数据补全成这样的：
# 1月  100
# 2月  200
# 3月  100
# 4月  200
# 5月  300
# 6月  400      
# 7月  500
# 8月  600
# 9月  700
# 10月 800
# 11月 900
# 12月 1000

# 请问有什么方法可以实现吗？

# 以下是我尝试的方法，但是没有成功，希望大家帮忙看看，谢谢！

# 1. 用pandas的reindex方法
# 2. 用pandas的shift方法
# 3. 用pandas的fillna方法
# 4. 用pandas的interpolate方法
# 5. 用pandas的ffill方法
# 6. 用pandas的bfill方法
# 7. 用pandas的asfreq方法
# 8. 用pandas的resample方法
# 9. 用pandas的rolling方法
# 10. 用pandas的ewm方法
# 11. 用pandas的expanding方法
# 12. 用pandas的diff方法
# 13. 用pandas的pct_change方法
# 14. 用pandas的cumsum方法
# 15. 用pandas的cumprod方法

# 以下是我尝试的代码，但是没有成功，希望大家帮忙看看，谢谢！

# 1. 用pandas的reindex方法
# 1.1 用pandas的reindex方法，把单月数据的index设置为累计数据的index
# 1.2 用pandas的reindex方法，把累计数据的index设置为单月数据的index
# 1.3 用pandas的reindex方法，把单月数据的index设置为累计数据的index，把method设置为ffill
# 1.4 用pandas的reindex方法，把单月数据的index设置为累计数据的index，把method设置为bfill
# 1.5 用pandas的reindex方法，把单月数据的index设置为累计数据的index，把method设置为nearest
# 1.6 用pandas的reindex方法，把单月数据的index设置为累计数据的index，把method设置为pad
# 1.7 用pandas的reindex方法，把单月数据的index设置为累计数据的index，把method设置为backfill
# 1.8 用pandas的reindex方法，把单月数据的index设置为累计数据的index，把method设置为nearest
# 1.9 用pandas的reindex方法，把单月数据的index设置为累计数据的index，把method设置为nearest，把limit设置为1
# 1.10 用pandas的reindex方法，把单月数据的index设置为累计数据的index，把method设置为nearest，把limit设置为2
# 1.11 用pandas的reindex方法，把单月数据的index设置为累计数据的index，把method设置为nearest，把limit设置为3
# 1.12 用pandas的reindex方法，把单月数据的index设置为累计数据的index，把method设置为nearest，把limit设置为4
# 1.13 用pandas的reindex方法，把单月数据的index设置为累计数据的index，把method设置为nearest，把limit设置为5
# 1.14 用pandas的reindex方法，把单月数据的index设置为累计数据的index，把method设置为nearest，把limit设置为6
# 1.15 用pandas的reindex方法，把单月数据的index设置为累计数据的index，把method设置为nearest，把limit设置为7
# 1.16 用pandas的reindex方法，把单月数据的index设置为累计数据的index，把method设置为nearest，把limit设置为8
# 1.17 用pandas的reindex方法，把单月数据的index设置为累计数据的index，把method设置为nearest，把limit设置为9
# 1.18 用pandas的reindex方法，把单月数据的index设置为累计数据的index，把method设置为nearest，把limit设置为10
# 1.19 用pandas的reindex方法，把单月数据的index设置为累计数据的index，把method设置为nearest，把limit设置为11
# 1.20 用pandas的reindex方法，把单月数据的index设置为累计数据的index，把method设置为nearest，把limit设置为12
# 给我具体的代码，谢谢！


OP:

# 1. 用pandas的reindex方法
# 1.1 用pandas的reindex方法，把单月数据的index设置为累计数据的index

import pandas as pd
import numpy as np

df1 = pd.DataFrame({'A': [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]}, index=pd.date_range('2019-03-01', periods=10, freq='M'))
df2 = pd.DataFrame({'A': [100, 200, 300, 500, 800, 1200, 1700, 2300, 3000, 3800, 4700, 5700]}, index=pd.date_range('2019-01-01', periods=12, freq='M'))

df1.reindex(df2.index)

# 1.2 用pandas的reindex方法，把累计数据的index设置为单月数据的index

df2.reindex(df1.index)

# 1.3 用pandas的reindex方法，把单月数据的index设置为累计数据的index，把method设置为ffill

df1.reindex(df2.index, method='ffill')


# 1.4 用pandas的reindex方法，把单月数据的index设置为累计数据的index，把method设置为bfill

df1.reindex(df2.index, method='bfill')

# 1.5 用pandas的reindex方法，把单月数据的index设置为累计数据的index，把method设置为nearest

df1.reindex(df2.index, method='nearest')

# 1.6 用pandas的reindex方法，把单月数据的index设置为累计数据的index，把method设置为pad

df1.reindex(df2.index, method='pad')

# 1.7 用pandas的reindex方法，把单月数据的index设置为累计数据的index，把method设置为backfill

df1.reindex(df2.index, method='backfill')

# 1.8 用pandas的reindex方法，把单月数据的index设置为累计数据的index，把method设置为nearest

df1.reindex(df2.index, method='nearest')

# 1.9 用pandas的reindex方法，把单月数据的index设置为累计数据的index，把method设置为nearest，把limit设置为1

df1.reindex(df2.index, method='nearest', limit=1)

# 1.10 用pandas的reindex方法，把单月数据的index设置为累计数据的index，把method设置为nearest，把limit设置为2

df1.reindex(df2.index, method='nearest', limit=2)

# 1.11 用pandas的reindex方法，把单月数据的index设置为累计数据的index，把method设置为nearest，把limit设置为3

df1.reindex(df2.index, method='nearest', limit=3)

# 1.12 用pandas的reindex方法，把单月数据的index设置为累计数据的index，把method设置为nearest，把limit设置为4

df1.reindex(df2.index, method='nearest', limit=4)

# 2. 用pandas的shift方法