import pandas as pd

target_df = pd.read_excel('excel_files/附件1：信创终端概况表-地市公司.xlsx', sheet_name='大同')

source_df = pd.read_excel('excel_files/信通联系方式.xls', sheet_name='Sheet1')

target_slice = target_df.loc[target_df.loc[:, '使用人姓名'].notna()]

source_df.loc[:, '手机'] = source_df.手机.astype(str)

merged_df = pd.merge(target_slice, source_df, left_on='使用人姓名', right_on='姓名', how='left')


merged_df.to_excel('excel_files/信创终端概况表-地市公司-联系方式.xlsx', index=False)
print('done')