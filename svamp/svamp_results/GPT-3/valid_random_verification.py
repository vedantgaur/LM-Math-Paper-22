import os
import openai

import pandas as pd
import numpy as np

openai.api_key = os.getenv("OPENAI_API_KEY")

root_dir = "~/onedrive/desktop/research paper"
df = pd.read_csv(f"{root_dir}/svamp/svamp_results/GPT-3/results/valid_tuple/numeric_answers.csv")
df1 = pd.read_csv(f"{root_dir}/svamp/svamp_results/GPT-3/results/valid_tuple/valid_random.csv")

answers = df1["Answer"]

with_steps_correct = 0
without_steps_correct = 0

for i in range(len(df)):
    try:
        if int(float(df["Answer With Steps"][i])) == answers[i]:
            with_steps_correct += 1
        if int(float(df["Answer Without Steps"][i])) == answers[i]:
            without_steps_correct += 1
    except:
        pass

print(with_steps_correct, without_steps_correct)