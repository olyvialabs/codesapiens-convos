import os
from pathlib import Path
import openai
from langchain.prompts import PromptTemplate
from config.settings import settings
from config.open_ai_models import models
from datetime import datetime
from llm.tokens import get_tokens_length
import time
import signal

# Define a custom exception for timeout


class TimeoutException(Exception):
    pass

# Define the signal handler function


def timeout_handler(signum, frame):
    raise TimeoutException()


# Set the signal handler for the SIGALRM signal
signal.signal(signal.SIGALRM, timeout_handler)

openai.api_key = settings.OPENAI_API_KEY


class ConversationlessOpenAI:
    def __init__(self, temperature, model):
        self.temperature = temperature
        self.model = model

    def query(self, prompt):
        max_retries = 10
        for attempt in range(max_retries):
            try:
                signal.alarm(20)  # Set the alarm for 20 seconds
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.temperature,
                )
                signal.alarm(0)  # Reset the alarm
                return response.choices[0].message['content'], None
            except TimeoutException:
                print("Request timed out, retrying...")
                signal.alarm(0)  # Reset the alarm
                if attempt < max_retries - 1:
                    time.sleep(1)  # Wait for 1 second before retrying
                continue  # Continue to the next iteration to retry
            except openai.error.Timeout:
                print("OpenAI Timeout, retrying...")
                if attempt < max_retries - 1:
                    time.sleep(1)
                continue
            # Add other exception handlers as required
            except (openai.error.APIError, openai.error.InvalidRequestError,
                    openai.error.AuthenticationError,
                    Exception) as e:
                print('OPENAI CALL ERROR', e)
                return None, 'OPENAI_API_ERROR'


def get_file(path: str):
    file_path = f"{path}"
    if not os.path.exists(file_path):
        return None, 'FILE_NOT_FOUND'
    try:
        with open(file_path, "r") as f:
            return f.read(), None
    except IOError:
        return None, 'TEMPLATE_IO_ERROR'
    except Exception as e:
        print('get file', e)
        return None, 'TEMPLATE_IO_UNKNOWN_ERROR'


def get_template(template: str = ''):
    content, error = get_file(f"templates/{template}.txt")
    if error:
        print('get template', error)
        return None, error
    return content, None


def generate_prompt_by_template(data={}, template: str = ''):
    question_template, error = get_template(template)
    if error:
        return None, error
    try:
        prompt_template = PromptTemplate.from_template(question_template)
        formatted_prompt = prompt_template.format(**data)
        return formatted_prompt, None
    except KeyError:
        return None, 'TEMPLATE_KEY_ERROR_IMPORTING_TEMPLATE'
    except Exception as e:
        return None, 'TEMPLATE_KEY_IMPORATING_UNKNOWN_ERROR'


def generate_prompt_and_fit_file_content(data={}, template: str = '', max_tokens: int = models['gpt-3.5-turbo'].max_token):
    optimistic_max_tokens = max_tokens * 0.95
    question_template, error = get_template(template)
    if error:
        return None, error

    prompt_length = 0
    file_content = data.get('trimmable_content', '')
    while prompt_length > optimistic_max_tokens or prompt_length == 0:
        try:
            prompt_template = PromptTemplate.from_template(question_template)
            data['trimmable_content'] = file_content
            formatted_prompt = prompt_template.format(**data)
            prompt_length = get_tokens_length(formatted_prompt)
            file_content = file_content[:-5]
        except KeyError:
            print(
                'generate prompt and fit file content error TEMPLATE_KEY_ERROR_IN_TEMPLATE')
            return None, 'TEMPLATE_KEY_ERROR_IN_TEMPLATE'
        except Exception as e:
            print('generate prompt and fit file content error')
            return None, 'TEMPLATE_KEY_UNKNOWN_ERROR'
    return formatted_prompt, None


def get_gpt_response_from_template(data={}, template: str = '', model=models['gpt-3.5-turbo'].name, max_tokens=models['gpt-3.5-turbo'].max_token, trim_content: bool = False, ignore_output_folder_on_save: bool = False, trim_path: str = '', save_to_subfolder: str = '', save_to_name: str = ''):
    print('TRING FOR')
    print('TRING FOR')
    print('TRING FOR')
    print('TRING FOR')
    print('TRING FOR')
    print(data)
    print('$$====-=-=-=-=-=-=-=-$$')
    if not template:
        return None, 'TEMPLATE_NAME_REQUIRED'

    if trim_content and trim_path:
        data['trimmable_content'], error = get_file(trim_path)
        if error:
            return None, error

    if trim_content:
        prompt, error = generate_prompt_and_fit_file_content(
            data=data, template=template, max_tokens=max_tokens)
    else:
        prompt, error = generate_prompt_by_template(
            data=data, template=template)

    if error:
        return None, error

    llm = ConversationlessOpenAI(temperature=0.2, model=model)
    response, error = llm.query(prompt)

    if error:
        return None, error

    if save_to_subfolder and save_to_name:
        saving_path = Path(save_to_subfolder) if ignore_output_folder_on_save else Path(
            settings.output_folder) / save_to_subfolder
        saving_path.mkdir(parents=True, exist_ok=True)
        file_path = saving_path / save_to_name

        try:
            with file_path.open("w") as f:
                f.write(response)
        except IOError:
            return None, 'SAVE_TO_FILE_ERROR'
        except Exception as e:
            print('saving to folder error', e)
            return None, 'SAVE_TO_FILE_UNKNOWN_ERROR'
    return response, None
