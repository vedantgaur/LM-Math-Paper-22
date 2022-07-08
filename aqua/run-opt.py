import os
import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


file_path = os.path.expanduser('~/Downloads/AQuA-master/train.json')


def compute_with_reasoning(index, tokenizer):
    columns = ["Trial 1", "Trial 2", "Trial 3", "Trial 4", "Trial 5", "Trial 6", "Trial 7", "Trial 8", "Trial 9", "Trial 10", "Answer"]
    df = pd.read_json(file_path, lines=True)
    data = pd.DataFrame(columns=columns)   

    for i in range(index):
        answer_list = []

        print(f"Question {i+1}")

        question = df["question"][i]
        options = df["options"][i]
        answer = df["correct"][i]
        print(f"ANSWER: {answer}")
        print(f"OPTIONS: {options}")

        _options = (",".join(options))
        _options = _options.replace(",", " ")
        problem = question + " " + _options

        for j in range(10):
            prompt=f"Give the answer with reasoning: \n{problem}"

            input_ids = tokenizer(prompt, return_tensors="pt").input_ids.cuda()

            generated_ids = model.generate(input_ids)

            _response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)

            print(f"GIVEN RESPONSE:  {_response}")
            print(f"------------------")
            
            answer_list.append(_response)
        _answer = _key(options, answer)
        answer_list.append(_answer)

        data_to_append = {}
        for i in range(len(data.columns)):
            data_to_append[data.columns[i]] = answer_list[i]
        data = data.append(data_to_append, ignore_index = True) #type: ignore

        print(f"Done with question {i+1}\n")

    return data


def compute_without_reasoning(index, tokenizer):
    columns = ["Trial 1", "Trial 2", "Trial 3", "Trial 4", "Trial 5", "Trial 6", "Trial 7", "Trial 8", "Trial 9", "Trial 10", "Answer"]
    df = pd.read_json(file_path, lines=True)
    data = pd.DataFrame(columns=columns)   

    for i in range(index):
        answer_list = []

        print(f"Question {i+1}")

        question = df["question"][i]
        options = df["options"][i]
        answer = df["correct"][i]
        print(f"ANSWER: {answer}")
        print(f"OPTIONS: {options}")

        _options = (",".join(options))
        _options = _options.replace(",", " ")
        problem = question + " " + _options

        for j in range(10):
            prompt=f"Give the answer without reasoning: \n{problem}"

            input_ids = tokenizer(prompt, return_tensors="pt").input_ids.cuda()

            generated_ids = model.generate(input_ids)

            _response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)

            print(f"GIVEN RESPONSE:  {_response}")
            print(f"------------------")
            
            answer_list.append(_response)
        _answer = _key(options, answer)
        answer_list.append(_answer)

        data_to_append = {}
        for i in range(len(data.columns)):
            data_to_append[data.columns[i]] = answer_list[i]
        data = data.append(data_to_append, ignore_index = True) #type: ignore

        print(f"Done with question {i+1}\n")

    return data


def compute_with_steps(index, tokenizer):
    columns = ["Trial 1", "Trial 2", "Trial 3", "Trial 4", "Trial 5", "Trial 6", "Trial 7", "Trial 8", "Trial 9", "Trial 10", "Answer"]
    df = pd.read_json(file_path, lines=True)
    data = pd.DataFrame(columns=columns)   

    for i in range(index):
        answer_list = []

        print(f"Question {i+1}")

        question = df["question"][i]
        options = df["options"][i]
        answer = df["correct"][i]
        print(f"ANSWER: {answer}")
        print(f"OPTIONS: {options}")

        _options = (",".join(options))
        _options = _options.replace(",", " ")
        problem = question + " " + _options

        for j in range(10):
            prompt=f"Give the answer with steps: \n{problem}"

            input_ids = tokenizer(prompt, return_tensors="pt").input_ids.cuda()

            generated_ids = model.generate(input_ids)

            _response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)

            print(f"GIVEN RESPONSE:  {_response}")
            print(f"------------------")
            
            answer_list.append(_response)
        _answer = _key(options, answer)
        answer_list.append(_answer)

        data_to_append = {}
        for i in range(len(data.columns)):
            data_to_append[data.columns[i]] = answer_list[i]
        data = data.append(data_to_append, ignore_index = True) #type: ignore

        print(f"Done with question {i+1}\n")

    return data


def _key(options, answer):
    if answer == 'A':
        return options[0]
    if answer == 'B':
        return options[1]
    if answer == 'C':
        return options[2]
    if answer == 'D':
        return options[3]
    if answer == 'E':
        return options[4]


if __name__ == "__main__":
    model = AutoModelForCausalLM.from_pretrained("facebook/opt-66b", torch_dtype=torch.float16).cuda()
    tokenizer = AutoTokenizer.from_pretrained("facebook/opt-66b", use_fast=False)

    folder_path = "results"
    _model = "otp"

    compute_with_steps(100, tokenizer).to_csv(f"{folder_path}/{_model}/steps.csv")
    compute_without_reasoning(100, tokenizer).to_csv(f"{folder_path}/{_model}/without.csv")
    compute_with_reasoning(100, tokenizer).to_csv(f"{folder_path}/{_model}/with.csv")