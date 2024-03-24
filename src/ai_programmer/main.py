import os
from openai import OpenAI
import subprocess
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure your OpenAI API key
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
def generate_code(project_name, frameworks, description):
    # Use OpenAI's API to generate code based on the project name and frameworks
    # This is a simplified example, you'll need to format the prompt for your specific use case
    prompt = f"Create a full stack web app demo called '{project_name}' using {frameworks}. The project file description is as follows: {description}. Output the file structure without any extraneous text as comma-separated values, without any introductory text."
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

def write_code_to_files(description, file_name, output_dir):
    code = description.replace(", ", "\n")
    with open(os.path.join(output_dir, file_name), 'w') as f:
        f.write(code)

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

def main():
    project_name = input("Enter the name of the project: ")
    frameworks = input("Enter the frameworks to use, comma-separated: ")
    package_manager = get_package_manager()
    description = input("Enter the project file description: ")
    files = generate_code(project_name, frameworks, description)
    output_dir = os.path.join("output", project_name)
    create_file_structure(output_dir, files)
    write_code_to_files(description, files, output_dir)

    # Change directory and run the code
    os.chdir(output_dir)
    subprocess.run(["python", "app.py"])

if __name__ == "__main__":
    main()