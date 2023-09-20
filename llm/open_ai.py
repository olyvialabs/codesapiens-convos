import os
from pathlib import Path

import openai
from langchain.prompts import PromptTemplate
from config.settings import settings
from config.open_ai_models import models
from datetime import datetime
from typing import Dict
from llm.tokens import get_tokens_length
from config.settings import settings
openai.api_key = settings.OPENAI_API_KEY


class ConversationlessOpenAI:
    def __init__(self, temperature, model):
        self.temperature = temperature
        self.model = model

    def query(self, prompt):
        # The max_tokens parameter is shared between the prompt and the completion
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
        )
        return response.choices[0].message['content']


def get_file(path: str):
    file_path = f"{path}"
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Cannot find path {file_path}")

    with open(file_path, "r") as f:
        return f.read()


def get_template(template: str = ''):
    return get_file(f"templates/{template}.txt")


def generate_prompt_by_template(data={}, template: str = '') -> PromptTemplate:
    question_template = get_template(template)

    prompt_template = PromptTemplate.from_template(question_template)
    formatted_prompt = prompt_template.format(**data)
    print(f"Formatted Prompt: {formatted_prompt}")
    return formatted_prompt


def generate_prompt_and_fit_file_content(data={}, template: str = '', max_tokens: int = models['gpt-3.5-turbo'].max_token):
    # TODO: remover cierta cantidad de caracteres del final del file_content
    # despues de cierto limite solo para estar seguro de que no se pase de los tokens
    # porque ya ha habido casos que tiktoken no calcjula bien
    # por ejemplo: para el gpt-3.5-turbo, endado caso que sea > 3900 retarle unos 100 tokens menos
    question_template = get_template(template)
    prompt_length = 0
    file_content = data['trimmable_content']
    while prompt_length > max_tokens or prompt_length == 0:
        prompt_template = PromptTemplate.from_template(question_template)
        data['trimmable_content'] = file_content
        prompt_template = prompt_template.format(
            **data)
        prompt_length = get_tokens_length(prompt_template)
        # remove last 5 characters
        file_content = file_content[:-5]
    return prompt_template


# save_to is a relative path, not absolute. value example : '/Configuration'
def get_gpt_response_from_template(data={}, template: str = '', model=models['gpt-3.5-turbo'].name, max_tokens=models['gpt-3.5-turbo'].max_token, trim_content: bool = False, trim_path: str = '', save_to_subfolder: str = '', save_to_name: str = ''):
    if not template:
        raise ValueError("Template name is required")
    if trim_content:
        # Only replace if path is provided
        print(f"Trim path: {trim_path}")
        if trim_path:
            data['trimmable_content'] = get_file(trim_path)
        prompt = generate_prompt_and_fit_file_content(
            data=data, template=template, max_tokens=max_tokens)
    else:
        prompt = generate_prompt_by_template(data=data, template=template)

    llm = ConversationlessOpenAI(temperature=0.2,
                                 model=model)

    print(f"{datetime.now().strftime('%H:%M:%S')} - Asking answer with template {template}")
    response = llm.query(prompt)
    print(f"{datetime.now().strftime('%H:%M:%S')} - Received answer with template {template}")
    print(f"{settings.output_folder} tf? {save_to_subfolder}")
    if save_to_subfolder and save_to_name:
        folder_to_save_path = f'{settings.output_folder}/{save_to_subfolder}'
        Path(folder_to_save_path).mkdir(parents=True, exist_ok=True)

        with open(f"{folder_to_save_path}/{save_to_name}", "w") as f:
            f.write(response)
    return response
