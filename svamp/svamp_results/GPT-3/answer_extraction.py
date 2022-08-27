import os
import openai

import pandas as pd
import numpy as np

from benchmarks_zero_shot import symbolic_prompt, symbolic_prompt_steps, symbolic_prompt_intermediate

openai.api_key = os.getenv("OPENAI_API_KEY")

root_dir = "~/onedrive/desktop/research paper"
df = pd.read_csv(f"{root_dir}/svamp/svamp_results/GPT-3/results/results_0temp.csv")

data = pd.DataFrame(columns=["Symbolic Answer With Steps", "Symbolic Answer Without Steps", "Symbolic Answer With Intermediate"], index=np.arange(len(df)))

for i in range(len(df)):
    prompt = "{}{}\n\nTherefore, the answer (symbolic) is: ".format(symbolic_prompt_steps(i), df["Symbolic With Steps"][i])
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0,
        max_tokens=256,
    )
    response = response["choices"][0]["text"]
    response = response.strip('\n')
    data["Symbolic Answer With Steps"][i] = response

    prompt = "{}{}\n\nTherefore, the answer (symbolic) is: ".format(symbolic_prompt(i), df["Symbolic Without Steps"][i])
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0,
        max_tokens=256,
    )
    response = response["choices"][0]["text"]
    response = response.strip('\n')
    data["Symbolic Answer Without Steps"][i] = response

    prompt = "{}{}\n\nTherefore, the answer (symbolic) is: ".format(symbolic_prompt_intermediate(i), df["Symbolic With Intermediate Variables"][i])
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0,
        max_tokens=256,
    )
    response = response["choices"][0]["text"]
    response = response.strip('\n')
    data["Symbolic Answer With Intermediate"][i] = response

    print(f"DONE WITH {i}")

data.to_csv(f"{root_dir}/svamp/svamp_results/GPT-3/results/symbolic_answers_2.csv")
    
    