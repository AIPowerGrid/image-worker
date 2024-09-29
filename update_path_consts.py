import fileinput
import sys
import os

# Assuming the script is executed in or below the 'image-worker' directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Commented out: we can't assume the root directory is called image-worker. This file is in the root folder anyway, so lets leave it be.
# Navigate up the directories to the 'image-worker', if not already there
#while os.path.basename(base_dir) != 'image-worker' and os.path.basename(base_dir) != '':
#    base_dir = os.path.dirname(base_dir)

# Construct the path to the file we need to edit
if sys.platform.startswith('win'):
    file_path = os.path.join(base_dir, 'conda', 'envs', 'windows', 'lib', 'site-packages', 'horde_model_reference', 'path_consts.py')
elif sys.platform.startswith('darwin'):
    file_path = os.path.join(base_dir, 'conda', 'envs', 'macos', 'lib', 'python3.10', 'site-packages', 'horde_model_reference', 'path_consts.py')
else:
    file_path = os.path.join(base_dir, 'conda', 'envs', 'linux', 'lib', 'python3.10', 'site-packages', 'horde_model_reference', 'path_consts.py')

# Check if the file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(f"The file '{file_path}' does not exist.")

owner_pattern = 'GITHUB_REPO_OWNER = "Haidra-Org"'
new_owner = 'GITHUB_REPO_OWNER = "AIPowergrid"'
repo_pattern = 'GITHUB_REPO_NAME = "AI-Horde-image-model-reference"'
new_repo = 'GITHUB_REPO_NAME = "grid-image-model-reference"'

with fileinput.FileInput(file_path, inplace=True, backup='.bak') as file:
    for line in file:
        line = line.replace(owner_pattern, new_owner)
        line = line.replace(repo_pattern, new_repo)
        sys.stdout.write(line)
