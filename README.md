### ai-programmer

1. [ ] Step 1: Make it that it generates file structure.
2. [ ] Step 2: Generate code for each file without pseudocode just using description.
3. [ ] Step 3: Chain of thought + recursive inclusion of filling buffer to.
4. [ ] Step 4: Intelligently include particular code snippets using pseudocode.
5. [ ] Step 5: Now that we have good code generation, need to create good harnesses for running + testing code.

File structure probably needs to be in long-term memory.
How stateless can I make writing a file as possible? I need to navigate to get this done, but I don't want to have to include everything. Knowing what to expect to import is good

Need to keep track of what the package-manager installs will be is important. So like another storage area, and then at the end just rn those installs so that they get added to the package.json or the venv? Only begin with support for npm or yarn, with python being seperate, and not allowing cross support.

### harnesses

1. [ ] Step 1: Make it that it generates file structure.
2. [ ] Step 2: Generate code for each file without pseudocode just using description.
3. [ ] Step 3: Chain of thought + recursive inclusion of filling buffer to.
4. [ ] Step 4: Intelligently include particular code snippets using pseudocode.
5. [ ] Step 5: Now that we have good code generation, need to create good harnesses for running + 


### Usage

Run with ```python -m src.ai_programmer.main```

### Design

If a file (A) imports another file (B) it is actually more important for file B to have insight into A's implementation than vice versa to have a consistent contract. Or maybe...

### Core frustration

The final structures can vary wildly in sophistication from prompt to prompt, not flexible enough to make low_entropy edits yet. Being able to critique the model and say "you know I rather your final strcuture be like xyz" is important. Need to log why I like something or not, and use that for long-term memory and post-training DPO. Can summarize ahead of prompt after having on machine for a while.

Being able to regenerate was such a good add, because if you like a file strucutre getting better quality code from improved recursion down the line is ++. Also good way to benchmark changes