import math
import numpy
from collections import deque

alphabet = 'AĄBCĆDEĘFGHIJKLŁMNŃOÓPQRSŚTUVWXYZŹŻ'

def decrypt(ciphertext, key):
    key_length = len(key)
    plaintext = ''
    i = 0
    for cipherletter in ciphertext:
        plainletter = alphabet[alphabet.find(cipherletter) - alphabet.find(key[i % key_length])]
        plaintext += plainletter
        i += 1

    return plaintext


ciphertext = 'KWĘDŃŁLŚÓXUQORIIDYOUŻMŹGACĘKUKIŹQĄAŁRQIQĆĘWXZCMMBCIPŹVPNNQSŁNBZĘSBDRQŚKŁWŚTOGUMIXFŃCPJU'
           # '012345012345012345012345012345012345012345012345012345012345012345012345012345012345012'

occurances_in_alpha = [8.91, 0.99, 1.47, 3.96, 0.4, 3.25, 7.66, 1.11, 0.3, 1.42, 1.08, 8.21, 2.28, \
    3.51, 2.1, 1.82, 2.8, 5.52, 0.2, 7.75, 0.85, 3.13, 0.14, 4.69, 4.32, 0.66, 3.98, 2.5, 0.04, 4.65, 0.02, 3.76, 5.64, 0.06, 0.83]

m = 6

ciphers_mono = ['' for i in range(m)]
occurances_mono = [[0 for x in range(len(alphabet))] for y in range(m)]

# podzielenie szyfrogramu na grupy w ten sposób, aby uzyskać 6 szyfrogramów o charakterze monoalfabetycznym
for i in range(0, len(ciphertext)):
    ciphers_mono[i % m] += ciphertext[i]

# zliczenie występowań poszczególnych znaków i normalizacja
for cipher_num in range(len(ciphers_mono)):
    for letter in alphabet:
        occurances = ciphers_mono[cipher_num].count(letter)
        if occurances != 0:
            occurances_mono[cipher_num][alphabet.find(letter)] = round(occurances/len(ciphers_mono[cipher_num])* 100, 2)

key_max_corr = [[-1 for x in range(2)] for y in range(m)]

# znalezienie klucza (przesunięcia) dla każdej z 6 grup
# maksymalna korelacja wektorów wystąpienia liter występuje dla kolejnych znaków klucza
for occ_num in range(len(occurances_mono)):
    for key in alphabet:
        shifted = occurances_mono[occ_num].copy()
        shifted = deque(shifted)
        shifted.rotate(-alphabet.find(key))
        shifted = list(shifted)
        corr_mat = numpy.corrcoef(occurances_in_alpha, shifted)
        corr_val = corr_mat[0][1]
        if corr_val > key_max_corr[occ_num][1]:
            key_max_corr[occ_num][0] = key
            key_max_corr[occ_num][1] = corr_val

key = ''
for x in key_max_corr:
    key += x[0]

print(key)
print(decrypt(ciphertext, key))