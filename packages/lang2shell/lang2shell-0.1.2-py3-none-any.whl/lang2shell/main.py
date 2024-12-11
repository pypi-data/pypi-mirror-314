import os
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI()

def interpret_command(natural_language_command):
    """Uses OpenAI API to interpret natural language commands into shell commands."""
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a Linux shell interpreter assistant."},
                {"role": "user", "content": f"Convert this natural language command to a MacOS shell command: {natural_language_command}"}
            ]
        )
        shell_command = completion.choices[0].message.content.strip()
        return shell_command
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
    while True:
        # Get natural language input from the user
        user_input = input("Enter a natural language command (or type 'exit' to quit): ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # Interpret the command using OpenAI API
        shell_command = interpret_command(user_input)
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
