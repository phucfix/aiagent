import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

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

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    # Get a response from the gemini-2.0-flash-001 model
    # The generate_content method returns a GenerateContentResponse object.
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages
    )

    if verbose:
        print(f"User prompt: {user_prompt}\n")
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()
