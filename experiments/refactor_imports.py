import os

def replace_in_file(filepath, old, new):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        print(f"Skipping {filepath} (encoding error)")
        return
    
    if old in content:
        print(f"Updating {filepath}: {old} -> {new}")
        new_content = content.replace(old, new)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

def main():
    root_dir = "bicameral"
    
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                replace_in_file(path, "ljpw_quantum", "bicameral.left")
                replace_in_file(path, "ljpw_nn", "bicameral.right")

if __name__ == "__main__":
    main()
