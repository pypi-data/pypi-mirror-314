import os
import sys
import subprocess
import logging
from transformers import AutoModelForCausalLM, AutoTokenizer
import argparse

# Disable warnings from Hugging Face transformers
logging.getLogger("transformers").setLevel(logging.ERROR)

# Global variable to track the current working directory
current_directory = os.getcwd()

# Suppress tokenizer parallelism warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Available models to choose from
MODEL_OPTIONS = {
    "1": "gpt2",  # Default GPT-2 model
    "2": "EleutherAI/gpt-j-6B",  # Powerful GPT-J 6B model
    "3": "mistral-7b",  # Mistral 7B (open-source model)
}

# Initialize model and tokenizer globally, but load them lazily to avoid performance issues
model = None
tokenizer = None

# Load the model and tokenizer when needed (lazy loading)
def load_model(model_name: str):
    global model, tokenizer
    if model is None or tokenizer is None:
        print(f"✨ Loading model '{model_name}'... ✨")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
    return model, tokenizer

# Perform the magic (text generation)
def perform_hokus_pokus(model_name: str, input_text: str, max_length: int, temperature: float):
    """Perform magic text generation."""
    print(f"✨ Casting Hokus Pokus with model '{model_name}'! ✨\n")

    # Load the model lazily
    model, tokenizer = load_model(model_name)

    # Prepare the input (spell)
    inputs = tokenizer(input_text, return_tensors="pt")

    # Generate the magic output (adding pad_token_id explicitly to avoid warnings)
    outputs = model.generate(
        inputs.input_ids,
        max_length=max_length,
        temperature=temperature,
        num_return_sequences=1,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id  # Explicitly setting pad_token_id
    )

    # Decode and return the result
    magic_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"🔮 Here's the result of your spell:\n\n{magic_output}\n")
    return magic_output

# Show the current working directory
def show_current_path():
    """Print the current directory path."""
    print(f"Current working directory: {current_directory}")

# Rename a file in the current directory
def rename_file(old_name: str, new_name: str):
    """Rename a file in the current directory."""
    if os.path.exists(old_name):
        os.rename(old_name, new_name)
        print(f"Renamed file from {old_name} to {new_name}.")
    else:
        print(f"File '{old_name}' does not exist.")

# Execute Linux shell commands
def execute_linux_command(command: str):
    """Execute a system shell command and return the output."""
    try:
        # Execute any Linux shell command
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        print(result.stdout)  # Print standard output of the command
        if result.stderr:
            print(result.stderr, file=sys.stderr)  # Print standard error (if any)
    except Exception as e:
        print(f"Error executing command: {e}", file=sys.stderr)

# Handle 'cd' command (persistent change of directory)
def change_directory(directory: str):
    """Change the current working directory."""
    global current_directory
    try:
        os.chdir(directory)
        current_directory = os.getcwd()  # Update the global directory state
        print(f"Changed directory to {current_directory}")
    except FileNotFoundError:
        print(f"Directory '{directory}' not found.")
    except PermissionError:
        print(f"Permission denied to access '{directory}'.")

# Interactive prompt to handle commands
def interactive_prompt(model_name: str):
    """Start the interactive Hokus Pokus CLI shell."""
    print("✨✨✨ Welcome to the Hokus Pokus Shell! ✨✨✨ \n Type 'exit' to leave. 🎩🪄\n")

    while True:
        try:
            # Display the prompt
            user_input = input(f"Hokus-Pokus✨ ({model_name})✨> ")

            # Exit condition
            if user_input.lower() == 'exit':
                print("Exiting Hokus Pokus Shell...")
                break

            # Split the command and arguments
            args = user_input.split()

            if not args:
                continue

            command = args[0].lower()
            command_args = args[1:]

            if command == 'path':
                show_current_path()

            elif command == 'rename':
                if len(command_args) == 2:
                    old_name, new_name = command_args
                    rename_file(old_name, new_name)
                else:
                    print("Please provide both the old and new filenames to rename.")

            elif command == 'cd':
                if command_args:
                    change_directory(command_args[0])
                else:
                    print("Please provide a directory to change to.")

            elif command in ('clear','ls', 'cd', 'cat', 'mkdir', 'touch', 'rm', 'cp', 'mv', 'pwd', 'echo', 'find', 'grep', 'chmod', 'chown', 'tar', 'zip', 'unzip', 'df', 'du', 'top', 'ps', 'kill', 'nano', 'vim', 'htop', 'ssh', 'scp', 'wget', 'curl', 'python3', 'python', 'pip', 'java' 'javac'):
                # Any Linux command will be executed by passing to the system shell
                execute_linux_command(user_input)

            else:
                # Treat the input as the spell or text for magic generation
                perform_hokus_pokus(model_name, user_input, max_length=50, temperature=1.0)

        except KeyboardInterrupt:
            print("\nExiting Hokus Pokus Shell...")
            break
        except Exception as e:
            print(f"Error: {e}")

# Ask user to select model from available options
def select_model():
    """Prompt the user to select a model from available options."""
    print("Author: Harshit \n✨✨✨ Welcome to the Hokus Pokus Shell! ✨✨✨ \n Please choose a model to use for text generation:")
    print("1: GPT-2 (small version)")
    print("2: GPT-J 6B (large, powerful model)")
    print("3: Mistral 7B (open-source powerful model)")

    choice = input("Enter the number of your choice: ")

    # Default to GPT-2 if invalid input
    model_name = MODEL_OPTIONS.get(choice, "gpt2")
    print(f"Selected model: {model_name}")
    return model_name

# Main entry point
def main():
    # Ask user to select model
    model_name = select_model()

    parser = argparse.ArgumentParser(
        prog="hokus-pokus",
        description="✨ Your magical CLI for generating text spells and performing tasks. ✨"
    )

    # Dynamic argument parsing for flexible commands
    parser.add_argument(
        'command', nargs=argparse.REMAINDER,
        help="Command to run (e.g. 'path', 'rename', etc.). If no command is provided, interactive mode starts."
    )

    args = parser.parse_args()

    if not args.command:
        # No command, start interactive prompt
        interactive_prompt(model_name)
    else:
        # Handle non-interactive commands (e.g., hokus-pokus path, rename, etc.)
        if args.command[0] == 'path':
            show_current_path()
        elif args.command[0] == 'rename' and len(args.command) == 3:
            rename_file(args.command[1], args.command[2])
        elif args.command[0] == 'cd' and len(args.command) == 2:
            change_directory(args.command[1])
        else:
            # Treat as spell for AI model
            perform_hokus_pokus(model_name, ' '.join(args.command), max_length=50, temperature=1.0)

if __name__ == "__main__":
    main()
