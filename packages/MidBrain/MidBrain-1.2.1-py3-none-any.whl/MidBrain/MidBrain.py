import os
import sys
import subprocess
import logging
from transformers import AutoModelForCausalLM, AutoTokenizer
import argparse

logging.getLogger("transformers").setLevel(logging.ERROR)

current_directory = os.getcwd()

os.environ["TOKENIZERS_PARALLELISM"] = "false"

MODEL_OPTIONS = {
    "1": "distilgpt2",  # A smaller version of GPT-2, good for fast, basic answers
    "2": "EleutherAI/gpt-neo-125M",  # A small but relevant model for tech questions
    "3": "EleutherAI/gpt-neo-1.3B",  # A mid-size model that handles tech queries better
    "4": "EleutherAI/gpt-neo-2.7B",  # A larger model for very relevant and detailed answers
    "5": "google/t5-small-lm-adapted-qa",  # T5 model fine-tuned for QA tasks (great for technical questions)
    "6": "EleutherAI/gpt-j-6B",  # Powerful model, suitable for complex, detailed technical queries
}
model = None
tokenizer = None

def load_model(model_name: str):
    """Load the AI model if not already loaded."""
    global model, tokenizer
    if model is None or tokenizer is None:
        print(f"✨ Loading model '{model_name}'... ✨")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
    return model, tokenizer

def perform_midbrain(model_name: str, input_text: str, max_length: int, temperature: float):
    """Generate text using the AI model."""
    print(f"✨ Creating MidBrain with model '{model_name}'! ✨\n")

    model, tokenizer = load_model(model_name)

    inputs = tokenizer(input_text, return_tensors="pt")

    outputs = model.generate(
        inputs.input_ids,
        max_length=max_length,
        temperature=temperature,
        num_return_sequences=1,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id  
    )

    magic_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"🔮 Here's the result of your spell:\n\n{magic_output}\n")
    return magic_output

def execute_system_command(command: str):
    """Execute a system shell command and return the output."""
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        print(result.stdout)  
        if result.stderr:
            print(result.stderr, file=sys.stderr) 
    except Exception as e:
        print(f"Error executing command: {e}", file=sys.stderr)

def interactive_prompt(model_name: str):
    """Start the interactive MidBrain shell."""
    print("✨✨✨ Welcome to the MidBrain! ✨✨✨ \n Type 'exit' to leave. 🎩🪄\n")

    while True:
        try:
            user_input = input(f"MidBrain✨ ({model_name})✨> ")

            if user_input.lower() == 'exit':
                print("Exiting MidBrain...")
                break

            # Check if the input starts with 'midbrain' and is a valid command
            if user_input.lower().startswith('midbrain '):
                command = user_input[9:]  # Remove 'midbrain ' and treat as a command
                perform_midbrain(model_name, command, max_length=50, temperature=1.0)
            else:
                # Treat as a normal shell command
                execute_system_command(user_input)

        except KeyboardInterrupt:
            print("\nExiting MidBrain...")
            break
        except Exception as e:
            print(f"Error: {e}")

def select_model():
    """Prompt the user to select a model from available options."""
    print("Author: Harshit \n✨✨✨ Welcome to the MidBrain! ✨✨✨ \n Please choose a model to use for text generation:")
    print("🔮 Choose your brain power for text generation (AI models):")
    print("1: distilGPT-2 (Lightweight and fast, good for basic answers)")
    print("2: GPT-Neo 125M (Small, yet relevant for tech questions)")
    print("3: GPT-Neo 1.3B (Great for handling tech queries with more context)")
    print("4: GPT-Neo 2.7B (Larger model for more detailed and accurate answers)")
    print("5: T5-small (Fine-tuned for QA tasks, excellent for technical questions)")
    print("6: GPT-J 6B (Powerful, perfect for complex and detailed technical queries)")

    choice = input("Enter the number of your choice: ")

    model_name = MODEL_OPTIONS.get(choice, "gpt2")
    print(f"Selected model: {model_name}")
    return model_name

def main():
    model_name = select_model()

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
            perform_midbrain(model_name, command, max_length=50, temperature=1.0)
        else:
            execute_system_command(user_input)

if __name__ == "__main__":
    main()
