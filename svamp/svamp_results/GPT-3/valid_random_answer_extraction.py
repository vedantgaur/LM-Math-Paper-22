import os
import openai

import pandas as pd
import numpy as np

openai.api_key = os.getenv("OPENAI_API_KEY")

root_dir = "~/onedrive/desktop/research paper"
df = pd.read_csv(f"{root_dir}/svamp/svamp_results/GPT-3/results/valid_tuple/results.csv")

data = pd.DataFrame(columns=["Answer With Steps", "Answer Without Steps"], index=np.arange(len(df)))

for i in range(len(df)):
    answer = df["With Steps"][i]
    prompt = "{}\n\nThus the final answer (only the number) is: ".format(answer)
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0,
        max_tokens=256,
    )
    response = response["choices"][0]["text"]
    response = response.strip('\n')
    data["Answer With Steps"][i] = response

    answer = df["Without Steps"][i]
    prompt = "{}\n\nThus the final answer (only the number) is: ".format(answer)
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0,
        max_tokens=256,
    )
    response = response["choices"][0]["text"]
    response = response.strip('\n')
    data["Answer Without Steps"][i] = response

    print(f"DONE WITH {i}")


data.to_csv(f"{root_dir}/svamp/svamp_results/GPT-3/results/numeric_answers.csv")
    
    