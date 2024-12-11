import os
import re
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI()

def get_shell_type():
    """Detects the current shell type (e.g., zsh or bash)."""
    shell_path = os.getenv("SHELL", "")
    if "zsh" in shell_path:
        return "zsh"
    elif "bash" in shell_path:
        return "bash"
    else:
        return "an unknown shell"

def extract_command(response):
    """Extracts the shell command from the OpenAI response."""
    # Use regex to extract content within code block or after explanatory text
    match = re.search(r'```[a-z]*\n(.*?)\n```', response, re.DOTALL)
    if match:
        return match.group(1).strip()
    # Fallback: Assume response starts with the command
    return response.split("\n")[0].strip()

def interpret_command(natural_language_command, shell_type):
    """Uses OpenAI API to interpret natural language commands into shell commands."""
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"You are a {shell_type} interpreter assistant for MacOS."},
                {"role": "user", "content": f"Convert this natural language command to a {shell_type} shell command: {natural_language_command}"}
            ]
        )
        shell_command = completion.choices[0].message.content.strip()
        return extract_command(shell_command)
    except Exception as e:
        print(f"Error interpreting command: {e}")
        return None

def execute_shell_command(shell_command):
    """Executes a shell command in the Linux environment."""
    try:
        print(f"Executing: {shell_command}")
        os.system(shell_command)
    except Exception as e:
        print(f"Error executing command: {e}")

def main():
    shell_type = get_shell_type()
    print(f"Detected shell: {shell_type}")
    
    while True:
        # Get natural language input from the user
        user_input = input("Enter a natural language command (or type 'exit' to quit): ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # Interpret the command using OpenAI API
        shell_command = interpret_command(user_input, shell_type)
        if shell_command:
            print(f"Suggested shell command: {shell_command}")

            # Confirm with the user before executing
            confirm = input("Do you want to execute this command? (yes/no): ").strip().lower()
            if confirm in ['yes', 'y']:
                execute_shell_command(shell_command)
            else:
                print("Command execution canceled.")

if __name__ == "__main__":
    main()
