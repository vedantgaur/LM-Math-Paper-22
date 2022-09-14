import os
import openai

import pandas as pd
import ast
import numpy as np
import random
import re

root_dir = "~/onedrive/desktop/research paper"
openai.api_key = os.getenv("OPENAI_API_KEY")

df = pd.read_csv(f"{root_dir}/svamp/svamp_results/GPT-3/results/valid_tuple/valid_random.csv")
data = pd.DataFrame(columns=["With Steps", "Without Steps"], index=np.arange(100))

problems = df["Problem"]

for i in range(100):
    problem = problems[i]
    print(problem)
    prompt = "Q: {}\n\nA: ".format(problem)
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0,
        max_tokens=256,
    )
    response = response["choices"][0]["text"]
    response = response.strip('\n')
    data["Without Steps"][i] = response

    prompt = "Q: {}\n\nA: Let's think step by step: ".format(problem)
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0,
        max_tokens=256,
    )
    response = response["choices"][0]["text"]
    response = response.strip('\n')
    data["With Steps"][i] = response
    print(f"DONE WITH {i}\n")

data.to_csv(f"{root_dir}/svamp/svamp_results/GPT-3/results/valid_tuple/results.csv")