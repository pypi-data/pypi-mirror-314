# Copyright (c) 2023-2024 Datalayer, Inc.
#
# BSD 3-Clause License

from dotenv import load_dotenv, find_dotenv

from langchain.agents import tool
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor

from jupyter_nbmodel_client import NbModelClient
from jupyter_kernel_client import KernelClient


def ask_agent(server_url: str, token: str, azure_deployment_name: str, notebook_path: str, input: str) -> list:
    """From a given instruction, code and markdown cells are added to a notebook."""

    load_dotenv(find_dotenv())

    kernel = KernelClient(server_url=server_url, token=token)
    kernel.start()

    notebook = NbModelClient(server_url=server_url, token=token, path=notebook_path)
    notebook.start()

    @tool
    def add_code_cell(cell_content: str) -> None:
        """Add a Python code cell with a content to the notebook and execute it."""
        cell_index = notebook.add_code_cell(cell_content)
        results = notebook.execute_cell(cell_index, kernel)
        assert results["status"] == "ok"
            
    @tool
    def add_markdown_cell(cell_content: str) -> None:
        """Add a Markdown cell with a content to the notebook."""
        notebook.add_markdown_cell(cell_content)

    tools = [add_code_cell, add_markdown_cell]
    agent = create_agent(azure_deployment_name, tools)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return list(agent_executor.stream({"input": input}))

def create_agent(azure_deployment_name: str, tools: list) -> dict:
    """Create an agent from a set of tools and an Azure deployment name."""
    llm = AzureChatOpenAI(azure_deployment=azure_deployment_name)
    llm_with_tools = llm.bind_tools(tools)
    prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a powerful coding assistant. Create and execute code in a notebook based on user instructions. Add markdown cells to explain the code and structure the notebook clearly. Assume that no packages are installed in the notebook, so install them using !pip install.",),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm_with_tools
    | OpenAIToolsAgentOutputParser())
    return agent
