import os

def print_directory_structure(path):
    """
    Udskriver strukturen af en given mappe.
    """
    for root, dirs, files in os.walk(path):
        print(root)
        for dir in dirs:
            print(f"  {dir}")
        for file in files:
            print(f"  {file}")

# Angiv mappen, du ønsker at udskrive strukturen for
directory_path = r'C:\Users\Bruger\source\repos\ApiService'

# Brug funktionen til at udskrive strukturen af mappen
print_directory_structure(directory_path)