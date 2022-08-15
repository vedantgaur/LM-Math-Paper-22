import numpy as np
import random
import argparse

root_dir = "c:/users/vedan/onedrive/desktop/research paper v2"

def check_duplicates(array, val, start, end):
    if val in array:
        val = random.randint(start, end)
        check_duplicates(array, val, start, end)
    
def generate_indices(start, end, num_indices, dataset):
    arr = np.zeros(num_indices)
    for i in range(num_indices):
        random_index = random.randint(start, end)
        check_duplicates(arr, random_index, start, end)     
        arr[i] = random_index
    print(arr)
    np.save(f'{root_dir}/datasets/{dataset}/{dataset}_indices.npy', arr)

if __name__ == "__main__":
    generate_indices(0, 1000, 50, "svamp")