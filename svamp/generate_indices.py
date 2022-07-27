import numpy as np
import random

arr = np.zeros(50)

for i in range(50):
    random_index = random.randint(21, 999)
    arr[i] = random_index

np.save('svamp/svamp_results/indices.npy', arr)
