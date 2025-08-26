import os

from google.genai import types

def write_file(working_directory, file_path, content):
    abs_wd_path = os.path.abspath(working_directory)
    abs_target_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # If the file_path is outside of the working_directory
    if not abs_target_file_path.startswith(abs_wd_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    # If the file_path doesn't exist
    if not os.path.exists(abs_target_file_path):
        try:    
            os.makedirs(os.path.dirname(abs_target_file_path), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"

    if os.path.exists(abs_target_file_path) and os.path.isdir(abs_target_file_path):
        return f'Error: "{file_path}" is a directory, not a file'

    # Overwrite the contents of the file with the content argument
    try:
        with open(abs_target_file_path, 'w') as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error writting file "{file_path}": {e}'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file within the working directory. Creates the file if it doesn't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)
