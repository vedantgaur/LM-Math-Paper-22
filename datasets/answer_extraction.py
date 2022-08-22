import os
import openai

import pandas as pd
import numpy as np

root_dir = "~/onedrive/desktop/research paper v2"

#TODO: make sure that the length matches up
data = pd.DataFrame(columns=["Symbolic Answer With Steps", "Symbolic Answer Without Steps", "Symbolic Answer With Intermediate", "Numeric Answer With Steps", "Numeric Answer Without Steps", "Numeric Answer With Intermediate"], index=np.arange(50))

def numeric_extraction(type):
    df = pd.read_csv(f"{root_dir}/.models/GPT-3/results/{type}.csv")
    steps = df["Numerical With Steps"]
    no_steps = df["Numerical Without Steps"]
    intermediate = df["Numerical With Intermediate Variables"]

    for i in range(len(df)):
        prompt = "{}\n\nThus the final answer (only the number) is:".format(steps(i))
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=prompt,
            temperature=0,
            max_tokens=256,
        )
        response = response["choices"][0]["text"]
        response = response.strip('\n')
        data["Numeric Answer With Steps"][i] = response

        prompt = "{}\n\nThus the final answer (only the number) is:".format(no_steps(i))
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=prompt,
            temperature=0,
            max_tokens=256,
        )
        response = response["choices"][0]["text"]
        response = response.strip('\n')
        data["Numeric Answer Without Steps"][i] = response

        prompt = "{}\n\nThus the final answer (only the number) is:".format(intermediate(i))
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

    data.to_csv(f".models/GPT-3/results/n_extract_{type}.csv")

def symbolic_extraction(type):
    df = pd.read_csv(f"{root_dir}/.models/GPT-3/results/{type}.csv")
    steps = df["Symbolic With Steps"]
    no_steps = df["Symbolic Without Steps"]
    intermediate = df["Symbolic With Intermediate Variables"]

    for i in range(len(df)):
        prompt = "{}\n\nThus the final answer (only the number) is:".format(steps(i))
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=prompt,
            temperature=0,
            max_tokens=256,
        )
        response = response["choices"][0]["text"]
        response = response.strip('\n')
        data["Symbolic Answer With Steps"][i] = response

        prompt = "{}\n\nThus the final answer (only the number) is:".format(no_steps(i))
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=prompt,
            temperature=0,
            max_tokens=256,
        )
        response = response["choices"][0]["text"]
        response = response.strip('\n')
        data["Symbolic Answer Without Steps"][i] = response

        prompt = "{}\n\nThus the final answer (only the number) is:".format(intermediate(i))
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

    data.to_csv(f".models/GPT-3/results/n_extract_{type}.csv")


if __name__ == "__main__":
    pass