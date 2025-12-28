import os
from google.genai import types


def write_file(working_directory, file_path, content):
  try:
    working_directory_abs_path = os.path.realpath(working_directory)
    full_path = os.path.realpath(os.path.join(working_directory, file_path))
    common_path = os.path.commonpath([working_directory_abs_path, full_path])
    
    if not common_path == working_directory_abs_path:
      return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if os.path.dirname(full_path):
      os.makedirs(os.path.dirname(full_path), exist_ok=True)

    with open(full_path, "w") as f:
      f.write(content)

    return (f'Successfully wrote to "{file_path}" ({len(content)} characters written)')

  except Exception as e:
    return f'Error: {e}'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the provided content to a file at the specified path within the working directory. Creates the file if it doesn't exist, and overwrites it if it does.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
          "working_directory": types.Schema(
              type=types.Type.STRING,
              description="The base directory that all file operations are restricted to. Must be an absolute or relative path.",
          ),
          "file_path": types.Schema(
              type=types.Type.STRING,
              description="The relative path (from the working directory) where the file will be written.",
          ),
          "content": types.Schema(
              type=types.Type.STRING,
              description="The full text content to write into the file.",
          )
        },
    ),
)

