import os

from google.genai import types
# All of our "tool call" functions should always return a string. If errors can be raised inside
# them, we need to catch those errors and return a string describing the error instead. This will
# allow the LLM to handle the errors gracefully.

def get_files_info(working_directory, directory="."):
    wd_abs_path = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, directory))

    # validate it stays within the working directory boundaries
    if not target_dir.startswith(wd_abs_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    # If the directory argument is not a directory
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    # Build and return a string representing the contents of the directory. Format:
    try:
        files_info = []
        for file_name in os.listdir(target_dir):
            file_path = os.path.join(target_dir, file_name)
            file_size = 0
            is_dir = os.path.isdir(file_path)
            file_size = os.path.getsize(file_path)
            files_info.append(
                f"- {file_name}: file_size={file_size} bytes, is_dir={is_dir}"
            )
        return "\n".join(files_info)
    except Exception as e:
        return f"Error listing files: {e}"

# Build the "declaration" or "schema" for a function
# This basically just tells the LLM how to use the function
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
# We won't allow the LLM to specify the working_directory parameter. We're going to hard code that.
