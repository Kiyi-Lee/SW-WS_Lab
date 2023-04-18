# IMU批量截取静止数据脚本，采用寻峰算法

# 引入模块
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import glob
from scipy.signal import find_peaks
from matplotlib.ticker import MultipleLocator,AutoMinorLocator
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

# 各种路径
# 原始excel文件目录路径
# raw_dir_path = r"D:\vscode_workspace\PracticeLab\IMU\filter_data"
raw_dir_path = root
# 保存对应excel文件生成的峰值图路径，每张图中包含传感器各轴峰值图
# raw_peak_image_path = r'D:\vscode_workspace\PracticeLab\IMU\img_peak'
raw_peak_image_path = root + r'\IMU\img_peak'
# 保存过滤后excel文件生成的图像路径，每张图中包含传感器各轴图
# split_image_path = r'D:\vscode_workspace\PracticeLab\IMU\filter_img'
split_image_path = root + r'\IMU\filter_img'
# 保存过滤后excel文件的目录路径
# split_excel_dir = r'D:\vscode_workspace\PracticeLab\IMU\filter_excel'
split_excel_dir = root + r'\IMU\filter_excel'

# 获取目录下以.xlsx结尾的所有文件的绝对路径
raw_excel_list = glob.glob(os.path.join(raw_dir_path, "*.csv"))
print("raw_excel_list:{}".format(raw_excel_list))
# 获取目录下所有文件的名称列表
# ！！！！！！注意源文件放一个单独目录下，且目录下不要有其它的文件夹，否则会把其它子目录保存
excel_name_list = os.listdir(raw_dir_path)
print("excel_name_list:{}".format(excel_name_list))


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


# excel_name_list 列表的索引
name_index = 0 

# 遍历文件夹下的所有excel文件
for i in raw_excel_list:
    # 读取excel文件
    data = pd.read_csv(i)
    # 遍历excel文件的列名列表，过滤掉列名含有01和23的列
    for j in data.columns:
        if(('23' in j) or ('type' in j)):
            data.drop(j, axis = 1, inplace=True) 
    
    # 创建一个空的DataFrame对象，用来存储过滤后的每列数据
    split_data = pd.DataFrame()
    is_peak = 0 # 表示只计算第一列的peak_low和peak_high

    # 寻找每列数据的峰值，先绘制每列的峰值图并保存，再去掉第一个峰值前小于一定范围值的数据，去掉最后一个峰值出现后小于一定范围值的数据
    # 只绘制第一列的峰值图，根据第一列峰值图，进行数据截取即可
    # for x in data.columns:
    x = '02-W-y'
    col = data.loc[:, x] # 读取x列的数据
    col_inverse = col * -1 # 将原始列进行倒置，正的变成负的，负的变成正的
    print("Inverse finsh......")
    # print(i + " " + x + " col_inverse_max：", col_inverse.max())
    # print(i + " " + x + " col_max：", col.max())
    # print(i + " " + x + " col_inverse_max_mean_mid_2：", (col_inverse.max() + col_inverse.mean(axis=0)) / 2)
    # print(i + " " + x + " col_max_mean_mid_2：", (col.max() + col.mean(axis=0)) / 2)
    # print(i + " " + x + " col_inverse_max_mean_mid_4：", (col_inverse.max() + col_inverse.mean(axis=0)) / 4)
    # print(i + " " + x + " col_max_mean_mid_4：", (col.max() + col.mean(axis=0)) / 4)
    # 注意！！！不知道为什么find_peaks的参数height范围不能同时为负数，可以一负一正，两正，因为小于0的话find_peak就不认为是波峰了，
    # 要想寻找到波谷就得将原始数据*（-1）再用这个函数寻找新的波峰（也就是原来数据的波谷）
    # if(is_peak == 0):
    peaks_low, _ = find_peaks(col_inverse, height = (col_inverse.max() * 0.25, col_inverse.max()), distance=96, prominence=1) 
    # 寻波谷 peaks_low：col中满足所有给定条件的峰的索引，height：所需的峰高范围，
    # distance：相邻峰之间的样本中所需的最小水平距离（x>=1）48 = 96 / 2为采样率的一半, 即0.5s间距
    peaks_high, _ = find_peaks(col, height = (col.max() * 0.25, col.max()), distance=96, prominence=1) 
    # 寻波峰 peaks
    # peaks_high_record = peaks_high
    # peaks_low_record = peaks_low
    # else:
    # peaks_high = peaks_high_record
    # peaks_low = peaks_low_record
    # print(i + " " + x + " peaks_high：", peaks_high)
    # print(i + " " + x + " peaks_low：", peaks_low)
    fig, (time, sample) = plt.subplots(2, 1, figsize = (32, 16))
    # 调整子图纵向间隔
    plt.subplots_adjust(hspace=0.5)
    # 绘制x轴为时间刻度峰值图
    time.plot(np.arange(col.shape[0]) / 96, col, color = 'black')
    #time.plot(-15, "--", color = "green")
    #time.plot(15, "--", color = "green")
    #time.plot(peaks_high, col.iloc[peaks_high], "X", color = "red")
    #time.plot(peaks_low, col.iloc[peaks_low], "X", color = "blue")
    time.set_xlim(0, col.shape[0] / 96) # 设置x轴的刻度范围
    time.set_ylim((col.min()-1), (col.max()+1)) # 设置y轴的刻度范围
    time.set_xlabel("time")
    if('A' in x):
        time.set_ylabel("acceleration")
    elif('W' in x):
        time.set_ylabel("Angular velocity")
    time.set_title(x)
    # 显示副刻度线
    #time.minorticks_on()
    # 设置主、副刻度线参数
    #time.xaxis.set_major_locator(MultipleLocator(1.0))
    #time.xaxis.set_minor_locator(AutoMinorLocator(4)) # 将每一份主刻度线等分成4份
    time.grid()
    
    # 绘制x轴为样本刻度峰值图
    sample.plot(list(col.index), col, color = 'black')
    sample.plot(-col_inverse.max(), "--", color = "green")
    sample.plot(-((col_inverse.max() + col_inverse.mean(axis=0)) / 2), "--", color = "green")
    sample.plot(col.max(), ":", color = "green")
    sample.plot((col.max() + col.mean(axis=0)) / 2, ":", color = "green")
    sample.plot(peaks_high, col.iloc[peaks_high], "X", color = "red")
    sample.plot(peaks_low, col.iloc[peaks_low], "X", color = "blue")
    sample.set_xlim(0, col.shape[0])
    sample.set_ylim((col.min()-1), (col.max()+1)) # 设置y轴的刻度范围
    sample.set_xlabel("sample")
    if('A' in x):
        sample.set_ylabel("acceleration")
    elif('W' in x):
        sample.set_ylabel("Angular velocity")
    sample.set_title(x)
    # 显示副刻度线
    # sample.minorticks_on()
    # 设置主、副刻度线参数
    # sample.xaxis.set_major_locator(MultipleLocator(1.0))
    # sample.xaxis.set_minor_locator(AutoMinorLocator(4)) # 将每一份主刻度线等分成4份
    sample.grid()
    
    # 定义要创建的目录
    mkpath = raw_peak_image_path + '\\' + excel_name_list[name_index].replace('.csv', '')
    mkdir(mkpath)
    fig.savefig(mkpath + '\\' + x + '_peak.png')
    plt.close(fig)
    
    print(i + " " + x + " col_first_high_peak_4：", col.iloc[peaks_high[0]] / 4)
    print(i + " " + x + " col_first_low_peak_4：", col.iloc[peaks_low[0]] / 4)
    print(i + " " + x + " col_last_high_peak_4：", col.iloc[peaks_high[-1]] / 4)
    print(i + " " + x + " col_last_low_peak_4：", col.iloc[peaks_low[-1]] / 4)
    print(i + " " + x + " col_first_high_peak_8：", col.iloc[peaks_high[0]] / 2)
    print(i + " " + x + " col_first_low_peak_8：", col.iloc[peaks_low[0]] / 2)
    print(i + " " + x + " col_last_high_peak_8：", col.iloc[peaks_high[-1]] / 2)
    print(i + " " + x + " col_last_low_peak_8：", col.iloc[peaks_low[-1]] / 2)
    
    # 用来记录要过滤掉的数据的索引
    split_index_list = []

    # 再去掉第一个峰值前小于一定范围值的数据，去掉最后一个峰值出现后小于一定范围值的数据
    '''if(peaks_high[0] <= peaks_low[0]):
        # 如果第一个峰是波峰，以第一个波峰的索引为截止点
        for a in range(0, peaks_high[0]):
            # 在第一个波峰前面的点中，凡是小于第一个波峰4分之一大小的点就删掉
            if(col.iloc[a] < col.iloc[peaks_high[0]] / 2):
                split_index_list.append(a)
    elif(peaks_high[0] > peaks_low[0]):
        # 如果第一个峰是波谷，以第一个波谷的索引为截止点
        for a in range(0, peaks_low[0]):
            # 在第一个波谷前面的点中，凡是大于第一个波谷4分之一大小的点就删掉
            if(col.iloc[a] > col.iloc[peaks_low[0]] / 2):
                split_index_list.append(a)
    if(peaks_high[-1] >= peaks_low[-1]):
        # 如果最后一个峰是波峰，以最后一个波峰的索引为起始点
        for b in range(peaks_high[-1], col.shape[0]):
            # 在最后一个波峰后面的点中，凡是小于最后一个波峰4分之一大小的点就删掉
            if(col.iloc[b] < col.iloc[peaks_high[-1]] / 2):
                split_index_list.append(b)
    elif(peaks_high[-1] < peaks_low[-1]):
        # 如果最后一个峰是波谷，以最后一个波谷的索引为起始点
        for b in range(peaks_low[-1], col.shape[0]):
            # 在最后一个波谷后面的点中，凡是大于最后一个波谷4分之一大小的点就删掉
            if(col.iloc[b] < col.iloc[peaks_low[-1]] / 2):
                split_index_list.append(b)'''
    
    # peaks_high 包含波峰样本点的索引
    # 直接删掉第一个波峰或波谷前面的所有点；直接删掉最后一个波峰或波谷后面的所有点
    # 如果第一个为波峰，则最后也删波峰，若删波谷会造成周期不对应
    if(peaks_high[0] <= peaks_low[0]):
        # 如果第一个峰是波峰，以第一个波峰的索引为截止点
        split_index_list.append(peaks_high[0])
        split_index_list.append(peaks_high[-1])
    else:
        split_index_list.append(peaks_low[0])
        split_index_list.append(peaks_low[-1])

    # if(peaks_high[-1] <= peaks_low[-1]):
    #     # 如果最后一个峰是波峰，以最后一个波峰的索引为起始点
    #     split_index_list.append(peaks_high[-1])
    # else:
    #     split_index_list.append(peaks_low[-1])

    print("peaks_high:{}\n".format(peaks_high))
    print("peaks_low:{}\n".format(peaks_low))
    print("type of split_index_list:{}\n".format(type(split_index_list)))

    print("split_index_list:{}\n".format(split_index_list))
    
    # col.drop(split_index_list, axis=0, inplace=True)
    # 保存过滤后的新列到新dataframe
    #split_data = pd.concat([split_data, pd.DataFrame(col)], axis=1) # 按列拼接
    # split_data[x] = col
    # 绘制下过滤后的数据
    fig_split, (time_split, sample_split) = plt.subplots(2, 1, figsize = (32, 16))
    # 调整子图纵向间隔
    plt.subplots_adjust(hspace=0.5)

    print("type of col:{}\n".format(type(col)))
    # col类型为panda.Series,索引过多会报错 to many indexers， 要转换为dataframe

    cols = pd.DataFrame(col).iloc[split_index_list[0]:split_index_list[1],:]

    # 绘制x轴为时间刻度峰值图
    time_split.plot(np.arange(cols.shape[0]) / 96, cols, color = 'black')
    #time_split.plot(-15, "--", color = "green")
    #time_split.plot(15, "--", color = "green")
    #time.plot(peaks, col.iloc[peaks], "X", color = "red")
    time_split.set_xlim(0, col.shape[0] / 96) # 设置x轴的刻度范围
    time_split.set_ylim((col.min()-1), (col.max()+1)) # 设置y轴的刻度范围
    time_split.set_xlabel("time")
    if('A' in x):
        time_split.set_ylabel("acceleration")
    elif('W' in x):
        time_split.set_ylabel("Angular velocity")
    time_split.set_title(x)
    # 显示副刻度线
    #time_split.minorticks_on()
    # 设置主、副刻度线参数
    #time_split.xaxis.set_major_locator(MultipleLocator(1.0))
    #time_split.xaxis.set_minor_locator(AutoMinorLocator(4)) # 将每一份主刻度线等分成4份
    time_split.grid()

    # 绘制x轴为样本刻度峰值图
    sample_split.plot(np.arange(cols.shape[0]), cols, color = 'black')
    #sample_split.plot(-15, "--", color = "green")
    #sample_split.plot(15, "--", color = "green")
    #sample_split.plot(peaks, col.iloc[peaks], "X", color = "red")
    sample_split.set_xlim(0, col.shape[0])
    sample_split.set_ylim((col.min()-1), (col.max()+1)) # 设置y轴的刻度范围
    sample_split.set_xlabel("sample")
    if('A' in x):
        sample_split.set_ylabel("acceleration")
    elif('W' in x):
        sample_split.set_ylabel("Angular velocity")
    sample_split.set_title(x)
    # 显示副刻度线
    #sample_split.minorticks_on()
    # 设置主、副刻度线参数
    #sample_split.xaxis.set_major_locator(MultipleLocator(1.0))
    #sample_split.xaxis.set_minor_locator(AutoMinorLocator(4)) # 将每一份主刻度线等分成4份
    sample_split.grid()
    
    # 定义要创建的目录
    mkpath_split = split_image_path + '\\' + excel_name_list[name_index].replace('.csv', '')
    mkdir(mkpath_split)
    fig_split.savefig(mkpath_split + '\\' + x + '.png')
    plt.close(fig_split)
    plt.cla() # 清除axes，即当前 figure 中的活动的axes，但其他axes保持不变。
    plt.clf() # 清除当前 figure 的所有axes，但是不关闭这个 window，所以能继续复用于其他的 plot。
    # is_peak += 1
    # 将过滤后的数据生成excel并保存到本地
    # creating excel writer object
    # writer_split = pd.ExcelWriter(split_excel_dir + '\\' + excel_name_list[name_index][0:-5] + '_split.xlsx')
    # # write dataframe to excel
    # split_data.to_excel(writer_split, index=False)
    # # save the excel
    # writer_split.save()
    # writer_split.close()
    print("split_index_list:{}".format(split_index_list))
    data = data.loc[split_index_list[0]:split_index_list[1]-1,:]
    # data.drop(index=range(split_index_list[0]), axis=1, inplace=True)
    # data.drop(index=range(split_index_list[1],data.shape[0]), axis=1, inplace=True)

    # 定义要创建的目录
    csv_split_path = split_excel_dir
    isExists=os.path.exists(csv_split_path)
    mkdir(csv_split_path)
    data.to_csv(csv_split_path + '\\' + excel_name_list[name_index].partition('-')[0]+ '_split.csv', index=False)

    print("image_peak is exported successfully to " + mkpath + '\\')
    print("image_split is exported successfully to " + mkpath_split + '\\')
    print("data_split is exported successfully to " + csv_split_path + '\\' + excel_name_list[name_index])
    name_index += 1