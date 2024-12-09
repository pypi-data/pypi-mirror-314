import re
import os

# checks all files in the entire directory, ignoring this testing file
# returns true if it detects/suspects a file may have hardcoded an API key
# returns false otherwise
def test_check_for_hardcoded_api_keys():
    directory = '.'
    not_detected = True
    # Define regex patterns for common API key formats
    patterns = [
        r'sk-[A-Za-z0-9-_]{32,}',  # Pattern specifically for OpenAI keys
        r'(?i)api[-_]?key\s*=\s*["\'][\w-]+["\']', # General pattern for setting api-key
        r'(?i)token\s*=\s*["\'][\w-]+["\']', # General pattern for setting token
        r'["\'][A-Za-z0-9-_]{40}["\']'  # General long strings that may look like keys
    ]

    # Compile regex patterns
    compiled_patterns = [re.compile(pattern) for pattern in patterns]

    # Walk through all files in the directory
    for root, _, files in os.walk(directory):
        if 'tests' in root: # disregard anything in the tests/directory
            continue
        for file_name in files:
            # Only check code files (add extensions as needed)
            if file_name.endswith(('.py', '.yml', '.yaml', '.txt')):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    for pattern in compiled_patterns:
                        matches = pattern.findall(content)
                        if matches:
                            print(f'Potential API key found in {file_path}:')
                            not_detected = False
                            for match in matches:
                                print(f'  {match}')
    assert not_detected
