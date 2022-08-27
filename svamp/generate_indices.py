import numpy as np
import random

arr = np.zeros(150)

for i in range(150):
    random_index = random.randint(21, 999)
    arr[i] = random_index

np.save('svamp/svamp_results/indices_plus.npy', arr)
