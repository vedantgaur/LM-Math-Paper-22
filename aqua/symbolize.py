import os
import pandas as pd
import re

vars = [
    "a", "b",
    "c", "d",
    "e", "f",
    "g", "h",
    "i", "j",
    "k", "l",
    "m", "n",
    "o", "p",
    "q", "r",
    "s", "t",
    "u", "v",
    "w", "x",
    "y", "z"
]

file_path = os.path.expanduser('~/Downloads/AQuA-master/train.json')
df = pd.read_json(file_path, lines=True)

question = df["question"][0]
options = df["options"][0]
answer = df["correct"][0]

_options = (",".join(options))
_options = _options.replace(",", " ")
problem = question + " " + _options

def replace(index):
    question = df["question"][index]
    print(question)
    print("")

    nums = re.findall("\d+", question)

    for i in range(len(nums)):
        x = question.find(",000")
        y = question.find("0.")

        if nums[i][0] != '0':
            _index = question.find(nums[i])
            for j in range(len(nums[i])):
                question = question[:_index] + question[_index+1:]
            question = question[:_index] + f"<{i}>" + question[_index:]
        if (x != -1):
            __index = x
            for j in range(4):
                question = question[:__index] + question[__index+1:]
        if (y != -1):
            ___index = y
            for j in range(2):
                question = question[:___index] + question[___index+1:]
    print(question)


if __name__ == "__main__":
    for i in range(10):
        replace(i)
        print('\n\n')

