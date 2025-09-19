import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", help="The user's prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    if len(sys.argv) < 2:
        print("Error!! Prompt not provided!!")
        sys.exit(1)

    prompt = args.prompt
    verbose = args.verbose

    if not api_key:
        print("Error : GEMINI_API_KEY is not set in .env")
        sys.exit(1)
      
    messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),   
    ]
    
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    
    config = types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt,
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=config,
    )
        
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if response.function_calls:
        for fc in response.function_calls:
            print(f"Calling function: {fc.name}({fc.args})")
    else:
        print(response.text)

    if verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
              


if __name__ == "__main__":
    main()
