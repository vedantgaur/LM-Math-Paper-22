import os
import openai

import pandas as pd
import numpy as np

openai.api_key = os.getenv("OPENAI_API_KEY")

root_dir = "~/onedrive/desktop/research paper"
df = pd.read_csv(f"{root_dir}/svamp/svamp_results/GPT-3/results/zero_shot/zero_shot_results.csv")

data = pd.DataFrame(columns=["With Steps", "Without Steps", "Intermediate"], index=np.arange(len(df)))

for i in range(len(df)):
    prompt = "{}\n\nThus the final answer (only the number) is: ".format(df["Numerical With Steps"][i])
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0,
        max_tokens=256,
    )
    response = response["choices"][0]["text"]
    response = response.strip('\n')
    data["With Steps"][i] = response

    prompt = "{}\n\nThus the final answer (only the number) is: ".format(df["Numerical Without Steps"][i])
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0,
        max_tokens=256,
    )
    response = response["choices"][0]["text"]
    response = response.strip('\n')
    data["Without Steps"][i] = response

    prompt = "{}\n\nThus the final answer (only the number) is: ".format(df["Numerical With Intermediate Variables"][i])
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0,
        max_tokens=256,
    )
    response = response["choices"][0]["text"]
    response = response.strip('\n')
    data["Intermediate"][i] = response


    print(f"DONE WITH {i}")

data.to_csv(f"{root_dir}/svamp/svamp_results/GPT-3/results/zero_shot/answers.csv")
    