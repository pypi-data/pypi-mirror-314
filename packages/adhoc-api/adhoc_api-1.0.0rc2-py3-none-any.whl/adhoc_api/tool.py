from archytas.tool_utils import tool
from typing import Callable, Any, TypedDict, Literal
from typing_extensions import Annotated, NotRequired
from functools import cache

from .utils import Logger, SimpleLogger, get_code, set_openai_api_key, set_gemini_api_key, set_anthropic_api_key
from .uaii import UAII, GeminiModel, GeminiAgent, OpenAIModel, OpenAIAgent, ClaudeModel, ClaudeAgent


import pdb


# configuration for agents that the user passes in
class GeminiConfig(TypedDict):
    provider: Literal['google']
    api_key: NotRequired[Annotated[str, 'The API key for the Gemini API']]
    model: Annotated[GeminiModel, 'The model to use for the Gemini API']
    ttl_seconds: NotRequired[Annotated[int, "The time-to-live in seconds for the Gemini API cache"]]
GEMINI_DEFAULTS = {
    'ttl_seconds': 1800
}


class GPTConfig(TypedDict):
    provider: Literal['openai']
    api_key: NotRequired[Annotated[str, 'The API key for the OpenAI API']]
    model: Annotated[OpenAIModel, 'The model to use for the OpenAI API']
GPT_DEFAULTS = {}


class ClaudeConfig(TypedDict):
    provider: Literal['anthropic']
    api_key: NotRequired[Annotated[str, 'The API key for the Anthropic API']]
    model: Annotated[ClaudeModel, 'The model to use for the Anthropic API']
CLAUDE_DEFAULTS = {}


class APISpec(TypedDict):
    name: Annotated[str, 'The name of the API']
    cache_key: NotRequired[Annotated[str, 'The key used to retrieve the cached API chat. If not provided, caching will be disabled. Note: only Gemini supports caching at the moment.']]
    description: Annotated[str, 'A description of the API']
    documentation: Annotated[str, "The raw extracted text of the API's documentation"]



DRAFTER_SYSTEM_PROMPT = '''\
You are an assistant who is helping users to write code to interact with the {name} API.
You will be provided with the raw API documentation, and you have 2 jobs:
1. Answer questions about the API
2. Write code to perform specific tasks using the API

Each user query will include a keyword specifying which job to do: ASK_API for 1, and WRITE_CODE for 2.

When answering questions (ASK_API), please follow these rules:
- Answer in plain English
- Be concise and comprehensive
- Do not write large code blocks. If you need to provide code, keep it short and inline with the text of your response

When drafting code (WRITE_CODE), please follow these rules:
- Your output should be a single python code block. do not include any other comments or explanations in your response.
- Your code should directly solve the problem posed in the query and nothing more.
- The code should be ready to run directly as a python script.
- Assume `requests`, `numpy`, and `pandas` are installed, as well as any API specific libraries mentioned in the API documentation.
'''


def make_ask_api_query(query: str) -> str:
    return f'ASK_API: {query}'

def make_write_code_query(query: str) -> str:
    return f'WRITE_CODE: {query}'



class AdhocApi:
    """
    Toolset for interacting with external APIs in an flexible manner. 
    These tools can be used to draft code that perform requests to APIs given some goal in plain English.
    Common usage is to first list APIs to determine which to use, then draft code to perform a specific task, then run the code.
    Note that each API maintains a separate chat history, so treat each API as a separate conversation.
    """
    def __init__(self, *,
        apis: list[APISpec],
        drafter_config: GeminiConfig | GPTConfig | ClaudeConfig,
        logger: Logger=SimpleLogger()
    ):
        """
        Create a new AdhocApi instance.

        Args:
            apis (list[APISpec]): A list of APIs available to the tool
            drafter_config_base (DrafterConfigBase): The base configuration for the drafter agent
            logger (Logger, optional): A logger to use for logging. Defaults to SimpleLogger.
        """
        self.logger = logger
        self.apis = {api['name']: api for api in apis}
        self.drafter_config = drafter_config
        self._set_api_key()

    def _set_api_key(self):
        """
        Set the API key for the specified provider.

        Args:
            provider (Literal['google', 'openai', 'anthropic']): The provider to set the API key for
        """
        provider = self.drafter_config['provider']
        if provider == 'google':      set_gemini_api_key(self.drafter_config.get('api_key', None))
        elif provider == 'openai':    set_openai_api_key(self.drafter_config.get('api_key', None))
        elif provider == 'anthropic': set_anthropic_api_key(self.drafter_config.get('api_key', None))
        else:
            raise ValueError(f'Unknown provider "{provider}"')

    def _get_api(self, api: str) -> APISpec:
        api_spec = self.apis.get(api)
        if api_spec is None:
            raise ValueError(f'API {api} not found. Please consult the list of available APIs: {[*self.apis.keys()]}')
        return api_spec
     
    @cache
    def _get_agent(self, api: str) -> UAII:
        """
        get the agent instance for the given API (make a new one if it doesn't exist)

        Args:
            api (str): The name of the API to get the agent for

        Returns:
            UAII: The agent instance
        """
        # @cache handles the case where the agent already exists

        # create a new agent if it doesn't exist
        api_spec = self._get_api(api)
        api_docs = api_spec['documentation']
        provider = self.drafter_config['provider']

        if provider == 'google':
            config: GeminiConfig = {**GEMINI_DEFAULTS, **self.drafter_config}
            return GeminiAgent(
                model=config['model'],
                cache_key=api_spec.get('cache_key', None),
                system_prompt=DRAFTER_SYSTEM_PROMPT.format(name=api),
                cache_content=api_docs,
                ttl_seconds=config['ttl_seconds'],
                logger=self.logger,
            )
        
        elif provider == 'openai':
            config: GPTConfig = {**GPT_DEFAULTS, **self.drafter_config}
            return OpenAIAgent(
                model=config['model'],
                system_prompt=DRAFTER_SYSTEM_PROMPT.format(name=api) + f'\n\n# API Documentation:\n{api_docs}',
            )

        elif provider == 'anthropic':
            config: ClaudeConfig = {**CLAUDE_DEFAULTS, **self.drafter_config}
            return ClaudeAgent(
                model=config['model'],
                system_prompt=DRAFTER_SYSTEM_PROMPT + f'\n\n# API Documentation:\n{api_docs}',
            )
        
        else:
            raise ValueError(f'Unknown provider {provider}')
        
    @tool
    def list_apis(self) -> dict:
        """
        This tool lists all the APIs available to you.

        Returns:
            dict: A dict mapping from API names to their descriptions
        """
        subset_keys = ['description']
        return {
            name: {
                key: api[key] for key in subset_keys if key in api
            }
            for name, api in self.apis.items()
        }
    
    @tool
    def ask_api(self, api: str, query: str) -> str:
        """
        Ask a question about the API to get more information.

        Args:
            api (str): The name of the API to ask about
            query (str): The question to ask

        Returns:
            str: The response to the query
        """
        self.logger.info({'api': api, 'ASK_API': query})
        agent = self._get_agent(api)
        query = make_ask_api_query(query)
        return agent.message(query)

    @tool
    def use_api(self, api: str, goal: str) -> str:
        """
        Draft python code for an API request given some goal in plain English.

        Args:
            api (str): The name of the API to use
            goal (str): The task to be performed by the API request (in plain English)

        Returns:
            str: The raw generated code to perform the task
        """
        self.logger.info({'api': api, 'WRITE_CODE': goal})
        agent = self._get_agent(api)
        query = make_write_code_query(goal)
        response = agent.message(query)
        
        # strip off any markdown syntax
        code = get_code(response)

        return code



import subprocess
import tempfile
import os

class PythonTool:
    """Tool for running python code. If the user asks you to write code, you can run it here."""
    def __init__(self, sideeffect:Callable[[str, str, str, int], Any]=lambda x: None):
        """
        Set up a PythonTool instance.

        Args:
            sideeffect (Callable[[str], Any], optional): A side effect function to run when the tool is used. Defaults to do nothing.
        """
        self.sideeffect = sideeffect

    @tool
    def run(self, code: str) -> tuple[str, str, int]:
        """
        Runs python code in a python subprocess.

        The environment is not persistent between runs, so any variables created will not be available in subsequent runs.
        The only visible effects of this tool are from output to stdout/stderr. If you want to view a result, you MUST print it.

        Args:
            code (str): The code to run

        Returns:
            tuple: The stdout, stderr, and returncode from executing the code
        """

        # make a temporary file to run the code
        with tempfile.NamedTemporaryFile(suffix='.py', mode='w+') as f:
            f.write(code)
            f.flush()
            f.seek(0)

            # run the file in a separate Python process and capture the output
            try:
                result = subprocess.run(['python', f.name], capture_output=True, text=True, cwd=os.getcwd())
                stdout = result.stdout
                stderr = result.stderr or (f'No error output available. Process returned non-zero error code {result.returncode}' if result.returncode != 0 else '')
                returncode = result.returncode
            except Exception as e:
                stdout, stderr, returncode = "", str(e), 1
        
        # perform side effect
        self.sideeffect(code, stdout, stderr, returncode)


        return stdout, stderr, returncode


from .files import tree
from pathlib import Path

@tool
def view_filesystem(max_depth:int=-1, max_similar: int=25, ignore: list[str] = []) -> str:
    """
    View files and directories in the current working directory, displayed in a tree structure.

    Args:
        max_depth (int, optional): The maximum depth to traverse. Set to negative for infinite depth.
        max_similar (int, optional): The maximum number of similar files to display. When too many similar files are found, further matches will be elided. Defaults to 25.
        ignore (list, optional): List of unix filename pattern strings (e.g. '*.py', 'file?.txt', 'file[!a-c]*.txt', etc.) to skip including in output. Defaults to [].

    Returns:
        str: A string representation of the tree structure of the current working directory.
    """
    return tree(Path('.'), ignore=ignore, max_depth=max_depth, max_similar=max_similar)