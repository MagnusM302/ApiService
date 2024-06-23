import os

def print_file_contents(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):  # Antager at vi kun er interesserede i Python-filer
                file_path = os.path.join(root, file)
                print(f"--- Indhold af {file_path} ---")
                with open(file_path, 'r', encoding='utf-8') as f:
                    print(f.read())
                print("\n\n")  # Tilføjer ekstra linjer mellem filer for bedre læsbarhed

# Erstat 'path_to_your_directory' med stien til mappen, hvor dine filer er placeret
directory_path = r'C:\Users\Bruger\source\repos\ApiService'
print_file_contents(directory_path)
