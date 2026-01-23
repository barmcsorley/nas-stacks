import os

def sanitize_file(filepath):
    """Creates a .env.example file with blank values."""
    example_path = filepath + ".example"
    
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    with open(example_path, 'w') as f:
        f.write("# SECURITY WARNING: This is an example file.\n")
        f.write("# RENAME to .env and insert your own secrets.\n\n")
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                f.write(line + '\n')
                continue
            
            # Split key=value. Keep Key, redact Value.
            if '=' in line:
                key, _ = line.split('=', 1)
                f.write(f"{key}=<REDACTED>\n")
    
    print(f"✅ Generated: {example_path}")

def scan_and_sanitize():
    # Walk through all folders
    for root, dirs, files in os.walk("."):
        for file in files:
            if file == ".env":
                full_path = os.path.join(root, file)
                sanitize_file(full_path)

if __name__ == "__main__":
    scan_and_sanitize()
