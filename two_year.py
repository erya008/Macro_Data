import pandas as pd
import numpy as np
import cufflinks as cf
import macro_func

# 导入需要的包
cf.set_config_file(offline=True,theme='white',dimensions=(550,350),colorscale='plotly')

two_year = macro_func.get_data('M0039354,M5567901,M5567902,M5567903,M0000545,M5767203,M0000607,M0000609,M0001428,M0061659,M0061660,M0000273,M0024063,M0024064','2015-01-01','','edb')
two_year.columns = macro_func.config(two_year)
two_year.to_csv(r'C:\Users\wanzh\OneDrive\金阳宏观\课题\两年平均增速/two_year.csv',encoding='utf_8_sig')
two_year_average = macro_func.two_average(two_year)
two_year_average.to_csv(r'C:\Users\wanzh\OneDrive\金阳宏观\课题\两年平均增速/two_year_average.csv',encoding='utf_8_sig')
