# from transformers import RobertaTokenizer, T5ForConditionalGeneration
import ast
# import inspect

import requests

API_URL = "https://api-inference.huggingface.co/models/pasho/codesapiens-poc-code-summarization"
headers = {"Authorization": "Bearer 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"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def ask_to_trained_model(input_text):
    # tokenizer = RobertaTokenizer.from_pretrained(
    #     'pasho/codesapiens-poc-code-summarization')

    # model = T5ForConditionalGeneration.from_pretrained(
    #     'pasho/codesapiens-poc-code-summarization')

    # input_ids = tokenizer(input_text, return_tensors="pt").input_ids

    # # simply generate a single sequence
    # generated_ids = model.generate(input_ids, max_length=10)
    # return tokenizer.decode(generated_ids[0], skip_special_tokens=True)

    # 👆 Previous implementation, current issues with heroku lead to using api :(
    output = query({
        "inputs": input_text,
    })
    print('******* RESPONSE *******')
    print('******* RESPONSE *******')
    print(output)
    return output[0]['generated_text']


def get_functions_from_file_in_plain_text(file_path):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()

        # Parse the file content
        tree = ast.parse(file_content)

        # Extracting function definitions
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Get start and end line numbers
                start_line = node.lineno - 1
                end_line = node.end_lineno if hasattr(
                    node, 'end_lineno') else start_line + 1

                # Extract the function code
                function_code = file_content.splitlines()[start_line:end_line]
                function_text = "\n".join(function_code)

                # Append function name and code as a tuple
                functions.append((node.name, function_text))

        return functions
    except Exception as e:
        return []
