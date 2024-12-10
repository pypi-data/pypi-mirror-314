#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

def worst_return_quantile(cum_ret):
    ''' 
    得到每天受益最差的分位数和收益最好的分位数

    参数：
    -----------
    cum_ret: pd.DataFrame
           按照指定调仓周期的各分位数每日累积收益
    
    return: int       
    '''
    worst_quantile=cum_ret.idxmin(axis=1)
    worst_quantile=worst_quantile.rename('worst_quantile')
    best_quantile=cum_ret.idxmax(axis=1)
    best_quantile=best_quantile.rename('best_quantile')
    return worst_quantile,best_quantile

def target_stock_quantile(factor_data, stock_code=None):
    ''' 
    目标股票所在分位数

    参数：
    ---------
    factor_data: pd.DataFrame - MultiIndex
        一个 DataFrame, index 为日期 (level 0) 和资产(level 1) 的 MultiIndex,
        values 包括因子的值, 各期因子远期收益, 因子分位数,
        因子分组(可选), 因子权重(可选)
    stock_code: str
        目标股票名称
    '''
    target=factor_data.loc[factor_data.index.get_level_values('asset') == stock_code, 'factor_quantile']
    target.index=target.index.droplevel(level=1)
    target=target.rename('目标股票所在层数')
    return target

def worst_return_quantile_stock_code(factor_data, cum_ret):
    '''  
    收益最差的分位数所包含的股票
    return: pd.Series
    '''

    w,_=worst_return_quantile(cum_ret)
    merged_df = pd.merge(factor_data['factor_quantile'].reset_index(),w.reset_index(), on='date', how='left')
    merged_df=merged_df[merged_df['factor_quantile']==merged_df['worst_quantile']]
    stock=merged_df.groupby('date')['asset'].apply(list)
    stock=stock.rename('最差层包含的证券代码')

    return stock



def stock_chinese_name(all_A,worst_stock):
    '''股票对应的中文名
    参数：
    -------
    all_A: A股数据
    worst_stock: 股票代码
    '''
    stock_df=pd.DataFrame(worst_stock)
    result={}
    for index,row in stock_df.iterrows():
        date=index
        asset_list=row['最差层包含的证券代码']
        asset_names=[]
        for asset_code in asset_list:
            asset_name=all_A[all_A['证券代码']==asset_code]['证券名称'].values[0]
            asset_names.append(asset_name) 
        
        result[date]=asset_names

    result=pd.Series(result)
    result=result.rename('最差层包含的证券名称')

    return result

def stock_select(factor_data,all_A,cum_ret,stock_code=None):
    '''
    目标股票所在分位数和最差分位数所包含股票
    '''
    target=target_stock_quantile(factor_data,stock_code)
    worststock=worst_return_quantile_stock_code(factor_data,cum_ret)
    stock_chinese=stock_chinese_name(all_A,worststock)
    w,b=worst_return_quantile(cum_ret)
    stock_df=pd.concat([b,target,w,worststock,stock_chinese],axis=1)

    return stock_df
    

  







