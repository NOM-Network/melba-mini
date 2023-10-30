from llama_cpp import Llama
import chromadb
from dataclasses import dataclass


@dataclass(init=False)
class PromptConfig:
    system_prefix: str
    system_suffix: str
    user_prefix: str
    user_suffx: str
    model_prefix: str
    model_suffix: str

    def build_system_prompt(self, message):
        return f"{self.system_prefix}{message}{self.system_suffix}\n"

    def build_user_prompt(self, message):
        return f"{self.user_prefix}{message}{self.user_suffix}\n"

    def build_model_response(self, model_response):
        return f"{self.model_prefix}{model_response}{self.model_suffix}\n"

    def build_prompt(self, system_message, user_message, history):
        return f"{self.build_system_prompt(system_message)}{history}{self.build_user_prompt(user_message)}{self.model_prefix}"


@dataclass(init=False)
class PygmalionPromptConfig(PromptConfig):
    def __init__(self):
        self.system_prefix = "<|system|>"
        self.system_suffix = ""
        self.user_prefix = "<|system|>"
        self.user_suffix = ""
        self.model_prefix = "<|model|>"
        self.model_suffix = ""


@dataclass(init=False)
class MistralPromptConfig(PromptConfig):
    def __init__(self):
        self.system_prefix = "<|im_start|>system\n"
        self.system_suffix = "<|im_end|>"
        self.user_prefix = "<|im_start|>user\n"
        self.user_suffix = "<|im_end|>"
        self.model_prefix = "<|im_start|>assistant\n"
        self.model_suffix = "<|im_end|>"


class MelbaLLM:
    def __init__(self, model_path, prompt_config, n_ctx=1024):
        self.llm = Llama(model_path=model_path, n_gpu_layers=-1, n_ctx=n_ctx)
        self.n_ctx = n_ctx
        # TODO: dynamic system prompt
        with open("generic_prompt.txt", "r") as f:
            system_prompt = f.read()
        # TODO: allow configuring model name
        self.system_prompt = system_prompt.replace("{llmName}", "Melba").strip()
        self.prompt_config = prompt_config

    # Allow checking the prompt size before trying to get a response
    # It needs to fit into the context size and have some space left for the response
    def check_prompt_size(self, prompt, history):
        prompt = self.prompt_config.build_prompt(self.system_prompt, prompt, history)
        prompt_size = len(self.llm.tokenize(prompt.encode()))
        response_headroom = 100
        if prompt_size > (self.n_ctx - 100):
            return False
        else:
            return True

    def get_response(self, prompt, history):
        prompt = self.prompt_config.build_prompt(self.system_prompt, prompt, history)
        #print(f"Full prompt:\n{prompt}")
        # TODO: make stop condition dependent on currently used model
        return self.llm(prompt, stop=["<|user", "<|im_"])["choices"][0]["text"]


class MelbaMemory:
    def __init__(self, prompt_config):
        self.client = chromadb.PersistentClient("db")
        self.collection = self.client.get_or_create_collection(name="MelbaMemory")

        self.prompt_config = prompt_config

    def _get_id(self, type: str, identifier: str):
        result = self.collection.get(
            where={
                "$and": [{"type": {"$eq": type}}, {"identifier": {"$eq": identifier}}]
            }
        )
        if len(result["ids"]) > 0:
            return result["ids"][0]
        else:
            return None

    def get_chat_history(self, username: str):
        document_id = self._get_id(type="chatlog", identifier=username)
        if document_id is not None:
            history_documents = self.collection.get(ids=document_id)["documents"]
            return history_documents[0]
        else:
            return ""
        return history

    def update_chat_history(self, username: str, user_prompt: str, llm_response: str):
        document_id = self._get_id(type="chatlog", identifier=username)
        chat_history = self.get_chat_history(username)
        added_history = f"{self.prompt_config.build_user_prompt(user_prompt)}{self.prompt_config.build_model_response(llm_response)}"
        #print("Old:")
        #print(chat_history)
        #print("Added:")
        #print(added_history)
        chat_history = f"{chat_history}{added_history}"
        metadata = {"type": "chatlog", "identifier": username}
        if document_id is None:
            document_id = str(self.collection.count() + 1)
        self.collection.upsert(
            ids=document_id, metadatas=metadata, documents=chat_history
        )

    def truncate_chat_history(self, username):
        document_id = self._get_id(type="chatlog", identifier=username)
        if document_id is None:
            return
        chat_history = self.get_chat_history(username)

        first_user = chat_history.find("<|user|>")
        first_model = chat_history.find("<|model|>")
        first_part = min(first_user, first_model)  # To be trimmed
        second_part = max(first_user, first_model)
        chat_history = chat_history[second_part:]

        metadata = {"type": "chatlog", "identifier": username}
        self.collection.upsert(
            ids=document_id, metadatas=metadata, documents=chat_history
        )


class Melba:
    def __init__(self):
        prompt_config = MistralPromptConfig()
        self.llm = MelbaLLM("./openhermes-2-mistral-7b.Q6_K.gguf", prompt_config)
        self.memory = MelbaMemory(prompt_config)

    def get_response(self, prompt, username):
        chat_history = self.memory.get_chat_history(username)
        while not self.llm.check_prompt_size(prompt, chat_history):
            chat_history = self.memory.truncate_chat_history(username)
        response = self.llm.get_response(prompt, chat_history)
        #print(f"LLM Response:{response}")
        self.memory.update_chat_history(username, prompt, response)
        return response
