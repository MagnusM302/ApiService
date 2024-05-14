import os

def show_directory_tree(path):
    for root, dirs, files in os.walk(path):
        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f'{indent}{os.path.basename(root)}/')

        if files:
            sub_indent = indent + ' ' * 4
            for file in files:
                print(f'{sub_indent}{file}')

if __name__ == '__main__':
    path = os.getcwd()  # Get current working directory
    show_directory_tree(path)