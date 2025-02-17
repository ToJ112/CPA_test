import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

aes_sbox = np.array([
    [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76],
    [0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0],
    [0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15],
    [0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75],
    [0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84],
    [0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF],
    [0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8],
    [0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2],
    [0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73],
    [0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB],
    [0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79],
    [0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08],
    [0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A],
    [0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E],
    [0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF],
    [0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16]
])


def sbox_trans(input):
    m = input // 16
    n = input % 16
    return aes_sbox[m][n]


def hamming_weight(k, plaintexts, N):
    hamWeight = np.zeros((256, N))
    for key in range(256):
        for tra in range(N):
            plaintext = eval('0x' + plaintexts[tra][k])
            ciphertext = key ^ plaintext
            hamWeight[key][tra] = bin(sbox_trans(ciphertext)).count('1')
    return hamWeight


def corr_paint_all(corr_key2trace, k):
    for i in tqdm(range(256)):
        X = np.linspace(0, 8500, 8500)
        Y = corr_key2trace[i]
        plt.plot(X, Y, ls="-", lw=2, label="correlation")
        plt.ylim(-1, 1)  # 设置y轴取值范围
        plt.savefig("相关能量分析_原始波_无滤波_100条_8500点/%s/%d.png" % (k, i), bbox_inches='tight')
        plt.clf()  # 清除生成图避免重叠


def corr_cal_before_sbox(k, plaintexts, trace, N=100):
    hamWeight = np.zeros((256, N))
    for key in range(256):
        for tra in range(N):
            plaintext = eval('0x' + plaintexts[tra][k])
            ciphertext = key ^ plaintext
            hamWeight[key][tra] = bin(ciphertext).count('1')  # S盒之前

    corr_key2trace = np.zeros((256, 8500))

    for i in tqdm(range(256)):
        for j in range(8500):
            hmWei = hamWeight[i, :]
            tra = trace[:, j]
            corr_key2trace[i][j] = np.corrcoef(hmWei, tra)[0][1]
    return corr_key2trace


def cipher_cal_before_sbox(k, plaintexts, trace, N=100):
    hamWeight = np.zeros((256, N))
    for key in range(256):
        for tra in range(N):
            plaintext = eval('0x' + plaintexts[tra][k])
            ciphertext = key ^ plaintext
            hamWeight[key][tra] = bin(ciphertext).count('1')  # S盒之前

    corr_key2trace = np.zeros((256, 8500))

    for i in tqdm(range(256)):
        for j in range(8500):
            hmWei = hamWeight[i, :]
            tra = trace[:, j]
            corr_key2trace[i][j] = np.corrcoef(hmWei, tra)[0][1]
    corr_abs = abs(corr_key2trace)
    cipher_key = np.argmax(np.max(corr_abs, axis=1))
    return '{0:02X}'.format(cipher_key)


def corr_cal_after_sbox(k, plaintexts, trace, N=100):
    hamWeight = hamming_weight(k, plaintexts, N)

    # 根据轨迹寻找泄漏点及密钥
    trace_matrix = np.array(trace)
    corr_key2trace = np.zeros((256, 8500))
    for i in tqdm(range(256)):
        for j in range(8500):
            hmWei = hamWeight[i, :]
            tra = trace_matrix[:, j]
            corr_key2trace[i][j] = np.corrcoef(hmWei, tra)[0][1]
    corr_abs = abs(corr_key2trace)
    cipher_key = np.argmax(np.max(corr_abs, axis=1))
    return '{0:02X}'.format(cipher_key)


def corr_cal_extract(k, plaintexts, trace_matrix, ipc, N=100):
    hamWeight = hamming_weight(k, plaintexts, N)
    # 根据轨迹寻找泄漏点及密钥
    corr_key2trace = np.zeros((256, ipc))
    for i in tqdm(range(256)):
        for j in range(ipc):
            hmWei = hamWeight[i, :]
            tra = trace_matrix[:, j]
            corr_key2trace[i][j] = np.corrcoef(hmWei, tra)[0][1]
    corr_abs = abs(corr_key2trace)
    cipher_key = np.argmax(np.max(corr_abs, axis=1))
    return '{0:02X}'.format(cipher_key)


def corr_cal_dpa(k, plaintexts, traces, N, method):
    max_diff = -1
    real_key = -1
    # hamWeight = hamming_weight(k, plaintexts, N)
    # for key in tqdm(range(256)):
    for key in range(256):
        trace0 = []
        trace1 = []
        for tra in range(N):
            plaintext = eval('0x' + plaintexts[tra][k])
            method_judge = -1
            if method == 'afterSbox_LSB':
                method_judge = (sbox_trans(key ^ plaintext) & 1)
            elif method == 'beforeSboxHwParity':
                hamWeight = bin(key ^ plaintext).count('1')
                method_judge = (hamWeight % 2 == 0)
            elif method == 'afterSboxHmGe4':
                hamWeight = bin(sbox_trans(key ^ plaintext)).count('1')
                method_judge = (hamWeight > 4)
            elif method == 'afterSbox_MSB':
                # hamWeight = bin(sbox_trans(key ^ plaintext)).count('1')
                method_judge = (sbox_trans(key ^ plaintext) & 128)
            if method_judge:
                trace1.append(traces[tra])
            else:
                trace0.append(traces[tra])
        mean_tra0 = np.einsum("ij->j", np.array(trace0)) / np.double(np.shape(trace0)[0])
        mean_tra1 = np.einsum("ij->j", np.array(trace1)) / np.double(np.shape(trace1)[0])
        diff_trace = np.max(abs(mean_tra1 - mean_tra0))
        if max_diff < diff_trace:
            max_diff = diff_trace
            real_key = key
    return '{0:02X}'.format(real_key)
