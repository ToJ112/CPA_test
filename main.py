# -*- coding: utf-8 -*-
# author: jtning

import DataPre
import CalPre
if __name__ == '__main__':
    N = 100  # 100条能量迹（根据提供文件）
    plaintexts, trace = DataPre.readfile('相关能量分析_原始波_无滤波_100条_8500点', N)
    cipher = []
    # for bit in range(16):
    #     print("第" + str(bit) + "字节")
    #     this_cipher = CalPre.corr_cal_before_sbox(bit, plaintexts, trace, N)
    #     cipher.append(this_cipher)
    # print(cipher)
    #['11', '22', '33', '44', '55', '66', '77', '88', '99', 'aa', 'bb', 'cc', 'dd', 'ee', 'ff', '00']
    for bit in range(16):
        print("第" + str(bit) + "字节")
        corr_arr = CalPre.corr_cal_before_sbox(bit, plaintexts, trace, N)
        CalPre.corr_paint_all(corr_arr, bit)