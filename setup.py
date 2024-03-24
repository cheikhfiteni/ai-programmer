# setup.py
from setuptools import setup, find_packages

setup(
    name='ai_programmer',
    version='0.1.0',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # List your project's dependencies here.
        # They will be installed by pip when your project is installed.
        'openai',
        'python-dotenv',
        # etc...
    ],
    entry_points={
        'console_scripts': [
            'ai_programmer=ai_programmer.main:main',
        ],
    },
    # Additional metadata about your package.
    author='Cheikh Fiteni',
    author_email='sfiteni@college.harvard.edu',
    description='An AI programmer tool to automate boilerplate generation + eventually perform autonomous edits',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # This is important to render README.md correctly
    url='https://github.com/cheikhfiteni/ai_programmer',
    # And more. See the Python Packaging User Guide for details.
)