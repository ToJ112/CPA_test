import pandas as pd


def num2str(num):
    if num < 9:
        return '00' + str(num+1)
    if num < 99:
        return '0' + str(num+1)
    else:
        return str(num+1)


def readfile(pathname, n=100):  # pathname为具体文件夹名，n为波形条数，默认100条
    filepath = './CPA测试数据/' + pathname

    plaintext_data = pd.read_csv(filepath + '/Plaintext.csv', header=None)
    plaintext = plaintext_data[(plaintext_data.index + 2) % 4 == 0]
    plaintext = plaintext[0].str.split()
    pt_list = plaintext.values.tolist()
    #plaintext.to_csv('plaintext_raw.csv',index=False,header=False)


    trace = []
    for i in range(n):
        trace_data = pd.read_csv(filepath+'/Trace000'+num2str(i)+'.csv', header=None)
        trace.append(trace_data[1].values.tolist())

    return pt_list,trace


if __name__ == '__main__':
    readfile('相关能量分析_原始波_无滤波_100条_8500点')
