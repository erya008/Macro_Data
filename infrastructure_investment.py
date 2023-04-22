from matplotlib.pyplot import axis
import pandas as pd
import numpy as np
import cufflinks as cf
import macro_func

# 导入需要的包
cf.set_config_file(offline=True,theme='white',dimensions=(550,350),colorscale='plotly')

# 企业中长期贷款当月值
loan = macro_func.get_data('M0057877','2008-01','','edb')
loan = loan.resample('M').mean()
loan_s = macro_func.seasonal_adj(loan)
loan_s_diff = loan_s.diff(periods=12)
loan_s_diff = macro_func.winsor_percentile(loan_s_diff,0.05,0.95)
loan_s_diff_bi = macro_func.bi_weight(loan_s_diff)
# loan_s_diff_bi = macro_func.normalization(loan_s_diff_bi)
loan_s_diff_bi.columns = ['贷款']
loan_s_diff_bi.iplot(title='企业中长期贷款')

# 新增信托贷款
trust = macro_func.get_data('M5206734','2008-01','','edb')
trust = trust.resample('M').mean()
trust_s = macro_func.seasonal_adj(trust)
trust_s_diff = trust_s.diff(periods=12)
trust_s_diff = macro_func.winsor_percentile(trust_s_diff,0.41,0.9)
trust_s_diff_bi = macro_func.bi_weight(trust_s_diff)
# trust_s_diff_bi = macro_func.normalization(trust_s_diff_bi)
trust_s_diff_bi.columns = ['信托']
trust_s_diff_bi.iplot(title='信托贷款')

# 新增M2
m2 = macro_func.get_data('M0001384','2007-12','','edb')
m2 = m2.resample('M').mean()
m2 = m2.diff()
m2.drop(m2.head(1).index, inplace=True)
m2_s = macro_func.seasonal_adj(m2)
m2_s_diff = m2_s.diff(periods=12)
m2_s_diff = macro_func.winsor_percentile(m2_s_diff,0.05,0.95)
m2_s_diff_bi = macro_func.bi_weight(m2_s_diff)
# m2_s_diff_bi = macro_func.normalization(m2_s_diff_bi)
m2_s_diff_bi.columns = ['M2']
m2_s_diff_bi.iplot(title='M2')

# 建筑业PMI
pmi = macro_func.get_data('M5207831','2012-02','','edb')
pmi = pmi.resample('M').mean()
pmi = pmi.rolling(12).mean()
pmi.drop(pmi.head(11).index, inplace=True)
pmi_s = macro_func.seasonal_adj(pmi)
pmi_s_bi = macro_func.bi_weight(pmi_s)
# pmi_s_bi = macro_func.normalization(pmi_s_bi)
pmi_s_bi.columns = ['PMI']
pmi_s_bi.iplot(title='pmi')

# 沥青开工率
liq = macro_func.get_data('S5449386','2015-06-05','','edb')
liq = liq.resample('M').mean()
liq_s = macro_func.seasonal_adj(liq)
liq_s_bi = macro_func.bi_weight(liq_s)
# liq_s_bi = macro_func.normalization(liq_s_bi)
liq_s_bi.columns = ['沥青']
liq_s_bi.iplot(title='沥青开工率')

# 螺纹钢产量
luowg = macro_func.get_data('S5713307','2015-02-27','','edb')
luowg = luowg.resample('M').mean()
luowg_s = macro_func.seasonal_adj(luowg)
luowg_s_rate = luowg_s.pct_change(12)*100
luowg_s_rate = macro_func.winsor_percentile(luowg_s_rate, 0.05, 0.95)
luowg_s_rate_bi = macro_func.bi_weight(luowg_s_rate)
# luowg_s_rate_bi = macro_func.normalization(luowg_s_rate_bi)
luowg_s_rate_bi.columns = ['螺纹钢']
luowg_s_rate_bi.iplot(title='螺纹钢产量')

# 水泥库容比
shuin = macro_func.get_data('C0740008','2017-06-02','','edb')
shuin = shuin.resample('M').mean()
shuin_s = macro_func.seasonal_adj(shuin)
shuin_s_bi = macro_func.bi_weight(shuin_s)
# shuin_s_bi = macro_func.normalization(shuin_s_bi)
shuin_s_bi.columns = ['水泥']
shuin_s_bi = shuin_s_bi * (-1)
shuin_s_bi.iplot(title='水泥库容比')

# 挖掘机开工小时数
waj = macro_func.get_data('S6018690','2017-05','','edb')
waj = waj.resample('M').mean()
waj_s = macro_func.seasonal_adj(waj)
waj_s = macro_func.winsor_percentile(waj_s,0.4,0.9)
waj_s_bi = macro_func.bi_weight(waj_s)
# waj_s_bi = macro_func.normalization(waj_s_bi)
waj_s_bi.columns = ['挖掘机']
waj_s_bi.iplot(title='挖掘机开工小时数')

# 合并数据
data = pd.concat([loan_s_diff_bi, trust_s_diff_bi, m2_s_diff_bi, pmi_s_bi, liq_s_bi, luowg_s_rate_bi, shuin_s_bi, waj_s_bi], axis=1)

# 剔除缺失值
data.dropna(inplace=True)

# data.drop(['loan','trust','m2','waj'], axis=1, inplace=True)

data.iplot()

# 标准化
data = macro_func.normalization(data)

data.iplot(title='基建主要指标跟踪')

result_pca = macro_func.pca_n(data, n=2)
result_pca.columns = ['基建_第一主成分', '基建_第二主成分']
result_pca = result_pca*(-1)
result_pca.iplot(title='基建投资的主成分指标')

from sklearn.decomposition import PCA
pca = PCA(n_components=2)
pca.fit(data)
jj_hq = pca.fit_transform(data)
jj_hq = pd.DataFrame(jj_hq*(-1),index=data.index,columns=['基建_第一主成分', '基建_第二主成分'])
data.join(jj_hq).iplot()

print(pca.explained_variance_ratio_)
print(pca.explained_variance_)

