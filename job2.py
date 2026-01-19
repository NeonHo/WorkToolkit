import pandas as pd

buy_df = pd.read_csv('excel_files/处理后采购类报账单.csv')

in_df = pd.read_excel('入账核算场景/入账.xls', sheet_name='2025.12')

# 用中台编号进行inner join
buy_df = buy_df.merge(in_df, left_on='中台编号', right_on='中台编号', how='inner')

# 合计税额和可抵扣税额相对比
tax_wrong = buy_df['合计税额'] != buy_df['可抵扣税额']

tax_indices = tax_wrong[tax_wrong].index

in_df.loc[tax_indices, '警告'] = '税额不一致'

# 保存结果
in_df.to_excel('入账核算场景/入账.xlsx', sheet_name='2025.12_检查', index=False)

print('done')