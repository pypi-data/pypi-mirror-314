import re
import random

def remove_symbols(input_string):
    # 使用正则表达式去掉所有非字母、数字和中文字符
    return re.sub(r'[^\w\u4e00-\u9fa5]', '', input_string)

def longest_common_subsequence(seq1, seq2): # 最长公共子序列
    m, n = len(seq1), len(seq2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # 填充 dp 数组
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = dp[i - 1][j - 1] + 1 if seq1[i - 1] == seq2[j - 1] else max(dp[i - 1][j], dp[i][j - 1])

    # 回溯找出 LCS
    lcs = []
    i, j = m, n
    while i > 0 and j > 0:
        if seq1[i - 1] == seq2[j - 1]:
            lcs.append(seq1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return dp[m][n], ''.join(reversed(lcs))

def generate_random_filename(length=8):
    # 生成一个只包含数字的随机文件名
    digits = '0123456789abcdefghijklmnopqrstuvwxyz'
    filename = ''.join(random.choices(digits, k=length))
    return filename