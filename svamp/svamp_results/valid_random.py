import os
import openai

import pandas as pd
import ast
import numpy as np
import random
import re

root_dir = "~/onedrive/desktop/research paper"
openai.api_key = os.getenv("OPENAI_API_KEY")

df = pd.read_csv("svamp/svamp_results/augmented_svamp.csv")
data = pd.DataFrame(columns=["Index", "Problem", "Expression", "Values", "Answer"], index=np.arange(750))

nums = df["Numbers"]
problems = df["Symbolic Problem"]
equations = df["Symbolic Equation"]
variables = df["Variables"]

num_arr = np.arange(1, 51)
indices = []

for i in range(150):
    random_index = random.randint(21, 999)
    indices.append(random_index)
print(indices)

for i in range(150):
    j = 0
    nums_len = len(ast.literal_eval(nums[indices[i]]))
    problem = problems[indices[i]]
    expression = equations[indices[i]]

    while j < 5:
        arr = []
        for k in range(nums_len):
            random_num = random.choice(num_arr)
            if k == 0:    
                _problem = re.sub(f"<{k+1}>", str(random_num), problem)
            else:
                _problem = re.sub(f"<{k+1}>", str(random_num), _problem)
            try:
                if k == 0: 
                    _expression = re.sub(f"<{k+1}>", str(random_num), expression)
                else:
                    _expression = re.sub(f"<{k+1}>", str(random_num), _expression)
            except:
                pass
            arr.append(random_num)
        print(arr)
        print(f"EXPRESSION: {_expression}")
        val = eval(_expression)
        print(type(val))
        
        if val > 0 and val-int(val) == 0:
            print(arr)
            print(_expression)
            print(_problem)
            print("GOOD ONE\n\n")
            data["Index"][5*i+j] = indices[i]
            data["Problem"][5*i+j] = _problem
            data["Expression"][5*i+j] = _expression
            data["Values"][5*i+j] = arr
            data["Answer"][5*i+j] = val
            j += 1
        else:
            print("NOT GOOD ONE\n\n")
        
        print(f"{j}/5")
    print(f"run {i}")
    print(val)

data.to_csv(f"{root_dir}/svamp/svamp_results/GPT-3/results/valid_tuple/valid_random_150.csv")


#             _nums.append(num_arr[0])
#             num_arr.pop(0)
#             print(f"\n{len(num_arr)}\n")
#             print(i)
#         if ()
#     data["Problem"][i] = problem # type: ignore
#     data["Expression"][i] = expression # type: ignore
#     data["Answer"][i] = eval(expression) # type: ignore
#     data["Number"][i] = _nums

#     prompt = "Q: {}\n\nA: ".format(data["Problem"][i])
#     response = openai.Completion.create(
#         model="text-davinci-002",
#         prompt=prompt,
#         temperature=0,
#         max_tokens=256,
#     )
#     response = response["choices"][0]["text"]
#     response = response.strip('\n')
#     data["Without Steps"][i] = response

#     prompt = "Q: {}\n\nA: Let's think step by step: ".format(data["Problem"][i])
#     response = openai.Completion.create(
#         model="text-davinci-002",
#         prompt=prompt,
#         temperature=0,
#         max_tokens=256,
#     )
#     response = response["choices"][0]["text"]
#     response = response.strip('\n')
#     data["With Steps"][i] = response

# data.to_csv(f"{root_dir}/svamp/svamp_results/GPT-3/results/shuffled/shuffled_svamp.csv")
