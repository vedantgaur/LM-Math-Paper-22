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
data = pd.DataFrame(columns=["With Steps", "Without Steps", "Problem", "Number", "Expression", "Answer"], index=np.arange(50))

nums = df["Numbers"]
problems = df["Symbolic Problem"]
equations = df["Symbolic Equation"]
variables = df["Variables"]

num_arr = []

for i in range(50):
    numbers = ast.literal_eval(nums[i])
    for num in numbers:
        num_arr.append(num)

print(num_arr)
random.shuffle(num_arr)
print(num_arr)

indices = np.load("C:/Users/vedan/OneDrive/Desktop/Research Paper/svamp/svamp_results/indices.npy")

for i in range(50):
    nums_len = len(ast.literal_eval(nums[i]))
    problem = problems[indices[i]]
    expression = equations[indices[i]]
    _nums = []
    for j in range(len(ast.literal_eval(variables[indices[i]]))):
        problem = re.sub(f"<{j+1}>", str(num_arr[0]), problem, count=1)
        print(problem)
        try:
            expression = re.sub(f"<{j+1}>", str(num_arr[0]), expression)
            print(expression)
        except:
            pass
        _nums.append(num_arr[0])
        num_arr.pop(0)
        print(f"\n{len(num_arr)}\n")
        print(i)
    data["Problem"][i] = problem # type: ignore
    data["Expression"][i] = expression # type: ignore
    data["Answer"][i] = eval(expression) # type: ignore
    data["Number"][i] = _nums

    prompt = "Q: {}\n\nA: ".format(data["Problem"][i])
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0,
        max_tokens=256,
    )
    response = response["choices"][0]["text"]
    response = response.strip('\n')
    data["Without Steps"][i] = response

    prompt = "Q: {}\n\nA: Let's think step by step: ".format(data["Problem"][i])
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0,
        max_tokens=256,
    )
    response = response["choices"][0]["text"]
    response = response.strip('\n')
    data["With Steps"][i] = response

data.to_csv(f"{root_dir}/svamp/svamp_results/GPT-3/results/shuffled/shuffled_svamp.csv")
