import os

# Path to your models directory
models_dir = 'c:/Users/Bruger/source/repos/ApiService'

# Printing all files and directories in the specified directory
for root, dirs, files in os.walk(models_dir):
    for name in files:
        print(os.path.join(root, name))
    for name in dirs:
        print(os.path.join(root, name))
