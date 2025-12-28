import os
from google.genai import types

def get_files_info(working_directory, directory="."):
  try:
    # validations
    # first check that the directory is a valid relative path, i.e. not out of bounds of the current working directory
    working_directory_abs_path = os.path.realpath(working_directory)
    full_path = os.path.realpath(os.path.join(working_directory, directory))
    common_path = os.path.commonpath([working_directory_abs_path, full_path])
    
    if not common_path == working_directory_abs_path:
      return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(full_path):
      return f'Error: "{directory}" is not a directory'

    output = []
    for item in os.listdir(full_path):
      full_item_path = os.path.join(full_path, item)
      output.append(f'- {item}: file_size={os.path.getsize(full_item_path)} bytes, is_dir={os.path.isdir(full_item_path)}')
    return '\n'.join(output)

  except OSError as e:
    return f'Error: {e}'

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
