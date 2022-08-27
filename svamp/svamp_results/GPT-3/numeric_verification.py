import os
import openai

import pandas as pd
import numpy as np

openai.api_key = os.getenv("OPENAI_API_KEY")

root_dir = "~/onedrive/desktop/research paper"
df = pd.read_csv(f"{root_dir}/svamp/svamp_results/GPT-3/results/two_step_v2/two_step_v2_150.csv")
df1 = pd.read_csv(f"{root_dir}/svamp/svamp_results/GPT-3/results/two_step_v2/answers_150.csv")

answers = df["Numerical Answer"]

with_steps_correct = 0
without_steps_correct = 0
with_intermediate_correct = 0

for i in range(len(df)):
    try:
        if int(df1["With Steps"][i]) == answers[i]:
            with_steps_correct += 1
        if int(df1["Without Steps"][i]) == answers[i]:
            without_steps_correct += 1
        if int(df1["With Intermediate"][i]) == answers[i]:
            with_intermediate_correct += 1
    except:
        pass

print(with_steps_correct, without_steps_correct, with_intermediate_correct)