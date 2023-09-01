# 批量去重脚本
# IMU数据处理第一步，将导出的calc格式以csv格式读取，
# 然后取出采用的下半身传感器模式的七个IMU数据，最后保存去重后的数据文件
import pandas as pd
from fnmatch import fnmatch
import argparse
import os

# 1、创建解析器
parser=argparse.ArgumentParser()
# 2、添加参数
parser.add_argument("--path", type=str, help="data dictionary path")
# 3、解析参数
opt = parser.parse_args()

root = opt.path
filepath_list = []

for dirpath, dirnames, filenames in os.walk(root):

    for filepath in filenames:
        if fnmatch(filepath, '*.calc'):
            print(os.path.join(dirpath, filepath))

            data = pd.read_csv(os.path.join(dirpath, filepath),header=2,delim_whitespace=True)
            # 去除 contactL 和 contactR 列
            df = data.drop(labels = ['contactL', 'contactR'], axis=1)

            # 遍历第一行标签索引，设置通配符匹配去除位移，速度和四元数列
            for label in data.iloc[:0 ,:]:
                if fnmatch(label, '*-X-*') or fnmatch(label, '*-V-*') or fnmatch(label, '*-Q-*'):
                    df.drop(labels = label, axis=1, inplace=True)

            # 数据每六列为一个有效传感器数据（三轴加速度和角速度），查看是否有多于列没有去除
            # 若整除，表示没有多于列；若未整除，表示有多于列需进一步处理
            print(df.iloc[0: ,:].T.drop_duplicates(keep='first').shape[0] / 6)

            # 因为已经指导下半身七个传感器模式，去除重复值后取出的列号为1-7
            if (df.iloc[0: ,:].T.drop_duplicates(keep='first').shape[0] / 6) !=0:
                for j in df.columns:
                    # 取出编号，例如 01-A-x, 即01
                    if int(j.partition('-')[0]) >7:
                        df.drop(j, axis = 1, inplace=True) 
                if df.iloc[0: ,:].T.drop_duplicates(keep='first').shape[0]//6 !=7:
                    filepath_list.append(os.path.join(dirpath, filepath))
                # print("after clear:{}".format(df.iloc[0: ,:].T.drop_duplicates(keep='first').shape[0] / 6))

            # 转置去重，再转置回，保存csv文件，不要索引
            df.iloc[0: ,:].T.drop_duplicates().T.to_csv(root+'/'+filepath.replace('Char00.calc', '')+'.csv', index=False)

print('\n')
print("filepath_list length: {}".format(len(filepath_list)))
print("filepath_list:\n")
print(filepath_list)
print('\n')
print("Preprocessing finished.")