#!/usr/bin/env python

# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import statsmodels.api as sm
from datetime import datetime
from datetime import timedelta
from tqdm import tqdm
"""
因子去极值、标准化、行业与市场中性化
"""

def filter_ST_stock(base_data,stock_info,newest_name):
    ''' 
    剔除上市未满一周年、剔除ST、*ST股票
    此函数为因子选股中因子计算所用
    '''
    #将stock_info中的首发上市日期转换为datetime格式
    stock_info_copy=stock_info.copy()
    stock_info_copy['首发上市日期']=pd.to_datetime(stock_info_copy['首发上市日期'])
    #取今天的日期
    today=datetime.today()
    #获取上市未满一周年的股票代码
    stock_list1=stock_info_copy[stock_info_copy['首发上市日期']>(today-timedelta(days=365))]['证券代码'].to_list()
    stock_list2=newest_name[newest_name['证券简称'].str.startswith(('ST','*ST'))]['证券代码'].to_list()
    stock_list=stock_list1+stock_list2
    #去除stock_list中的重复元素
    stock_list=list(set(stock_list))
    base_data_copy=base_data.copy()
    base_data_copy=base_data_copy.drop(columns=stock_list)
    return base_data_copy

def  filter_less_oneyear_ST_stock(base_data,stock_info,trading_status,day):
    '''
    剔除建仓/换仓日上市未满一周年、剔除ST、*ST股票
    此函数为因子选股模型回测计算所用
    trading_status: DataFrame,交易状态
                   index为日期,columns为股票代码
    '''
    #将stock_info中的首发上市日期转换为datetime格式
    stock_info_copy=stock_info.copy()   
    stock_info_copy['首发上市日期']=pd.to_datetime(stock_info_copy['首发上市日期'])
    #将trade_status的index转换为datetime格式
    trading_status_copy=trading_status.copy()
    trading_status_copy.index=pd.to_datetime(trading_status_copy.index,format='%Y/%m/%d')
    #将day转为datetime格式, 取建仓/换仓日前一天的日期
    day=datetime.strptime(day,'%Y/%m/%d')
    day_before=day-timedelta(days=1)
    #获取上市未满一周年的股票代码
    stock_list1=stock_info_copy[stock_info_copy['首发上市日期']>(day_before-timedelta(days=365))]['证券代码'].to_list()
    #获取trading_status中day_before交易状态不为‘交易’的列名list
    stock_list2=trading_status_copy.loc[day_before][trading_status_copy.loc[day_before]!='交易'].index.to_list()
    stock_list=stock_list1+stock_list2
    #去除stock_list中的重复元素
    stock_list=list(set(stock_list))
    base_data_copy=base_data.copy()
    base_data_copy=base_data_copy.drop(columns=stock_list)
    return base_data_copy



def winsorize(factor,method,n=5):
    """
    因子去极值
    ----------------
    factor: DataFrame, 因子矩阵
    method: int, 去极值的方法
          1='MAD',2='3-sigma',3='Percent'
    """
    def mad(factor,n):
        data=factor.dropna().copy()
        median=data.quantile(0.5)
        diff_median=((data-median).abs()).quantile(0.5)
        max_range=median+n*diff_median
        min_range=median-n*diff_median
        return np.clip(data,min_range,max_range)


    def sigma(factor,n=3,have_negative=True):
        r=factor.dropna().copy()

        if have_negative==False:
            r=r[r>=0]
        edge_up=r.mean()+n*r.std()
        edge_low=r.mean()-n*r.std()

        return np.clip(r,edge_low,edge_up)
    
    def Percent(factor,min=0.025,max=0.975):
       
       r=(factor.dropna().copy()).sort_values()
       q=r.quantile([min,max])
       return np.clip(factor,q.iloc[0],q.iloc[-1])
    
    factor_copy=factor.stack(dropna=False)
    factor_copy.index=factor_copy.index.rename(['date','asset'])

    if method==1:
        result=factor_copy.groupby('date').apply(mad,n)
    elif method==2:
        result=factor_copy.groupby('date').apply(sigma)
    elif method==3:
        result=factor_copy.groupby('date').apply(Percent)
    if result.index.nlevels>2:
        result=result.droplevel(0)
    result=result.unstack()
    return result

def standardize(factor,method):
    """
    因子标准化
    ----------------
    factor: DataFrame, 因子矩阵
    method: int, 标准化方法
          1='MinMax',2='Standard',3='maxabs'
    """

    def MinMax(data):
        factor=data.dropna().copy()
        result=(factor-factor.min())/(factor.max()-factor.min())
        return result
    
    def Standard(data):
        factor=data.dropna().copy()
        result=(factor-factor.mean())/factor.std()
        return result
    
    def maxabs(data):
        factor=data.dropna().copy()
        result=factor/10**np.ceil(np.log10(factor.abs().max()))
        return result
    
    
    factor_copy=factor.stack(dropna=False)
    factor_copy.index=factor_copy.index.rename(['date','asset'])
    if method==1:
        result=factor_copy.groupby('date').apply(MinMax)
    elif method==2:
        result=factor_copy.groupby('date').apply(Standard)
    elif method==3:
        result=factor_copy.groupby('date').apply(maxabs)
    if result.index.nlevels>2:
        result=result.droplevel(0)
    result=result.unstack()
    return result


def get_industry_exposure(stock_list,sw_industry_df):
    sw_industry_df=sw_industry_df.set_index('证券代码')
    sw=sw_industry_df.rename_axis(None,axis=0)
    sw22=pd.DataFrame(sw['sw22'])
    goal=sw22.loc[stock_list,:]
    result=pd.get_dummies(goal,columns=['sw22'],prefix='', prefix_sep='').astype(int)
    result=result.rename_axis(None,axis=0)
    return result




def neutralization(factor,sw_industry_df,is_mkt_cap=False,mkt_cap=None,industry=True):
    """
    市值行业中性化
    """
    y=factor
    factor_copy=factor.copy().reset_index()
    if is_mkt_cap:
        if type(mkt_cap)==pd.Series:
            LnMktcap=mkt_cap.apply(lambda x:np.log(x))
            if industry:
                dummy_industry=get_industry_exposure(factor_copy['asset'],sw_industry_df)
                dummy_industry.index=factor.index
                data=pd.concat([y,LnMktcap,dummy_industry],axis=1)
            else:
                data=pd.concat([y,LnMktcap],axis=1)
    elif industry:
        dummy_industry=get_industry_exposure(factor.index.levels[-1],sw_industry_df)
        data=pd.concat([y,dummy_industry],axis=1)
    data=data.replace([-np.inf,np.inf],np.nan).dropna()
    result=sm.OLS(data.iloc[:,0].astype(float),data.iloc[:,1:].astype(float),missing='drop').fit()
    return result.resid


def get_win_stand_neutra(factor,sw_industry_df,win_method,stand_method,is_mkt_cap=True,mkt_cap=None,is_industry=True,MAD_n=5):
    """
    因子去极值, 标准化, 市场行业中性化
    
    参数
    -----------------------
    factor: DataFrame,因子值
    sw_industry_df: sw行业df
    win_method:int, 去极值的方法
               1='MAD',2='3-sigma',3='Percent'
    
    stand_method: int, 标准化方法
                  1='MinMax',2='Standard',3='maxabs'
    is_mkt_cap: bool 默认True
                是否市值中性化
    mkt_cap: DataFrame,市值
            is_mkt_cap为True时, 不能为None
    is_industry: bool 默认为True
                 是否行业中性化
    MAD_n: 去极值方法为'MAD'时的参数n, 默认为5
    
    """
    factor=winsorize(factor,win_method,MAD_n)
    factor=standardize(factor,stand_method)
    factor_copy=factor.copy()
    factor_copy.index=pd.to_datetime(factor_copy.index,format="%Y/%m/%d")
    factor_copy=factor_copy.stack(dropna=False)
    factor_copy.index = factor_copy.index.rename(['date', 'asset'])
    merged_data=pd.DataFrame([],index=factor_copy.index)
    merged_data['factor']=factor_copy

    if is_mkt_cap:
        try:
            mkt_cap_slice=mkt_cap.loc[factor.index,:]
            mkt_cap_slice.index=pd.to_datetime(mkt_cap_slice.index,format="%Y/%m/%d")
            mkt_cap_copy=mkt_cap_slice.stack(dropna=False)
            merged_data['mkt_cap']=mkt_cap_copy
            merged_data=merged_data.dropna()
            tqdm.pandas(desc="市值中性化")
            result=merged_data.groupby('date').progress_apply(lambda x: neutralization(x['factor'],sw_industry_df,True,x['mkt_cap'],is_industry))
        except ValueError:
            print('请保证因子与市值的index对齐')
    else:
        merged_data=merged_data.dropna()
        tqdm.pandas(desc="行业中性化")
        result=merged_data.groupby('date').progress_apply(lambda x: neutralization(x['factor'],sw_industry_df,industry=is_industry))
    result=result.droplevel(0)
    result=result.unstack() 
    result.index=result.index.strftime('%Y/%m/%d') 

    return result


          


