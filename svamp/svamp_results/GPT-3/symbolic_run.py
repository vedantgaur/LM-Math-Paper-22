import os
import openai

import pandas as pd
import numpy as np
import ast
import re

openai.api_key = os.getenv("OPENAI_API_KEY")
root_dir = "~/onedrive/desktop/research paper"

data = pd.DataFrame(columns=["With Steps", "Without Steps", "Extracted Steps", "Extracted Without Steps", "True Expression", "Correct Steps", "Correct Without Steps"], index=np.arange(150))

df = pd.read_csv(f"{root_dir}/svamp/svamp_results/GPT-3/results/valid_tuple/valid_random_150.csv")
df1 = pd.read_csv(f"{root_dir}/svamp/svamp_results/augmented_svamp.csv")
svamp_df = pd.read_csv(f"{root_dir}/svamp/svamp_results/wxyz_dataset.csv")

problems = svamp_df["Question"]
_indices = df["Index"]
equation = svamp_df["Equation"]

vars = ["w", "x", "y", "z"]
subs = [12, 4, 2, 7]

indices = []
for i in range(len(_indices)):
    if i % 5 == 0:
        indices.append(_indices[i])

print(indices)

path_exists = os.path.isdir(f'c://users/vedan/onedrive/desktop/research paper/svamp/svamp_results/GPT-3/results/symbolic/results.csv')
print(f"THE PATH EXISTS?? ??? ?? ? {path_exists}")

for i in range(len(indices)):
 
    problem = problems[i]
    # nums_len = len(ast.literal_eval(df1["Numbers"][index]))

    # WITH STEPS
    prompt = "Q: {}\n\nA: Let's think step by step".format(problem)
    print(prompt)
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0,
        max_tokens=256,
    )
    response = response["choices"][0]["text"]
    response = response.strip('\n')
    print(f"First Run: {response}")
    data["With Steps"][i] = response

    prompt = "{}\n\nThus the final answer (only the expression) is: ".format(response)
    print(prompt)
    _response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0,
        max_tokens=256,
    )
    _response = _response["choices"][0]["text"]
    _response = _response.strip('\n')
    _response = _response.replace("$", "")
    _response = _response.replace("* n", "")
    _response = _response.replace("*n", "")
    print(f"Second Run: {_response}")
    data["Extracted Steps"][i] = _response

    for k in range(4):
        try:
            print(f"CURRENT VAR: {vars[k]}")
            if k == 0:
                expression = re.sub(f"{vars[k]}", str(subs[k]), _response)
                true_expression = re.sub(f"{vars[k]}", str(subs[k]), equation[indices[i]])
                print(indices[i])
            else:
                expression = re.sub(f"{vars[k]}", str(subs[k]), expression)
                true_expression = re.sub(f"{vars[k]}", str(subs[k]), true_expression)
        except:
            pass

    print(f"Output Expression: {expression}")
    print(f"True Expression: {true_expression}")

    try:
        val = eval(expression)
    except:
        val = -12321321
    
    try:
        true_val = eval(true_expression)
    except:
        true_val = 435432534

    print(f"Outputted eval: {val}")
    print(f"True eval: {true_val}")
    print(true_val == val)

    if true_val == val:
        data["Correct Steps"][i] = 1
    else:
        data["Correct Steps"][i] = 0

    #========================================================

    # WITHOUT STEPS
    prompt = "Q: {}\n\nA: Let's think step by step".format(problem)
    print(prompt)
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0,
        max_tokens=256,
    )
    response = response["choices"][0]["text"]
    response = response.strip('\n')
    print(f"First Run: {response}")
    data["Without Steps"][i] = response

    prompt = "{}\n\nThus the final answer (only the expression) is: ".format(response)
    print(prompt)
    _response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0,
        max_tokens=256,
    )
    _response = _response["choices"][0]["text"]
    _response = _response.strip('\n')
    _response = _response.replace("$", "")
    _response = _response.replace("* n", "")
    _response = _response.replace("*n", "")
    print(f"Second Run: {_response}")
    data["Extracted Without Steps"][i] = _response

    for j in range(4):
        try:
            print(f"CURRENT VAR: {vars[j]}")
            if j == 0:
                expression = re.sub(f"{vars[j]}", str(subs[j]), _response)
                true_expression = re.sub(f"{vars[j]}", str(subs[j]), equation[indices[i]])
            else:
                expression = re.sub(f"{vars[j]}", str(subs[j]), expression)
                true_expression = re.sub(f"{vars[j]}", str(subs[j]), true_expression)
        except:
            pass

    print(f"Output Expression: {expression}")
    print(f"True Expression: {true_expression}")

    try:
        val = eval(expression)
    except:
        val = -12321321
    
    try:
        true_val = eval(true_expression)
    except:
        true_val = 435432534

    print(f"Outputted eval: {val}")
    print(f"True eval: {true_val}")
    print(true_val == val)

    if true_val == val:
        data["Correct Without Steps"][i] = 1
    else:
        data["Correct Without Steps"][i] = 0
    
    if i == 2:
        break

data.to_csv(f"{root_dir}/svamp/svamp_results/GPT-3/results/symbolic/results.csv")