"""Universal AI Interface (UAII) for OpenAI GPT-4 and (eventually) other AI models."""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Literal, Generator
from openai import OpenAI
from google import generativeai as genai
from typing import overload

from .utils import Logger, SimpleLogger

import pdb



"""
TODO: long term want this to be more flexible/generic
mixin classes to cover different features that LLMs may have (text, images, audio, video)
class GPT4o: ...
class GPT4Vision: ...
use __new__ to look at the model type and return the appropriate class for type hints

class OpenAIAgent:
    @overload
    def __new__(cls, model: Literal['gpt-4o', 'gpt-4o-mini'], timeout=None) -> GPT4o: ...
    @overload
    def __new__(cls, model: Literal['gpt-4v', 'gpt-4v-mini'], timeout=None) -> GPT4Vision: ...
    def __new__(cls, model: OpenAIModel, timeout=None):
        if model in ['gpt-4o', 'gpt-4o-mini']:
            return GPT4o(model, timeout)
        elif model in ['gpt-4v', 'gpt-4v-mini']:
            return GPT4Vision(model, timeout)
        elif:
            ...
"""


class UAII(ABC):
    @abstractmethod
    def multishot(self, messages: list[dict], stream:bool=False, **kwargs) -> Generator[str, None, None]|str: ...
    @abstractmethod
    def oneshot(self, query:str, stream:bool=False, **kwargs) -> Generator[str, None, None]|str: ...
    @abstractmethod
    def message(self, message:str, stream:bool=False, **kwargs) -> Generator[str, None, None]|str: ...
    @abstractmethod
    def clear_messages(self): ...
    @abstractmethod
    def set_system_prompt(self, prompt:str): ...


################## For now, only OpenAIAgent uses this ##################

class OpenAIRole(str, Enum):
    system = "system"
    assistant = "assistant"
    user = "user"

class OpenAIMessage(dict):
    def __init__(self, role: OpenAIRole, content: str):
        super().__init__(role=role.value, content=content)


OpenAIModel = Literal['gpt-4o', 'gpt-4o-mini', 'o1-preview', 'o1-mini', 'gpt-4', 'gpt-4-turbo']

class OpenAIAgent(UAII):
    def __init__(self, model: OpenAIModel, system_prompt:str|None, timeout:float|None=None):
        self.model = model
        self.timeout = timeout
        self.messages: list[OpenAIMessage] = []
        self.set_system_prompt(system_prompt)
        
    def _chat_gen(self, messages: list[OpenAIMessage], **kwargs) -> Generator[str, None, None]:
        client = OpenAI()
        gen = client.chat.completions.create(
            model=self.model,
            messages=[*self.system_prompt, *messages],
            timeout=self.timeout,
            stream=True,
            temperature=0.0,
            **kwargs
        )
        chunks: list[str] = []
        for chunk in gen:
            try:
                content = chunk.choices[0].delta.content
                if content:
                    chunks.append(content)
                    yield content
            except:
                pass
    
        # save the agent response to the list of messages
        messages.append(OpenAIMessage(role=OpenAIRole.assistant, content=''.join(chunks)))
        self.messages = messages

    @overload
    def multishot(self, messages: list[OpenAIMessage], stream:Literal[True], **kwargs) -> Generator[str, None, None]: ...
    @overload
    def multishot(self, messages: list[OpenAIMessage], stream:Literal[False]=False, **kwargs) -> str: ...
    def multishot(self, messages: list[OpenAIMessage], stream:bool=False, **kwargs) -> Generator[str, None, None]|str:
        gen = self._chat_gen(messages, **kwargs)
        return gen if stream else ''.join([*gen])
    
    @overload
    def oneshot(self, query:str, stream:Literal[True], **kwargs) -> Generator[str, None, None]: ...
    @overload
    def oneshot(self, query:str, stream:Literal[False]=False, **kwargs) -> str: ...
    def oneshot(self, query:str, stream:bool=False, **kwargs) -> Generator[str, None, None]|str:
        self.clear_messages()
        self.messages.append(OpenAIMessage(role=OpenAIRole.user, content=query))
        return self.multishot(self.messages, stream=stream, **kwargs)
    
    @overload
    def message(self, message:str, stream:Literal[True], **kwargs) -> Generator[str, None, None]: ...
    @overload
    def message(self, message:str, stream:Literal[False]=False, **kwargs) -> str: ...
    def message(self, message:str, stream:bool=False, **kwargs) -> Generator[str, None, None]|str:
        self.messages.append(OpenAIMessage(role=OpenAIRole.user, content=message))
        return self.multishot(self.messages, stream=stream, **kwargs)

    def clear_messages(self):
        self.messages = []
    
    def set_system_prompt(self, system_prompt:str|None):
        self.system_prompt: tuple[()] | tuple[OpenAIMessage] = (
            (OpenAIMessage(role=OpenAIRole.system, content=system_prompt),) 
            if system_prompt else ()
        )





################## For now, keeping gemini agent completely separate ##################

class GeminiRole(str, Enum):
    model = "model"
    user = "user"

class GeminiMessage(dict):
    def __init__(self, role: GeminiRole, parts: list[str]):
        super().__init__(role=role.value, parts=parts)


GeminiModel = Literal['gemini-1.5-flash-001', 'gemini-1.5-pro-001']


class GeminiAgent(UAII):
    def __init__(
            self,
            model: GeminiModel,
            cache_key:str|None,
            system_prompt:str,
            cache_content:str,
            ttl_seconds:int,
            logger:Logger=SimpleLogger()
        ):
        """
        Gemini agent with conversation caching

        Args:
            model (GeminiModel): The model to use for the Gemini API
            cache_key (str): The key used to retrieve the cached API chat
            system_prompt (str): The system prompt for the Gemini API chat
            cache_content (str): The content to cache for the Gemini API chat
            ttl_seconds (int): The time-to-live in seconds for the Gemini API cache.
            logger (Logger, optional): The logger to use for the Gemini API chat. Defaults to SimpleLogger()
        """
        self.model = model
        self.system_prompt = system_prompt
        self.cache_key = cache_key
        self.cache_content = cache_content
        self.cache: genai.caching.CachedContent = None
        self.ttl_seconds = ttl_seconds
        self.logger = logger

        self.messages: list[GeminiMessage] = []

    def load_cache(self):
        """Load the cache for the Gemini API chat instance. Raises an exception if unable to make/load the cache."""
        # Don't cache if cache_key is None
        if self.cache_key is None:
            raise ValueError('cache_key is None')

        # Don't need to load cache if it's already loaded
        if self.cache is not None:
            return

        caches = genai.caching.CachedContent.list()
        try:
            self.cache, = filter(lambda c: c.display_name == self.cache_key, caches)
            self.logger.info({'cache': f'found cached content for "{self.cache_key}"'})

        except ValueError:
            self.logger.info({'cache': f'No cached content found for "{self.cache_key}". pushing new instance.'})
            # this may also raise an exception if the cache content is too small
            self.cache = genai.caching.CachedContent.create(
                model=self.model,
                display_name=self.cache_key,
                system_instruction=self.system_prompt,
                contents=self.cache_content,
                ttl=self.ttl_seconds,
            )

    def _chat_gen(self, messages: list[GeminiMessage], **kwargs) -> Generator[str, None, None]:
        try:
            self.load_cache()
            model = genai.GenerativeModel.from_cached_content(cached_content=self.cache)
            system_messages: tuple[()] = ()
        except Exception as e:
            if 'Cached content is too small' not in str(e) and 'cache_key is None' not in str(e):
                raise
            # if cache is too small, just run the model from scratch without caching
            self.logger.info({'cache': f'{e}. Running model without cache.'})
            model = genai.GenerativeModel(model_name=self.model, system_instruction=self.system_prompt, **kwargs)
            system_messages: tuple[GeminiMessage] = (GeminiMessage(role=GeminiRole.model, parts=[self.cache_content]),)

        response = model.generate_content([*system_messages, *messages], stream=True, **kwargs)
        chunks: list[str] = []
        for chunk in response:
            try:
                content = chunk.text
                if content:
                    chunks.append(content)
                    yield content
            except:
                pass
        
        # save the agent response to the list of messages
        messages.append(GeminiMessage(role=GeminiRole.model, parts=[''.join(chunks)]))
        self.messages = messages

    @overload
    def multishot(self, messages: list[GeminiMessage], stream:Literal[True], **kwargs) -> Generator[str, None, None]: ...
    @overload
    def multishot(self, messages: list[GeminiMessage], stream:Literal[False]=False, **kwargs) -> str: ...
    def multishot(self, messages: list[GeminiMessage], stream:bool=False, **kwargs) -> Generator[str, None, None]|str:
        gen = self._chat_gen(messages, **kwargs)
        return gen if stream else ''.join([*gen])
    
    @overload
    def oneshot(self, query:str, stream:Literal[True], **kwargs) -> Generator[str, None, None]: ...
    @overload
    def oneshot(self, query:str, stream:Literal[False]=False, **kwargs) -> str: ...
    def oneshot(self, query:str, stream:bool=False, **kwargs) -> Generator[str, None, None]|str:
        self.clear_messages()
        self.messages.append(GeminiMessage(role=GeminiRole.user, parts=[query]))
        return self.multishot(self.messages, stream=stream, **kwargs)
    
    @overload
    def message(self, message:str, stream:Literal[True], **kwargs) -> Generator[str, None, None]: ...
    @overload
    def message(self, message:str, stream:Literal[False]=False, **kwargs) -> str: ...
    def message(self, message:str, stream:bool=False, **kwargs) -> Generator[str, None, None]|str:
        self.messages.append(GeminiMessage(role=GeminiRole.user, parts=[message]))
        return self.multishot(self.messages, stream=stream, **kwargs)


    def clear_messages(self):
        self.messages = []
    
    def set_system_prompt(self, system_prompt:str, cache_content:str):
        self.system_prompt = system_prompt
        self.cache_content = cache_content
        self.cache = None



########################################################################################

from anthropic import Anthropic, NotGiven, NOT_GIVEN


class ClaudeRole(str, Enum):
    model = "assistant"
    user = "user"

class ClaudeMessage(dict):
    def __init__(self, role: ClaudeRole, text: str):
        super().__init__(role=role.value, content=[{'type': 'text', 'text': text}])


ClaudeModel = Literal['claude-3-5-sonnet-latest', 'claude-3-5-haiku-latest']


class ClaudeAgent(UAII):
    def __init__(self, model: ClaudeModel, system_prompt: str|NotGiven=NOT_GIVEN, timeout:float|None=None):
        """
        Create a ClaudeAgent instance

        Args:
            model (ClaudeModel): The model to use for the Claude API
            timeout (float, optional): The timeout in seconds for the Claude API. Defaults to None (i.e. no timeout).
        """
        self.model = model
        self.system_prompt = system_prompt
        self.timeout = timeout
        self.messages: list[ClaudeMessage] = []
    
    def _chat_gen(self, messages: list[ClaudeMessage], **kwargs) -> Generator[str, None, None]:
        client = Anthropic()
        chunks: list[str] = []
        with client.messages.stream(
            model=self.model,
            messages=messages,
            timeout=self.timeout,
            max_tokens=1000,
            system=self.system_prompt,
            **kwargs
        ) as gen:
            for chunk in gen.text_stream:
                chunks.append(chunk)
                yield chunk

        # save the agent response to the list of messages
        messages.append(ClaudeMessage(role=ClaudeRole.model, text=''.join(chunks)))
        self.messages = messages
    
    @overload
    def multishot(self, messages: list[ClaudeMessage], stream:Literal[True], **kwargs) -> Generator[str, None, None]: ...
    @overload
    def multishot(self, messages: list[ClaudeMessage], stream:Literal[False]=False, **kwargs) -> str: ...
    def multishot(self, messages: list[ClaudeMessage], stream:bool=False, **kwargs) -> Generator[str, None, None]|str:
        gen = self._chat_gen(messages, **kwargs)
        return gen if stream else ''.join([*gen])
    
    @overload
    def oneshot(self, query:str, stream:Literal[True], **kwargs) -> Generator[str, None, None]: ...
    @overload
    def oneshot(self, query:str, stream:Literal[False]=False, **kwargs) -> str: ...
    def oneshot(self, query:str, stream:bool=False, **kwargs) -> Generator[str, None, None]|str:
        self.clear_messages()
        self.messages.append(ClaudeMessage(role=ClaudeRole.user, text=query))
        return self.multishot(self.messages, stream=stream, **kwargs)

    @overload
    def message(self, message:str, stream:Literal[True], **kwargs) -> Generator[str, None, None]: ...
    @overload
    def message(self, message:str, stream:Literal[False]=False, **kwargs) -> str: ...
    def message(self, message:str, stream:bool=False, **kwargs) -> Generator[str, None, None]|str:
        self.messages.append(ClaudeMessage(role=ClaudeRole.user, text=message))
        return self.multishot(self.messages, stream=stream, **kwargs)
    
    def clear_messages(self):
        self.messages = []

    def set_system_prompt(self, system_prompt:str|NotGiven=NOT_GIVEN):
        self.system_prompt = system_prompt


########################################################################################





if __name__ == "__main__":
    from pathlib import Path
    from easyrepl import REPL
    import yaml
    here = Path(__file__).parent
    with open(here/'api_agent.yaml', 'r') as f:
        base_cache_content:str = yaml.safe_load(f)['apis']['default']['cache_body']
    gdc_docs = (here/'api_documentation/gdc.md').read_text()
    cache_contents = base_cache_content.format(additional_cache_body='', docs=gdc_docs)

    # insert the secret number into the cache
    cache_contents = f'{cache_contents[:len(cache_contents)//2]}\nthe secret number is 23\n{cache_contents[len(cache_contents)//2:]}'
    agent = GeminiAgent(
        "gemini-1.5-flash-001",
        "test_cache",
        'You are a python programmer writing code to perform API requests',
        cache_contents
    )

    messages: list[GeminiMessage] = []
    for query in REPL(history_file='.chat'):
        messages.append(GeminiMessage(role=GeminiRole.user, parts=[query]))
        chunks:list[str] = []
        for chunk in agent.multishot_streaming(messages):
            chunks.append(chunk)
            print(chunk, end="")
        messages.append(GeminiMessage(role=GeminiRole.model, parts=[''.join(chunks)]))

