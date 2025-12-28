import os
from config import FILE_READ_CHARACTER_COUNT
from google.genai import types

def get_file_content(working_directory, file_path):
  try:
    working_directory_abs_path = os.path.realpath(working_directory)
    full_path = os.path.realpath(os.path.join(working_directory, file_path))
    common_path = os.path.commonpath([working_directory_abs_path, full_path])
    
    if not common_path == working_directory_abs_path:
      return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(full_path):
      return f'Error: File not found or is not a regular file: "{file_path}"'

    with open(full_path, "r") as f:
      content = f.read(FILE_READ_CHARACTER_COUNT + 1)

    if len(content) > FILE_READ_CHARACTER_COUNT:
      truncated_file_content = content[:FILE_READ_CHARACTER_COUNT]
      return f'{truncated_file_content} [...File "{file_path}" truncated at {FILE_READ_CHARACTER_COUNT} characters]'
    else:
      return content
  except Exception as e:
    return f'Error: {e}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the contents of a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
          "working_directory": types.Schema(
              type=types.Type.STRING,
              description="The absolute or relative base directory to constrain file access to. All file access is restricted to this directory.",
          ),
          "file_path": types.Schema(
              type=types.Type.STRING,
              description="The path to the file, relative to the working directory, whose contents should be returned.",
          )
        },
    ),
)

