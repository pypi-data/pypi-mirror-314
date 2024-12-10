# -*- coding: utf-8 -*-

from __future__ import division
import pandas as pd
import numpy as np
import sys
from .exceptions import MaxLossExceededError, non_unique_bin_edges_error
from .utils import get_forward_returns_columns
from datetime import datetime


@non_unique_bin_edges_error
def quantize_factor(factor_data, quantiles=5, bins=None, by_group=False, no_raise=False, zero_aware=False):
    """
    计算每期因子分位数

    参数
    ----------
    factor_data : pd.DataFrame - MultiIndex
        一个 DataFrame, index 为日期 (level 0) 和资产(level 1) 的 MultiIndex,
        values 包括因子的值, 各期因子远期收益, 因子分位数, 因子分组(可选), 因子权重(可选)
    quantiles : int or sequence[float]
        在因子分组中按照因子值大小平均分组的组数或分位数序列, 允许不均匀分组
        例如 [0, .10, .5, .90, 1.] 或 [.05, .5, .95]
        'quantiles' 和 'bins' 有且只能有一个不为 None
    bins : int or sequence[float]
        在因子分组中使用的等宽 (按照因子值) 区间的数量
        或边界值序列, 允许不均匀的区间宽度
        例如 [-4, -2, -0.5, 0, 10]
        'quantiles' 和 'bins' 有且只能有一个不为 None
    by_group : bool
        如果是 True, 按照 group 分别计算分位数（按照行业计算分位数）
    no_raise: bool, optional
        如果为 True，则不抛出任何异常，并且将抛出异常的值设置为 np.NaN
    zero_aware : bool, optional
        如果为True，则分别为正负因子值计算分位数。
        适用于您的信号聚集并且零是正值和负值的分界线的情况.

    返回值
    -------
    factor_quantile : pd.Series
        index 为日期 (level 0) 和资产(level 1) 的因子分位数
    """
    if not ((quantiles is not None and bins is None) or
            (quantiles is None and bins is not None)):
        raise ValueError('quantiles 和 bins 至少要输入一个')

    if zero_aware and not (isinstance(quantiles, int)
                           or isinstance(bins, int)):
        msg = ("只有 quantiles 或 bins 为 int 类型时， 'zero_aware' 才能为 True")
        raise ValueError(msg)

    def quantile_calc(x, _quantiles, _bins, _zero_aware, _no_raise):
        try:
            if _quantiles is not None and _bins is None and not _zero_aware:
                return pd.qcut(x, _quantiles, labels=False,duplicates='drop') + 1  #从小往大排，值越大组越高
            #后续使用报错maybe需要修改代码  return pd.qcut(x, _quantiles, labels=False,duplicates='drop') + 1
            #参数 labels=False 表示返回的结果不使用标签，而是使用整数编码表示每个分位数区间。
            #通过在结果上加1，可以将整数编码标签上移，使得最小值为1而不是0。
            elif _quantiles is not None and _bins is None and _zero_aware:
                pos_quantiles = pd.qcut(x[x >= 0], _quantiles // 2,
                                        labels=False) + _quantiles // 2 + 1
                neg_quantiles = pd.qcut(x[x < 0], _quantiles // 2,
                                        labels=False) + 1
                return pd.concat([pos_quantiles, neg_quantiles]).sort_index()
            elif _bins is not None and _quantiles is None and not _zero_aware:
                return pd.cut(x, _bins, labels=False) + 1
            elif _bins is not None and _quantiles is None and _zero_aware:
                pos_bins = pd.cut(x[x >= 0], _bins // 2,
                                  labels=False) + _bins // 2 + 1
                neg_bins = pd.cut(x[x < 0], _bins // 2,
                                  labels=False) + 1
                return pd.concat([pos_bins, neg_bins]).sort_index()
        except Exception as e:
            if _no_raise:
                return pd.Series(index=x.index)
            raise e

    grouper = [factor_data.index.get_level_values('date')]
    if by_group:
        if 'group' not in factor_data.columns:  
            raise ValueError('只有输入了 groupby 参数时 binning_by_group 才能为 True')
        grouper.append('group')

    factor_quantile = factor_data.groupby(grouper)['factor'] \
        .apply(quantile_calc, quantiles, bins, zero_aware, no_raise)
    factor_quantile.name = 'factor_quantile'  

    if factor_quantile.index.nlevels>2:
        if by_group:
            factor_quantile.index=factor_quantile.index.droplevel(level=[1,2])
        else:    
            factor_quantile.index=factor_quantile.index.droplevel(level=1)

    return factor_quantile.dropna()

def change_data_index_format(data):
    '''
    修改data.index的格式
    将%Y/%m/%d转化为%Y-%m-%d
    '''
    date_index=pd.to_datetime(data.index)
    new=date_index.strftime('%Y-%m-%d')
    data.index=new
    return data



def compute_forward_returns(factor,
                            prices,
                            periods=(14,)):
    """
    计算每个因子值对应的 N 期因子远期收益

    参数
    ----------
    factor : pd.Series - MultiIndex
        一个 Series, index 为日期 (level 0) 和资产(level 1) 的 MultiIndex,
        values 为因子值
    prices : pd.DataFrame
        用于计算因子远期收益的价格数据
        columns 为资产, index 为日期.
        价格数据必须覆盖因子分析时间段以及额外远期收益计算中的最大预期期数.
    periods : sequence[int]
        远期收益的期数
    Returns
    -------
    forward_returns : pd.DataFrame - MultiIndex
        因子远期收益
        index 为日期 (level 0) 和资产(level 1) 的 MultiIndex
        column 为远期收益的期数
    """

    factor_dateindex = factor.index.levels[0]



    factor_dateindex = factor_dateindex.intersection(prices.index)

    if len(factor_dateindex) == 0:
        raise ValueError("Factor and prices indices don't match: make sure "
                         "they have the same convention in terms of datetimes "
                         "and symbol-names")

    prices = prices.filter(items=factor.index.levels[1]) #过滤掉不在因子中的列

    forward_returns = pd.DataFrame(
        index=pd.MultiIndex
        .from_product([factor_dateindex, prices.columns], names=['date', 'asset'])
    )
    
    for period in periods:
            delta = prices.pct_change(period).shift(-period).reindex(factor_dateindex)
            #shift只移动数据，不移动索引，reindex：与因子索引对齐
            forward_returns['period_{p}'.format(p=period)] = delta.stack()

    forward_returns.index = forward_returns.index.rename(['date', 'asset'])

    return forward_returns

def demean_forward_returns(factor_data, grouper=None):
    """
    根据相关分组为因子远期收益去均值.
    分组去均值包含了投资组合分组中性化约束的假设，因此允许跨组评估因子.

    Parameters
    ----------
    factor_data : pd.DataFrame - MultiIndex
        因子远期收益
        index 为日期 (level 0) 和资产(level 1) 的 MultiIndex
        column 为远期收益的期数
    grouper : list
        如果为 None, 则只根据日期去均值
        否则则根据列表中提供的组分组去均值（按照行业去均值）

    返回值
    -------
    adjusted_forward_returns : pd.DataFrame - MultiIndex
        和 factor_data 相同形状的 DataFrame, 但每个收益都被分组去均值了
    """

    factor_data = factor_data.copy()

    if not grouper:
        grouper = factor_data.index.get_level_values('date')

    cols = get_forward_returns_columns(factor_data.columns) 

    if 'weights' in factor_data.columns:
        a= factor_data.groupby(grouper, as_index=False
            )[cols.append(pd.Index(['weights']))].apply(
            lambda x: x[cols].subtract(
            np.average(x[cols], axis=0, weights=x['weights'].fillna(0.0).values),
            axis=1))
        if a.index.nlevels>2:
            a.index=a.index.droplevel(level=0)  #非常隐秘的一个bug
        factor_data[cols]=a
    else:
        factor_data[cols] = factor_data.groupby(grouper)[cols] \
        .transform(lambda x: x - x.mean())
    
    return factor_data

def benchmark_return(factor_data):
    '''计算基准收益(全部股票按天收益加权平均)'''
    factor_data=factor_data.copy()
    grouper=factor_data.index.get_level_values('date')
    cols=get_forward_returns_columns(factor_data.columns)
    
    a= factor_data.groupby(grouper, as_index=False
            )[cols.append(pd.Index(['weights_benchmark']))].apply(
            lambda x: pd.DataFrame(np.average(x[cols], axis=0, weights=x['weights_benchmark'].fillna(0.0).values).reshape(1,-1), 
                                   index=[x.index.get_level_values('date')[0]],columns=[cols]))
    a.index=a.index.droplevel(level=0)
    benchmark=a
    
    return benchmark


        
        

def industry_info_todict(industry,sw):
    ''' 
    将读取的stock_info中的行业数据转换成dict
    参数：
    -------------
    '''
    industry_data=industry.copy()
    industry_data=industry_data.dropna()
    if sw==2:
        groupby=industry_data.set_index('证券代码')['sw22'].to_dict()
    elif sw==3:
        groupby=industry_data.set_index('证券代码')['sw33'].to_dict()
    elif sw==1:
        groupby=industry_data.set_index('证券代码')['sw11'].to_dict()

    return groupby

def weights_info_todict(weights_data):
    ''' 
    将读取的csv权重数据转换成dict(key为stock_code)
    参数：
    -------------
    weights_data: index为stock_data, column为权重
    '''
    weights_data=weights_data.dropna()
    weights=weights_data.set_index('code')['weights'].to_dict()
    return weights

def get_clean_factor(factor,
                     forward_returns,
                     groupby=None,
                     weights=None,
                     binning_by_group=False,
                     specify_industry=False,
                     industry=None,
                     quantiles=5,
                     bins=None,
                     max_loss=0.25,
                     zero_aware=False):
    """
    将因子值, 因子远期收益, 因子分组数据, 因子权重数据
    格式化为以时间和资产的 MultiIndex 作为索引的 DataFrame.
    指定industry时, 得到指定行业数据

    参数
    ----------
    factor : pd.Series - MultiIndex
        一个 Series, index 为日期 (level 0) 和资产(level 1) 的 MultiIndex,
        values 为因子的值
    forward_returns : pd.DataFrame - MultiIndex
        一个 DataFrame, index 为日期 (level 0) 和资产(level 1) 的 MultiIndex,
        values 为因子的远期收益, columns 为因子远期收益的期数.
    groupby : pd.Series - MultiIndex or dict
        index 为日期和资产的 Series，为每个资产每天的分组，或资产-分组映射的字典.
        如果传递了dict，则假定分组映射在整个时间段内保持不变.
    specify_industry: bool
        是否指定行业
    industry: str
        指定的行业，如果specify_industry为True, industry不能为空
    weights : pd.Series - MultiIndex or dict
        index 为日期和资产的 Series，为每个资产每天的权重，或资产-权重映射的字典.
        如果传递了dict，则假定权重映射在整个时间段内保持不变.
    binning_by_group : bool
        如果为 True, groupby非None, 则对每个组分别计算分位数
        适用于因子值范围在各个组(行业）上变化很大的情况.
        如果要分析分组(行业)中性的组合, 最好设置为 True
        如果是False, 则按照全行业得到后续returns
    quantiles : int or sequence[float]
        在因子分组中按照因子值大小平均分组的组数。
         或分位数序列, 允许不均匀分组
        例如 [0, .10, .5, .90, 1.] 或 [.05, .5, .95]
        'quantiles' 和 'bins' 有且只能有一个不为 None
    bins : int or sequence[float]
        在因子分组中使用的等宽 (按照因子值) 区间的数量
        或边界值序列, 允许不均匀的区间宽度
        例如 [-4, -2, -0.5, 0, 10]
        'quantiles' 和 'bins' 有且只能有一个不为 None
    max_loss : float, optional
        允许的丢弃因子数据的最大百分比 (0.00 到 1.00),
        计算比较输入因子索引中的项目数和输出 DataFrame 索引中的项目数.
        因子数据本身存在缺陷 (例如 NaN),
        没有提供足够的价格数据来计算所有因子值的远期收益，
        或者因为分组失败, 因此可以部分地丢弃因子数据
        设置 max_loss = 0 以停止异常捕获.
    zero_aware : bool, optional
        如果为True，则分别为正负因子值计算分位数。
        适用于您的信号聚集并且零是正值和负值的分界线的情况.

    返回值
    -------
    merged_data : pd.DataFrame - MultiIndex
        一个 DataFrame, index 为日期 (level 0) 和资产(level 1) 的 MultiIndex,
        values 包括因子的值, 各期因子远期收益, 因子分位数,
        因子分组(可选), 因子权重(可选)
        - 各期因子远期收益的列名满足 'period_1', 'period_5' 的格式
    """

    factor_copy = factor.copy()
    factor_copy.index = factor_copy.index.rename(['date', 'asset'])

    merged_data = forward_returns.copy()
    merged_data['factor'] = factor_copy

    if weights is not None:  #有别的加权方式（如按市值加权之类的）
        if isinstance(weights, dict):
            diff = set(factor_copy.index.get_level_values(
                'asset')) - set(weights.keys())
            if len(diff) > 0:
                raise KeyError(
                    "Assets {} not in weights mapping".format(
                        list(diff)))

            ww = pd.Series(weights)
            weights = pd.Series(index=factor_copy.index,
                                data=ww[factor_copy.index.get_level_values(
                                    'asset')].values)
        elif isinstance(weights, pd.DataFrame):
            weights = weights.stack()
        merged_data['weights'] = weights
        merged_data['weights_benchmark']=weights
        #merged_data['weights'] = merged_data['weights'].astype(float)

    

    if groupby is not None:
        if isinstance(groupby, dict):
            diff = set(factor_copy.index.get_level_values(
                'asset')) - set(groupby.keys()) 
            if len(diff) > 0:
                raise KeyError(
                    "Assets {} not in group mapping".format(
                        list(diff)))

            ss = pd.Series(groupby)
            groupby = pd.Series(index=factor_copy.index,
                                data=ss[factor_copy.index.get_level_values(
                                    'asset')].values) 

        elif isinstance(groupby, pd.DataFrame):
            groupby = groupby.stack()
        merged_data['group'] = groupby

        

    if groupby is not None:
        if specify_industry: #指定行业
            merged_data=merged_data[merged_data['group']==industry]
            initial_amount = float(len(merged_data.index))
            merged_data=merged_data.replace([np.inf,-np.inf],np.nan)
            merged_data = merged_data.dropna()
            quantile_data = quantize_factor(merged_data,quantiles,bins,binning_by_group,True,zero_aware)
            merged_data['factor_quantile'] = quantile_data
            merged_data = merged_data.dropna()
            merged_data['factor_quantile'] = merged_data['factor_quantile'].astype(int)
            
            #计算在同分位数的因子的权重值
            if 'weights' in merged_data.columns:
                b= merged_data.set_index(
                    'factor_quantile', append=True
                    ).groupby(level=['date', 'factor_quantile'])['weights'].apply(
                    lambda s: s.divide(s.sum()))
                if b.index.nlevels>3:
                    merged_data['weights']=b.droplevel(level=(2,4)).reset_index('factor_quantile',drop=True)
                else:
                    merged_data['weights']=b.reset_index('factor_quantile',drop=True)
            binning_amount = float(len(merged_data.index))
            
            tot_loss = (initial_amount - binning_amount) / initial_amount #因为每一步都删了空值
            no_raise = True if max_loss == 0 else False
            if tot_loss > max_loss and not no_raise:
                message = ("max_loss (%.1f%%) 超过 %.1f%%"
                           % (tot_loss * 100, max_loss * 100))
                raise MaxLossExceededError(message)
        
        else: #全行业
            initial_amount = float(len(merged_data.index))
            merged_data=merged_data.replace([np.inf,-np.inf],np.nan)
            merged_data = merged_data.dropna()
            quantile_data = quantize_factor(merged_data,quantiles,bins,binning_by_group,True,zero_aware)
            #binning_by_group: True：全行业中分组计算因子分位数, False: 不分组计算
            merged_data['factor_quantile'] = quantile_data
            merged_data = merged_data.dropna()
            merged_data['factor_quantile'] = merged_data['factor_quantile'].astype(int)
            
            #计算在同分位数的因子的权重值
            if 'weights' in merged_data.columns:
                b= merged_data.set_index(
                    'factor_quantile', append=True
                    ).groupby(level=['date', 'factor_quantile'])['weights'].apply(
                    lambda s: s.divide(s.sum()))
                if b.index.nlevels>3:
                    merged_data['weights']=b.droplevel(level=(2,4)).reset_index('factor_quantile',drop=True)
                else:
                    merged_data['weights']=b.reset_index('factor_quantile',drop=True)
            binning_amount = float(len(merged_data.index))
            
            tot_loss = (initial_amount - binning_amount) / initial_amount #因为每一步都删了空值
            no_raise = True if max_loss == 0 else False
            
            if tot_loss > max_loss and not no_raise:
                message = ("max_loss (%.1f%%) 超过 %.1f%%"
                           % (tot_loss * 100, max_loss * 100))
                raise MaxLossExceededError(message)
    else: # 没有group时
        initial_amount = float(len(merged_data.index))
        merged_data = merged_data.dropna()
        quantile_data = quantize_factor(
            merged_data,
            quantiles,
            bins,
            binning_by_group,
            True,
            zero_aware
            )
        
        merged_data['factor_quantile'] = quantile_data
        merged_data=merged_data.replace([np.inf,-np.inf],np.nan)
        merged_data = merged_data.dropna()
        merged_data['factor_quantile'] = merged_data['factor_quantile'].astype(int)

        if 'weights' in merged_data.columns:
            b= merged_data.set_index('factor_quantile', append=True
                ).groupby(level=['date', 'factor_quantile'])['weights'].apply(
                lambda s: s.divide(s.sum()))
            if b.index.nlevels>3:
                merged_data['weights']=b.droplevel(level=(2,4)).reset_index('factor_quantile',drop=True)
            else:
                merged_data['weights']=b.reset_index('factor_quantile',drop=True)

        binning_amount = float(len(merged_data.index))

        tot_loss = (initial_amount - binning_amount) / initial_amount 

        no_raise = True if max_loss == 0 else False
        if tot_loss > max_loss and not no_raise:
            message = ("max_loss (%.1f%%) 超过 %.1f%%"
                   % (tot_loss * 100, max_loss * 100))
            raise MaxLossExceededError(message)

    return merged_data

def get_clean_factor_and_forward_returns(factor,
                                         prices,
                                         groupby=None,
                                         weights=None,
                                         binning_by_group=False,
                                         specify_industry=False,
                                         industry=None,
                                         quantiles=5,
                                         bins=None,
                                         periods=(14,),
                                         max_loss=0.25,
                                         zero_aware=False):
    """
    将因子数据, 价格数据, 分组映射和权重映射格式化为
    由包含时间和资产的 MultiIndex 作为索引的 DataFrame
    可以指定特定行业

    参数
    ----------
    factor : pd.Series - MultiIndex
     一个 Series, index 为日期 (level 0) 和资产(level 1) 的 MultiIndex,
        values 为因子的值

    prices : pd.DataFrame
        用于计算因子远期收益的价格数据
        columns 为资产, index 为 日期.
        价格数据必须覆盖因子分析时间段以及额外远期收益计算中的最大预期期数.
    groupby : pd.Series - MultiIndex or dict
        index 为日期和资产的 Series，为每个资产每天的分组，或资产-分组映射的字典.
        如果传递了dict，则假定分组映射在整个时间段内保持不变.
    specify_industry: bool
        是否指定行业
    industry: str
        指定的行业，如果specify_industry为True, industry不能为空
    weights : pd.Series - MultiIndex or dict
        index 为日期和资产的 Series，为每个资产每天的权重，或资产-权重映射的字典.
        如果传递了dict，则假定权重映射在整个时间段内保持不变.
    binning_by_group : bool
        如果为 True, 则对每个组分别计算分位数.
        适用于因子值范围在各个组上变化很大的情况.
        如果要分析分组(行业)中性的组合, 您最好设置为 True
    quantiles : int or sequence[float]
        在因子分组中按照因子值大小平均分组的组数。
         或分位数序列, 允许不均匀分组
        例如 [0, .10, .5, .90, 1.] 或 [.05, .5, .95]
        'quantiles' 和 'bins' 有且只能有一个不为 None
    bins : int or sequence[float]
        在因子分组中使用的等宽 (按照因子值) 区间的数量
        或边界值序列, 允许不均匀的区间宽度
        例如 [-4, -2, -0.5, 0, 10]
        'quantiles' 和 'bins' 有且只能有一个不为 None
    periods : sequence[int]
        远期收益的期数
    max_loss : float, optional
        允许的丢弃因子数据的最大百分比 (0.00 到 1.00),
        计算比较输入因子索引中的项目数和输出 DataFrame 索引中的项目数.
        因子数据本身存在缺陷 (例如 NaN),
        没有提供足够的价格数据来计算所有因子值的远期收益，
        或者因为分组失败, 因此可以部分地丢弃因子数据
        设置 max_loss = 0 以停止异常捕获.
    zero_aware : bool, optional
        如果为True，则分别为正负因子值计算分位数。
        适用于您的信号聚集并且零是正值和负值的分界线的情况.

    返回值
    -------
    merged_data : pd.DataFrame - MultiIndex
        一个 DataFrame, index 为日期 (level 0) 和资产(level 1) 的 MultiIndex,
        values 包括因子的值, 各期因子远期收益, 因子分位数,
        因子分组(可选), 因子权重(可选)
        - 各期因子远期收益的列名满足 'period_1', 'period_5' 的格式
    """
    forward_returns = compute_forward_returns(factor, prices, periods)
    
    factor_data = get_clean_factor(factor, forward_returns,groupby=groupby, weights=weights,binning_by_group=binning_by_group,
                                   specify_industry=specify_industry,
                                   industry=industry,
                                   quantiles=quantiles, bins=bins,
                                   max_loss=max_loss, zero_aware=zero_aware)

    return factor_data


def common_start_returns(factor,prices,before,after,cumulative=False,mean_by_date=False, demean_by=None):
    '''
    给定因子在每个日期的前 before 个交易日到后 after 个交易日内, 资产的收益率。

    参数：
    ---------------
    factor : pd.Series- MultiIndex
        一个 DataFrame, index 为日期 (level 0) 和资产(level 1) 的 MultiIndex,
        values 包括因子的值
    prices : pd.DataFrame
        用于计算因子远期收益的价格数据
        columns 为资产, index 为 日期.
        价格数据必须覆盖因子分析时间段以及额外远期收益计算中的最大预期期数.
    before: int 
            要计算的收益率时间段的前置期长度。
    after: int
            要计算的收益率时间段的后置期长度。
    cumulative: bool, 是否计算累积收益率
                如果为 True, 则返回的是从 day_zero 开始的累积收益率；如果为 False, 则返回的是每日收益率。
    mean_by_date: bool, 是否按日期计算资产的平均收益率
                如果为 True,则返回每个日期的平均收益率；如果为 False,则返回每个日期和每个资产的收益率。
    demean_by: pd.Series - MultiIndex
              一个 DataFrame, index 为date (level 0) 和asset(level 1) 的 MultiIndex

       

    '''
    if cumulative:
        returns = prices
    else:
        returns = prices.pct_change(axis=0)

    all_returns = []

    for timestamp, df in factor.groupby(level='date'):

        equities = df.index.get_level_values('asset')

        try:
            day_zero_index = returns.index.get_loc(timestamp)
        except KeyError:
            continue

        starting_index = max(day_zero_index - before, 0)
        ending_index = min(day_zero_index + after + 1, len(returns.index))

        equities_slice = set(equities)
        if demean_by is not None:
            demean_equities = demean_by.loc[timestamp] \
                .index.get_level_values('asset')
            equities_slice |= set(demean_equities) #取并集

        series = returns.loc[returns.
                             index[starting_index:ending_index], list(equities_slice)]
        series.index = range(
            starting_index - day_zero_index, ending_index - day_zero_index
        )

        if cumulative:
            series = (series / series.loc[0, :]) - 1

        if demean_by is not None:
            mean = series.loc[:, demean_equities].mean(axis=1)
            series = series.loc[:, equities]
            series = series.sub(mean, axis=0)

        if mean_by_date:
            series = series.mean(axis=1) #按行操作  

        all_returns.append(series)

    return pd.concat(all_returns, axis=1)

def rate_of_return(period_ret):
    """
    转换回报率为"每期"回报率：如果收益以稳定的速度增长, 则相当于每期的回报率
    用处：知道某个资产在某个时间段内的总收益率（例如 10%），想知道它在每个交易日的平均回报率是多少
    """
    period = int(period_ret.name.replace('period_', '')) #取天数，比如period_5,取出5
    return period_ret.add(1).pow(1. / period).sub(1)


def std_conversion(period_std):
    """
    转换回报率标准差为"每期"回报率标准差
    """
    period_len = int(period_std.name.replace('period_', ''))
    return period_std / np.sqrt(period_len)

def industry_get(group,stock):

    stock_industry=group[stock]
    return stock_industry

