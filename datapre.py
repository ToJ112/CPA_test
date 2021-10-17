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


def max_traces(traces, ipc, N=100):
    trace_max_list = np.argsort(traces, axis=1)[:, -ipc:]
    trace_maxs = np.sort(trace_max_list, axis=1)
    return np.vstack([traces[i, tuple(trace_maxs[i])] for i in range(traces.shape[0])])


def original_consolidation(traces, slices):
    for i in range(slices):
        np
if __name__ == '__main__':
    pt_list, trace = readfile('相关能量分析_原始波_无滤波_100条_8500点')

    # np.savetxt("trace_max_list.csv",max_traces(trace, 160), delimiter=',', fmt="%.4f")
