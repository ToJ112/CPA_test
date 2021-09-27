import pandas as pd

def readflie(pathname):
    filepath = './CPA测试数据/'
    plaintext = []
    plaintext_data = pd.read_csv(filepath+pathname+'/Plaintext.csv')
    print(plaintext_data)

if __name__ == '__main__':
    readflie('相关能量分析_原始波_无滤波_100条_8500点')