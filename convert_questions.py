import pandas as pd

# Task
# source file: excel_files/3-2重点人员、一线人员--信息专业+规章制度+严重违章释义.xls
# format file: excel_files/kaoshibaoExcel20221101.xlsx


questions = pd.read_excel('excel_files/3-2重点人员、一线人员--信息专业+规章制度+严重违章释义.xls')

formats = pd.read_excel('excel_files/kaoshibaoExcel20221101.xlsx')

# columns ['序号', '一级纲要', '二级纲要', '题目分类', '题型', '题干', '选项', '答案', '题目依据', '试题分数', '试题编码', '备注', '说明', '判断题解析'] to 
# columns ['题干（必填）', '题型 （必填）', '选项 A', '选项 B', '选项 C', '选项 D', '选项E&#10;(勿删)', '选项F&#10;(勿删)', '选项G&#10;(勿删)', '选项H&#10;(勿删)', '正确答案&#10;（必填）', '解析&#10;（勿删）', '章节&#10;（勿删）', '难度']

col_dict = {
    '题干': '题干（必填）',
    '题型': '题型 （必填）',
    '说明': '解析&#10;（勿删）',
    '判断题解析': '解析&#10;（勿删）',
    '一级纲要': '章节&#10;（勿删）'
}

new_questions = pd.DataFrame()

# convert columns from questions to formats
new_questions['题干（必填）'] = questions['题干']
new_questions['题型 （必填）'] = questions['题型']
new_questions['正确答案&#10;（必填）'] = questions['答案']
new_questions['章节&#10;（勿删）'] = questions['一级纲要']

# 选项需要通过‘|’split 成 多个选项
new_questions['选项 A'] = questions['选项'].str.split('|').str[0]
new_questions['选项 B'] = questions['选项'].str.split('|').str[1]
new_questions['选项 C'] = questions['选项'].str.split('|').str[2]
new_questions['选项 D'] = questions['选项'].str.split('|').str[3]
new_questions['选项E&#10;(勿删)'] = ''
new_questions['选项F&#10;(勿删)'] = ''
new_questions['选项G&#10;(勿删)'] = ''
new_questions['选项H&#10;(勿删)'] = ''


print('done')