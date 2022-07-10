import os
import openai

import pandas as pd
import numpy as np

openai.api_key = os.getenv("OPENAI_API_KEY")

df = pd.read_csv("svamp/svamp_results/test.csv")
data = pd.DataFrame(columns=["With Reasoning", "Without Reasoning"], index=np.arange(20))

questions = df["Question"]

for i in range(20):
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=f"Give the answer: \n{questions[i]}",
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    _response = response["choices"][0]["text"]
    _response = _response[2:]
    print(f"GIVEN RESPONSE:  {_response}")
    print(f"------------------")
    data["Without Reasoning"][i] = _response

for j in range(20):
    response_ = openai.Completion.create(
        model="text-davinci-002",
        prompt=f"Think step-by-step and give me the answer: \n{questions[j]}",
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    _response_ = response_["choices"][0]["text"]
    _response_ = _response_[2:]
    print(f"GIVEN RESPONSE:  {_response_}")
    print(f"------------------")
    data["With Reasoning"][j] = _response_

data.to_csv("svamp/svamp_results/GPT-3/results.csv")