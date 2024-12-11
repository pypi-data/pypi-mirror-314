import os
import sys

def find_root(filename: str, start_path: str) -> str | None:
    current_path = os.path.abspath(start_path)
    
    while current_path:
        files = os.listdir(current_path)

        if filename in files:
            return os.path.join(current_path, filename)

        parent_path = os.path.dirname(current_path)
        
        if parent_path == current_path:
            break
        
        current_path = parent_path 

    return None

def setup():
    root_file_path = find_root("root.vmm", sys.path[0])

    if not root_file_path: return

    with open(root_file_path, 'r') as file:
        file_content = file.read().strip()
        if not file_content:
            print(os.path.dirname(root_file_path))            
            sys.path.append(os.path.dirname(root_file_path))
        else:
            if os.path.isabs(file_content):
                sys.path.append(file_content)
            else:
                joined_path = os.path.join(os.path.dirname(root_file_path), file_content)
                sys.path.append(joined_path)
setup()

