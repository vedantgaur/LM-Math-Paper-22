import os
import openai

import pandas as pd
import numpy as np

openai.api_key = os.getenv("OPENAI_API_KEY")

df = pd.read_csv("svamp/svamp_results/wxyz_dataset.csv")
df1 = pd.read_csv("svamp/svamp_results/augmented_svamp.csv")

data = pd.DataFrame(
    columns=[
    "Symbolic With Steps", 
    "Symbolic Without Steps", 
    "Symbolic With Intermediate Variables", 
    "Numerical With Steps", 
    "Numerical Without Steps", 
    "Numerical With Intermediate Variables",
    "Symbolic Answers", 
    "Numerical Answers",
    "Numerical Equations"
    ], 
    index=np.arange(20)
    )

symbolic_questions = df["Question"]
symbolic_answers = df["Equation"]

numerical_questions = df1["Question"]
numerical_answers = df1["Answer"]
numerical_equations = df1["Equation"]

for i in range(20):
    # SYMBOLIC WITHOUT STEPS
    _prompt = f"Q: {symbolic_questions[i]}\n\nA: "
    print(_prompt)
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=_prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    _response = response["choices"][0]["text"]
    _response = _response[2:]
    print(f"Symbolic no reasoning:  {_response}")
    print(f"------------------")
    data["Symbolic Without Steps"][i] = _response

    # SYMBOLIC WITH STEPS
    _prompt = f"Q: {symbolic_questions[i]}\n\nA: Let's think step by step."
    print(_prompt)
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=_prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    _response = response["choices"][0]["text"]
    _response = _response[2:]
    print(f"Symbolic with reasoning:  {_response}")
    print(f"------------------")
    data["Symbolic With Steps"][i] = _response

    # SYMBOLIC WITH INTERMEDIARY
    _prompt = f"Q: {symbolic_questions[i]}\n\nA: Let's think step by step. Introduce intermediate variables and solve the task symbolically."
    print(_prompt)
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=_prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    _response = response["choices"][0]["text"]
    _response = _response[2:]
    print(f"Symbolic with intermediary:  {_response}")
    print(f"------------------")
    data["Symbolic With Intermediate Variables"][i] = _response

    data["Symbolic Answer"] = symbolic_answers[i]
    print(f"Symbolic Answer: {symbolic_answers[i]}")
    print(f"------------------")

    # NUMERICAL WITHOUT STEPS
    _prompt = f"Q: {numerical_questions[i]}\n\nA: "
    print(_prompt)
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=_prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    _response = response["choices"][0]["text"]
    _response = _response[2:]
    print(f"Numerical no reasoning:  {_response}")
    print(f"------------------")
    data["Numerical Without Steps"][i] = _response

    # NUMERICAL WITH STEPS
    _prompt = f"Q: {numerical_questions[i]}\n\nA: Let's think step by step."
    print(_prompt)
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=_prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    _response = response["choices"][0]["text"]
    _response = _response[2:]
    print(f"Numerical with reasoning:  {_response}")
    print(f"------------------")
    data["Numerical With Steps"][i] = _response

    # SYMBOLIC WITH INTERMEDIARY
    _prompt = f"Q: {numerical_questions[i]}\n\nA: Let's think step by step. Introduce intermediate variables and solve the task symbolically."
    print(_prompt)
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=_prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    _response = response["choices"][0]["text"]
    _response = _response[2:]
    print(f"Numerical with intermediary:  {_response}")
    print(f"------------------")
    data["Numerical With Intermediate Variables"][i] = _response

    data["Numerical Answer"] = numerical_answers[i]
    print(f"Numerical Answer: {numerical_answers[i]}")
    print(f"------------------")

    data["Numerical Equation"] = numerical_equations[i]
    print(f"Numerical Equation: {numerical_equations[i]}")
    print(f"------------------")

data.to_csv("svamp/svamp_results/GPT-3/results.csv")