import matplotlib.pyplot as plt
import pandas as pd
from fnmatch import fnmatch, fnmatchcase
import argparse
import os
import re

# 1、创建解析器
parser=argparse.ArgumentParser()
# 2、添加参数
parser.add_argument("--path", type=str, help="data dictionary path")
# 3、解析参数
opt = parser.parse_args()

root = opt.path

for dirpath, dirnames, filenames in os.walk(root):

    for filepath in filenames:
        if fnmatch(filepath, '*.xlsx'):
            print(os.path.join(dirpath, filepath))

            data = pd.read_excel(os.path.join(dirpath, filepath),header=5)
            # data = pd.read_excel(os.path.join(dirpath, filepath),header=0) # 因为数据已删除bones那几行
            # 去除 contactL 和 contactR 列
            df = data.drop(labels = ['contactL', 'contactR'], axis=1)

            # 遍历第一行标签索引，设置通配符匹配去除位移，速度和四元数列
            for label in data.iloc[:0 ,:]:
                if fnmatch(label, '*-X-*') or fnmatch(label, '*-V-*') or fnmatch(label, '*-Q-*'):
                    df.drop(labels = label, axis=1, inplace=True)

            # 转置去重，再转置回，保存csv文件，不要索引
            df.iloc[0: ,:].T.drop_duplicates().T.to_csv('./filter_data'+filepath+'_test.csv', index=False)

            print('\n')
            # 数据每六列为一个有效传感器数据（三轴加速度和角速度），查看是否有多于列没有去除
            # 若整除，表示没有多于列；若未整除，表示有多于列需进一步处理
            print(df.iloc[0: ,:].T.drop_duplicates(keep='first').shape[0] / 6)
