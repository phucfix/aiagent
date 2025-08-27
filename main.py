import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    # Create a new instance of a Gemini client
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)
    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    try:
        for _ in range(20):
            response = generate_content(client, messages, verbose)
            # If it returned the response.text property
            if response:
                # It's done, print this final response and break out of the loop
                print(f"Final response:\n{response}")
                break
            
    except Exception as e:
        print(f"An error occurr: {e}")
        sys.exit(2)
        

def generate_content(client, messages, verbose):
    # Get a response from the gemini-2.0-flash-001 model
    # The generate_content method returns a GenerateContentResponse object.
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )   

    # The .candidates property of the response. It's a list of response variations (usually just one).
    # It contains the equivalent of "I want to call get_files_info..."
    # Add it to our conversation.
    for candidate in response.candidates:
        messages.append(candidate.content)

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)

        # The types.Content that return from call_function should have a 
        # .parts[0].function_response.response within.
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response.response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        # After each actual function call, use the types.Content function to
        # convert the function_responses into a message with a role of user and append it into your messages
        messages.append(
            types.Content(
                role="user",
                parts=[function_call_result.parts[0]]
            )
        )

        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")

if __name__ == "__main__":
    main()
