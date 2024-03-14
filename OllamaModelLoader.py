import json
from langchain.llms import Ollama

class OllamaModelLoader:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path

    def load_ollama_model(self):
        with open(self.config_file_path, 'r') as config_file:
            config = json.load(config_file)

        model_kwargs = {key: value for key, value in config.items() if key != 'model' and value is not None}
        model = config.get('model')

        return Ollama(model=model, **model_kwargs)

