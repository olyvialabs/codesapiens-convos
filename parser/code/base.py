import ast
import os
from pathlib import Path

import tiktoken
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from config.settings import settings


def parse_functions(functions_dict, formats, dir):
    c1 = len(functions_dict)
    for i, (source, functions) in enumerate(functions_dict.items(), start=1):
        print(f"Processing file {i}/{c1}")
        print(source, functions, "functions")
        # .replace("." + formats, ".md")
        source_w = source.replace(dir + "/", "").replace('.js', '.md')
        subfolders = "/".join(source.split("/")[:-1])
        Path(f"outputs/{subfolders}").mkdir(parents=True, exist_ok=True)
        for j, (name, function) in enumerate(functions.items(), start=1):
            print(f"Processing function {j}/{len(functions)}")
            prompt = PromptTemplate(
                input_variables=["code"],
                template="Code: \n{code}, \nDocumentation: ",
            )
            llm = OpenAI(temperature=0, openai_api_key=settings.OPENAI_API_KEY)
            response = llm(prompt.format(code=function))
            mode = "a" if Path(f"outputs/{source_w}").exists() else "w"
            with open(f"outputs/{source_w}", mode) as f:
                f.write(
                    f"\n\n# Function name: {name} \n\nFunction: \n```\n{function}\n```, \nDocumentation: \n{response}")


def parse_classes(classes_dict, formats, dir):
    c1 = len(classes_dict)
    for i, (source, classes) in enumerate(classes_dict.items()):
        print(f"Processing file {i + 1}/{c1}")
        source_w = source.replace(dir + "/", "").replace("." + formats, ".md")
        subfolders = "/".join(source_w.split("/")[:-1])
        Path(f"outputs/{subfolders}").mkdir(parents=True, exist_ok=True)
        for name, function_names in classes.items():
            print(f"Processing Class {i + 1}/{c1}")
            prompt = PromptTemplate(
                input_variables=["class_name", "functions_names"],
                template="Class name: {class_name} \nFunctions: {functions_names}, \nDocumentation: ",
            )
            llm = OpenAI(temperature=0, openai_api_key=settings.OPENAI_API_KEY)
            response = llm(prompt.format(class_name=name,
                           functions_names=function_names))

            with open(f"outputs/{source_w}", "a" if Path(f"outputs/{source_w}").exists() else "w") as f:
                f.write(
                    f"\n\n# Class name: {name} \n\nFunctions: \n{function_names}, \nDocumentation: \n{response}")


def transform_to_docs(functions_dict, classes_dict, dir):
    formats = [".rst", ".md"]
    docs_content = ''.join([str(key) + str(value)
                           for key, value in functions_dict.items()])
    docs_content += ''.join([str(key) + str(value)
                            for key, value in classes_dict.items()])

    num_tokens = len(tiktoken.get_encoding("cl100k_base").encode(docs_content))
    total_price = ((num_tokens / 1000) * 0.02)

    print(f"Total price: {total_price} USD")
    if not Path("outputs").exists():
        Path("outputs").mkdir()
    parse_functions(functions_dict, formats, dir)
    parse_classes(classes_dict, formats, dir)
    print("All done!")
