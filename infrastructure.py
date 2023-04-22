import pandas as pd
import numpy as np
import cufflinks as cf
import macro_func

# 导入需要的包
cf.set_config_file(offline=True,theme='white',dimensions=(550,350),colorscale='plotly')

# 基建固定资产投资的处理
investment_infrastructure = macro_func.value_yty_adj('M5440434,M5440435','2004-02',base=2017)
investment_infrastructure = macro_func.cusum_q(investment_infrastructure)
investment_infrastructure = macro_func.seasonal_adj(investment_infrastructure, fq='Q')

# 电力热力固定资产投资的处理
investment_utility = macro_func.value_yty_adj('M0000418,M0000419','2004-02',base=2017)
investment_utility = macro_func.cusum_q(investment_utility)
investment_utility = macro_func.seasonal_adj(investment_utility, fq='Q')

# 交运仓储固定资产投资的处理
investment_transport = macro_func.value_yty_adj('M0000428,M0000429','2004-02',base=2017)
investment_transport = macro_func.cusum_q(investment_transport)
investment_transport = macro_func.seasonal_adj(investment_transport, fq='Q')

# 水利环境固定资产投资的处理
investment_environment = macro_func.value_yty_adj('M0000454,M0000455','2004-02',base=2017)
investment_environment = macro_func.cusum_q(investment_environment)
investment_environment = macro_func.seasonal_adj(investment_environment, fq='Q')

# ppi_index = macro_func.value_yty_adj('M5567965,M0001227','2002-03')
# investment = investment.join(ppi_index)
# investment.iloc[:,0] = np.array(investment.iloc[:,0])/np.array(investment.iloc[:,1])
# investment = macro_func.seasonal_adj(investment.iloc[:,0].to_frame())
# investment.columns = ['investment']
# investment.to_csv(r'C:\Users\wanzh\OneDrive\金阳宏观\课题\Nowcast\invest.csv')