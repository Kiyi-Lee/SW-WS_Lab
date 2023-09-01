# IMU批量打标签、连接为指定训练格式脚本

# 引入模块
import re
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import glob
from fnmatch import fnmatch, fnmatchcase
#plt.rcParams.update({'figure.max_open_warning': 0})
plt.rcParams["figure.dpi"] = 400 # 设置分辨率
# 配置参数中的字体（font）为黑体（SimHei）
plt.rcParams['font.sans-serif']=['SimHei']
# 配置参数总的轴（axes）正常显示正负号（minus）
plt.rcParams['axes.unicode_minus']=False

# 1、创建解析器
parser=argparse.ArgumentParser()
# 2、添加参数
parser.add_argument("--path", type=str, help="data dictionary path")
# 3、解析参数
opt = parser.parse_args()

root = opt.path

path_list = []
dirpath_list = []
filepath_list = []

activity_list = {
    "弓步": "1",
    "侧踢": "2"
    # "慢走": "walk", "中走": "walk", "快走": "walk",
    # "慢上楼梯": "up stairs", "中上楼梯": "up stairs", "快上楼梯": "up stairs",
    # "慢下楼梯": "down stairs", "中下楼梯": "down stairs", "快下楼梯": "down stairs",
    # "慢坐椅子": "sit down", "中坐椅子": "sit down", "快坐椅子": "sit down",
    # "SQUAT": "squat"
}

level_list = {
    "低": "L1",
    "中": "L2",
    "高": "L3"
    # "慢走": "walk", "中走": "walk", "快走": "walk",
    # "慢上楼梯": "up stairs", "中上楼梯": "up stairs", "快上楼梯": "up stairs",
    # "慢下楼梯": "down stairs", "中下楼梯": "down stairs", "快下楼梯": "down stairs",
    # "慢坐椅子": "sit down", "中坐椅子": "sit down", "快坐椅子": "sit down",
    # "SQUAT": "squat"
}

flag = False

for dirpath, dirnames, filenames in os.walk(root):

    for filepath in filenames:
        if fnmatch(filepath, '*.csv'):
            print(os.path.join(dirpath, filepath))

            df = pd.read_csv(os.path.join(dirpath, filepath),header=0)

            # 遍历第一行标签索引，设置通配符匹配去除陀螺仪和type列
            for label in df.iloc[:0 ,:]:
                if fnmatch(label, 'type'):
                    df.drop(labels=label, axis=1, inplace=True)

            id = ''
            for i in filepath.partition('-')[0]:
                if(i not in "'"):
                    id = id + i
            print(id)

            # example
            # filepath： 01-快上楼梯-1.xlsx
            # os.path.join(dirpath, filepath)： D:\vscode_workspace\PracticeLab\IMU\test_data_dic\01-快上楼梯-1.xlsx
            # ↓↓↓ filepath.partition('-'), filepath.partition('-')[2], filepath.partition('-')[2].partition('-')[0]
            # 0:('01', '-', '快上楼梯-1.xlsx'), 1:快上楼梯-1.xlsx, 2:快上楼梯

            df.insert(loc=df.shape[1], column='user', value=id)
            df.insert(loc=df.shape[1], column='activity', value=activity_list[filepath.partition('-')[2].partition('-')[0]])
            df.insert(loc=df.shape[1], column='level', value=level_list[filepath.partition('-')[2].partition('-')[2].partition('-')[0]])
            df.insert(loc=df.shape[1], column='number', value=filepath.partition('-')[2].partition('-')[2].partition('-')[2].replace('.csv',''))

            print("df.shape:{0:>6}".format(str(df.shape)))

            if flag:
                for i in range(0,6):
                    # d1-d3: A-x,y,z , d4-d6: W-x,y,z ,  d7: userId , d8: activity
                    # 新增：d9: level , d10: number(某组锻炼第几次索引)
                    d1_new = np.append(d1_new,df.iloc[:,3*i:3*i+1].to_numpy())
                    d2_new = np.append(d2_new,df.iloc[:,3*i+1:3*i+2].to_numpy())
                    d3_new = np.append(d3_new,df.iloc[:,3*i+2:3*i+3].to_numpy())
                    d4_new = np.append(d4_new,df.iloc[:,3*i+3:3*i+4].to_numpy())
                    d5_new = np.append(d5_new,df.iloc[:,3*i+4:3*i+5].to_numpy())
                    d6_new = np.append(d6_new,df.iloc[:,3*i+5:3*i+6].to_numpy())

                    d7_new = np.append(d7_new,df.iloc[:,df.shape[1]-4:df.shape[1]-3].to_numpy())
                    d8_new = np.append(d8_new,df.iloc[:,df.shape[1]-3:df.shape[1]-2].to_numpy())
                    d9_new = np.append(d9_new,df.iloc[:,df.shape[1]-2:df.shape[1]-1].to_numpy())
                    d10_new = np.append(d10_new,df.iloc[:,df.shape[1]-1:df.shape[1]].to_numpy())


                print("After append,  d1.shape:{0:<4}d2.shape:{1:<4}d3.shape{2:<4}d4.shape:{3:<4}d5.shape:{4:<4}d6.shape{5:<4}"
                ,d1_new.shape,d2_new.shape,d3_new.shape,d4_new.shape,d5_new.shape,d6_new.shape)
            else:
                d1 = df.iloc[:,:1].to_numpy()
                d2 = df.iloc[:,1:2].to_numpy()
                d3 = df.iloc[:,2:3].to_numpy()
                d4 = df.iloc[:,3:4].to_numpy()
                d5 = df.iloc[:,4:5].to_numpy()
                d6 = df.iloc[:,5:6].to_numpy()

                d7 = df.iloc[:,df.shape[1]-4:df.shape[1]-3].to_numpy()
                d8 = df.iloc[:,df.shape[1]-3:df.shape[1]-2].to_numpy()
                d9 = df.iloc[:,df.shape[1]-2:df.shape[1]-1].to_numpy()
                d10 = df.iloc[:,df.shape[1]-1:df.shape[1]].to_numpy()

                for i in range(1,6):
                    d1 = np.append(d1,df.iloc[:,3*i:3*i+1].to_numpy())
                    d2 = np.append(d2,df.iloc[:,3*i+1:3*i+2].to_numpy())
                    d3 = np.append(d3,df.iloc[:,3*i+2:3*i+3].to_numpy())
                    d4 = np.append(d4,df.iloc[:,3*i+3:3*i+4].to_numpy())
                    d5 = np.append(d5,df.iloc[:,3*i+4:3*i+5].to_numpy())
                    d6 = np.append(d6,df.iloc[:,3*i+5:3*i+6].to_numpy())
                    d7 = np.append(d7,df.iloc[:,df.shape[1]-4:df.shape[1]-3].to_numpy())
                    d8 = np.append(d8,df.iloc[:,df.shape[1]-3:df.shape[1]-2].to_numpy())
                    d9 = np.append(d9,df.iloc[:,df.shape[1]-2:df.shape[1]-1].to_numpy())
                    d10 = np.append(d10,df.iloc[:,df.shape[1]-1:df.shape[1]].to_numpy())

                d1_new = d1
                d2_new = d2
                d3_new = d3
                d4_new = d4
                d5_new = d5
                d6_new = d6
                d7_new = d7
                d8_new = d8
                d9_new = d9
                d10_new = d10

                flag = True

                print("After append,  d1.shape:{0:<4}d2.shape:{1:<4}d3.shape{2:<4}d4.shape:{3:<4}d5.shape:{4:<4}d6.shape{5:<4}"
                ,d1.shape,d2.shape,d3.shape,d4.shape,d5.shape,d6.shape)

d_new = np.append(d1_new, d2_new)
d_new = np.append(d_new, d3_new)
d_new = np.append(d_new, d4_new)
d_new = np.append(d_new, d5_new)
d_new = np.append(d_new, d6_new)
d_new = np.append(d_new, d7_new)
d_new = np.append(d_new, d8_new)
d_new = np.append(d_new, d9_new)
d_new = np.append(d_new, d10_new)

print(d_new.shape[0])
print('\n')

d_new = pd.DataFrame(d_new.reshape((d_new.shape[0]//10), 10, order='F'), columns=['A-x', 'A-y', 'A-z', 'W-x', 'W-y', 'W-z', 'user', 'activity', 'level', 'number'])

# d_new.to_excel(r'D:\vscode_workspace\PracticeLab\IMU' + '_concat.xlsx', index=False) # ValueError: sheet is too large
d_new.to_csv(root + '\IMU' + '_concat.txt', index=False, sep='\t')
