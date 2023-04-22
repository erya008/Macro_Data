# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 09:29:35 2018

@author: lenovo
"""


#内插算法

import pandas as pd
rating=pd.read_excel('F:/债权曲线和估值/系统升级_二期/业务测试/测试数据/测试结果/rate.xlsx')

#loc和iloc的区别：loc需要以行名和列名来取数，iloc需要以行数和列数来取数

x_set=[0,0.5,1,3,5,10]
#一、AAA曲线
y_set_AAA=[rating.loc[0,'0y'],rating.loc[0,'0.5y'],rating.loc[0,'1y'],rating.loc[0,'3y'],rating.loc[0,'5y'],rating.loc[0,'10y']]
di_set_AAA=[(rating.loc[0,'0.5y']-rating.loc[0,'0y'])/0.5,(rating.loc[0,'0.5y']-rating.loc[0,'0y'])/0.5,(rating.loc[0,'1y']-rating.loc[0,'0.5y'])/0.5,(rating.loc[0,'3y']-rating.loc[0,'1y'])/2,(rating.loc[0,'5y']-rating.loc[0,'3y'])/2,(rating.loc[0,'10y']-rating.loc[0,'5y'])/5]
rate_AAA=[]
lx=[]
for i in range(len(x_set)-1):
    xi=x_set[i]
    xj=x_set[i+1]
    lx_i=[]
    j=xi
    while j<xj:
        j=round(j+0.001,3)
        lx_i.append(j)
    lx.extend(lx_i)    
    rate_i_AAA=[]    
    for x in lx_i:
        H1_AAA=3*((xj-x)/(xj-xi))**2-2*((xj-x)/(xj-xi))**3
        H2_AAA=3*((x-xi)/(xj-xi))**2-2*((x-xi)/(xj-xi))**3
        H3_AAA=((xj-x)**2)/(xj-xi)-((xj-x)**3)/((xj-xi)**2)
        H4_AAA=((x-xi)**3)/((xj-xi)**2)-((x-xi)**2)/(xj-xi)
        yi_AAA=y_set_AAA[i]
        yj_AAA=y_set_AAA[i+1]
        di_AAA=di_set_AAA[i]
        dj_AAA=di_set_AAA[i+1]
        y_AAA=yi_AAA*H1_AAA+yj_AAA*H2_AAA+di_AAA*H3_AAA+dj_AAA*H4_AAA
        rate_i_AAA.append(y_AAA)
    rate_AAA.extend(rate_i_AAA)
    
lx.insert(0,0)
rate_AAA.insert(0,y_set_AAA[0])

#二、AA+曲线
y_set_AA1=[rating.loc[1,'0y'],rating.loc[1,'0.5y'],rating.loc[1,'1y'],rating.loc[1,'3y'],rating.loc[1,'5y'],rating.loc[1,'10y']]
di_set_AA1=[(rating.loc[1,'0.5y']-rating.loc[1,'0y'])/0.5,(rating.loc[1,'0.5y']-rating.loc[1,'0y'])/0.5,(rating.loc[1,'1y']-rating.loc[1,'0.5y'])/0.5,(rating.loc[1,'3y']-rating.loc[1,'1y'])/2,(rating.loc[1,'5y']-rating.loc[1,'3y'])/2,(rating.loc[1,'10y']-rating.loc[1,'5y'])/5]
rate_AA1=[]
lx=[]
for i in range(len(x_set)-1):
    xi=x_set[i]
    xj=x_set[i+1]
    lx_i=[]
    j=xi
    while j<xj:
        j=round(j+0.001,3)
        lx_i.append(j)
    lx.extend(lx_i)    
    rate_i_AA1=[]    
    for x in lx_i:
        H1_AA1=3*((xj-x)/(xj-xi))**2-2*((xj-x)/(xj-xi))**3
        H2_AA1=3*((x-xi)/(xj-xi))**2-2*((x-xi)/(xj-xi))**3
        H3_AA1=((xj-x)**2)/(xj-xi)-((xj-x)**3)/((xj-xi)**2)
        H4_AA1=((x-xi)**3)/((xj-xi)**2)-((x-xi)**2)/(xj-xi)
        yi_AA1=y_set_AA1[i]
        yj_AA1=y_set_AA1[i+1]
        di_AA1=di_set_AA1[i]
        dj_AA1=di_set_AA1[i+1]
        y_AA1=yi_AA1*H1_AA1+yj_AA1*H2_AA1+di_AA1*H3_AA1+dj_AA1*H4_AA1
        rate_i_AA1.append(y_AA1)
    rate_AA1.extend(rate_i_AA1)
    
lx.insert(0,0)
rate_AA1.insert(0,y_set_AA1[0])


#三、AA曲线
y_set_AA2=[rating.loc[2,'0y'],rating.loc[2,'0.5y'],rating.loc[2,'1y'],rating.loc[2,'3y'],rating.loc[2,'5y'],rating.loc[2,'10y']]
di_set_AA2=[(rating.loc[2,'0.5y']-rating.loc[2,'0y'])/0.5,(rating.loc[2,'0.5y']-rating.loc[2,'0y'])/0.5,(rating.loc[2,'1y']-rating.loc[2,'0.5y'])/0.5,(rating.loc[2,'3y']-rating.loc[2,'1y'])/2,(rating.loc[2,'5y']-rating.loc[2,'3y'])/2,(rating.loc[2,'10y']-rating.loc[2,'5y'])/5]
rate_AA2=[]
lx=[]
for i in range(len(x_set)-1):
    xi=x_set[i]
    xj=x_set[i+1]
    lx_i=[]
    j=xi
    while j<xj:
        j=round(j+0.001,3)
        lx_i.append(j)
    lx.extend(lx_i)    
    rate_i_AA2=[]    
    for x in lx_i:
        H1_AA2=3*((xj-x)/(xj-xi))**2-2*((xj-x)/(xj-xi))**3
        H2_AA2=3*((x-xi)/(xj-xi))**2-2*((x-xi)/(xj-xi))**3
        H3_AA2=((xj-x)**2)/(xj-xi)-((xj-x)**3)/((xj-xi)**2)
        H4_AA2=((x-xi)**3)/((xj-xi)**2)-((x-xi)**2)/(xj-xi)
        yi_AA2=y_set_AA2[i]
        yj_AA2=y_set_AA2[i+1]
        di_AA2=di_set_AA2[i]
        dj_AA2=di_set_AA2[i+1]
        y_AA2=yi_AA2*H1_AA2+yj_AA2*H2_AA2+di_AA2*H3_AA2+dj_AA2*H4_AA2
        rate_i_AA2.append(y_AA2)
    rate_AA2.extend(rate_i_AA2)
    
lx.insert(0,0)
rate_AA2.insert(0,y_set_AA2[0])

#三、AA-曲线
y_set_AA3=[rating.loc[3,'0y'],rating.loc[3,'0.5y'],rating.loc[3,'1y'],rating.loc[3,'3y'],rating.loc[3,'5y'],rating.loc[3,'10y']]
di_set_AA3=[(rating.loc[3,'0.5y']-rating.loc[3,'0y'])/0.5,(rating.loc[3,'0.5y']-rating.loc[3,'0y'])/0.5,(rating.loc[3,'1y']-rating.loc[3,'0.5y'])/0.5,(rating.loc[3,'3y']-rating.loc[3,'1y'])/2,(rating.loc[3,'5y']-rating.loc[3,'3y'])/2,(rating.loc[3,'10y']-rating.loc[3,'5y'])/5]
rate_AA3=[]
lx=[]
for i in range(len(x_set)-1):
    xi=x_set[i]
    xj=x_set[i+1]
    lx_i=[]
    j=xi
    while j<xj:
        j=round(j+0.001,3)
        lx_i.append(j)
    lx.extend(lx_i)    
    rate_i_AA3=[]    
    for x in lx_i:
        H1_AA3=3*((xj-x)/(xj-xi))**2-2*((xj-x)/(xj-xi))**3
        H2_AA3=3*((x-xi)/(xj-xi))**2-2*((x-xi)/(xj-xi))**3
        H3_AA3=((xj-x)**2)/(xj-xi)-((xj-x)**3)/((xj-xi)**2)
        H4_AA3=((x-xi)**3)/((xj-xi)**2)-((x-xi)**2)/(xj-xi)
        yi_AA3=y_set_AA3[i]
        yj_AA3=y_set_AA3[i+1]
        di_AA3=di_set_AA3[i]
        dj_AA3=di_set_AA3[i+1]
        y_AA3=yi_AA3*H1_AA3+yj_AA3*H2_AA3+di_AA3*H3_AA3+dj_AA3*H4_AA3
        rate_i_AA3.append(y_AA3)
    rate_AA3.extend(rate_i_AA3)
    
lx.insert(0,0)
rate_AA3.insert(0,y_set_AA3[0])

#画曲线图
import matplotlib.pyplot as plt
plt.figure()#plt.figure(figsize=(8,4))
#plt.plot(test, rate, linestyle = ' ', marker='o', color='red',linewidth=1)
plt.plot(lx, rate_AAA, 'green',linewidth=1,label='AAA')
plt.plot(lx, rate_AA1, 'red',linewidth=1,label='AA+')
plt.plot(lx, rate_AA2, 'blue',linewidth=1,label='AA')
plt.plot(lx, rate_AA3, 'skyblue',linewidth=1,label='AA-')
plt.xlabel('待偿期')  
plt.ylabel('到期收益率')  
plt.title('收益率曲线')
#plt.ylim(3,7)
plt.xlim(0,11)
'''x_lable=[lx[0],lx[100],lx[300],lx[500],lx[700],lx[1000]]
y_lable=[rate_AAA[0],rate_AAA[100],rate_AAA[300],rate_AAA[500],rate_AAA[700],rate_AAA[1000]]
print(x_lable)
for a,b in zip(x_lable,y_lable):
    plt.text(a, b+0.05, '%.0f' % b, ha='center', va= 'bottom',fontsize=7)显示4位小数问题'''
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
plt.legend()
plt.show()
#plt.savefig('rate.jpg')

combine_ratingdata=pd.DataFrame([lx,rate_AAA,rate_AA1,rate_AA2,rate_AA3]).T
combine_ratingdata.to_excel('F:/债权曲线和估值/系统升级_二期/业务测试/测试数据/测试结果/quxian_neicha.xlsx')





#外插算法
import pandas as pd
rating=pd.read_excel('F:/债权曲线和估值/系统升级_二期/业务测试/测试数据/测试结果/rate.xlsx')


#1-10之间用内插
x_set=[1,3,5,10]
#一、AAA曲线
y_set_AAA=[rating.loc[0,'1y'],rating.loc[0,'3y'],rating.loc[0,'5y'],rating.loc[0,'10y']]
di_set_AAA=[(rating.loc[0,'3y']-rating.loc[0,'1y'])/2,(rating.loc[0,'3y']-rating.loc[0,'1y'])/2,(rating.loc[0,'5y']-rating.loc[0,'3y'])/2,(rating.loc[0,'10y']-rating.loc[0,'5y'])/5]
rate_AAA=[]
lx=[]
for i in range(len(x_set)-1):
    xi=x_set[i]
    xj=x_set[i+1]
    lx_i=[]
    j=xi
    while j<xj:
        j=round(j+0.01,2)
        lx_i.append(j)
    lx.extend(lx_i)    
    rate_i_AAA=[]    
    for x in lx_i:
        H1_AAA=3*((xj-x)/(xj-xi))**2-2*((xj-x)/(xj-xi))**3
        H2_AAA=3*((x-xi)/(xj-xi))**2-2*((x-xi)/(xj-xi))**3
        H3_AAA=((xj-x)**2)/(xj-xi)-((xj-x)**3)/((xj-xi)**2)
        H4_AAA=((x-xi)**3)/((xj-xi)**2)-((x-xi)**2)/(xj-xi)
        yi_AAA=y_set_AAA[i]
        yj_AAA=y_set_AAA[i+1]
        di_AAA=di_set_AAA[i]
        dj_AAA=di_set_AAA[i+1]
        y_AAA=yi_AAA*H1_AAA+yj_AAA*H2_AAA+di_AAA*H3_AAA+dj_AAA*H4_AAA
        rate_i_AAA.append(y_AAA)
    rate_AAA.extend(rate_i_AAA)
    
lx.insert(0,1)
rate_AAA.insert(0,y_set_AAA[0])

#二、AA+曲线
y_set_AA1=[rating.loc[1,'1y'],rating.loc[1,'3y'],rating.loc[1,'5y'],rating.loc[1,'10y']]
di_set_AA1=[(rating.loc[1,'3y']-rating.loc[1,'1y'])/2,(rating.loc[1,'3y']-rating.loc[1,'1y'])/2,(rating.loc[1,'5y']-rating.loc[1,'3y'])/2,(rating.loc[1,'10y']-rating.loc[1,'5y'])/5]
rate_AA1=[]
lx=[]
for i in range(len(x_set)-1):
    xi=x_set[i]
    xj=x_set[i+1]
    lx_i=[]
    j=xi
    while j<xj:
        j=round(j+0.01,2)
        lx_i.append(j)
    lx.extend(lx_i)    
    rate_i_AA1=[]    
    for x in lx_i:
        H1_AA1=3*((xj-x)/(xj-xi))**2-2*((xj-x)/(xj-xi))**3
        H2_AA1=3*((x-xi)/(xj-xi))**2-2*((x-xi)/(xj-xi))**3
        H3_AA1=((xj-x)**2)/(xj-xi)-((xj-x)**3)/((xj-xi)**2)
        H4_AA1=((x-xi)**3)/((xj-xi)**2)-((x-xi)**2)/(xj-xi)
        yi_AA1=y_set_AA1[i]
        yj_AA1=y_set_AA1[i+1]
        di_AA1=di_set_AA1[i]
        dj_AA1=di_set_AA1[i+1]
        y_AA1=yi_AA1*H1_AA1+yj_AA1*H2_AA1+di_AA1*H3_AA1+dj_AA1*H4_AA1
        rate_i_AA1.append(y_AA1)
    rate_AA1.extend(rate_i_AA1)
    
lx.insert(0,1)
rate_AA1.insert(0,y_set_AA1[0])


#三、AA曲线
y_set_AA2=[rating.loc[2,'1y'],rating.loc[2,'3y'],rating.loc[2,'5y'],rating.loc[2,'10y']]
di_set_AA2=[(rating.loc[2,'3y']-rating.loc[2,'1y'])/2,(rating.loc[2,'3y']-rating.loc[2,'1y'])/2,(rating.loc[2,'5y']-rating.loc[2,'3y'])/2,(rating.loc[2,'10y']-rating.loc[2,'5y'])/5]
rate_AA2=[]
lx=[]
for i in range(len(x_set)-1):
    xi=x_set[i]
    xj=x_set[i+1]
    lx_i=[]
    j=xi
    while j<xj:
        j=round(j+0.01,2)
        lx_i.append(j)
    lx.extend(lx_i)    
    rate_i_AA2=[]    
    for x in lx_i:
        H1_AA2=3*((xj-x)/(xj-xi))**2-2*((xj-x)/(xj-xi))**3
        H2_AA2=3*((x-xi)/(xj-xi))**2-2*((x-xi)/(xj-xi))**3
        H3_AA2=((xj-x)**2)/(xj-xi)-((xj-x)**3)/((xj-xi)**2)
        H4_AA2=((x-xi)**3)/((xj-xi)**2)-((x-xi)**2)/(xj-xi)
        yi_AA2=y_set_AA2[i]
        yj_AA2=y_set_AA2[i+1]
        di_AA2=di_set_AA2[i]
        dj_AA2=di_set_AA2[i+1]
        y_AA2=yi_AA2*H1_AA2+yj_AA2*H2_AA2+di_AA2*H3_AA2+dj_AA2*H4_AA2
        rate_i_AA2.append(y_AA2)
    rate_AA2.extend(rate_i_AA2)
    
lx.insert(0,1)
rate_AA2.insert(0,y_set_AA2[0])

#三、AA-曲线
y_set_AA3=[rating.loc[3,'1y'],rating.loc[3,'3y'],rating.loc[3,'5y'],rating.loc[3,'10y']]
di_set_AA3=[(rating.loc[3,'3y']-rating.loc[3,'1y'])/2,(rating.loc[3,'3y']-rating.loc[3,'1y'])/2,(rating.loc[3,'5y']-rating.loc[3,'3y'])/2,(rating.loc[3,'10y']-rating.loc[3,'5y'])/5]
rate_AA3=[]
lx=[]
for i in range(len(x_set)-1):
    xi=x_set[i]
    xj=x_set[i+1]
    lx_i=[]
    j=xi
    while j<xj:
        j=round(j+0.01,2)
        lx_i.append(j)
    lx.extend(lx_i)    
    rate_i_AA3=[]    
    for x in lx_i:
        H1_AA3=3*((xj-x)/(xj-xi))**2-2*((xj-x)/(xj-xi))**3
        H2_AA3=3*((x-xi)/(xj-xi))**2-2*((x-xi)/(xj-xi))**3
        H3_AA3=((xj-x)**2)/(xj-xi)-((xj-x)**3)/((xj-xi)**2)
        H4_AA3=((x-xi)**3)/((xj-xi)**2)-((x-xi)**2)/(xj-xi)
        yi_AA3=y_set_AA3[i]
        yj_AA3=y_set_AA3[i+1]
        di_AA3=di_set_AA3[i]
        dj_AA3=di_set_AA3[i+1]
        y_AA3=yi_AA3*H1_AA3+yj_AA3*H2_AA3+di_AA3*H3_AA3+dj_AA3*H4_AA3
        rate_i_AA3.append(y_AA3)
    rate_AA3.extend(rate_i_AA3)
    
lx.insert(0,1)
rate_AA3.insert(0,y_set_AA3[0])

#画曲线图
import matplotlib.pyplot as plt
plt.figure()#plt.figure(figsize=(8,4))
#plt.plot(test, rate, linestyle = ' ', marker='o', color='red',linewidth=1)
plt.plot(lx, rate_AAA, 'green',linewidth=1,label='AAA')
plt.plot(lx, rate_AA1, 'red',linewidth=1,label='AA+')
plt.plot(lx, rate_AA2, 'blue',linewidth=1,label='AA')
plt.plot(lx, rate_AA3, 'skyblue',linewidth=1,label='AA-')
plt.xlabel('待偿期')  
plt.ylabel('到期收益率')  
plt.title('收益率曲线')
#plt.ylim(3,7)
plt.xlim(0,11)
'''x_lable=[lx[0],lx[100],lx[300],lx[500],lx[700],lx[1000]]
y_lable=[rate_AAA[0],rate_AAA[100],rate_AAA[300],rate_AAA[500],rate_AAA[700],rate_AAA[1000]]
print(x_lable)
for a,b in zip(x_lable,y_lable):
    plt.text(a, b+0.05, '%.0f' % b, ha='center', va= 'bottom',fontsize=7)显示4位小数问题'''
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
plt.legend()
plt.show()
#plt.savefig('rate.jpg')
combine_date1=pd.DataFrame([lx,rate_AAA,rate_AA1,rate_AA2,rate_AA3]).T
#combine_ratingdata=pd.DataFrame([lx,rate_AAA,rate_AA1,rate_AA2,rate_AA3]).T
#combine_ratingdata.to_excel('F:/债权曲线和估值/测试/测试数据/combine20180615_budian.xlsx')
#loc和iloc的区别：loc需要以行名和列名来取数，iloc需要以行数和列数来取数

#一、AAA曲线
y_out_set_AAA=[]
d1=(rate_AAA[1]-rate_AAA[0])/0.01
for i in range(100):
    y_out=rate_AAA[0]-d1*0.01*(i+1)
    y_out_set_AAA.append(y_out)
y_out_set_AAA=y_out_set_AAA[::-1]
y_out_set_AAA.extend(rate_AAA[0:901]) 

#二、AA1曲线
y_out_set_AA1=[]
d2=(rate_AA1[1]-rate_AA1[0])/0.01
for i in range(100):
    y_out=rate_AA1[0]-d2*0.01*(i+1)
    y_out_set_AA1.append(y_out)
y_out_set_AA1=y_out_set_AA1[::-1]
y_out_set_AA1.extend(rate_AA1[0:901]) 

#二、AA2曲线
y_out_set_AA2=[]
d3=(rate_AA2[1]-rate_AA2[0])/0.01
for i in range(100):
    y_out=rate_AA2[0]-d3*0.01*(i+1)
    y_out_set_AA2.append(y_out)
y_out_set_AA2=y_out_set_AA2[::-1]
y_out_set_AA2.extend(rate_AA2[0:901]) 

#三、AA3曲线
y_out_set_AA3=[]
d4=(rate_AA3[1]-rate_AA3[0])/0.01
for i in range(100):
    y_out=rate_AA3[0]-d4*0.01*(i+1)
    y_out_set_AA3.append(y_out)
y_out_set_AA3=y_out_set_AA3[::-1]
y_out_set_AA3.extend(rate_AA3[0:901]) 

lx_out_set=[]
for i in range(100):
    lx_out=i/100
    lx_out_set.append(lx_out)
lx_out_set.extend(lx[0:901])    

#画曲线图
import matplotlib.pyplot as plt
plt.figure()#plt.figure(figsize=(8,4))
#plt.plot(test, rate, linestyle = ' ', marker='o', color='red',linewidth=1)
plt.plot(lx_out_set, y_out_set_AAA, 'green',linewidth=1,label='AAA')
plt.plot(lx_out_set, y_out_set_AA1, 'red',linewidth=1,label='AA+')
plt.plot(lx_out_set, y_out_set_AA2, 'blue',linewidth=1,label='AA')
plt.plot(lx_out_set, y_out_set_AA3, 'skyblue',linewidth=1,label='AA-')
plt.xlabel('待偿期（年）')  
plt.ylabel('到期收益率（%）')  
plt.title('收益率曲线')
#plt.ylim(0,8)
plt.xlim(0,11)
'''x_lable=[lx[0],lx[100],lx[300],lx[500],lx[700],lx[1000]]
y_lable=[rate_AAA[0],rate_AAA[100],rate_AAA[300],rate_AAA[500],rate_AAA[700],rate_AAA[1000]]
print(x_lable)
for a,b in zip(x_lable,y_lable):
    plt.text(a, b+0.05, '%.0f' % b, ha='center', va= 'bottom',fontsize=7)显示4位小数问题'''
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
plt.legend()
plt.show()
#plt.savefig('rate.jpg')

combine_date_out=pd.DataFrame([lx_out_set,y_out_set_AAA,y_out_set_AA1,y_out_set_AA2,y_out_set_AA3]).T
combine_date_out.to_excel('F:/债权曲线和估值/系统升级_二期/业务测试/测试数据/测试结果/quxian_waicha.xlsx')


'''
#四、估值计算
#手动筛选数据：曲线测试数据20180621；1.删除承销商缴款截止日期大于今天的数据；2.删除评级数据不在4个评级中的数据；3.删除面值为空的数据；4.删除到期日为空的数据；5.删除付息方式、付息频率为空的数据；
testdata=pd.read_excel('F:/债权曲线和估值/测试/测试数据/曲线测试数据20180621.xlsx')
'''
testdata=testdata[testdata['PUB_CREDITRATE']>0]
testdata=testdata[testdata['FACE_VALUE']>0]
testdata=testdata[testdata['INTEREST_MODE']>0]
testdata=testdata[testdata['IRST_FREQUENCY']>0]
#testdata=testdata[testdata['MATURITY_DATE']>0]
'''
testdata.dtypes
testdata['MATURITY_DATE']=testdata['MATURITY_DATE'].astype('str')
testdata['FIRST_PAY_DAY']=testdata['FIRST_PAY_DAY'].astype('str')
testdata['VALUE_DATE']=testdata['VALUE_DATE'].astype('str')
testdata['CONSIGN_PAY_END_DATE']=testdata['CONSIGN_PAY_END_DATE'].astype('str')
'''
#付息频率转换
testdata['IRST_FREQUENCY1']=testdata['IRST_FREQUENCY']
testdata.loc[testdata['IRST_FREQUENCY']==3,'IRST_FREQUENCY1']=4
'''
#主体评级转换
testdata['PUB_CREDITRATE'][(testdata['PUB_CREDITRATE']==31)]=1
testdata['PUB_CREDITRATE'][(testdata['PUB_CREDITRATE']==29)]=2
testdata['PUB_CREDITRATE'][(testdata['PUB_CREDITRATE']==28)]=3
testdata['PUB_CREDITRATE'][(testdata['PUB_CREDITRATE']==27)]=4
testdata.to_excel('F:/债权曲线和估值/data/testdata_clear.xlsx')
'''
