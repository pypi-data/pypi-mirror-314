#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""
快捷化读取本地行情数据
"""

import pandas as pd
import platform



def close_hfq(file_path):
    """读取收盘价(后复权)数据
    参数:
    ------------
    file_path: 字符串, 文件路径
    
    """
    current_os=platform.system()
    if current_os=='Windows':
        if '\\' in file_path:
            if file_path[-1]=='\\':
                file_path=file_path+'close_hfq'
            else:
                file_path=file_path+'\\close_hfq'
        elif '/' in file_path:
            if file_path[-1]=='/':
                file_path=file_path+'close_hfq'
            else:
                file_path=file_path+'/close_hfq'
        else:
            print('请输入正确的文件路径')
    elif current_os=='Darwin' or current_os=='Linux':
        if file_path[-1]=='/':
            file_path=file_path+'close_hfq'
        else:
            file_path=file_path+'/close_hfq'

    try:
        close=pd.read_csv(file_path+'.csv',index_col=[0])
    except ValueError or FileNotFoundError:
        close=pd.read_excel(file_path+'.xlsx',index_col=[0])
    return close

def close_bfq(file_path):
    """读取收盘价(不复权)数据
    参数:
    ------------
    file_path: 字符串, 文件路径
    
    """
    current_os=platform.system()
    if current_os=='Windows':
        if '\\' in file_path:
            if file_path[-1]=='\\':
                file_path=file_path+'close_bfq'
            else:
                file_path=file_path+'\\close_bfq'
        elif '/' in file_path:
            if file_path[-1]=='/':
                file_path=file_path+'close_bfq'
            else:
                file_path=file_path+'/close_bfq'
        else:
            print('请输入正确的文件路径')
    elif current_os=='Darwin' or current_os=='Linux':
        if file_path[-1]=='/':
            file_path=file_path+'close_bfq'
        else:
            file_path=file_path+'/close_bfq'

    try:
        close=pd.read_csv(file_path+'.csv',index_col=[0])
    except ValueError or FileNotFoundError:
        close=pd.read_excel(file_path+'.xlsx',index_col=[0])
    return close

def open_hfq(file_path):
    """读取开盘价(后复权)数据
    参数:
    ------------
    file_path: 字符串, 文件路径
    
    """
    current_os=platform.system()
    if current_os=='Windows':
        if '\\' in file_path:
            if file_path[-1]=='\\':
                file_path=file_path+'open_hfq'
            else:
                file_path=file_path+'\\open_hfq'
        elif '/' in file_path:
            if file_path[-1]=='/':
                file_path=file_path+'open_hfq'
            else:
                file_path=file_path+'/open_hfq'
        else:
            print('请输入正确的文件路径')
    elif current_os=='Darwin' or current_os=='Linux':
        if file_path[-1]=='/':
            file_path=file_path+'open_hfq'
        else:
            file_path=file_path+'/open_hfq'

    try:
        Open=pd.read_csv(file_path+'.csv',index_col=[0])
    except ValueError or FileNotFoundError:
        Open=pd.read_excel(file_path+'.xlsx',index_col=[0]) 
    return Open

def high_hfq(file_path):
    """读取最高价(后复权)数据
    参数:
    ------------
    file_path: 字符串, 文件路径
    
    """
    current_os=platform.system()
    if current_os=='Windows':
        if '\\' in file_path:
            if file_path[-1]=='\\':
                file_path=file_path+'high_hfq'
            else:
                file_path=file_path+'\\high_hfq'
        elif '/' in file_path:
            if file_path[-1]=='/':
                file_path=file_path+'high_hfq'
            else:
                file_path=file_path+'/high_hfq'
        else:
            print('请输入正确的文件路径')
    elif current_os=='Darwin' or current_os=='Linux':
        if file_path[-1]=='/':
            file_path=file_path+'high_hfq'
        else:
            file_path=file_path+'/high_hfq'

    try:
        high=pd.read_csv(file_path+'.csv',index_col=[0])
    except ValueError or FileNotFoundError:
        high=pd.read_excel(file_path+'.xlsx',index_col=[0])  
    return high

def low_hfq(file_path):
    """读取最低价(后复权)数据
    参数:
    ------------
    file_path: 字符串, 文件路径
    
    """
    current_os=platform.system()
    if current_os=='Windows':
        if '\\' in file_path:
            if file_path[-1]=='\\':
                file_path=file_path+'low_hfq'
            else:
                file_path=file_path+'\\low_hfq'
        elif '/' in file_path:
            if file_path[-1]=='/':
                file_path=file_path+'low_hfq'
            else:
                file_path=file_path+'/low_hfq'
        else:
            print('请输入正确的文件路径')
    elif current_os=='Darwin' or current_os=='Linux':
        if file_path[-1]=='/':
            file_path=file_path+'low_hfq'
        else:
            file_path=file_path+'/low_hfq'

    try:
        low=pd.read_csv(file_path+'.csv',index_col=[0])
    except ValueError or FileNotFoundError:
        low=pd.read_excel(file_path+'.xlsx',index_col=[0])  
    return low

def volume(file_path):
    """读取成交量数据
    参数:
    ------------
    file_path: 字符串, 文件路径
    
    """
    current_os=platform.system()
    if current_os=='Windows':
        if '\\' in file_path:
            if file_path[-1]=='\\':
                file_path=file_path+'volume'
            else:
                file_path=file_path+'\\volume'
        elif '/' in file_path:
            if file_path[-1]=='/':
                file_path=file_path+'volume'
            else:
                file_path=file_path+'/volume'
        else:
            print('请输入正确的文件路径')
    elif current_os=='Darwin' or current_os=='Linux':
        if file_path[-1]=='/':
            file_path=file_path+'volume'
        else:
            file_path=file_path+'/volume'

    try:
        volume=pd.read_csv(file_path+'.csv',index_col=[0])
    except ValueError or FileNotFoundError:
        volume=pd.read_excel(file_path+'.xlsx',index_col=[0])  
    return volume

def amount(file_path):
    """读取成交额数据
    参数:
    ------------
    file_path: 字符串, 文件路径
    
    """
    current_os=platform.system()
    if current_os=='Windows':
        if '\\' in file_path:
            if file_path[-1]=='\\':
                file_path=file_path+'amount'
            else:
                file_path=file_path+'\\amount'
        elif '/' in file_path:
            if file_path[-1]=='/':
                file_path=file_path+'amount'
            else:
                file_path=file_path+'/amount'
        else:
            print('请输入正确的文件路径')
    elif current_os=='Darwin' or current_os=='Linux':
        if file_path[-1]=='/':
            file_path=file_path+'amount'
        else:
            file_path=file_path+'/amount'

    try:
        amount=pd.read_csv(file_path+'.csv',index_col=[0])
    except ValueError or FileNotFoundError:
        amount=pd.read_excel(file_path+'.xlsx',index_col=[0]) 
    return amount

def totalShares(file_path):
    """读取总股本数据
    参数:
    ------------
    file_path: 字符串, 文件路径
    
    """
    current_os=platform.system()
    if current_os=='Windows':
        if '\\' in file_path:
            if file_path[-1]=='\\':
                file_path=file_path+'totalShares'
            else:
                file_path=file_path+'\\totalShares'
        elif '/' in file_path:
            if file_path[-1]=='/':
                file_path=file_path+'totalShares'
            else:
                file_path=file_path+'/totalShares'
        else:
            print('请输入正确的文件路径')
    elif current_os=='Darwin' or current_os=='Linux':
        if file_path[-1]=='/':
            file_path=file_path+'totalShares'
        else:
            file_path=file_path+'/totalShares'

    try:
        totalShares=pd.read_csv(file_path+'.csv',index_col=[0])
    except ValueError or FileNotFoundError:
        totalShares=pd.read_excel(file_path+'.xlsx',index_col=[0])
    return totalShares

def floatSharesOfAShares(file_path):
    """读取A股流通股本数据
    参数:
    ------------
    file_path: 字符串, 文件路径
    
    """
    current_os=platform.system()
    if current_os=='Windows':
        if '\\' in file_path:
            if file_path[-1]=='\\':
                file_path=file_path+'floatSharesOfAShares'
            else:
                file_path=file_path+'\\floatSharesOfAShares'
        elif '/' in file_path:
            if file_path[-1]=='/':
                file_path=file_path+'floatSharesOfAShares'
            else:
                file_path=file_path+'/floatSharesOfAShares'
        else:
            print('请输入正确的文件路径')
    elif current_os=='Darwin' or current_os=='Linux':
        if file_path[-1]=='/':
            file_path=file_path+'floatSharesOfAShares'
        else:
            file_path=file_path+'/floatSharesOfAShares'

    try:
        floatSharesOfAShares=pd.read_csv(file_path+'.csv',index_col=[0])
    except ValueError or FileNotFoundError:
        floatSharesOfAShares=pd.read_excel(file_path+'.xlsx',index_col=[0])
    return floatSharesOfAShares

def floatCapitalOfAShares(file_path):
    """读取A股流通市值数据
    参数:
    ------------
    file_path: 字符串, 文件路径
    
    """
    current_os=platform.system()
    if current_os=='Windows':
        if '\\' in file_path:
            if file_path[-1]=='\\':
                file_path=file_path+'floatCapitalOfAShares'
            else:
                file_path=file_path+'\\floatCapitalOfAShares'
        elif '/' in file_path:
            if file_path[-1]=='/':
                file_path=file_path+'floatCapitalOfAShares'
            else:
                file_path=file_path+'/floatCapitalOfAShares'
        else:
            print('请输入正确的文件路径')
    elif current_os=='Darwin' or current_os=='Linux':
        if file_path[-1]=='/':
            file_path=file_path+'floatCapitalOfAShares'
        else:
            file_path=file_path+'/floatCapitalOfAShares'

    try:
        floatCapitalOfAShares=pd.read_csv(file_path+'.csv',index_col=[0])
    except ValueError or FileNotFoundError:
        floatCapitalOfAShares=pd.read_excel(file_path+'.xlsx',index_col=[0])
    return floatCapitalOfAShares


def cap(file_path):
    """读取总市值数据
    参数:
    ------------
    file_path: 字符串, 文件路径
    
    """
    current_os=platform.system()
    if current_os=='Windows':
        if '\\' in file_path:
            if file_path[-1]=='\\':
                file_path=file_path+'cap'
            else:
                file_path=file_path+'\\cap'
        elif '/' in file_path:
            if file_path[-1]=='/':
                file_path=file_path+'cap'
            else:
                file_path=file_path+'/cap'
        else:
            print('请输入正确的文件路径')
    elif current_os=='Darwin' or current_os=='Linux':
        if file_path[-1]=='/':
            file_path=file_path+'cap'
        else:
            file_path=file_path+'/cap'

    try:
        cap=pd.read_csv(file_path+'.csv',index_col=[0])
    except ValueError or FileNotFoundError:
        cap=pd.read_excel(file_path+'.xlsx',index_col=[0])  
    return cap

def transactionAmount(file_path):
    """读取成交笔数数据
    参数:
    ------------
    file_path: 字符串, 文件路径
    
    """
    current_os=platform.system()
    if current_os=='Windows':
        if '\\' in file_path:
            if file_path[-1]=='\\':
                file_path=file_path+'transactionAmount'
            else:
                file_path=file_path+'\\transactionAmount'
        elif '/' in file_path:
            if file_path[-1]=='/':
                file_path=file_path+'transactionAmount'
            else:
                file_path=file_path+'/transactionAmount'
        else:
            print('请输入正确的文件路径')
    elif current_os=='Darwin' or current_os=='Linux':
        if file_path[-1]=='/':
            file_path=file_path+'transactionAmount'
        else:
            file_path=file_path+'/transactionAmount'

    try:
        transactionAmount=pd.read_csv(file_path+'.csv',index_col=[0])
    except ValueError or FileNotFoundError:
        transactionAmount=pd.read_excel(file_path+'.xlsx',index_col=[0])
    return transactionAmount

def turnover(file_path):
    """读取换手率数据
    参数:
    ------------
    file_path: 字符串, 文件路径
    
    """
    current_os=platform.system()
    if current_os=='Windows':
        if '\\' in file_path:
            if file_path[-1]=='\\':
                file_path=file_path+'turnover'
            else:
                file_path=file_path+'\\turnover'
        elif '/' in file_path:
            if file_path[-1]=='/':
                file_path=file_path+'turnover'
            else:
                file_path=file_path+'/turnover'
        else:
            print('请输入正确的文件路径')
    elif current_os=='Darwin' or current_os=='Linux':
        if file_path[-1]=='/':
            file_path=file_path+'turnover'
        else:
            file_path=file_path+'/turnover'

    try:
        turnover=pd.read_csv(file_path+'.csv',index_col=[0])
    except ValueError or FileNotFoundError:
        turnover=pd.read_excel(file_path+'.xlsx',index_col=[0]) 
    return turnover

def PE_ttm(file_path):
    """读取市盈率(TTM)数据
    参数:
    ------------
    file_path: 字符串, 文件路径
    
    """
    current_os=platform.system()
    if current_os=='Windows':
        if '\\' in file_path:
            if file_path[-1]=='\\':
                file_path=file_path+'PE_ttm'
            else:
                file_path=file_path+'\\PE_ttm'
        elif '/' in file_path:
            if file_path[-1]=='/':
                file_path=file_path+'PE_ttm'
            else:
                file_path=file_path+'/PE_ttm'
        else:
            print('请输入正确的文件路径')
    elif current_os=='Darwin' or current_os=='Linux':
        if file_path[-1]=='/':
            file_path=file_path+'PE_ttm'
        else:
            file_path=file_path+'/PE_ttm'

    try:
        PE_ttm=pd.read_csv(file_path+'.csv',index_col=[0])
    except ValueError or FileNotFoundError:
        PE_ttm=pd.read_excel(file_path+'.xlsx',index_col=[0])
    return PE_ttm

def pb_lf(file_path):
    """读取市净率(后复权)数据
    参数:
    ------------
    file_path: 字符串, 文件路径
    
    """
    current_os=platform.system()
    if current_os=='Windows':
        if '\\' in file_path:
            if file_path[-1]=='\\':
                file_path=file_path+'pb_lf'
            else:
                file_path=file_path+'\\pb_lf'
        elif '/' in file_path:
            if file_path[-1]=='/':
                file_path=file_path+'pb_lf'
            else:
                file_path=file_path+'/pb_lf'
        else:
            print('请输入正确的文件路径')
    elif current_os=='Darwin' or current_os=='Linux':
        if file_path[-1]=='/':
            file_path=file_path+'pb_lf'
        else:
            file_path=file_path+'/pb_lf'

    try:
        pb_lf=pd.read_csv(file_path+'.csv',index_col=[0])
    except ValueError or FileNotFoundError:
        pb_lf=pd.read_excel(file_path+'.xlsx',index_col=[0])
    return pb_lf

def ps_ttm(file_path):
    """读取市销率(后复权)数据
    参数:
    ------------
    file_path: 字符串, 文件路径
    
    """
    current_os=platform.system()
    if current_os=='Windows':
        if '\\' in file_path:
            if file_path[-1]=='\\':
                file_path=file_path+'ps_ttm'
            else:
                file_path=file_path+'\\ps_ttm'
        elif '/' in file_path:
            if file_path[-1]=='/':
                file_path=file_path+'ps_ttm'
            else:
                file_path=file_path+'/ps_ttm'
        else:
            print('请输入正确的文件路径')
    elif current_os=='Darwin' or current_os=='Linux':
        if file_path[-1]=='/':
            file_path=file_path+'ps_ttm'
        else:
            file_path=file_path+'/ps_ttm'

    try:
        ps_ttm=pd.read_csv(file_path+'.csv',index_col=[0])
    except ValueError or FileNotFoundError:
        ps_ttm=pd.read_excel(file_path+'.xlsx',index_col=[0])
    return ps_ttm

def vwap(file_path):
    """读取市值加权均价数据
    参数:
    ------------
    file_path: 字符串, 文件路径
    
    """
    current_os=platform.system()
    if current_os=='Windows':
        if '\\' in file_path:
            if file_path[-1]=='\\':
                file_path=file_path+'vwap'
            else:
                file_path=file_path+'\\vwap'
        elif '/' in file_path:
            if file_path[-1]=='/':
                file_path=file_path+'vwap'
            else:
                file_path=file_path+'/vwap'
        else:
            print('请输入正确的文件路径')
    elif current_os=='Darwin' or current_os=='Linux':
        if file_path[-1]=='/':
            file_path=file_path+'vwap'
        else:
            file_path=file_path+'/vwap'

    try:
        vwap=pd.read_csv(file_path+'.csv',index_col=[0])
    except ValueError or FileNotFoundError:
        vwap=pd.read_excel(file_path+'.xlsx',index_col=[0])   
    return vwap

def returns(file_path):
    """读取日收益率(%)数据
       等同于close_hfq.pct_change()
    参数:
    ------------
    file_path: 字符串, 文件路径
    
    """
    current_os=platform.system()
    if current_os=='Windows':
        if '\\' in file_path:
            if file_path[-1]=='\\':
                file_path=file_path+'change_ratio'
            else:
                file_path=file_path+'\\change_ratio'
        elif '/' in file_path:
            if file_path[-1]=='/':
                file_path=file_path+'change_ratio'
            else:
                file_path=file_path+'/change_ratio'
        else:
            print('请输入正确的文件路径')
    elif current_os=='Darwin' or current_os=='Linux':
        if file_path[-1]=='/':
            file_path=file_path+'change_ratio'
        else:
            file_path=file_path+'/change_ratio'

    try:
        change_ratio=pd.read_csv(file_path+'.csv',index_col=[0])
    except ValueError or FileNotFoundError:
        change_ratio=pd.read_excel(file_path+'.xlsx',index_col=[0]) 
    return change_ratio

def sw3hy_close(file_path):
    """读取申万三级行业指数日收盘价数据
    参数:
    ------------
    file_path: 字符串, 文件路径
    
    """
    current_os=platform.system()
    if current_os=='Windows':
        if '\\' in file_path:
            if file_path[-1]=='\\':
                file_path=file_path+'sw3hyzs_close_hfq'
            else:
                file_path=file_path+'\\sw3hyzs_close_hfq'
        elif '/' in file_path:
            if file_path[-1]=='/':
                file_path=file_path+'sw3hyzs_close_hfq'
            else:
                file_path=file_path+'/sw3hyzs_close_hfq'
        else:
            print('请输入正确的文件路径')
    elif current_os=='Darwin' or current_os=='Linux':
        if file_path[-1]=='/':
            file_path=file_path+'sw3hyzs_close_hfq'
        else:
            file_path=file_path+'/sw3hyzs_close_hfq'

    try:
        sw3hyzs_close_hfq=pd.read_csv(file_path+'.csv',index_col=[0])
    except ValueError or FileNotFoundError:
        sw3hyzs_close_hfq=pd.read_excel(file_path+'.xlsx',index_col=[0])  
    return sw3hyzs_close_hfq

def KJindex_close(file_path):
    """读取宽基指数日收盘价数据
    参数:
    ------------
    file_path: 字符串, 文件路径
    
    """
    current_os=platform.system()
    if current_os=='Windows':
        if '\\' in file_path:
            if file_path[-1]=='\\':
                file_path=file_path+'ZS_close'
            else:
                file_path=file_path+'\\ZS_close'
        elif '/' in file_path:
            if file_path[-1]=='/':
                file_path=file_path+'ZS_close'
            else:
                file_path=file_path+'/ZS_close'
        else:
            print('请输入正确的文件路径')
    elif current_os=='Darwin' or current_os=='Linux':
        if file_path[-1]=='/':
            file_path=file_path+'ZS_close'
        else:
            file_path=file_path+'/ZS_close'

    try:
        ZS_close=pd.read_csv(file_path+'.csv',index_col=[0])
    except ValueError or FileNotFoundError:
        ZS_close=pd.read_excel(file_path+'.xlsx',index_col=[0])
    return ZS_close

def all_stock_info(file_path):
    """读取股票信息数据
    参数:
    ------------
    file_path: 字符串, 文件路径
    
    """
    current_os=platform.system()
    if current_os=='Windows':
        if '\\' in file_path:
            if file_path[-1]=='\\':
                file_path=file_path+'all_stock_info'
            else:
                file_path=file_path+'\\all_stock_info'
        elif '/' in file_path:
            if file_path[-1]=='/':
                file_path=file_path+'all_stock_info'
            else:
                file_path=file_path+'/all_stock_info'
        else:
            print('请输入正确的文件路径')
    elif current_os=='Darwin' or current_os=='Linux':
        if file_path[-1]=='/':
            file_path=file_path+'all_stock_info'
        else:
            file_path=file_path+'/all_stock_info'

    try:
        industry=pd.read_csv(file_path+'.csv',encoding='gbk')
    except ValueError or FileNotFoundError or UnicodeDecodeError:
        industry=pd.read_csv(file_path+'.csv')
    return industry

def newest_stock_name(file_path):
    """读取最新证券名称
    参数:
    ------------
    file_path: 字符串, 文件路径
    
    """
    current_os=platform.system()
    if current_os=='Windows':
        if '\\' in file_path:
            if file_path[-1]=='\\':
                file_path=file_path+'newest_name'
            else:
                file_path=file_path+'\\newest_name'
        elif '/' in file_path:
            if file_path[-1]=='/':
                file_path=file_path+'newest_name'
            else:
                file_path=file_path+'/newest_name'
        else:
            print('请输入正确的文件路径')
    elif current_os=='Darwin' or current_os=='Linux':
        if file_path[-1]=='/':
            file_path=file_path+'newest_name'
        else:
            file_path=file_path+'/newest_name'

    try:
        stock_name=pd.read_csv(file_path+'.csv',encoding='gbk')
    except ValueError or FileNotFoundError or UnicodeDecodeError:
        stock_name=pd.read_csv(file_path+'.csv')
    return stock_name

'''
def SW(file_path):
    """读取SW行业
    参数:
    ------------
    file_path: 字符串, 文件路径
    
    """
    current_os=platform.system()
    if current_os=='Windows':
        if '\\' in file_path:
            if file_path[-1]=='\\':
                file_path=file_path+'sw_industry'
            else:
                file_path=file_path+'\\sw_industry'
        elif '/' in file_path:
            if file_path[-1]=='/':
                file_path=file_path+'sw_industry'
            else:
                file_path=file_path+'/sw_industry'
        else:
            print('请输入正确的文件路径')
    elif current_os=='Darwin' or current_os=='Linux':
        if file_path[-1]=='/':
            file_path=file_path+'sw_industry'
        else:
            file_path=file_path+'/sw_industry'

    try:
        sw=pd.read_csv(file_path+'.csv',index_col=[0],encoding='gbk')
    except ValueError or FileNotFoundError or UnicodeDecodeError:
        sw=pd.read_csv(file_path+'.csv',index_col=[0])
    return sw
'''

'''
def stock_list(file_path):
    """读取股票列表
    参数:
    ------------
    file_path: 字符串, 文件路径
    
    """
    current_os=platform.system()
    if current_os=='Windows':
        if '\\' in file_path:
            if file_path[-1]=='\\':
                file_path=file_path+'stock_info'
            else:
                file_path=file_path+'\\stock_info'
        elif '/' in file_path:
            if file_path[-1]=='/':
                file_path=file_path+'stock_info'
            else:
                file_path=file_path+'/stock_info'
        else:
            print('请输入正确的文件路径')
    elif current_os=='Darwin' or current_os=='Linux':
        if file_path[-1]=='/':
            file_path=file_path+'stock_info'
        else:
            file_path=file_path+'/stock_info'

    try:
        list=pd.read_csv(file_path+'.csv',encoding='gbk')
    except ValueError or FileNotFoundError or UnicodeDecodeError:
        list=pd.read_csv(file_path+'.csv')
    return list
'''

def is_mm_ss(file_path):
    """读取是否两融标的表
    参数:
    ------------
    file_path: 字符串, 文件路径
    
    """
    current_os=platform.system()
    if current_os=='Windows':
        if '\\' in file_path:
            if file_path[-1]=='\\':
                file_path=file_path+'两融标的'
            else:
                file_path=file_path+'\\两融标的'
        elif '/' in file_path:
            if file_path[-1]=='/':
                file_path=file_path+'两融标的'
            else:
                file_path=file_path+'/两融标的'
        else:
            print('请输入正确的文件路径')
    elif current_os=='Darwin' or current_os=='Linux':
        if file_path[-1]=='/':
            file_path=file_path+'两融标的'
        else:
            file_path=file_path+'/两融标的'

    try:
        mm_ss=pd.read_csv(file_path+'.csv',encoding='gbk')
    except ValueError or FileNotFoundError or UnicodeDecodeError:
        mm_ss=pd.read_csv(file_path+'.csv')
    return mm_ss


def trading_status(file_path):
    """读取交易状态数据
    参数:
    ------------
    file_path: 字符串, 文件路径
    
    """
    current_os=platform.system()
    if current_os=='Windows':
        if '\\' in file_path:
            if file_path[-1]=='\\':
                file_path=file_path+'trading_status_stock'
            else:
                file_path=file_path+'\\trading_status_stock'
        elif '/' in file_path:
            if file_path[-1]=='/':
                file_path=file_path+'trading_status_stock'
            else:
                file_path=file_path+'/trading_status_stock'
        else:
            print('请输入正确的文件路径')
    elif current_os=='Darwin' or current_os=='Linux':
        if file_path[-1]=='/':
            file_path=file_path+'trading_status_stock'
        else:
            file_path=file_path+'/trading_status_stock'

    try:
        close=pd.read_csv(file_path+'.csv',index_col=[0],encoding='gbk')
    except ValueError or FileNotFoundError or UnicodeEncodeError:
        close=pd.read_csv(file_path+'.csv',index_col=[0],encoding='utf-8')
    return close

