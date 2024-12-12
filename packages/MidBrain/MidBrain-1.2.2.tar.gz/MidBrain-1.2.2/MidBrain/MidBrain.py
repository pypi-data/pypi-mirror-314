import os
import sys
import subprocess
import logging
from transformers import AutoModelForCausalLM, AutoTokenizer
import argparse
import openai
from colorama import Fore, Style, init

init(autoreset=True)

logging.getLogger("transformers").setLevel(logging.ERROR)

os.environ["TOKENIZERS_PARALLELISM"] = "false"
current_directory = os.getcwd()

MODEL_OPTIONS = {
    "1": "distilgpt2",
    "2": "EleutherAI/gpt-neo-125M",
    "3": "EleutherAI/gpt-neo-1.3B",
    "4": "EleutherAI/gpt-neo-2.7B",
    "5": "google/t5-small-lm-adapted-qa",
    "6": "EleutherAI/gpt-j-6B",
    "7": "openai-gpt",
}

openai.api_key = None

OPENAI_MODELS = {
    "1": "gpt-3.5-turbo",
    "2": "gpt-4",
}

model = None
tokenizer = None

def load_model(model_name: str):
    global model, tokenizer
    response = "could not find model "
    if model is None or tokenizer is None and model_name is not None:
        print(Fore.CYAN + f"✨ Generating answer/Loading model '{model_name}'... ✨\n")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        return model, tokenizer
    else:
        return model, tokenizer, response

def perform_midbrain(model_name: str, input_text: str, max_length: int = 50, temperature: float = 0):
    '''creaitng midbrain with model'''
    if model_name in OPENAI_MODELS.values():
        return perform_midbrain_openai(input_text, model_name, max_length, temperature)

    model, tokenizer, response = load_model(model_name)

    inputs = tokenizer(input_text, return_tensors="pt")

    outputs = model.generate(
        inputs.input_ids,
        max_length=max_length,
        temperature=temperature,
        num_return_sequences=1,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id,
        top_k=50,    # Optional: Use top-k sampling for diversity
        no_repeat_ngram_size=2  # Optional: Prevent repetitive phrases
    )

    output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"\n🔮{output}\n")
    return output

def perform_midbrain_openai(input_text: str, model_name: str, max_length: int = 50, temperature: float = 0.7):
    """Generate text using OpenAI GPT models."""
    if not openai.api_key:
        print(Fore.RED + "Error: OpenAI API key is missing.")
        return ""

    try:
        response = openai.Completion.create(
            engine=model_name,
            prompt=input_text,
            max_tokens=max_length,
            temperature=temperature,
            top_p=0.95,
            top_k=50,
        )

        output = response.choices[0].text.strip()
        return output
    except Exception as e:
        print(Fore.RED + f"Error with OpenAI API: {e}")
        return ""

def execute_system_command(command: str):
    """Execute a system shell command and return the output."""
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        print(Fore.YELLOW + result.stdout)  
        if result.stderr:
            print(Fore.RED + result.stderr, file=sys.stderr) 
    except Exception as e:
        print(Fore.RED + f"Error executing command: {e}", file=sys.stderr)

def interactive_prompt(model_name: str):
    print(Fore.MAGENTA + "✨✨✨ Welcome to the MidBrain! ✨✨✨ \n Type 'exit' to leave. 🎩🪄\n")

    while True:
        try:
            user_input = input(Fore.CYAN + f"MidBrain✨ ({model_name})> ")

            if user_input.lower() == 'exit':
                print(Fore.MAGENTA + "Exiting MidBrain...")
                break

            if user_input.lower().startswith('midbrain '):
                command = user_input[9:]
                if model_name == "openai-gpt":
                    perform_midbrain_openai(command, model_name, max_length=1000, temperature=1.0)
                else:
                    perform_midbrain(model_name, command, max_length=50, temperature=1.0)
            else:
                execute_system_command(user_input)

        except KeyboardInterrupt:
            print(Fore.MAGENTA + "\nExiting MidBrain...")
            break
        except Exception as e:
            print(Fore.RED + f"Error: {e}")

def select_model():
    print(Fore.MAGENTA + "Author: Harshit \n✨✨✨ Welcome to the MidBrain! ✨✨✨ \n Please choose a model to use for text generation:")
    print(Fore.CYAN + "🔮 Choose your brain power for text generation (AI models):")
    print("1: distilGPT-2 (Lightweight and fast, good for basic answers)")
    print("2: GPT-Neo 125M (Small, yet relevant for tech questions)")
    print("3: GPT-Neo 1.3B (Great for handling tech queries with more context)")
    print("4: GPT-Neo 2.7B (Larger model for more detailed and accurate answers)")
    print("5: T5-small (Fine-tuned for QA tasks, excellent for technical questions)")
    print("6: GPT-J 6B (Powerful, perfect for complex and detailed technical queries)")
    print("7: OpenAI GPT (Requires API key for access)")

    choice = input(Fore.CYAN + "Enter the number of your choice: ")

    model_name = MODEL_OPTIONS.get(choice, "gpt2")
    
    if model_name == "openai-gpt":
        print("You have selected OpenAI GPT model. Please choose the specific OpenAI model:")
        print("1: gpt-3.5-turbo (GPT-3.5 model)")
        print("2: gpt-4 (GPT-4 model, most advanced)")

        openai_choice = input("Enter the number of your choice: ")
        openai_model_name = OPENAI_MODELS.get(openai_choice, "text-davinci-003")
        max_retries = 5
        exhausted_count = 0
        
        while True:
            openai.api_key = input("Enter your OpenAI API key: ").strip()
            
            if not openai.api_key:
                print(Fore.RED + "Error: API key is required to use OpenAI GPT models.")
                exhausted_count += 1
                if exhausted_count >= max_retries:
                    print(Fore.RED + "Max retries reached. Exiting...")
                    return None 
                print(Fore.YELLOW + f"Retrying... ({exhausted_count}/{max_retries})")
                continue
            
            try:
                openai.Model.list() 
                print(Fore.GREEN + "Successfully connected to OpenAI API!")
                break
            except openai.error.AuthenticationError:
                print(Fore.RED + f"Error: Invalid OpenAI API key. Please check your key and try again.")
                exhausted_count += 1
                if exhausted_count >= max_retries:
                    print(Fore.RED + "Max retries reached. Exiting...")
                    return None
                print(Fore.YELLOW + f"Retrying... ({exhausted_count}/{max_retries})")
            except Exception as e:
                print(Fore.RED + f"Error connecting to OpenAI API: {e}")
                return None

        return openai_model_name
    else:
        print(Fore.GREEN + f"Selected model: {model_name}")
        return model_name


def main():
    global openai_api_key
    model_name = select_model()

    if model_name == "openai-gpt":
        if not openai.api_key:
            print(Fore.RED + "Error: OpenAI API key is missing.")
            sys.exit(1)

    parser = argparse.ArgumentParser(
        prog="midbrain",
        description="✨ Your magical CLI for generating text spells and performing tasks. ✨"
    )

    parser.add_argument(
        'command', nargs=argparse.REMAINDER,
        help="Command to run (e.g. 'path', 'rename', etc.). If no command is provided, interactive mode starts."
    )

    args = parser.parse_args()

    if not args.command:
        interactive_prompt(model_name)
    else:
        user_input = ' '.join(args.command)

        if user_input.lower().startswith('midbrain '):
            command = user_input[9:]
            if model_name == "openai-gpt":
                perform_midbrain_openai(command, model_name, max_length=50, temperature=0.7)
            else:
                perform_midbrain(model_name, command, max_length=50, temperature=0.7)
        else:
            execute_system_command(user_input)

if __name__ == "__main__":
    main()
