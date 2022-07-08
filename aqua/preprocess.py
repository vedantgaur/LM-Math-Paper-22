import os
import pandas as pd
import openai
import re

openai.api_key = os.getenv("OPENAI_API_KEY")
file_path = os.path.expanduser('~/Downloads/AQuA-master/train.json')


def compute_with_reasoning(index):
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
            response = openai.Completion.create(
                model="text-davinci-002",
                prompt=f"Give the answer with reasoning: \n{problem}",
                temperature=0.7,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            _response = response["choices"][0]["text"]
            _response = _response[2:]
            # print(f"GIVEN RESPONSE:  {_response}")
            # print(f"------------------")
            
            answer_list.append(_response)
        _answer = _key(options, answer)
        answer_list.append(_answer)

        data_to_append = {}
        for i in range(len(data.columns)):
            data_to_append[data.columns[i]] = answer_list[i]
        data = data.append(data_to_append, ignore_index = True) #type: ignore

        print(f"Done with question {i+1}\n")

    return data

def compute_with_steps(index):
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
            response = openai.Completion.create(
                model="text-davinci-002",
                prompt=f"Give the answer with steps: \n{problem}",
                temperature=0.7,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            _response = response["choices"][0]["text"]
            _response = _response[2:]
            # print(f"GIVEN RESPONSE:  {_response}")
            # print(f"------------------")
            
            answer_list.append(_response)
        _answer = _key(options, answer)
        answer_list.append(_answer)

        data_to_append = {}
        for i in range(len(data.columns)):
            data_to_append[data.columns[i]] = answer_list[i]
        data = data.append(data_to_append, ignore_index = True) #type: ignore

        print(f"Done with question {i+1}\n")
        data.to_csv("with_steps.csv")

    


def compute_without_reasoning(index):
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
            response = openai.Completion.create(
                model="text-davinci-002",
                prompt=f"Give solely the answer: \n{problem}",
                temperature=0.7,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            _response = response["choices"][0]["text"]
            _response = _response[2:]
            # print(f"GIVEN RESPONSE:  {_response}")
            # print(f"------------------")
            
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
    compute_with_steps(100)
    # compute_without_reasoning(100).to_csv("no_reasoning.csv")
    # compute_with_reasoning(100).to_csv("with_reasoning.csv")










# df = pd.read_json(file_path, lines=True)
# compute_with_reasoning(len(df)).to_csv("test.csv")
    
# response = openai.Completion.create(
#     model="text-davinci-edit-001",
#     input=f"{problem}",
#     instruction="Solve the problem",
#     temperature=0.7,
#     top_p=1
# )






# print(re.findall("\d+", problem))




# problem = df["question"][0]
# print(problem)

# # df.to_csv('problems.csv')
# # words = problem.split(" ")
# # print(words)

# print(re.findall("\d+", problem))

# for word in words:
#     if word.isnumeric():