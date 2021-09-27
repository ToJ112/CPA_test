import pandas as pd


def num2str(num):
    if num < 10:
        return '00' + str(num)
    if num < 100:
        return '0' + str(num)
    else:
        return str(num)


def readfile(pathname, n=100):  # pathname为具体文件夹名，n为波形条数，默认100条
    filepath = './CPA测试数据/' + pathname
    plaintext = []

    plaintext_data = pd.read_csv(filepath + '/Plaintext.csv', header=None)
    plaintext = plaintext_data[(plaintext_data.index + 2) % 4 == 0]
    pt_list = plaintext.values.tolist()
    plaintext.to_csv('plaintext_raw.csv',index=False,header=False)

if __name__ == '__main__':
    readfile('相关能量分析_原始波_无滤波_100条_8500点')
