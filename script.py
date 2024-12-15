from autogen import AssistantAgent, UserProxyAgent
from autogen.coding import LocalCommandLineCodeExecutor
import os
from pathlib import Path

# IPython is not necessary for this task unless you plan to display images or use interactive features in the console
# from IPython.display import Image, display

import autogen

# Configuration for the LLM
config_list = [{"model": "gpt-4", "api_key": 'YOUR_API_KEY'}]  # Use environment variables for API key security

# Create an AssistantAgent named "assistant"
assistant = autogen.AssistantAgent(
    name="WebCodeReviewer",
    llm_config={
        "cache_seed": 41,  # seed for caching and reproducibility
        "config_list": config_list,  # a list of OpenAI API configurations
        "temperature": 0,  # temperature for sampling
    },
)

# Create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "executor": LocalCommandLineCodeExecutor(work_dir="C:\\Users\\jjohn\\Desktop\\Web Page\\daedalus\\public"),
        "last_n_messages": 2,  # Number of messages to keep in context for code execution
    },
)

# Function to read content from files
def read_file_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# The task to review HTML, CSS, and JS
task_message = """
Please review the HTML, CSS, and JavaScript files in this directory. Provide feedback on:

- HTML structure and semantics
- CSS efficiency and best practices
- JavaScript functionality, performance, and security

Here are the files:

- HTML: index.html
- CSS: styles.css
- JavaScript: script.js

"""

# Read the content of files
file_contents = {
    "index.html": read_file_content("C:\\Users\\jjohn\\Desktop\\Web Page\\daedalus\\public\\index.html")}

# Combine file contents in the task message
for filename, content in file_contents.items():
    task_message += f"\n\n**{filename}**:\n```\n{content}\n```"

# Initiate the chat with the task message
chat_res = user_proxy.initiate_chat(
    assistant,
    message=task_message,
    summary_method="reflection_with_llm"
)