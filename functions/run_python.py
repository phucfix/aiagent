import os
import subprocess

from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_wd_path = os.path.abspath(working_directory)
    abs_target_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # If the file_path is outside of the working_directory
    if not abs_target_file_path.startswith(abs_wd_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    # If the file_path doesn't exist
    if not os.path.exists(abs_target_file_path):
        return f'Error: File "{file_path}" not found.'

    # If the file doesn't end with ".py"
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        # Execute the Python file and get back a "completed_process" object
        commands = ["python", abs_target_file_path]
        if args:
            commands.extend(args)
        complete_proc = subprocess.run(
            commands,
            timeout=30,
            capture_output=True, 
            text=True,
            cwd=abs_wd_path
        )

        output = [] 
        if complete_proc.stdout: 
            output.append(f"STDOUT:\n{complete_proc.stdout}\n")
        if complete_proc.stderr:
            output.append(f"STDERR:\n{complete_proc.stderr}\n")

        status_code = complete_proc.returncode
        if status_code != 0:
            output.append(f"Process exited with code {status_code}\n")
        
        # If no output is produced
        return "\n".join(output) if output else "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)
