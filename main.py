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


def before_sbox_test1(plaintexts, trace, N=100):
    cipher = []
    for bit in range(16):
        print("第" + str(bit + 1) + "字节")
        this_cipher = calpre.cipher_cal_before_sbox(bit, plaintexts, trace, N)
        cipher.append(this_cipher)
        print(this_cipher)
    return cipher


def after_sbox_cpa(plaintexts, trace, N=100):
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
        this_cipher = calpre.corr_cal_extract(bit, plaintexts, trace, ipc, N)
        cipher.append(this_cipher)
        print(this_cipher)
    return cipher


def after_sbox_consolidation(plaintexts, trace, intervals, method, N=100):
    cipher = []
    trace_consolidation = datapre.consolidation(trace, intervals, method)
    slices = int(8500 / intervals)
    for bit in range(16):
        print("第" + str(bit + 1) + "字节")
        this_cipher = calpre.corr_cal_extract(bit, plaintexts, trace_consolidation, slices, N)
        cipher.append(this_cipher)
        print(this_cipher)
    print(cipher)
    return cipher


def after_sbox_dpa(plaintexts, trace, N, method):
    cipher = []
    for bit in range(16):
        this_cipher = calpre.corr_cal_dpa(bit, plaintexts, trace, N, method)
        cipher.append(this_cipher)
        print("第" + str(bit + 1) + "字节的密钥为" + this_cipher)
    return cipher


if __name__ == '__main__':
    time_start = time.time()
    N = 100  # 100条能量迹（根据提供文件）
    ipc = 980
    intervals = 340  # 整合的时间段中的点数
    plaintexts, trace = datapre.readfile('相关能量分析_原始波_无滤波_%s条_8500点' % N, N)
    trace_max_extract = datapre.max_traces(trace, ipc)
    print("数据成功载入...")
    # cipher_before_sbox = before_sbox_test1(plaintexts, trace, N)
    # cipher_after_sbox = after_sbox_cpa(plaintexts, trace_max_extract, N)
    # cipher_extract = after_sbox_consolidation(plaintexts, trace, intervals, 'pow', N)
    cipher_dpa = after_sbox_dpa(plaintexts, trace, N, 'afterSbox_MSB')
    print(cipher_dpa)
    time_end = time.time()
    print('总耗时%.2fs' % (time_end - time_start))

    # ['11', '22', '33', '44', '55', '66', '77', '88', '99', 'aa', 'bb', 'cc', 'dd', 'ee', 'ff', '00']
