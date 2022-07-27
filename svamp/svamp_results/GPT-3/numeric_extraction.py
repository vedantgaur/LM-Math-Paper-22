import os
import openai

import pandas as pd
import numpy as np

from benchmarks import numeric_prompt, numeric_prompt_steps, numeric_prompt_intermediate

openai.api_key = os.getenv("OPENAI_API_KEY")

root_dir = "~/onedrive/desktop/research paper"
df = pd.read_csv(f"{root_dir}/svamp/svamp_results/GPT-3/results/results_0temp.csv")

data = pd.DataFrame(columns=["Numeric Answer With Steps", "Numeric Answer Without Steps", "Numeric Answer With Intermediate"], index=np.arange(len(df)))

for i in range(len(df)):
    prompt = "{}{}\n\nTherefore, the answer (numerical) is: ".format(numeric_prompt_steps(i), df["Numerical With Steps"][i])
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0,
        max_tokens=256,
    )
    response = response["choices"][0]["text"]
    response = response.strip('\n')
    data["Numeric Answer With Steps"][i] = response

    prompt = "{}{}\n\nTherefore, the answer (numerical) is: ".format(numeric_prompt(i), df["Numerical Without Steps"][i])
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0,
        max_tokens=256,
    )
    response = response["choices"][0]["text"]
    response = response.strip('\n')
    data["Numeric Answer Without Steps"][i] = response

    prompt = "{}{}\n\nTherefore, the answer (numerical) is: ".format(numeric_prompt_intermediate(i), df["Numerical With Intermediate Variables"][i])
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0,
        max_tokens=256,
    )
    response = response["choices"][0]["text"]
    response = response.strip('\n')
    data["Numeric Answer With Intermediate"][i] = response

    print(f"DONE WITH {i}")

data.to_csv(f"{root_dir}/svamp/svamp_results/GPT-3/results/numeric_answers.csv")
    