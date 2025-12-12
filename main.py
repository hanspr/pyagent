import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

def main():
    load_dotenv()
    os.environ["GRPC_VERBOSITY"] = "ERROR"
    os.environ["GLOG_minloglevel"] = "2"

    print("Begin ----------------------------------")
    api_key = os.environ.get("GEMINI_API_KEY")
    options = dict()
    model_name = "gemini-2.5-flash"
    user_prompt = ""
    options["verbose"] = False
    for arg in (sys.argv[1:]):
        if arg.startswith("--"):
            options[arg[2:]] = True
        else:
            user_prompt = arg
    if user_prompt == "":
        print("Mensaje es requerido")
        sys.exit(1)
    available_functions = types.Tool(function_declarations=[schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file])
    messages = [types.Content(role = "user", parts=[types.Part(text = user_prompt)]),]
    client = genai.Client(api_key = api_key)
    #print("check")
    #sys.exit(1)
    for i in range(1, 20):
        done = True
        try:
            response = client.models.generate_content(
                model = model_name,
                contents = messages,
                config = types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction = system_prompt
                ),
            )
        except Exception as e:
            print(f"Gemini error: {e}")
            sys.exit(1)
        for candidate in response.candidates:
            messages.append(types.Content(role = "user", parts = candidate.content.parts))
        if response.function_calls != None:
            function_call_responses = []
            for function_call_part in response.function_calls:
                done = False
                result = call_function(function_call_part, verbose = options["verbose"])
                try:
                    test = result.parts[0].function_response.response
                except Exception as e:
                    raise Exception("Error: resultado de la llamada inválido {e}")
                    sys.exit(1)
                function_call_responses.append(result.parts[0])
                if options["verbose"]:
                    print(f"-> {result.parts[0].function_response.response}")
            if len(function_call_responses) > 0:
                messages.append(types.Content(role = "user", parts = function_call_responses))
        if response.text != None and done:
            print(f"Final response:\n\n{response.text}\n\n")
            break
        elif response.text != None:
            print(f"Response not done ?: response\n{response.text}")
        if options["verbose"]:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print("Finished -------------------------------")

if __name__ == "__main__":
    main()
