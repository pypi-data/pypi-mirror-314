# rootdump

A Python library for dumping directory contents into a single text file. It allows you to easily inspect and document your project structure and file contents.

## Features

- Dump all text files from a directory into a single file
- Exclude binary files (optional)
- Filter files by extension
- Generate tree-style directory structure visualization
- UTF-8 support

## Installation

```bash
pip install rootdump
```

## Usage

### Command Line Interface

Basic usage:
```bash
rootdump /path/to/source output.txt
```

Exclude binary files:
```bash
rootdump /path/to/source output.txt --exclude-binary
```

Include only specific file extensions:
```bash
rootdump /path/to/source output.txt --extensions .py .txt .md

Skip directory tree structure:
```bash
rootdump /path/to/source output.txt --no-tree
```

### Python API

```python
from rootdump import dump_directory

# Basic usage
dump_directory("source_dir", "output.txt")

# Exclude binary files and include only specific extensions
dump_directory(
    "source_dir",
    "output.txt",
    exclude_binary=True,
    include_extensions=[".py", ".txt"],
    show_tree=True  # Set to False to skip directory tree
)
```

## Output Format

The output file will contain:

1. A tree-style directory structure overview
2. Contents of each file, separated by headers showing the relative path

Example output:
```
# Directory structure:
# .
# ├── src/
# │   ├── __init__.py
# │   └── core.py
# └── tests/
#     └── test_core.py

## src/__init__.py

[file contents here]

## src/core.py

[file contents here]
```

## License

MIT License