# 引入模块
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse

# 1、创建解析器
parser=argparse.ArgumentParser()
# 2、添加参数
parser.add_argument("--file_name", type=str, help="excel file name have .xlsx")
# 3、解析参数
opt = parser.parse_args()
# 原数据所在文件夹的路径
# raw_dir_path = r'D:\MotionFile\data\raw'
raw_dir_path = 'D:/vscode_workspace/signal_process/data/raw'
# 第一次过滤后数据保存的文件夹路径
# filter1_dir_path = r'D:\MotionFile\data\filter1'
filter1_dir_path = 'D:\\vscode_workspace\\signal_process\\data\\filter1'
# 第二次过滤后数据保存的文件夹路径
# filter2_dir_path = r'D:\MotionFile\data\filter2'
filter2_dir_path = 'D:\\vscode_workspace\\signal_process\\data\\filter2'
# 最后生成的图片保存的文件夹路径
# image_dir_path = r'D:\MotionFile\data\image'
image_dir_path = 'D:\\vscode_workspace\\signal_process\\data\\image'
# 原数据excel文件名称 4、调用参数
# raw_excel_name = 'test_label_01_1Char00_total.xlsx'
raw_excel_name = opt.file_name
# 第一次过滤后保存的excel文件名称
filter1_excel_name = raw_excel_name[0:-5] + '_filter1.xlsx'
# 第二次过滤后保存的excel文件名称
filter2_excel_name = raw_excel_name[0:-5] + '_filter2.xlsx'
# file = r'D:\MotionFile\Test\test_label_01_1Char00.csv'    '前面的r是对斜杠/进行转义
# data = pd.read_csv(file)
# print(data)
raw_file_path = raw_dir_path + '/' + raw_excel_name
data = pd.read_excel(raw_file_path)
# print(data.head(5))
# print(data.dtypes)# 查看列的数据类型
# print(data.index)# 查看行名
# print(data.columns)# 查看列名
# print(data.info())

#使用pandas的rename方法修改列名，新旧列名称按照字典形式成对，columns={'旧的列名': '新的列名'}
#a.rename(columns={'第一列':'td_a', '第二列':'td_b'}, inplace = True)它默认的不是原地修改，需要原地修改就得设置inplace参数
# 第一次过滤，从原表格中获取有用的列
data_filter1 = pd.DataFrame()
col_str_flt = ["-A-x", "-A-y", "-A-z", "-W-x", "-W-y", "-W-z"]
for i in range(1, 60):
    if i>=1 and i<=9:
        for j in col_str_flt:
            data_filter1["0"+str(i)+j] = data["0"+str(i)+j]
    else:
        for j in col_str_flt:
            data_filter1[str(i)+j] = data[str(i)+j]
# 将表格中列的类型为int64的列转换为float64
for col_name in data_filter1.columns:
    data_filter1[col_name] = data_filter1[col_name].astype("float")
# print(data_filter1.dtypes)# 查看列的数据类型
# print(data_filter1.info())# 6*59=354
# 保存过滤后的表格
# creating excel writer object
writer_filter1 = pd.ExcelWriter(filter1_dir_path + '\\' + filter1_excel_name)
# write dataframe to excel
data_filter1.to_excel(writer_filter1, index=False)
# save the excel
writer_filter1.save()
print("data_filter1 is exported successfully to " + filter1_dir_path + '\\' + filter1_excel_name)

# 获得表格中的重复列（以含有'-A-x'列为例）
def getDuplicateColumns_A_x(df):
    # 创建空集合 用来存放重复列名
    duplicateColumnNames = set()
    # 创建空字典，用来存放列和它对应的重复列列表
    dict_duplicateColumn = {}
    bol = True
    # 遍历表格的每一列
    for x in range(0, df.shape[1], 6):
        col = df.iloc[:, x] # 取出x列的所有数据
        # 这里的判断是为了不将已经确认有重复的列再遍历判断一次
        if(len(dict_duplicateColumn) != 0):
            for w in list(dict_duplicateColumn.keys()):
                if(bol == False):
                    break
                for v in dict_duplicateColumn.get(w):
                    if v == df.columns.values[x]:
                        bol = False
                        break
        if(bol == False):
            bol = True
            continue
        # 遍历表格x列后面的每一列
        for y in range(x+6, df.shape[1], 6):
            otherCol = df.iloc[:, y]
            if col.equals(otherCol):
                duplicateColumnNames.add(df.columns.values[y])
        dict_duplicateColumn[df.columns.values[x]] = list(duplicateColumnNames)
        duplicateColumnNames = set()
    return dict_duplicateColumn
dict_column_duplicate_A_x = getDuplicateColumns_A_x(data_filter1)
for k, v in dict_column_duplicate_A_x.items():
    print(k, v)
    print("/n")

# 获得表格中的重复列（这次以全部列）
def getDuplicateColumns(df):
    # 创建空集合 用来存放重复列名
    duplicateColumnNames = set()
    # 创建空字典，用来存放列和它对应的重复列列表
    dict_duplicateColumn = {}
    bol = True
    # 遍历表格的每一列
    for r in range(0, 6):
        for x in range(r, df.shape[1], 6):
            col = df.iloc[:, x] # 取出x列的所有数据
            # 这里的判断是为了不将已经确认有重复的列再遍历判断一次
            if(len(dict_duplicateColumn) != 0):
                for w in list(dict_duplicateColumn.keys()):
                    if(bol == False):
                        break
                    for v in dict_duplicateColumn.get(w):
                        if v == df.columns.values[x]:
                            bol = False
                            break
            if(bol == False):
                bol = True
                continue
            # 遍历表格x列后面的每一列
            for y in range(x+6, df.shape[1], 6):
                otherCol = df.iloc[:, y]
                if col.equals(otherCol):
                    duplicateColumnNames.add(df.columns.values[y])
            dict_duplicateColumn[df.columns.values[x]] = list(duplicateColumnNames)
            duplicateColumnNames = set()
    return dict_duplicateColumn
dict_column_duplicate = getDuplicateColumns(data_filter1)
# for k, v in dict_column_duplicate.items():
#     print(k, v)
#     print("==============================================================================")

# print(dict_column_duplicate.keys())
list_dict_column_duplicate = sorted(list(dict_column_duplicate.keys()))
# print("==============================================================================")
# print(list_dict_column_duplicate)

# 第二次过滤，在第一次过滤获得的表格的基础上去掉重复的列
data_filter2 = pd.DataFrame()
for d in list_dict_column_duplicate:
    data_filter2[d] = data_filter1[d]
# 保存第二次过滤得到的列
# print(data_filter2.dtypes)# 查看列的数据类型
# print(data_filter2.info())# 4*6=24
# 保存过滤后的表格
# creating excel writer object
writer_filter2 = pd.ExcelWriter(filter2_dir_path + '\\' + filter2_excel_name)
# write dataframe to excel
data_filter2.to_excel(writer_filter2, index=False)
# save the excel
writer_filter2.save()
print("data_filter2 is exported successfully to " + filter2_dir_path + '\\' + filter2_excel_name)

def mkdir(path):
    # 去除首位空格
    # path=path.strip()
    # 去除尾部 \ 符号
    # path=path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path) 
        print(path+' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path+' 目录已存在')
        return False

# 绘制第二次过滤后的表格的各列波形图并保存到本地
first_id = 0
while(first_id < data_filter2.shape[1]):
    fig, (Ax, Ay, Az, Wx, Wy, Wz) = plt.subplots(6, 1, figsize = (16, 64), sharex = True)
    Ax.plot(list(data_filter2.index), data_filter2[data_filter2.columns.values[first_id]], color='red', alpha=0.5)
    Ax.set_ylim(-10, 10) # 设置y轴的刻度范围
    Ax.set_title(data_filter2.columns.values[first_id])
    Ax.grid()

    Ay.plot(list(data_filter2.index), data_filter2[data_filter2.columns.values[first_id+1]], color='green', alpha=0.5)
    Ay.set_ylim(-10, 10) # 设置y轴的刻度范围
    Ay.set_title(data_filter2.columns.values[first_id+1])
    Ay.grid()

    Az.plot(list(data_filter2.index), data_filter2[data_filter2.columns.values[first_id+2]], color='blue', alpha=0.5)
    Az.set_ylim(-10, 10) # 设置y轴的刻度范围
    Az.set_title(data_filter2.columns.values[first_id+2])
    Az.grid()

    Wx.plot(list(data_filter2.index), data_filter2[data_filter2.columns.values[first_id+3]], color='red', alpha=0.5)
    Wx.set_ylim(-10, 10) # 设置y轴的刻度范围
    Wx.set_title(data_filter2.columns.values[first_id+3])
    Wx.grid()

    Wy.plot(list(data_filter2.index), data_filter2[data_filter2.columns.values[first_id+4]], color='green', alpha=0.5)
    Wy.set_ylim(-10, 10) # 设置y轴的刻度范围
    Wy.set_title(data_filter2.columns.values[first_id+4])
    Wy.grid()

    Wz.plot(list(data_filter2.index), data_filter2[data_filter2.columns.values[first_id+5]], color='blue', alpha=0.5)
    Wz.set_ylim(-10, 10) # 设置y轴的刻度范围
    Wz.set_title(data_filter2.columns.values[first_id+5])
    Wz.grid()
    # 定义要创建的目录
    mkpath = image_dir_path + '\\' + raw_excel_name
    isExists=os.path.exists(mkpath)
    if not isExists:
    	# 调用函数
        mkdir(mkpath)
    fig.savefig(mkpath + '\\' +  'id_' + data_filter2.columns.values[first_id][0:2] + '.png')
    first_id = first_id + 6
print("image is exported successfully to " + mkpath + '\\')