class OpenAIModel:
    def __init__(self, name, max_token, encoding_base):
        self.name = name
        self.max_token = max_token
        self.encoding_base = encoding_base


models = {
    'gpt-3.5-turbo': OpenAIModel('gpt-3.5-turbo', 4096, 'cl100k_base'),
    'gpt-4': OpenAIModel('gpt-4', 8192, 'cl100k_base'),
}
