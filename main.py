# -*- coding: utf-8 -*-
# author: jtning
import time

import numpy as np

import datapre
import calpre


def before_sbox(plaintexts, trace, N=100):
    for bit in range(16):
        print("第" + str(bit + 1) + "字节")
        corr_arr = calpre.corr_cal_before_sbox(bit, plaintexts, trace, N)
        calpre.corr_paint_all(corr_arr, bit)


def after_sbox_test1(plaintexts, trace, N=100):
    cipher = []
    for bit in range(16):
        print("第" + str(bit + 1) + "字节")
        this_cipher = calpre.corr_cal_after_sbox(bit, plaintexts, trace, N)
        cipher.append(this_cipher)
        print(this_cipher)
    return cipher


def after_sbox_max_extract(plaintexts, trace, ipc, N=100):
    cipher = []
    for bit in range(16):
        print("第" + str(bit + 1) + "字节")
        this_cipher = calpre.corr_cal_max_extract(bit, plaintexts, trace,ipc, N)
        cipher.append(this_cipher)
        print(this_cipher)
    return cipher


if __name__ == '__main__':
    time_start = time.time ()
    N = 100  # 100条能量迹（根据提供文件）
    ipc = 980
    plaintexts, trace = datapre.readfile('相关能量分析_原始波_7M滤波_%s条_8500点'%N, N)
    trace_max_extract = datapre.max_traces(trace, ipc, N)
    print("数据成功载入……")
    # vv = after_sbox_test1(plaintexts, trace, N)
    cipher = after_sbox_max_extract(plaintexts, trace_max_extract, ipc,N)
    time_end = time.time()
    print( time_end - time_start)
    # print(cipher)
    # ['11', '22', '33', '44', '55', '66', '77', '88', '99', 'aa', 'bb', 'cc', 'dd', 'ee', 'ff', '00']