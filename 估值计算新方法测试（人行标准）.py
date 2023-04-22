# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 16:43:29 2019

@author: lenovo
"""

import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
inford_product_element=pd.read_excel('F:/债权曲线和估值/系统升级_二期/业务测试/测试数据/版本2/inford_product_element.xlsx')
inford_product_element=inford_product_element.loc[:,['BOND_ID','VALUE_DATE','INTEREST_MODE','IRST_FREQUENCY','MATURITY_DATE','BOND_TERM','TERM_UNIT','PUB_CREDITRATE','REPAY_MODEL','APP_TYPE','FACE_VALUE']]
inford_product_publish=pd.read_excel('F:/债权曲线和估值/系统升级_二期/业务测试/测试数据/版本2/inford_product_publish.xlsx')
inford_product_publish=inford_product_publish.loc[:,['BOND_ID','CENTURY_PUBLISH_PRICE','FIRST_PAY_DATE']]
inford_product_basic=pd.read_excel('F:/债权曲线和估值/系统升级_二期/业务测试/测试数据/版本2/inford_product_basic.xlsx')
inford_product_basic=inford_product_basic.loc[:,['BOND_ID','BOND_FULL_NAME','BOND_SHORT_NAME','BOND_CODE','BOND_TYPE','BJS_IDENTIFY']]
inford_product_survival=pd.read_excel('F:/债权曲线和估值/系统升级_二期/业务测试/测试数据/版本2/inford_product_survival.xlsx')
inford_product_survival=inford_product_survival.loc[:,['BOND_ID','FINAL_COUPON_RATE','BOND_BALANCE']]
a=pd.merge(inford_product_element,inford_product_publish,how='outer',on='BOND_ID')
b=pd.merge(a,inford_product_basic,how='outer',on='BOND_ID')
data=pd.merge(b,inford_product_survival,how='outer',on='BOND_ID')
data=data[data['BOND_TYPE']==1]
data=data[data['BJS_IDENTIFY']==3]
data=data.reset_index(drop = True)

data.to_excel('F:/债权曲线和估值/系统升级_二期/业务测试/测试数据/版本2/data.xlsx')

#1.删除第1列
#2.增加待偿期在一年以上的到期一次还本付息债券（深绿）、一年以内零息债券（浅绿），一年以上零息债券等情况数据
#3.修改评级数据，AAA_1，去掉评级不在范围内或无评级数据
#4.删除永续债券

data=pd.read_excel('C:/Users/P300-001/Desktop/债融数据分析/data.xlsx')


data['VALUE_DATE']=data['VALUE_DATE'].astype(str)
value_date=[]
for i in range(len(data)):
    u=data.loc[i,'VALUE_DATE'][0:4]
    v=data.loc[i,'VALUE_DATE'][4:6]
    w=data.loc[i,'VALUE_DATE'][6:8]          
    u=int(u)
    v=int(v)
    w=int(w)
    dw=datetime.date(u,v,w)
    value_date.append(dw)
data['VALUE_DATE_1']=value_date


data['MATURITY_DATE']=data['MATURITY_DATE'].astype(str)
maturity_date=[]
for i in range(len(data)):
    r=data.loc[i,'MATURITY_DATE'][0:4]
    s=data.loc[i,'MATURITY_DATE'][4:6]
    t=data.loc[i,'MATURITY_DATE'][6:8]          
    r=int(r)
    s=int(s)
    t=int(t)
    dt=datetime.date(r,s,t)
    maturity_date.append(dt)
data['MATURITY_DATE_1']=maturity_date


data['FIRST_PAY_DATE']=data['FIRST_PAY_DATE'].astype(str)
firstpay_date=[]
for i in range(len(data)):
    try:
        r=data.loc[i,'FIRST_PAY_DATE'][0:4]
        s=data.loc[i,'FIRST_PAY_DATE'][4:6]
        t=data.loc[i,'FIRST_PAY_DATE'][6:8]          
        r=int(r)
        s=int(s)
        t=int(t)
        dt=datetime.date(r,s,t)
        firstpay_date.append(dt)
    except:
        firstpay_date.append('nan')
data['FIRST_PAY_DATE_1']=firstpay_date


interest_pay_plan_info=pd.read_excel('C:/Users/P300-001/Desktop/债融数据分析/interest_pay_plan_info.xlsx')
interest_pay_plan_info=interest_pay_plan_info.reset_index(drop = True)
interest_pay_plan_info['INTE_PAY_DATE']=interest_pay_plan_info['INTE_PAY_DATE'].astype(str)
pay_date=[]
for i in range(len(interest_pay_plan_info)):
    z=interest_pay_plan_info.loc[i,'INTE_PAY_DATE'][0:4]
    y=interest_pay_plan_info.loc[i,'INTE_PAY_DATE'][4:6]
    x=interest_pay_plan_info.loc[i,'INTE_PAY_DATE'][6:8]          
    z=int(z)
    y=int(y)
    x=int(x)
    dz=datetime.date(z,y,x)
    pay_date.append(dz)
interest_pay_plan_info['INTE_PAY_DATE_1']=pay_date


#确定到期日的取数
maturityfinal=[]
maturityfuxi=[]
for i in range(len(data)):
    interest_pay_plan_info_2=interest_pay_plan_info[interest_pay_plan_info['BOND_ID']==data.loc[i,'BOND_ID']]
    interest_pay_plan_info_2=interest_pay_plan_info_2.sort_values('INTE_PAY_DATE',axis=0,ascending=True)
    interest_pay_plan_info_2=interest_pay_plan_info_2.reset_index(drop = True)
    qixiri=data.loc[i,'VALUE_DATE_1']
    maturitydate1=data.loc[i,'MATURITY_DATE_1'] #到期日
    maturitydate2=interest_pay_plan_info_2.iloc[-1,21] #付息兑付计划表最后一行付息日
    c1=round(interest_pay_plan_info_2.iloc[-1,10]*10000,2)
    c2=round(interest_pay_plan_info_2.iloc[-1,12],2)
    c3=round(interest_pay_plan_info_2.iloc[-1,14],2)    
    
    if qixiri==maturitydate1:
        maturityfinal.append(maturitydate2)
    elif int(c1+c2)>int(c3):
        maturityfinal.append(maturitydate1)
    elif int(c1+c2)==int(c3) and maturitydate2<maturitydate1:
        maturityfinal.append(maturitydate2)
    elif maturitydate2>maturitydate1:
        maturityfinal.append(maturitydate1)
    elif maturitydate1==maturitydate2:
        maturityfinal.append(maturitydate2)
    else:
        maturityfinal.append(maturitydate1)
    
    maturityfuxi.append(maturitydate2)
        
data['MATURITYFINAL']=maturityfinal
data['MATURITYFUXI']=maturityfuxi


#判断付息兑付计划表是否完整
wanzhengbiaoshi=[]
for i in range(len(data)):
    interest_pay_plan_info_1=interest_pay_plan_info[interest_pay_plan_info['BOND_ID']==data.loc[i,'BOND_ID']]
    interest_pay_plan_info_1=interest_pay_plan_info_1.sort_values('INTE_PAY_DATE_1',axis=0,ascending=True)
    interest_pay_plan_info_1=interest_pay_plan_info_1.reset_index(drop = True)
    benjin=round(interest_pay_plan_info_1.iloc[-1,10]*10000,2)
    lixi=round(interest_pay_plan_info_1.iloc[-1,12],2)
    benxi=round(interest_pay_plan_info_1.iloc[-1,14],2)
    if int(benjin+lixi)==int(benxi):
        wanzhengbiaoshi.append(1)
    else:
        wanzhengbiaoshi.append(0)
        
data['BIAOSHI']=wanzhengbiaoshi

data.to_excel('C:/Users/P300-001/Desktop/债融数据分析/data_check.xlsx')

#生成完整的付息兑付计划表
fuxiduifubiao=pd.DataFrame(columns=['BOND_ID','INTE_PAY_DATE_1','INTE_RATE','INTE_SCALE','PAY_INTEREST','THIS_PERIOD_TRANS_MONEY'])
for i in range(len(data)):
    interest_pay_plan_info_1=interest_pay_plan_info[interest_pay_plan_info['BOND_ID']==data.loc[i,'BOND_ID']]
    interest_pay_plan_info_1=interest_pay_plan_info_1.sort_values('INTE_PAY_DATE_1',axis=0,ascending=True)
    interest_pay_plan_info_1=interest_pay_plan_info_1.reset_index(drop = True)
    bond_id=data.loc[i,'BOND_ID']
    fuxiduifubiao_1=pd.DataFrame(columns=['BOND_ID','INTE_PAY_DATE_1','INTE_RATE','INTE_SCALE','PAY_INTEREST','THIS_PERIOD_TRANS_MONEY'])
    f=data.loc[i,'IRST_FREQUENCY']
    if data.loc[i,'BIAOSHI']==1:
        bond_id_1=[]
        inte_pay_date_1=[]
        inte_rate_1=[]
        inte_scale_1=[]
        inte_money_1=[]
        this_period_trans_money_1=[]       
        for j in range(len(interest_pay_plan_info_1)):
            inte_pay_date=interest_pay_plan_info_1.loc[j,'INTE_PAY_DATE_1']
            inte_rate=interest_pay_plan_info_1.loc[j,'INTE_RATE']
            inte_scale=interest_pay_plan_info_1.loc[j,'INTE_SCALE']
            inte_money=interest_pay_plan_info_1.loc[j,'PAY_INTEREST']
            this_period_trans_money=interest_pay_plan_info_1.loc[j,'THIS_PERIOD_TRANS_MONEY']
            bond_id_1.append(bond_id)
            inte_pay_date_1.append(inte_pay_date)
            inte_rate_1.append(inte_rate)
            inte_scale_1.append(inte_scale)
            inte_money_1.append(inte_money)
            this_period_trans_money_1.append(this_period_trans_money)
    else:
        bond_id_1=[]
        inte_pay_date_1=[]
        inte_rate_1=[]
        inte_scale_1=[]
        inte_money_1=[]
        this_period_trans_money_1=[]
        
        for j in range(len(interest_pay_plan_info_1)):
            inte_pay_date=interest_pay_plan_info_1.loc[j,'INTE_PAY_DATE_1']
            inte_rate=interest_pay_plan_info_1.loc[j,'INTE_RATE']
            inte_scale=interest_pay_plan_info_1.loc[j,'INTE_SCALE']
            inte_money=interest_pay_plan_info_1.loc[j,'PAY_INTEREST']
            this_period_trans_money=interest_pay_plan_info_1.loc[j,'THIS_PERIOD_TRANS_MONEY']
            bond_id_1.append(bond_id)
            inte_pay_date_1.append(inte_pay_date)
            inte_rate_1.append(inte_rate)
            inte_scale_1.append(inte_scale)
            inte_money_1.append(inte_money)
            this_period_trans_money_1.append(this_period_trans_money)        
        
        fuxiriqi_1=[]
        qixiri=data.loc[i,'VALUE_DATE_1']
        daoqiri=data.loc[i,'MATURITYFINAL']
        shouci=data.loc[i,'FIRST_PAY_DATE_1']        
        pay_time=int((float(repr((daoqiri-qixiri).days))/365)*(12/data.loc[i,'IRST_FREQUENCY']))+5-int(len(interest_pay_plan_info_1))            
        last_pay=interest_pay_plan_info_1.iloc[-1,21]
        #last_pay_1=interest_pay_plan_info_1.iloc[-2,21]
        for k in range(pay_time):
            dl=last_pay+relativedelta(months=int((data.loc[i,'IRST_FREQUENCY'])*(k+1)))
            if dl<daoqiri:
                fuxiriqi_1.append(dl)
            else:
                fuxiriqi_1.append(daoqiri)
        fuxiriqi_1.append(last_pay)
        #fuxiriqi_1.append(last_pay_1)
        fuxiriqi_1=list(set(fuxiriqi_1))
        fuxiriqi_1.sort()
        
        for m in range(len(fuxiriqi_1)-2):            
            inte_pay_date=fuxiriqi_1[m+1]
            inte_rate=interest_pay_plan_info_1.iloc[-1,9]
            inte_scale=interest_pay_plan_info_1.iloc[-1,10]
            ts=(fuxiriqi_1[m+1]-fuxiriqi_1[m]).days            
            inte_money=inte_rate*inte_scale*100*ts/365
            this_period_trans_money=inte_money
            bond_id_1.append(bond_id)
            inte_pay_date_1.append(inte_pay_date)
            inte_rate_1.append(inte_rate)
            inte_scale_1.append(inte_scale)
            inte_money_1.append(inte_money)
            this_period_trans_money_1.append(this_period_trans_money)
        
        inte_pay_date=fuxiriqi_1[-1]
        inte_rate=interest_pay_plan_info_1.iloc[-1,9]
        inte_scale=interest_pay_plan_info_1.iloc[-1,10]
        if len(fuxiriqi_1)>2:
            ts=(fuxiriqi_1[-1]-fuxiriqi_1[-2]).days
        else:
            ts=(fuxiriqi_1[1]-fuxiriqi_1[0]).days
        inte_money=inte_rate*inte_scale*100*ts/365
        this_period_trans_money=inte_money+inte_scale*10000
        bond_id_1.append(bond_id)
        inte_pay_date_1.append(inte_pay_date)
        inte_rate_1.append(inte_rate)
        inte_scale_1.append(inte_scale)
        inte_money_1.append(inte_money)
        this_period_trans_money_1.append(this_period_trans_money)
                
    fuxiduifubiao_1['BOND_ID']=bond_id_1
    fuxiduifubiao_1['INTE_PAY_DATE_1']=inte_pay_date_1
    fuxiduifubiao_1['INTE_RATE']=inte_rate_1
    fuxiduifubiao_1['INTE_SCALE']=inte_scale_1    
    fuxiduifubiao_1['PAY_INTEREST']=inte_money_1
    fuxiduifubiao_1['THIS_PERIOD_TRANS_MONEY']=this_period_trans_money_1    
    fuxiduifubiao=fuxiduifubiao.append(fuxiduifubiao_1)

fuxiduifubiao=fuxiduifubiao.reset_index(drop = True)
fuxiduifubiao.to_excel('C:/Users/P300-001/Desktop/债融数据分析/fuxiduifubiao.xlsx')

today=datetime.date(2019,7,31)

rate=pd.read_excel('C:/Users/P300-001/Desktop/债融数据分析/quxian.xlsx')

#一、待偿期在一年及以内的到期一次还本付息债券
data1=pd.DataFrame(columns=['BOND_CODE','FINAL_COUPON_RATE','BOND_ID','VALUE_DATE','INTEREST_MODE','IRST_FREQUENCY','MATURITY_DATE','BOND_TERM','TERM_UNIT','PUB_CREDITRATE','REPAY_MODEL','APP_TYPE','FACE_VALUE','CENTURY_PUBLISH_PRICE','FIRST_PAY_DATE','BOND_FULL_NAME','BOND_SHORT_NAME','BOND_TYPE','BJS_IDENTIFY','VALUE_DATE_1','MATURITY_DATE_1','FIRST_PAY_DATE_1','MATURITYFINAL','MATURITYFUXI','BIAOSHI'])
data1_1=data[data['INTEREST_MODE']==3]
data1_2=data[data['INTEREST_MODE']==4]
data1_3=data[data['INTEREST_MODE']==5]
data1_4=data1_1.append(data1_2)
data1_5=data1_4.append(data1_3)
data1_5=data1_5.reset_index(drop=True)
#1、取出待偿期在一年及以内的到期一次还本付息债券的数据
for i in range(len(data1_5)):
    qixian=(data1_5.loc[i,'MATURITYFINAL']-today).days
    fuxiduifubiao_1=fuxiduifubiao[fuxiduifubiao['BOND_ID']==data1_5.loc[i,'BOND_ID']]
    fuxiduifubiao_1=fuxiduifubiao_1.sort_values('INTE_PAY_DATE_1',axis=0,ascending=True)
    fuxiduifubiao_1=fuxiduifubiao_1.reset_index(drop = True)
    fuxigeshu=len(fuxiduifubiao_1)  
    if qixian<=366 and fuxigeshu==1:
        data1=data1.append(data1_5.iloc[i,:])
       
data1=data1.reset_index(drop = True)   
data1.to_excel('C:/Users/P300-001/Desktop/债融数据分析/data1.xlsx')

#2、计算到期收益率、估值和应计利息
ytm=[]
pv_quan=[]
ai_set=[]
r_set=[]
for i in range(len(data1)):
    fuxiduifubiao_1=fuxiduifubiao[fuxiduifubiao['BOND_ID']==data1.loc[i,'BOND_ID']]
    fuxiduifubiao_1=fuxiduifubiao_1.reset_index(drop = True)    
    y=fuxiduifubiao_1.iloc[-1,2]    
    fv=fuxiduifubiao_1.loc[0,'THIS_PERIOD_TRANS_MONEY'] *0.01/fuxiduifubiao_1.loc[0,'INTE_SCALE']
    d=(data1.loc[i,'MATURITYFINAL']-today).days
    ty=(data1.loc[i,'VALUE_DATE_1']+relativedelta(months=12)-data1.loc[i,'VALUE_DATE_1']).days
    qixian=int(round(d/ty,3)*1000)
    pingji=int(data1.loc[i,'PUB_CREDITRATE'])
    r=rate.iloc[qixian,pingji]/100
    qixiri=data1.loc[i,'VALUE_DATE_1']    
    t=(today-qixiri).days
    c=data1.loc[i,'FINAL_COUPON_RATE']    
        
    pv_quanjia=round(fv/(1+r*d/ty),4)    
    ai=round(y*t/ty,4)

    ytm.append(y)
    pv_quan.append(pv_quanjia)
    ai_set.append(ai)
    r_set.append(r)
    
data1['YTM']=ytm
data1['PV']=pv_quan
data1['AI']=ai_set
data1['RATE']=r_set

data1.to_excel('C:/Users/P300-001/Desktop/债融数据分析/data1_result.xlsx')

#六、待偿期在一年以上的到期一次还本付息债券
data6=pd.DataFrame(columns=['BOND_CODE','FINAL_COUPON_RATE','BOND_ID','VALUE_DATE','INTEREST_MODE','IRST_FREQUENCY','MATURITY_DATE','BOND_TERM','TERM_UNIT','PUB_CREDITRATE','REPAY_MODEL','APP_TYPE','FACE_VALUE','CENTURY_PUBLISH_PRICE','FIRST_PAY_DATE','BOND_FULL_NAME','BOND_SHORT_NAME','BOND_TYPE','BJS_IDENTIFY','VALUE_DATE_1','MATURITY_DATE_1','FIRST_PAY_DATE_1','MATURITYFINAL','MATURITYFUXI','BIAOSHI'])
data6_1=data[data['INTEREST_MODE']==3]
data6_2=data[data['INTEREST_MODE']==4]
data6_3=data[data['INTEREST_MODE']==5]
data6_4=data6_1.append(data6_2)
data6_5=data6_4.append(data6_3)
data6_5=data6_5.reset_index(drop=True)

#1、取出待偿期在一年以上的到期一次还本付息债券的数据
for i in range(len(data6_5)):
    qixian=(data6_5.loc[i,'MATURITYFINAL']-today).days
    fuxiduifubiao_1=fuxiduifubiao[fuxiduifubiao['BOND_ID']==data6_5.loc[i,'BOND_ID']]
    fuxiduifubiao_1=fuxiduifubiao_1.sort_values('INTE_PAY_DATE_1',axis=0,ascending=True)
    fuxiduifubiao_1=fuxiduifubiao_1.reset_index(drop = True)
    fuxigeshu=len(fuxiduifubiao_1)  
    if qixian>366 and fuxigeshu==1:
        data6=data6.append(data6_5.iloc[i,:])
       
data6=data6.reset_index(drop = True)   
data6.to_excel('C:/Users/P300-001/Desktop/债融数据分析/data6.xlsx')
#2、计算到期收益率、估值和应计利息
ytm=[]
pv_quan=[]
ai_set=[]
r_set=[]
for i in range(len(data6)):
    fuxiduifubiao_1=fuxiduifubiao[fuxiduifubiao['BOND_ID']==data6.loc[i,'BOND_ID']]
    fuxiduifubiao_1=fuxiduifubiao_1.reset_index(drop = True)    
    fv=fuxiduifubiao_1.loc[0,'THIS_PERIOD_TRANS_MONEY'] *0.01/fuxiduifubiao_1.loc[0,'INTE_SCALE']
    if data6.loc[i,'CENTURY_PUBLISH_PRICE']>0:
        pv=data6.loc[i,'CENTURY_PUBLISH_PRICE']
    else:
        pv=100
    dym=(data6.loc[i,'MATURITYFINAL']-data6.loc[i,'VALUE_DATE_1']).days/365
    ty=365
    dym_1=(data6.loc[i,'MATURITYFINAL']-today).days/365
    d=(data6.loc[i,'MATURITYFINAL']-today).days/365
    qixian=min(int(round(d/ty,3)*1000),10000)
    pingji=int(data6.loc[i,'PUB_CREDITRATE'])
    r=rate.iloc[qixian,pingji]/100
    qixiri=data6.loc[i,'VALUE_DATE_1']
    t=(today-qixiri).days
    c=fuxiduifubiao_1.loc[0,'INTE_RATE']
    
    y=round(pow(fv/pv,1/dym)-1,4)
    pv_quanjia=round(fv/pow(1+r,dym_1),4) 
    ai=round(c*t/ty,4)

    ytm.append(y)
    pv_quan.append(pv_quanjia)
    ai_set.append(ai)
    r_set.append(r)
    
data6['YTM']=ytm
data6['PV']=pv_quan
data6['AI']=ai_set
data6['RATE']=r_set

data6.to_excel('C:/Users/P300-001/Desktop/债融数据分析/data6_result.xlsx')


#二、待偿期在一年及以内的零息债券

#1、取出待偿期在一年及以内的零息债券的数据
data2=pd.DataFrame(columns=['BOND_CODE','FINAL_COUPON_RATE','BOND_ID','VALUE_DATE','INTEREST_MODE','IRST_FREQUENCY','MATURITY_DATE','BOND_TERM','TERM_UNIT','PUB_CREDITRATE','REPAY_MODEL','APP_TYPE','FACE_VALUE','CENTURY_PUBLISH_PRICE','FIRST_PAY_DATE','BOND_FULL_NAME','BOND_SHORT_NAME','BOND_TYPE','BJS_IDENTIFY','VALUE_DATE_1','MATURITY_DATE_1','FIRST_PAY_DATE_1','MATURITYFINAL','MATURITYFUXI','BIAOSHI'])
for i in range(len(data)):
    qixian=(data.loc[i,'MATURITYFINAL']-today).days
    fs=data.loc[i,'INTEREST_MODE']
    if qixian<=366 and fs==1:
        data2=data2.append(data.iloc[i,:])

data2=data2.reset_index(drop = True)
data2.to_excel('C:/Users/P300-001/Desktop/债融数据分析/data2.xlsx')

#3、计算到期收益率、估值全价和应计利息
ytm=[]
pv_quan=[]
ai_set=[]
r_set=[]
for i in range(len(data2)):
    fuxiduifubiao_2=fuxiduifubiao[fuxiduifubiao['BOND_ID']==data2.loc[i,'BOND_ID']]
    fuxiduifubiao_2=fuxiduifubiao_2.reset_index(drop = True)
    fv=100
    pv=data2.loc[i,'CENTURY_PUBLISH_PRICE']
    ty=(data2.loc[i,'VALUE_DATE_1']+relativedelta(months=12)-data2.loc[i,'VALUE_DATE_1']).days
    qixiri=data2.loc[i,'VALUE_DATE_1']
    D=(data2.loc[i,'MATURITYFINAL']-qixiri).days
    d=(data2.loc[i,'MATURITYFINAL']-today).days
    qixian=int(round(d/ty,3)*1000)
    pingji=data2.loc[i,'PUB_CREDITRATE']
    r=rate.iloc[qixian,pingji]/100  
    t=(today-qixiri).days 
    
    y=round(((fv-pv)/pv)*ty*100/D,4)
    pv_quanjia=round(fv/(1+r*d/ty),4)    
    ai=round((100-pv)*t/D,4)

    ytm.append(y)
    pv_quan.append(pv_quanjia)
    ai_set.append(ai)
    r_set.append(r)
    
data2['YTM']=ytm
data2['PV']=pv_quan
data2['AI']=ai_set
data2['RATE']=r_set

data2.to_excel('C:/Users/P300-001/Desktop/债融数据分析/data2_result.xlsx')

#三、待偿期在一年以上的零息债券

#1、取出待偿期在一年以上的零息债券的数据
data3=pd.DataFrame(columns=['BOND_CODE','FINAL_COUPON_RATE','BOND_ID','VALUE_DATE','INTEREST_MODE','IRST_FREQUENCY','MATURITY_DATE','BOND_TERM','TERM_UNIT','PUB_CREDITRATE','REPAY_MODEL','APP_TYPE','FACE_VALUE','CENTURY_PUBLISH_PRICE','FIRST_PAY_DATE','BOND_FULL_NAME','BOND_SHORT_NAME','BOND_TYPE','BJS_IDENTIFY','VALUE_DATE_1','MATURITY_DATE_1','FIRST_PAY_DATE_1','MATURITYFINAL','MATURITYFUXI','BIAOSHI'])

for i in range(len(data)):
    qixian=(data.loc[i,'MATURITYFINAL']-today).days
    fs=data.loc[i,'INTEREST_MODE']
    if qixian>366 and fs==1:
        data3=data3.append(data.iloc[i,:])

data3=data3.reset_index(drop = True)
data3.to_excel('C:/Users/P300-001/Desktop/债融数据分析/data3.xlsx')


#3、计算到期收益率、估值全价和应计利息
ytm=[]
pv_quan=[]
ai_set=[]
r_set=[]
for i in range(len(data3)):
    fuxiduifubiao_2=fuxiduifubiao[fuxiduifubiao['BOND_ID']==data3.loc[i,'BOND_ID']]
    fuxiduifubiao_2=fuxiduifubiao_2.reset_index(drop = True)    
    fv=100
    pv=data3.loc[i,'CENTURY_PUBLISH_PRICE']    
    qixiri=data3.loc[i,'VALUE_DATE_1']
    ty=365
    t=(today-qixiri).days   
    D=(data3.loc[i,'MATURITYFINAL']-qixiri).days
    Dtym=round(((data3.loc[i,'MATURITYFINAL']-qixiri).days)/365,2)
    dtym=round(((data3.loc[i,'MATURITYFINAL']-today).days)/365,2)    
    qixian=min(int(round((data3.loc[i,'MATURITYFINAL']-today).days/ty,3)*1000),10000)
    pingji=int(data3.loc[i,'PUB_CREDITRATE'])
    r=rate.iloc[qixian,pingji]/100
    
    y=round((pow(fv/pv,1/Dtym)-1)*100,4)
    pv_quanjia=round(fv/pow(1+r,dtym),4)    
    ai=round((100-pv)*t/D,4)

    ytm.append(y)
    pv_quan.append(pv_quanjia)
    ai_set.append(ai)
    r_set.append(r)   
data3['YTM']=ytm
data3['PV']=pv_quan
data3['AI']=ai_set
data3['RATE']=r_set

data3.to_excel('C:/Users/P300-001/Desktop/债融数据分析/data3_result.xlsx')


#四、处于最后付息周期的固定利率、浮息债券
data4=pd.DataFrame(columns=['BOND_CODE','FINAL_COUPON_RATE','BOND_ID','VALUE_DATE','INTEREST_MODE','IRST_FREQUENCY','MATURITY_DATE','BOND_TERM','TERM_UNIT','PUB_CREDITRATE','REPAY_MODEL','APP_TYPE','FACE_VALUE','CENTURY_PUBLISH_PRICE','FIRST_PAY_DATE','BOND_FULL_NAME','BOND_SHORT_NAME','BOND_TYPE','BJS_IDENTIFY','VALUE_DATE_1','MATURITY_DATE_1','FIRST_PAY_DATE_1','MATURITYFINAL','MATURITYFUXI','BIAOSHI'])
data_temp1=data[data['INTEREST_MODE']==4]
data_temp2=data[data['INTEREST_MODE']==5]
data_temp=data_temp1.append(data_temp2)
data_temp=data_temp.reset_index(drop = True)
data_temp3=pd.DataFrame(columns=['BOND_CODE','FINAL_COUPON_RATE','BOND_ID','VALUE_DATE','INTEREST_MODE','IRST_FREQUENCY','MATURITY_DATE','BOND_TERM','TERM_UNIT','PUB_CREDITRATE','REPAY_MODEL','APP_TYPE','FACE_VALUE','CENTURY_PUBLISH_PRICE','FIRST_PAY_DATE','BOND_FULL_NAME','BOND_SHORT_NAME','BOND_TYPE','BJS_IDENTIFY','VALUE_DATE_1','MATURITY_DATE_1','FIRST_PAY_DATE_1','MATURITYFINAL','MATURITYFUXI','BIAOSHI'])

for i in range(len(data_temp)):
    fuxiduifubiao_5=fuxiduifubiao[fuxiduifubiao['BOND_ID']==data_temp.loc[i,'BOND_ID']]
    fuxiduifubiao_5=fuxiduifubiao_5.sort_values('INTE_PAY_DATE_1',axis=0,ascending=True) 
    fuxiduifubiao_5=fuxiduifubiao_5.reset_index(drop = True)   
    if len(fuxiduifubiao_5)>=2:
        data_temp3=data_temp3.append(data_temp.iloc[i,:])        
data_temp3=data_temp3.reset_index(drop = True)

for i in range(len(data_temp3)):
    fuxiduifubiao_6=fuxiduifubiao[fuxiduifubiao['BOND_ID']==data_temp3.loc[i,'BOND_ID']]
    fuxiduifubiao_6=fuxiduifubiao_6.sort_values('INTE_PAY_DATE_1',axis=0,ascending=True)
    fuxiduifubiao_6=fuxiduifubiao_6.reset_index(drop = True)
    day_1=fuxiduifubiao_6.iloc[-1,1]
    day_2=fuxiduifubiao_6.iloc[-2,1]
    if day_2<=today<day_1:
        data4=data4.append(data_temp3.iloc[i,:])
data4=data4.reset_index(drop = True)

data4.to_excel('C:/Users/P300-001/Desktop/债融数据分析/data4.xlsx')   


pv_quan=[]
ai_set=[]
r_set=[]
for i in range(len(data4)):
    fuxiduifubiao_3=fuxiduifubiao[fuxiduifubiao['BOND_ID']==data4.loc[i,'BOND_ID']]
    fuxiduifubiao_3=fuxiduifubiao_3.sort_values('INTE_PAY_DATE_1',axis=0,ascending=True)
    fuxiduifubiao_3=fuxiduifubiao_3.reset_index(drop = True)
    bidrate=data4.loc[i,'FINAL_COUPON_RATE']
    benjin=fuxiduifubiao_3.iloc[-1,3]*10000
    lixi=fuxiduifubiao_3.iloc[-1,4]
    benxi=fuxiduifubiao_3.iloc[-1,5]
    fv=benxi*100/benjin
    d=(data4.loc[i,'MATURITYFINAL']-today).days
    ty=365
    qixian=int(round(d/ty,3)*1000)
    pingji=int(data4.loc[i,'PUB_CREDITRATE'])
    r=rate.iloc[qixian,pingji]/100
    
    fuxiduifubiao_3_1=pd.DataFrame(columns=['BOND_ID','INTE_PAY_DATE_1','INTE_RATE','INTE_SCALE','INTE_MONEY','THIS_PERIOD_TRANS_MONEY'])    
    fuxiduifubiao_3_2=pd.DataFrame(columns=['BOND_ID','INTE_PAY_DATE_1','INTE_RATE','INTE_SCALE','INTE_MONEY','THIS_PERIOD_TRANS_MONEY'])
    for j in range(len(fuxiduifubiao_3)):
        if fuxiduifubiao_3.loc[j,'INTE_PAY_DATE_1']<=today:
            fuxiduifubiao_3_1=fuxiduifubiao_3_1.append(fuxiduifubiao_3.loc[j,:])
        else:
            fuxiduifubiao_3_2=fuxiduifubiao_3_2.append(fuxiduifubiao_3.loc[j,:])
    fuxiduifubiao_3_1=fuxiduifubiao_3_1.sort_values('INTE_PAY_DATE_1',axis=0,ascending=True)
    fuxiduifubiao_3_1=fuxiduifubiao_3_1.reset_index(drop = True)
    fuxiduifubiao_3_2=fuxiduifubiao_3_2.sort_values('INTE_PAY_DATE_1',axis=0,ascending=True)
    fuxiduifubiao_3_2=fuxiduifubiao_3_2.reset_index(drop = True)

    if len(fuxiduifubiao_3_1)==0:
        t=(today-data4.loc[i,'VALUE_DATE_1']).days
    else:
        t=(today-fuxiduifubiao_3_1.iloc[-1,1]).days
    
    pv_quanjia=round(fv/(1+r*d/ty),4) 
    ai=round(bidrate*t/ty,4)
    
    pv_quan.append(pv_quanjia)
    ai_set.append(ai)
    r_set.append(r)

data4['PV']=pv_quan
data4['AI']=ai_set
data4['RATE']=r_set
data4.to_excel('C:/Users/P300-001/Desktop/债融数据分析/data4_result.xlsx')

#五、不处于最后付息周期的固定利率、浮息债券
#1.取出附息固定、附息浮动且不处于最后付息周期的数据    
data5=pd.DataFrame(columns=['BOND_CODE','FINAL_COUPON_RATE','BOND_ID','VALUE_DATE','INTEREST_MODE','IRST_FREQUENCY','MATURITY_DATE','BOND_TERM','TERM_UNIT','PUB_CREDITRATE','REPAY_MODEL','APP_TYPE','FACE_VALUE','CENTURY_PUBLISH_PRICE','FIRST_PAY_DATE','BOND_FULL_NAME','BOND_SHORT_NAME','BOND_TYPE','BJS_IDENTIFY','VALUE_DATE_1','MATURITY_DATE_1','FIRST_PAY_DATE_1','MATURITYFINAL','MATURITYFUXI','BIAOSHI'])
data5_1=pd.DataFrame(columns=['BOND_CODE','FINAL_COUPON_RATE','BOND_ID','VALUE_DATE','INTEREST_MODE','IRST_FREQUENCY','MATURITY_DATE','BOND_TERM','TERM_UNIT','PUB_CREDITRATE','REPAY_MODEL','APP_TYPE','FACE_VALUE','CENTURY_PUBLISH_PRICE','FIRST_PAY_DATE','BOND_FULL_NAME','BOND_SHORT_NAME','BOND_TYPE','BJS_IDENTIFY','VALUE_DATE_1','MATURITY_DATE_1','FIRST_PAY_DATE_1','MATURITYFINAL','MATURITYFUXI','BIAOSHI'])
data5_2=pd.DataFrame(columns=['BOND_CODE','FINAL_COUPON_RATE','BOND_ID','VALUE_DATE','INTEREST_MODE','IRST_FREQUENCY','MATURITY_DATE','BOND_TERM','TERM_UNIT','PUB_CREDITRATE','REPAY_MODEL','APP_TYPE','FACE_VALUE','CENTURY_PUBLISH_PRICE','FIRST_PAY_DATE','BOND_FULL_NAME','BOND_SHORT_NAME','BOND_TYPE','BJS_IDENTIFY','VALUE_DATE_1','MATURITY_DATE_1','FIRST_PAY_DATE_1','MATURITYFINAL','MATURITYFUXI','BIAOSHI'])
data_temp1=data[data['INTEREST_MODE']==4]
data_temp2=data[data['INTEREST_MODE']==5]
data_temp=data_temp1.append(data_temp2)
data_temp=data_temp.reset_index(drop=True)

#不处于最后付息周期
for i in range(len(data_temp)):
    fuxiduifubiao_5=fuxiduifubiao[fuxiduifubiao['BOND_ID']==data_temp.loc[i,'BOND_ID']]
    fuxiduifubiao_5=fuxiduifubiao_5.sort_values('INTE_PAY_DATE_1',axis=0,ascending=True)
    fuxiduifubiao_5=fuxiduifubiao_5.reset_index(drop = True)
    if len(fuxiduifubiao_5)>=2 and fuxiduifubiao_5.iloc[-2,1]>today:
        data5=data5.append(data_temp.iloc[i,:]) 
data5=data5.reset_index(drop = True)

data5.to_excel('C:/Users/P300-001/Desktop/债融数据分析/data5.xlsx')   

#2、拆分付息周期规律和付息周期不规律数据
for i in range(len(data5)):
    fuxiduifubiao_6=fuxiduifubiao[fuxiduifubiao['BOND_ID']==data5.loc[i,'BOND_ID']]
    fuxiduifubiao_6=fuxiduifubiao_6.sort_values('INTE_PAY_DATE_1',axis=0,ascending=True)
    fuxiduifubiao_6=fuxiduifubiao_6.reset_index(drop = True)
    d1=data5.loc[i,'VALUE_DATE_1']
    d2=fuxiduifubiao_6.loc[0,'INTE_PAY_DATE_1']
    zhouqi1=(d2-d1).days
    d3=fuxiduifubiao_6.iloc[-2,1]
    d4=fuxiduifubiao_6.iloc[-1,1]
    zhouqi2=(d4-d3).days
    pinlv=data5.loc[i,'IRST_FREQUENCY']
    fenqi=data5.loc[i,'REPAY_MODEL']
    if pinlv*30-7<zhouqi1<pinlv*30+7 and pinlv*30-7<zhouqi2<pinlv*30+7 and fenqi==1:
        data5_1=data5_1.append(data5.loc[i,:])#付息周期规律
    else:
        data5_2=data5_2.append(data5.loc[i,:])#付息周期不规律

data5_1=data5_1.reset_index(drop=True)
data5_2=data5_2.reset_index(drop=True)        

data5_1.to_excel('C:/Users/P300-001/Desktop/债融数据分析/data5_1.xlsx') 
data5_2.to_excel('C:/Users/P300-001/Desktop/债融数据分析/data5_2.xlsx')         

#付息周期规律
pv_quan=[]
ai_set=[]
r_set=[]
for i in range(len(data5_1)):
    fuxiduifubiao_6=fuxiduifubiao[fuxiduifubiao['BOND_ID']==data5_1.loc[i,'BOND_ID']]
    fuxiduifubiao_6=fuxiduifubiao_6.sort_values('INTE_PAY_DATE_1',axis=0,ascending=True)
    fuxiduifubiao_6=fuxiduifubiao_6.reset_index(drop = True)
    fuxiduifubiao_6_1=pd.DataFrame(columns=['BOND_ID','INTE_PAY_DATE_1','INTE_RATE','INTE_SCALE','INTE_MONEY','THIS_PERIOD_TRANS_MONEY'])    
    fuxiduifubiao_6_2=pd.DataFrame(columns=['BOND_ID','INTE_PAY_DATE_1','INTE_RATE','INTE_SCALE','INTE_MONEY','THIS_PERIOD_TRANS_MONEY']) 
    for j in range(len(fuxiduifubiao_6)):
        if fuxiduifubiao_6.loc[j,'INTE_PAY_DATE_1']<=today:
            fuxiduifubiao_6_1=fuxiduifubiao_6_1.append(fuxiduifubiao_6.loc[j,:])
        else:
            fuxiduifubiao_6_2=fuxiduifubiao_6_2.append(fuxiduifubiao_6.loc[j,:])
    fuxiduifubiao_6_1=fuxiduifubiao_6_1.reset_index(drop=True)
    fuxiduifubiao_6_2=fuxiduifubiao_6_2.reset_index(drop=True)
    bidrate=data5_1.loc[i,'FINAL_COUPON_RATE']
    f=data5_1.loc[i,'IRST_FREQUENCY']
    td=(data5_1.loc[i,'MATURITYFINAL']-today).days
    ty=365
    qixian=min(int(round(td/ty,3)*1000),10000)
    pingji=int(data5_1.loc[i,'PUB_CREDITRATE'])  
    r=rate.iloc[qixian,pingji]/100
    d=(fuxiduifubiao_6_2.loc[0,'INTE_PAY_DATE_1']-today).days
    m=data5_1.loc[i,'FACE_VALUE']
    if len(fuxiduifubiao_6_1)==0:
        ts=(fuxiduifubiao_6_2.loc[0,'INTE_PAY_DATE_1']-data5_1.loc[i,'VALUE_DATE_1']).days
        t=(today-data5_1.loc[i,'VALUE_DATE_1']).days
    else:
        ts=(fuxiduifubiao_6_2.loc[0,'INTE_PAY_DATE_1']-fuxiduifubiao_6_1.iloc[-1,1]).days
        t=(today-fuxiduifubiao_6_1.iloc[-1,1]).days
    
    pv=0
    for l in range(len(fuxiduifubiao_6_2)):        
        pv=pv+(fuxiduifubiao_6_2.loc[l,'INTE_RATE']*f/12)/((1+r*f/12)**(d/ts+l))
    pv=round(pv+(100/((1+r*f/12)**(d/ts+len(fuxiduifubiao_6_2)-1))),4)
    ai=round((bidrate*f/12)*t/ts,4)            
    
    pv_quan.append(pv)
    ai_set.append(ai)
    r_set.append(r)
 
data5_1['PV']=pv_quan
data5_1['AI']=ai_set
data5_1['RATE']=r_set

data5_1.to_excel('C:/Users/P300-001/Desktop/债融数据分析/data5_1_result.xlsx')

#付息周期不规律
pv_quan=[]
ai_set=[]
r_set=[]
for i in range(len(data5_2)):
    fuxiduifubiao_6=fuxiduifubiao[fuxiduifubiao['BOND_ID']==data5_2.loc[i,'BOND_ID']]
    fuxiduifubiao_6=fuxiduifubiao_6.sort_values('INTE_PAY_DATE_1',axis=0,ascending=True)
    fuxiduifubiao_6=fuxiduifubiao_6.reset_index(drop = True)
    fuxiduifubiao_6_1=pd.DataFrame(columns=['BOND_ID','INTE_PAY_DATE_1','INTE_RATE','INTE_SCALE','INTE_MONEY','THIS_PERIOD_TRANS_MONEY'])    
    fuxiduifubiao_6_2=pd.DataFrame(columns=['BOND_ID','INTE_PAY_DATE_1','INTE_RATE','INTE_SCALE','INTE_MONEY','THIS_PERIOD_TRANS_MONEY']) 
    for j in range(len(fuxiduifubiao_6)):
        if fuxiduifubiao_6.loc[j,'INTE_PAY_DATE_1']<=today:
            fuxiduifubiao_6_1=fuxiduifubiao_6_1.append(fuxiduifubiao_6.loc[j,:])
        else:
            fuxiduifubiao_6_2=fuxiduifubiao_6_2.append(fuxiduifubiao_6.loc[j,:])
    fuxiduifubiao_6_1=fuxiduifubiao_6_1.reset_index(drop=True)
    fuxiduifubiao_6_2=fuxiduifubiao_6_2.reset_index(drop=True)
    bidrate=data5_2.loc[i,'FINAL_COUPON_RATE']    
    td=(data5_2.loc[i,'MATURITYFINAL']-today).days
    ty=365
    qixian=min(int(round(td/ty,3)*1000),10000)
    pingji=int(data5_2.loc[i,'PUB_CREDITRATE'])    
    r=rate.iloc[qixian,pingji]/100
    if len(fuxiduifubiao_6_1)==0:
        t=(today-data5_2.loc[i,'VALUE_DATE_1']).days
    else:
        t=(today-fuxiduifubiao_6_1.iloc[-1,1]).days
    pv=0
    for l in range(len(fuxiduifubiao_6_2)):
        lixi=fuxiduifubiao_6_2.loc[l,'PAY_INTEREST']
        benjin=fuxiduifubiao_6_2.loc[l,'INTE_SCALE']*10000
        d=(fuxiduifubiao_6_2.loc[l,'INTE_PAY_DATE_1']-today).days
        pv=pv+(lixi*100/benjin)/((1+r)**(d/365))
    
    pv=round(pv+(100/((1+r)**(td/365))),4)
    ai=round(bidrate*t/365,4)            
    
    pv_quan.append(pv)
    ai_set.append(ai)
    r_set.append(r)
 
data5_2['PV']=pv_quan
data5_2['AI']=ai_set
data5_2['RATE']=r_set

data5_2.to_excel('C:/Users/P300-001/Desktop/债融数据分析/data5_2_result.xlsx')          

#七、应收账款债权融资计划
#取应收账款债权融资计划（不含次级债）
inford_product_element_ys=pd.read_excel('C:/Users/P300-001/Desktop/债融数据分析/inford_product_element.xlsx')
inford_product_element_ys=inford_product_element_ys.loc[:,['BOND_ID','VALUE_DATE','MATURITY_DATE']]
inford_product_basic_ys=pd.read_excel('C:/Users/P300-001/Desktop/债融数据分析/inford_product_basic.xlsx')
inford_product_basic_ys=inford_product_basic_ys.loc[:,['BOND_ID','BOND_FULL_NAME','BOND_SHORT_NAME','BOND_CODE','BOND_TYPE','BJS_IDENTIFY']]
inford_product_survival_ys=pd.read_excel('C:/Users/P300-001/Desktop/债融数据分析/inford_product_survival.xlsx')
inford_product_survival_ys=inford_product_survival_ys.loc[:,['BOND_ID','FINAL_COUPON_RATE']]
b=pd.merge(inford_product_element_ys,inford_product_basic_ys,how='outer',on='BOND_ID')
data_ys=pd.merge(b,inford_product_survival_ys,how='outer',on='BOND_ID')
data_ys=data_ys[data_ys['BOND_TYPE']==2]
data_ys=data_ys[data_ys['BJS_IDENTIFY']==3]
data_ys=data_ys[~data_ys['BOND_SHORT_NAME'].str.contains('次级')]
data_ys=data_ys.reset_index(drop = True)
data_ys.to_excel('C:/Users/P300-001/Desktop/债融数据分析/data_ys.xlsx')

data_ys['VALUE_DATE']=data_ys['VALUE_DATE'].astype(str)
value_date=[]
for i in range(len(data_ys)):
    u=data_ys.loc[i,'VALUE_DATE'][0:4]
    v=data_ys.loc[i,'VALUE_DATE'][4:6]
    w=data_ys.loc[i,'VALUE_DATE'][6:8]          
    u=int(u)
    v=int(v)
    w=int(w)
    dw=datetime.date(u,v,w)
    value_date.append(dw)
data_ys['VALUE_DATE_1']=value_date


#计算应计利息
ai_set=[]
for i in range(len(data_ys)):
    interest_pay_plan_info_1=interest_pay_plan_info[interest_pay_plan_info['BOND_ID']==data_ys.loc[i,'BOND_ID']]
    interest_pay_plan_info_1=interest_pay_plan_info_1.sort_values('INTE_PAY_DATE_1',axis=0,ascending=True)
    interest_pay_plan_info_1=interest_pay_plan_info_1.reset_index(drop = True)
    interest_pay_plan_info_1_1=pd.DataFrame(columns=['ID','BOND_ID','INTE_PAY_BIZ_CODE','INTE_PAY_BIZ_YEAR','INTE_PAY_TYPE','INTE_PAY_DATE','REAL_ARR_DATE','REAL_PAY_DATE','INTE_RATE','INTE_SCALE','PLAN_PAY_TYPE','PAY_INTEREST','PAY_CORPUS', 'THIS_PERIOD_TRANS_MONEY','FRUCTUS_AMOUNT','INTE_PAY_STATUS','REMARK','RESERVE','RESERVE1','RESERVE2','INTE_PAY_DATE_1'])    
    interest_pay_plan_info_1_2=pd.DataFrame(columns=['ID','BOND_ID','INTE_PAY_BIZ_CODE','INTE_PAY_BIZ_YEAR','INTE_PAY_TYPE','INTE_PAY_DATE','REAL_ARR_DATE','REAL_PAY_DATE','INTE_RATE','INTE_SCALE','PLAN_PAY_TYPE','PAY_INTEREST','PAY_CORPUS', 'THIS_PERIOD_TRANS_MONEY','FRUCTUS_AMOUNT','INTE_PAY_STATUS','REMARK','RESERVE','RESERVE1','RESERVE2','INTE_PAY_DATE_1'])
    for j in range(len(interest_pay_plan_info_1)):
        if interest_pay_plan_info_1.loc[j,'INTE_PAY_DATE_1']<=today:
            interest_pay_plan_info_1_1=interest_pay_plan_info_1_1.append(interest_pay_plan_info_1.loc[j,:])
        else:
            interest_pay_plan_info_1_2=interest_pay_plan_info_1_2.append(interest_pay_plan_info_1.loc[j,:])
    interest_pay_plan_info_1_1=interest_pay_plan_info_1_1.reset_index(drop=True)
    interest_pay_plan_info_1_2=interest_pay_plan_info_1_2.reset_index(drop=True)    
    
    if len(interest_pay_plan_info_1_1)==0:
        t=(today-data_ys.loc[i,'VALUE_DATE_1']).days
    else:
        t=(today-interest_pay_plan_info_1_1.iloc[-1,20]).days    
    c=data_ys.loc[i,'FINAL_COUPON_RATE']
    ai=round(c*t/365,4)
    ai_set.append(ai)
 
data_ys['AI']=ai_set
data_ys.to_excel('C:/Users/P300-001/Desktop/债融数据分析/data_ys_result.xlsx')          