import requests as re
import json
import http.client
import asyncio
from urllib.parse import urlparse


class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434") -> None:
        self.base_url = base_url
        parsed_url = urlparse(base_url)
        self._HTTPclient = http.client.HTTPConnection(parsed_url.netloc)
    
    def generate(self, model:str, prompt:str,system:str=None) -> dict:
        # input checks
        if not model:
            raise ValueError("No model provided.")
        
        # prepare API body
        body = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        if system:
            body["system": system]

        # perform API request
        headers = {'Content-type': 'application/json'}
        self._HTTPclient.request("POST", "/api/generate", json.dumps(body), headers)
        response = self._HTTPclient.getresponse()

        if not response.status == 200:
            raise AssertionError(f"Ollama Server returns http status code: {response.status_code}")

        return json.loads(response.read().decode())

    def chat(self, model:str, messages:list) -> dict:
        # input checks
        if not model:
            raise ValueError("No model provided.")
        for message in messages:
            if not isinstance(message, dict):
                raise TypeError("Messages must be a list of dict-like objects")
            if not (role := message.get("role")) or role not in ["system", "user", "assistant"]:
                raise ValueError('messages must contain a role and it must be one of "system", "user", or "assistant"')
            if "content" not in message:
                raise ValueError("Messages must contain content")

        # prepare API body
        body = {
            "model": model,
            "messages": messages,
            "stream": False
        }

        # perform API request
        headers = {'Content-type': 'application/json'}
        self._HTTPclient.request("POST", "/api/chat", json.dumps(body), headers)
        response = self._HTTPclient.getresponse()
        if not response.status == 200:
            raise AssertionError(f"Ollama Server returns http status code: {response.status_code}")
        return json.loads(response.read().decode())

    def list_models(self) -> None:
        self._HTTPclient.request("GET", "/api/tags")
        response = self._HTTPclient.getresponse()
        if not response.status == 200:
            raise AssertionError(f"Ollama Server returns http status code: {response.status_code}")
        return json.loads(response.read().decode())


# class OllamaClientRequests:
#     def __init__(self, base_url:str ="http://localhost:11434") -> None:
#         self.base_url = base_url
#         self._session = re.Session()

#     def generate(self, model:str, prompt:str,system:str=None, stream:bool=False) -> dict:
#         # input checks
#         if not model:
#             raise ValueError("No model provided.")
        
#         # prepare API body
#         body = {
#             "model": model,
#             "prompt": prompt,
#             "stream": stream
#         }
#         if system:
#             body["system": system]

#         # perform API request
#         response = self._session.post(
#             url=self.base_url+"/api/generate",
#             proxies={"no":"pass"},   # workaround to disable global proxy, see https://github.com/psf/requests/issues/879
#             json=body
#         )
#         if not response.status_code == 200:
#             raise AssertionError(f"Ollama Server returns http status code: {response.status_code}")

#         if not stream:
#             return json.loads(response.content.decode())
#         else:
#             stream_snippets = []
#             for elem in response.content.decode().split("\n")[0:-1]:
#                 stream_snippets.append(json.loads(elem))
#             return stream_snippets
    
#     def chat(self, model:str, messages:list) -> dict:
#         # input checks
#         if not model:
#             raise ValueError("No model provided.")
#         for message in messages:
#             if not isinstance(message, dict):
#                 raise TypeError("Messages must be a list of dict-like objects")
#             if not (role := message.get("role")) or role not in ["system", "user", "assistant"]:
#                 raise ValueError('messages must contain a role and it must be one of "system", "user", or "assistant"')
#             if "content" not in message:
#                 raise ValueError("Messages must contain content")

#         # perform API request
#         response = self._session.post(
#             url=self.base_url+"/api/chat",
#             proxies={"no":"pass"},   # workaround to disable global proxy, see https://github.com/psf/requests/issues/879
#             json={"model":model,
#                   "messages":messages,
#                   "stream":False
#                   }
#         )
#         if not response.status_code == 200:
#             raise AssertionError(f"Ollama Server returns http status code: {response.status_code}")
#         return json.loads(response.content.decode())

#     def list_models(self) -> None:
#         response = self._session.get(
#             url=self.base_url+"/api/tags"
#         )
#         if not response.status_code == 200:
#             raise AssertionError(f"Ollama Server returns http status code: {response.status_code}")
#         return json.loads(response.content.decode())


# class AsyncOllamaClientRequests:
#     def __init__(self, base_url:str ="http://localhost:11434") -> None:
#         self.base_url = base_url
#         self._session = re.Session()

#     async def generate(self, model:str, prompt:str, stream:bool=False):
#         with self._session.post(
#             url=self.base_url+"/api/generate",
#             proxies={"no":"pass"},   # workaround to disable global proxy, see https://github.com/psf/requests/issues/879
#             json={"model":model,
#                   "prompt":prompt,
#                   "stream":stream
#                   },
#             stream=stream
#         ) as response:
#             for line in response.iter_lines(decode_unicode=True):
#                 if line:
#                     yield json.loads(line.decode())

#     async def chat(self, model:str, messages:list, stream:bool=False):
#         with self._session.post(
#             url=self.base_url+"/api/chat",
#             proxies={"no":"pass"},   # workaround to disable global proxy, see https://github.com/psf/requests/issues/879
#             json={"model":model,
#                   "messages":messages,
#                   "stream":stream
#                   },
#             stream=stream
#         ) as response:
#             for line in response.iter_lines(decode_unicode=True):
#                 if line:
#                     yield json.loads(line.decode())

#     async def list_models(self):
#         response = self._session.get(
#             url=self.base_url+"/api/ps"
#         )
#         return json.loads(response.decode())


class AsyncOllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434") -> None:
        self.base_url = base_url
        parsed_url = urlparse(base_url)
        self._HTTPclient = http.client.HTTPConnection(parsed_url.netloc)

    async def generate(self, model:str, prompt:str,system:str=None, stream:bool = False):
        headers = {'Content-type': 'application/json'}
        body = {
            "model": model,
            "prompt": prompt,
            "stream": stream
        }
        if system:
            body["system"] = system

        self._HTTPclient.request("POST", "/api/generate", json.dumps(body), headers)
        response = self._HTTPclient.getresponse()

        if not stream:
            response_str = response.read().decode()
            yield json.loads(response_str)

        else:
        # If streaming, process each line as it arrives
            buffer = ""
            while True:
                chunk = response.read(1).decode()
                if not chunk:
                    break
                buffer += chunk
                if buffer.endswith('\n'):
                    line = buffer.strip()
                    buffer = ""
                    yield json.loads(line)

    async def chat(self, model: str, messages: list, stream: bool = False):
        headers = {'Content-type': 'application/json'}
        body = json.dumps({
            "model": model,
            "messages": messages,
            "stream": stream
        })

        self._HTTPclient.request("POST", "/api/chat", body, headers)
        response = self._HTTPclient.getresponse()
        if not response.status == 200:
            raise AssertionError(f"Ollama Server returns http status code: {response.status_code}")

        if not stream:
            response_str = response.read().decode()
            yield json.loads(response_str)
        else:
            buffer = ""
            while True:
                chunk = response.read(1).decode()
                if not chunk:
                    break
                buffer += chunk
                if buffer.endswith('\n'):
                    line = buffer.strip()
                    buffer = ""
                    yield json.loads(line)

    async def list_models(self):
        self._HTTPclient.request("GET", "/api/ps")
        response = self._HTTPclient.getresponse()
        response_str = response.read().decode()
        return json.loads(response_str)


#----------------------------------------------------------------------


class Ollama:
    def __init__(self, model:str="llama3", system:str=None, base_url:str ="http://localhost:11434") -> None:
        self.base_url = base_url
        self._client = OllamaClient(base_url)
        self.model = model
        available_models = self.list_models()
        if not model in available_models:
            raise ValueError(f"Model not installed in Ollama. Available models are {available_models}")
        self.system = system
        self.messages = []
        if system:
            self.messages.append({"role": "system", "content":system})
        self._asyncclient = AsyncOllamaClient(base_url)

    def generate(self, prompt:str) -> str:
        response = self._OllamaClient.generate(model=self.model, prompt=prompt, system=self.system)
        return response["response"]
    
    def chat(self, prompt:str) -> str:
        self.messages.append({"role":"user", "content":prompt})
        response = self._client.chat(model=self.model, messages=self.messages)
        msg = response["message"]
        self.messages.append(msg)
        return msg["content"]
    
    def list_models(self) -> list:
        models_dict = self._client.list_models()["models"]
        model_names = []
        for model in models_dict:
            model_names.append(model["name"].split(":latest")[0])
        return model_names
    
    async def agenerate(self, prompt:str, stream:bool=True):
        msg_str = ""
        async for partial_response in self._asyncclient.generate(
            model=self.model, 
            prompt=prompt, 
            system=self.system, 
            stream=stream
            ):
            if not partial_response["done"]:
                msg_str = msg_str + partial_response["content"]
            yield partial_response["content"]

    async def achat(self, prompt:str, stream:str=True):
        self.messages.append({"role":"user", "content":prompt})
        msg_str = ""
        async for partial_response in self._asyncclient.chat(self.model, self.messages, stream=stream):
            if not partial_response["done"]:
                msg_str = msg_str + partial_response["message"]["content"]
            yield partial_response["message"]["content"]
        self.messages.append({"role":"assistant", "content":msg_str})


#----------------------------------------------------------------------


async def async_test_client():
    AsyncClient = AsyncOllamaClient()
    model = "llama3"
    messages = [{"role":"user", "content":"Who are you?"}]
    isStream = False
    chunks = []
    async for partial_response in AsyncClient.chat(model, messages, stream=isStream):
        print(partial_response)
        chunks.append(partial_response)
    return chunks

async def async_test_model():
    LLM = Ollama(model="llama3", system="You are a Pirat. Answer everything in pirate language.")
    async for partial_response in LLM.achat(prompt="My name is Tom.", stream=True):
        print(partial_response)
    print("---")
    print(LLM.messages)

if __name__ == "__main__":
    # synchron client test
    client = OllamaClient()
    response = client.generate("llama3", "Who are you?")
    print(response)

    # synchron model test
    LLM = Ollama(model="llama3")
    a1 = LLM.chat("My name is tom!")
    a2 = LLM.chat("What is my name?")
    models_list = LLM.list_models()
    print(LLM.list_models())

    ## asynchron client test
    # chunks = asyncio.run(async_test_client())

    ## asynchron model test
    # asyncio.run(async_test_model())






    