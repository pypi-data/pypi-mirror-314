# -*- coding: utf-8 -*-

from .version import __version__
from .analyze import FactorAnalyzer
from .pos import stock_select
from . import data_load,preprocess,prepare

def analyze_factor(
    factor, prices, groupby=None, weights=1.0, 
                 quantiles=5, bins=None, periods=(1,14),
                 binning_by_group=False, specify_industry=False,industry=None,
                 max_loss=0.25, zero_aware=False
):

    return FactorAnalyzer(factor, prices, groupby=groupby, weights=weights, 
                 quantiles=quantiles, bins=bins, periods=periods,
                 binning_by_group=binning_by_group, specify_industry=specify_industry,industry=industry,
                 max_loss=max_loss, zero_aware=zero_aware)

def pos_select(factor_data,all_A,cum_ret,stock):
    return stock_select(factor_data,all_A,cum_ret,stock_code=stock)

