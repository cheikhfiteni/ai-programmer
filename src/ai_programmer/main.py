import os
from openai import OpenAI
import subprocess
from dotenv import load_dotenv
import logging
from datetime import datetime
# Load environment variables
load_dotenv()

# Configure your OpenAI API key
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
def generate_file_structure(project_name, frameworks, description):
    # Use OpenAI's API to generate code based on the project name and frameworks
    # This is a simplified example, you'll need to format the prompt for your specific use case
    prompt = f"Create a full stack web app demo called '{project_name}' using {frameworks}. The project file description is as follows: {description}. Output the file structure without any extraneous text as comma-separated values, without any introductory or extra text."
    completion = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who can code."},
            {"role": "user", "content": prompt}
        ]
    )
    print(completion.choices[0].message)
    file_paths = completion.choices[0].message.content.split(',')
    # Strip whitespace from each file path
    file_paths = [path.strip() for path in file_paths]
    return file_paths

def generate_code_for_file(file_name, message_history):
    # Add a user message indicating the file to generate code for
    message_history.append({
        "role": "user",
        "content": f"File: {file_name}. Please provide the code as plain text without any comments or markdown."
    })

    # Request code generation from OpenAI. Switch to 4 for more performance later.
    completion = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=message_history
    )

    # Extract the generated code
    generated_code = completion.choices[0].message.content.strip()

    # Check if the generated code is wrapped in markdown code block syntax
    if '```' in generated_code:
        # Split the code into lines
        lines = generated_code.split('\n')
        # Find the indices of the lines containing the starting and ending backticks
        start_idx = next((i for i, line in enumerate(lines) if '```' in line), None)
        end_idx = next((i for i, line in enumerate(lines[start_idx + 1:], start=start_idx + 1) if '```' in line), None)
        
        # Extract the code within the markdown code block, excluding the lines with backticks
        if start_idx is not None and end_idx is not None:
            generated_code = '\n'.join(lines[start_idx + 1:end_idx]).strip()

    # Add the generated code as a system message to the history
    message_history.append({
        "role": "system",
        "content": f"Here is the code for {file_name}:\n{generated_code}"
    })

    # Return the generated code and the updated message history
    return generated_code, message_history

def write_code_to_files(output_dir, files, description):
    prompt = f"You are a code gen assistant building an entire repo. You will be given a description of what to build and the entire file structure of the project upfront. On each successive call, you will be given a file name (and the previous context of the code you've already generated) and will output just the code for that file, with no extra text.\n\nDescription: {description}\n\nProject file structure:{files}"
    # Initialize message history with the description and file structure
    message_history = [
        {"role": "system", "content": prompt},
    ]

    for file_name in files:
        # Check if the path has a file extension, indicating that it's a file
        if '.' in os.path.basename(file_name):
            code, message_history = generate_code_for_file(file_name, message_history)
            file_path = os.path.join(output_dir, file_name)
            with open(file_path, 'w') as f:
                f.write(code)
            print(f"Code for {file_name} written successfully.")
        else:
            # It's a directory, so continue without writing code
            continue

def create_file_structure(output_dir, files):
    # Create the file structure in the output directory
    for file in files:
        file_path = os.path.join(output_dir, file)
        # Check if the path has a file extension
        if '.' in os.path.basename(file_path):
            # It's a file, create necessary directories and then the file
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                f.write("")
            print(file_path, ' created successfully')
        else:
            # It's a directory, create it
            os.makedirs(file_path, exist_ok=True)
            print(file_path, ' directory created successfully')

def handle_dependencies(frameworks):
    # Handle dependencies based on the frameworks used
    dependencies = {
        "React": "npm install react",
        "Vue": "npm install vue",
        "Angular": "npm install angular"
    }
    frameworks = frameworks.split(',')
    for framework in frameworks:
        if framework in dependencies:
            print(dependencies[framework])

def get_package_manager():
    valid_package_managers = ['pip', 'yarn', 'npm']
    package_manager = input("Enter the package manager to use: ").strip().lower()
    if package_manager not in valid_package_managers:
        raise ValueError(f"Invalid package manager. Supported package managers are: {', '.join(valid_package_managers)}")
    return package_manager

# Configure logging
logging.basicConfig(filename='project_creation.log', level=logging.INFO, format='%(message)s')

def log_inputs(project_name, frameworks, description):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"{timestamp}\nProject Name: {project_name}\nFrameworks: {frameworks}\nDescription: {description}"
    logging.info(log_message)

def main():
    project_name = input("Enter the name of the project: ")
    frameworks = input("Enter the frameworks to use, comma-separated: ")
    description = input("Enter the project file description: ")

    # Log the inputs
    log_inputs(project_name, frameworks, description)


    files = generate_file_structure(project_name, frameworks, description)
    output_dir = os.path.join("output", project_name)
    create_file_structure(output_dir, files)
    write_code_to_files(output_dir, files, description)

    # Change directory and run the code
    os.chdir(output_dir)
    subprocess.run(["python", "app.py"])

if __name__ == "__main__":
    main()