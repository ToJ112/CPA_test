
import numpy as np
import pandas as pd
test=np.load('cpatest16.npy')  #加载文件

np_to_csv = pd.DataFrame(data=test)

# 存入具体目录下的np_to_csv.csv 文件
np_to_csv.to_csv('npsv.csv')