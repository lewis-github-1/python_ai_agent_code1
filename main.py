import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def main():
    if len(sys.argv) < 2:
        print("Error!! Prompt not provided!!")
        sys.exit(1)

    prompt = sys.argv[1]
    
    # Add CLI commands
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", help="The user's prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    prompt = args.prompt
    verbose = args.verbose

    
    
    messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),   
    ]
        
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages)
    
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count


    if verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

       


if __name__ == "__main__":
    main()
