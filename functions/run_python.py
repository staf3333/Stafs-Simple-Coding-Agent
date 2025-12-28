import os
from subprocess import run
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
  try:
    working_directory_abs_path = os.path.realpath(working_directory)
    full_path = os.path.realpath(os.path.join(working_directory, file_path))
    common_path = os.path.commonpath([working_directory_abs_path, full_path])
    
    if not common_path == working_directory_abs_path:
      return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(full_path):
      return f'Error: File "{file_path}" not found.'

    if not full_path.endswith('.py'):
      return f'Error: "{file_path}" is not a Python file.'

    try:
      run_args = ["python3", full_path, *args]
      result = run(args=run_args, capture_output=True, timeout=30, cwd=working_directory_abs_path)
      if result.returncode != 0:
        return f'Error: Process exited with code {result.returncode}'

      if not result.stdout.strip() and not result.stderr.strip():
        return "No output produced"

      return f'STDOUT: {result.stdout} \n STDERR: {result.stderr}'

    except Exception as e:
      return f'Error: executing python file: {e}'


  except Exception as e:
    return f'Error: {e}'

schema_run_python= types.FunctionDeclaration(
    name="run_python_file",
    description="Runs python file in the specified file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the Python file to execute. Must be within the working directory.",
            ),
        },
    ),
)

