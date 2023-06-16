import numpy as np

def splot(signal1, signal2, mode = 'full'):
    signal1Len = len(signal1)
    signal2Len = len(signal2)
    fullLen = signal1Len + signal2Len - 1
    
    result = [0] * fullLen
    for i in range(signal1Len):
        for j in range(signal2Len):
            result[i + j] += signal1.iloc[i] * signal2.iloc[j]

    if mode == 'full':
        return np.array(result)
    elif mode == 'same':
        if  signal1Len > signal2Len:
            start = int(np.ceil((fullLen - signal1Len) / 2))
            end = start + signal1Len
        else:
            start = int(np.ceil((fullLen - signal1Len) / 2))
            end = start + signal2Len
        return np.array(result[start:end])
    elif mode == 'valid':
        start = signal2Len - 1
        end = signal1Len + start 
        return np.array(result[start:end])

