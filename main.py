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
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file


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

    Start by listing files in ./calculator, then read relevant files to answer.
    """
    
    config = types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt,
    )

    for i in range(20):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=config,        
            )
           
            if response.candidates:
                for candidate in response.candidates:
                    messages.append(candidate.content)
            
            if response.function_calls:
                for fc in response.function_calls:
                    result_content = call_function(fc, verbose=verbose)
                    messages.append(result_content)

                    if verbose:
                        print(f"-> {result_content.parts[0].function_response.response}")
            
            if response.text and not response.function_calls:
                    print(response.text)
                    break
            

        except Exception as e:
            print(f"Error: {e}")
        
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    

    if verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
              
def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = dict(function_call_part.args or {})
    function_args["working_directory"] = "./calculator"

    if function_name == "get_files_info":
        function_args.pop("directory", None)
    elif function_name in ("get_file_content", "run_python_file", "write_file"):
        if "path" in function_args and isinstance(function_args["path"], str):
            function_args["path"] = os.path.basename(function_args["path"])

    print(f" - Calling function: {function_name}")
    if verbose:
        print(f"Calling function: {function_name}({function_args})")   
    
    functions = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
        }

    func = functions.get(function_name)
    if func is None:
        return types.Content(
            role="tool",
            parts=[types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_name}"},
            )],
        )
    
    function_result = func(**function_args)
    payload = {"result": function_result}
    if function_name == "get_files_info" and isinstance(function_result, list):
        payload = {"files": function_result}
    return types.Content(
        role="user",
        parts=[types.Part.from_function_response(
            name=function_name,
            response=payload,
        )],
    )

    

if __name__ == "__main__":
    main()
