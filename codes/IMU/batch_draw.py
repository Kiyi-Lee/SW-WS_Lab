# IMU批量绘图脚本

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import MultipleLocator,AutoMinorLocator
from fnmatch import fnmatch, fnmatchcase
import argparse
import os

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

for dirpath, dirnames, filenames in os.walk(root):
    for filepath in filenames:
        if fnmatch(filepath, '*.csv'):
            path_list.append(os.path.join(dirpath, filepath).replace('\\','/'))
            dirpath_list.append(dirpath.replace('\\','/'))
            filepath_list.append(filepath.rstrip('.xlsx'))
            print(os.path.join(dirpath, filepath))

for j, path in enumerate(path_list):

    df = pd.read_csv(path,header=0)

    print(df.shape)

    plt.rcParams["figure.dpi"] = 400 # 设置分辨率
    # 配置参数中的字体（font）为黑体（SimHei）
    plt.rcParams['font.sans-serif']=['SimHei']
    # 配置参数总的轴（axes）正常显示正负号（minus）
    plt.rcParams['axes.unicode_minus']=False


    # 频率，96HZ
    f = 96
    # x轴长度
    length = df.shape[0]
    # 换算时间
    time = length / f
    # 构造x轴时间序列
    t = np.arange(length)/f

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

    index_list = range(df.shape[1]//6)

    # 遍历绘图
    for i in range(df.shape[1]//6):
        # plt.cla() # 清除axes，即当前 figure 中的活动的axes，但其他axes保持不变。
        # plt.clf() # 清除当前 figure 的所有axes，但是不关闭这个 window，所以能继续复用于其他的 plot。
        # plt.close() # 关闭 window，如果没有指定，则指当前 window。

        # 5行一列， sharex 共用x轴
        fig1, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, sharex=False, figsize=(16,32))
        fig2, (ax4, ax5) = plt.subplots(nrows=2, ncols=1, sharex=False, figsize=(16,32))

        mkpath = dirpath_list[0] + '/' + filepath_list[j].replace('.csv', '')
        isExists=os.path.exists(mkpath)
        if not isExists:
            # 调用函数
            mkdir(mkpath)


        # 调整子图纵向间隔
        plt.subplots_adjust(hspace=1)
        # grid 设置网格线性
        ax1.grid(True, which="major", linestyle="--", color="gray", linewidth=0.75)
        ax1.grid(True, which="minor", linestyle=":", color="lightgray", linewidth=0.75)
        ax2.grid(True, which="major", linestyle="--", color="gray", linewidth=0.75)
        ax2.grid(True, which="minor", linestyle=":", color="lightgray", linewidth=0.75)
        ax3.grid(True, which="major", linestyle="--", color="gray", linewidth=0.75)
        ax3.grid(True, which="minor", linestyle=":", color="lightgray", linewidth=0.75)
        ax4.grid(True, which="major", linestyle="--", color="gray", linewidth=0.75)
        ax4.grid(True, which="minor", linestyle=":", color="lightgray", linewidth=0.75)
        ax5.grid(True, which="major", linestyle="--", color="gray", linewidth=0.75)
        ax5.grid(True, which="minor", linestyle=":", color="lightgray", linewidth=0.75)

        # x轴加速度和角速度图
        ax1.plot(t, df.iloc[:,6*i:6*i+1], color='red', label=df.columns.values[6*i])
        ax1.plot(t, df.iloc[:,6*i+3:6*i+4], color='blue', label=df.columns.values[6*i+3])
        ax1.set_xlim(0, time) # 设置x轴的刻度范围
        ax1.set_ylim(-15, 15) # 设置y轴的刻度范围
        
        # y轴加速度和角速度图
        ax2.plot(t, df.iloc[:,6*i+1:6*i+2], color='red', label=df.columns.values[6*i+1])
        ax2.plot(t, df.iloc[:,6*i+4:6*i+5], color='blue', label=df.columns.values[6*i+4])
        ax2.set_xlim(0, time) # 设置x轴的刻度范围
        ax2.set_ylim(-15, 15) # 设置y轴的刻度范围

        # z轴加速度和角速度图
        ax3.plot(t, df.iloc[:,6*i+2:6*i+3], color='red', label=df.columns.values[6*i+2])
        ax3.plot(t, df.iloc[:,6*i+5:6*i+6], color='blue', label=df.columns.values[6*i+5])
        ax3.set_xlim(0, time) # 设置x轴的刻度范围
        ax3.set_ylim(-15, 15) # 设置y轴的刻度范围

        # 加速度xyz轴图
        ax4.plot(t, df.iloc[:,6*i:6*i+1], color='red', label=df.columns.values[6*i])
        ax4.plot(t, df.iloc[:,6*i+1:6*i+2], color='blue', label=df.columns.values[6*i+1])
        ax4.plot(t, df.iloc[:,6*i+2:6*i+3], color='green', label=df.columns.values[6*i+2])
        ax4.set_xlim(0, time) # 设置x轴的刻度范围
        ax4.set_ylim(-15, 15) # 设置y轴的刻度范围

        # 角速度xyz轴图
        ax5.plot(t, df.iloc[:,6*i+3:6*i+4], color='red', label=df.columns.values[6*i+3])
        ax5.plot(t, df.iloc[:,6*i+4:6*i+5], color='blue', label=df.columns.values[6*i+4])
        ax5.plot(t, df.iloc[:,6*i+5:6*i+6], color='green', label=df.columns.values[6*i+5])
        ax5.set_xlim(0, time) # 设置x轴的刻度范围
        ax5.set_ylim(-15, 15) # 设置y轴的刻度范围

        ax1.legend()
        ax1.set_title(filepath_list[j].replace('.csv', '') + ' X-axis')
        ax1.set_ylabel('加速度/角速度')
        # 显示副刻度线
        ax1.minorticks_on()
        # 设置主、副刻度线参数
        ax1.xaxis.set_major_locator(MultipleLocator(1.0))
        ax1.xaxis.set_minor_locator(AutoMinorLocator(4)) # 将每一份主刻度线等分成4份

        ax2.legend()
        ax2.set_title(filepath_list[j].replace('.csv', '') + ' Y-axis')
        ax2.set_ylabel('加速度/角速度')
        # 显示副刻度线
        ax2.minorticks_on()
        # 设置主、副刻度线参数
        ax2.xaxis.set_major_locator(MultipleLocator(1.0))
        ax2.xaxis.set_minor_locator(AutoMinorLocator(4)) # 将每一份主刻度线等分成4份

        ax3.legend()
        ax3.set_title(filepath_list[j].replace('.csv', '') + ' Z-axis')
        ax3.set_ylabel('加速度/角速度')
        # 显示副刻度线
        ax3.minorticks_on()
        # 设置主、副刻度线参数
        ax3.xaxis.set_major_locator(MultipleLocator(1.0))
        ax3.xaxis.set_minor_locator(AutoMinorLocator(4)) # 将每一份主刻度线等分成4份

        ax4.legend()
        ax4.set_title(filepath_list[j].replace('.csv', '') + ' A-xyz')
        ax4.set_ylabel('加速度')
        # 显示副刻度线
        ax4.minorticks_on()
        # 设置主、副刻度线参数
        ax4.xaxis.set_major_locator(MultipleLocator(1.0))
        ax4.xaxis.set_minor_locator(AutoMinorLocator(4)) # 将每一份主刻度线等分成4份

        ax5.legend()
        ax5.set_title(filepath_list[j].replace('.csv', '') + ' W-xyz')
        ax5.set_ylabel('角速度')
        # 显示副刻度线
        ax5.minorticks_on()
        # 设置主、副刻度线参数
        ax5.xaxis.set_major_locator(MultipleLocator(1.0))
        ax5.xaxis.set_minor_locator(AutoMinorLocator(4)) # 将每一份主刻度线等分成4份

        # plt.show() # 每张图挨个输出
        fig1.savefig(mkpath + '/' + filepath_list[j].replace('.csv', '') + '-A&W-' + str(index_list[i]+1) + '.png')
        fig2.savefig(mkpath + '/' + filepath_list[j].replace('.csv', '') + '-XYZ-' + str(index_list[i]+1) + '.png')

        # plt.cla() # 清除axes，即当前 figure 中的活动的axes，但其他axes保持不变。
        # plt.clf() # 清除当前 figure 的所有axes，但是不关闭这个 window，所以能继续复用于其他的 plot。
        plt.close(fig1) # 关闭 window，如果没有指定，则指当前 window。
        plt.close(fig2)

    # plt.show() # 最后一起输出

plt.cla() # 清除axes，即当前 figure 中的活动的axes，但其他axes保持不变。
plt.clf() # 清除当前 figure 的所有axes，但是不关闭这个 window，所以能继续复用于其他的 plot。
plt.close(fig1)
plt.close(fig2)

print(path_list)
print('output finish')
