import pandas as pd
import re


def extract_numbers(input_string):
    """Neon Toolkit, 从字符串找到至少一个连续数字组成的字符串并提取出来。

    Args:
        input_string (str): 输入的连续字符串

    Returns:
        str: 返回的连续数字字符串.
    """
    # 正则表达式模式，用于匹配10位连续的数字
    pattern = r'\d{1,}'
    # 查找所有匹配的模式
    matches = re.findall(pattern, input_string)
    return matches[0]

def preprocess_account(state_df: pd.DataFrame):
    """预处理 进项发票台账导出-全部(增值税发票) 文件 发票主表及状态信息 表
        1. 提取出采购类记录作为子表
        2. 提取单据编号中的若干位连续数字作为中台编号 
        3. 提取单据摘要中的10位连续数字作为采购订单号 
    Args:
        state_df (pd.DataFrame): 进项发票台账导出-全部(增值税发票) 文件 发票主表及状态信息 表
    Returns:
        pd.DataFrame: 预处理后的采购类报账单记录
    """
    state_df = state_df[['开票日期','发票号码','发票状态','合计金额','合计税额','价税合计','销售方名称','单据编号','单据摘要']].copy()
    no_ser = state_df['单据编号']
    state_df.loc[:, '采购类'] = no_ser.apply(lambda x: '采购类报账单' in str(x))
    buy_df = state_df[state_df['采购类'] == True]  # 提取出采购类记录作为子表
    buy_df_copy = buy_df.copy()
    buy_df_copy.loc[:, '中台编号'] = buy_df.apply(lambda x: extract_numbers(x['单据编号']), axis=1)  # 提取单据编号中的若干位连续数字作为中台编号 
    buy_df_copy.loc[:, '采购订单'] = buy_df.apply(lambda x: extract_numbers(x['单据摘要']), axis=1)  # 提取单据摘要中的10位连续数字作为采购订单号 
    
    return buy_df_copy

def job_compare_tax(state_df: pd.DataFrame, in_df: pd.DataFrame):
    """比较 进项发票台账导出-全部(增值税发票) 文件 发票主表及状态信息 表 中采购类报账单记录 与 入账文件 中 2025.12 表 的入账记录 两者 合计税额 和 可抵扣税额 是否一致

    Args:
        state_df (pd.DataFrame): 进项发票台账导出-全部(增值税发票) 文件 发票主表及状态信息 表
        in_df (pd.DataFrame): 入账文件 中 2025.12 表
    """
    buy_df = preprocess_account(state_df)
    
    in_df_notna = in_df.loc[in_df['中台编号'].notna()].copy()
    
    # 步骤1：将列转换为object类型避免类型冲突
    in_df_notna = in_df_notna.astype({'中台编号': 'object'})
    
    # 步骤2：对数值类型进行转换
    # 使用mask选择数值类型的值
    numeric_mask = pd.to_numeric(in_df_notna['中台编号'], errors='coerce').notna()
    
    # 对数值类型的值进行转换
    if numeric_mask.any():
        # 提取数值部分
        numeric_values = pd.to_numeric(in_df_notna.loc[numeric_mask, '中台编号'], errors='coerce')
        # 取整并转换为字符串
        in_df_notna.loc[numeric_mask, '中台编号'] = numeric_values.astype('int64').astype('str')
        
    # 用中台编号进行inner join
    buy_df = buy_df.merge(in_df_notna, left_on='中台编号', right_on='中台编号', how='inner')

    # 合计税额和可抵扣税额相对比
    tax_wrong = buy_df['合计税额'] != buy_df['可抵扣税额']

    tax_indices = tax_wrong[tax_wrong].index

    in_df_copy = in_df_notna.copy(deep=True)
    in_df_copy.loc[tax_indices, '核验税额结果'] = '税额不一致'
    print('Neon提示您：共有{}个未配额的税额记录，在入账核算文件中核验税额结果列中标记为“税额不一致”'.format(len(tax_indices)))
    return in_df_copy
    

def unit_test():
    """单元测试"""
    state_df = pd.read_excel('入账核算场景/进项发票台账导出-全部(增值税发票) (1).XLSX', sheet_name='发票主表及状态信息')
    
    in_df = pd.read_excel('入账核算场景/入账.xls', sheet_name='2025.12')
    
    result_df = job_compare_tax(state_df, in_df)
    
    result_df.to_excel('入账核算场景/入账核算结果.xlsx', sheet_name='2025.12')
    
if __name__ == '__main__':
    unit_test()
    
    