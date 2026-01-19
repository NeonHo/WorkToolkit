import pandas as pd
import re

state_df = pd.read_excel('入账核算场景/进项发票台账导出-全部(增值税发票) (1).XLSX', sheet_name='发票主表及状态信息')
detail_df = pd.read_excel('入账核算场景/进项发票台账导出-全部(增值税发票) (1).XLSX', sheet_name='发票明细')

# '开票日期','发票号码','发票状态','合计金额','合计税额','价税合计','销售方名称','单据编号','单据摘要'
state_df = state_df[['开票日期','发票号码','发票状态','合计金额','合计税额','价税合计','销售方名称','单据编号','单据摘要']]

no_ser = state_df['单据编号']

state_df['采购类'] = no_ser.apply(lambda x: '采购类报账单' in str(x))

buy_df = state_df[state_df['采购类'] == True]

def extract_numbers(input_string):
    # 正则表达式模式，用于匹配10位连续的数字
    pattern = r'\d{1,}'
    # 查找所有匹配的模式
    matches = re.findall(pattern, input_string)
    return matches[0]

buy_df['中台编号'] = buy_df.apply(lambda x: extract_numbers(x['单据编号']), axis=1)

buy_df['采购订单'] = buy_df.apply(lambda x: extract_numbers(x['单据摘要']), axis=1)

buy_df.to_csv('excel_files/处理后采购类报账单.csv', index=False)
print('done')