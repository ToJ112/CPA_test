import numpy as np
import pandas as pd
import os


def num2str(num):
    if num < 9:
        return '00' + str(num + 1)
    if num < 99:
        return '0' + str(num + 1)
    else:
        return str(num + 1)


def readfile(pathname, N=100):  # pathname为具体文件夹名，n为波形条数，默认100条
    filepath = './CPA测试数据/' + pathname

    plaintext_data = pd.read_csv(filepath + '/Plaintext.csv', header=None)
    plaintext = plaintext_data[(plaintext_data.index + 2) % 4 == 0]
    plaintext = plaintext[0].str.split()
    pt_list = plaintext.values.tolist()

    trace_list = [pd.read_csv(filepath + '/Trace000' + num2str(i) + '.csv', header=None)[1].values.tolist() for i in
                  range(N)]
    trace = np.array(trace_list)
    return pt_list, trace


def max_traces(traces, ipc):
    '''
    最大值方法，健壮性差
    :param traces: 整合前的能量迹矩阵
    :param ipc: 估计的时钟周期（取出最大值的点数）
    :return: 返回处理后的能量迹
    '''
    trace_max_list = np.argsort(traces, axis=1)[:, -ipc:]
    trace_maxs = np.sort(trace_max_list, axis=1)
    return np.vstack([traces[i, tuple(trace_maxs[i])] for i in range(traces.shape[0])])

def square(l):
    return [i**2 for i in l]

def consolidation(traces, intervals, method):
    '''
    整合方法
    :param traces: 整合前的能量迹矩阵，slices为点数/intervals
    :param intervals: 需要将多少个点整合为一个点
    :param method: 选择的整合方法
    :return:返回整合后的能量迹
    '''
    slices = int(8500 / intervals)
    # traces_slice = []
    try:
        if method == 'original':
            traces_slice = np.array(np.hsplit(traces, slices)).sum(axis=-1).T
        elif method == 'abs':
            traces_slice = abs(np.array(np.hsplit(traces, slices))).sum(axis=-1).T
        elif method == 'pow':
            traces_slice = np.array(square(np.hsplit(traces, slices))).sum(axis=-1).T
        return traces_slice
    except Exception as e:
        print(e)



if __name__ == '__main__':
    pt_list, trace = readfile('相关能量分析_原始波_无滤波_100条_8500点')
    # original_consolidation(trace, 100, 100)
    # np.savetxt("trace_max_list.csv",max_traces(trace, 160), delimiter=',', fmt="%.4f")
    traces = np.arange(500).reshape(5, 100)
    intervals = 5
    slices = 10
    print(traces)
    print(np.array(np.hsplit(traces, slices)))
    print(np.array(np.hsplit(traces, slices)).sum(axis=-1).T)
    # traces_slice = np.array(np.hsplit(traces, slices)).sum(axis=1).T
