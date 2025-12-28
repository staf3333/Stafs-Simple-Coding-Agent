import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python import run_python_file, schema_run_python
from functions.write_file import write_file, schema_write_file


def main():
    print("Hello from stafs-ai-coding-agent!")

    # check if command is valid
    is_verbose = "--verbose" in sys.argv
    if (len(sys.argv) < 2) or (len(sys.argv) == 2 and is_verbose):
        print("You need to pass in a prompt for this script to work")
        sys.exit(1)

    # load gemini api
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    # use gemini api
    user_prompt = sys.argv[1]
    if is_verbose:
        print(f"User prompt: {user_prompt}")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_run_python,
            schema_get_file_content,
            schema_write_file
        ]
    )
    client = genai.Client(api_key=api_key)
    for i in range(20):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt)
            )

            for candidate in response.candidates:
              messages.append(candidate.content)

            if response.function_calls:
              function_responses = []
              for function_call in response.function_calls:
                function_result = call_function(function_call)
                # Add the results part to function response list
                function_responses.append(function_result.parts[0])

              messages.append(types.Content(
                  role="user",
                  parts=function_responses
              ))
            if not response.function_calls:
                if response.text:
                    print("Final response:")
                    print(response.text)
                    break
        except Exception as e:
            print(f'Error: {e}')


def call_function(function_call_part, verbose=False):
    if verbose:
        print(
            f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_name = function_call_part.name
    function_to_call = available_functions.get(function_name)

    if not function_to_call:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ]
        )
    args = function_call_part.args.copy()
    args["working_directory"] = "./calculator"
    function_result = function_to_call(**args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )


available_functions = {
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "get_file_content": get_file_content,
    "write_file": write_file
}

if __name__ == "__main__":
    main()
