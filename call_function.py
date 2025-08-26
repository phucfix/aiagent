from google.genai import types

from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python import schema_run_python_file, run_python_file

# Create list of available function
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)

# function_call_part is a types.FunctionCall that most importantly has:
#  - A .name property (the name of the function, a string)
#  - A .args property (a dictionary of named arguments to the function)
def call_function(function_call_part, verbose=False):
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file
    }

    # If verbose is specified, print the function name and args:
    function_name = function_call_part.name
    function_args = function_call_part.args
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    function_to_run = function_map.get(f"{function_name}")
    # If the function name is invalid, return a types.Content that explains the error:
    if not function_to_run:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    # Call the function and capture the result
    function_result = function_to_run(**{**function_args, 'working_directory': './calculator'})

    # Return types.Content with a from_function_response describing the result of the function call:
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                # From_function_response requires the response to be a dictionary, so just shove 
                # the string result into a "result" field
                response={"result": function_result},
                )
        ],
    )

