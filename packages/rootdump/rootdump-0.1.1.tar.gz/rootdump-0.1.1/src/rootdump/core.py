import os
import pathlib
from typing import List, Optional, Dict
import mimetypes


def is_binary_file(file_path: str) -> bool:
    """
    Determine if a file is binary.
    """
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        return True
    return not mime_type.startswith('text/')


def generate_tree(
    root_path: pathlib.Path,
    prefix: str = "",
    is_last: bool = True,
    exclude_binary: bool = True,
    include_extensions: Optional[List[str]] = None,
) -> str:
    """
    Generate a tree-style representation of the directory structure.

    Args:
        root_path (pathlib.Path): The root directory path
        prefix (str): Prefix for the current line (used for recursion)
        is_last (bool): Whether this is the last item in the current directory
        exclude_binary (bool): Whether to exclude binary files
        include_extensions (List[str], optional): List of extensions to include

    Returns:
        str: Tree-style representation of the directory
    """
    if not root_path.exists():
        return ""

    # Determine the marker and next prefix
    marker = "└── " if is_last else "├── "
    next_prefix = prefix + ("    " if is_last else "│   ")

    # Get the name of the current path
    name = root_path.name if root_path.name else str(root_path)

    # Start with the current directory/file
    tree = prefix + marker + name

    # If it's a directory, process its contents
    if root_path.is_dir():
        tree += "/\n"  # Add slash for directories

        # Get and sort the contents
        contents = list(root_path.iterdir())
        contents.sort(key=lambda x: (not x.is_dir(), x.name.lower()))

        # Filter contents based on criteria
        filtered_contents = []
        for item in contents:
            if item.is_dir():
                filtered_contents.append(item)
            elif item.is_file():
                if include_extensions and item.suffix not in include_extensions:
                    continue
                if exclude_binary and is_binary_file(str(item)):
                    continue
                filtered_contents.append(item)

        # Generate tree for each item
        for i, item in enumerate(filtered_contents):
            is_last_item = i == len(filtered_contents) - 1
            tree += generate_tree(
                item,
                next_prefix,
                is_last_item,
                exclude_binary,
                include_extensions
            )
    else:
        tree += "\n"

    return tree


def dump_directory(
    root_path: str,
    output_path: str,
    exclude_binary: bool = True,
    include_extensions: Optional[List[str]] = None,
    show_tree: bool = True,
) -> None:
    """
    Dump the contents of a directory into a single file, including a tree structure.

    Args:
        root_path (str): Root directory path to start exploration
        output_path (str): Output file path
        exclude_binary (bool): Whether to exclude binary files
        include_extensions (List[str], optional): List of extensions to include
        show_tree (bool): Whether to show the directory tree structure

    Returns:
        None
    """
    root_path = pathlib.Path(root_path).resolve()

    with open(output_path, 'w', encoding='utf-8') as f:
        # Add the tree structure if requested
        if show_tree:
            tree = generate_tree(
                root_path,
                exclude_binary=exclude_binary,
                include_extensions=include_extensions
            )
            f.write("# Directory structure:\n")
            for line in tree.split('\n'):
                if line:
                    f.write(f"# {line}\n")
            f.write("\n")

        # Then write the file contents
        for path in root_path.rglob('*'):
            if not path.is_file():
                continue

            if include_extensions and path.suffix not in include_extensions:
                continue

            if exclude_binary and is_binary_file(str(path)):
                continue

            try:
                relative_path = path.relative_to(root_path)

                # Read file contents
                with open(path, 'r', encoding='utf-8') as content_file:
                    content = content_file.read()

                # Write formatted output
                f.write(f"\n## {relative_path}\n\n")
                f.write(f"{content}\n\n")

            except (UnicodeDecodeError, PermissionError):
                continue


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Dump directory contents to a file')
    parser.add_argument('root_path', help='Root directory to dump')
    parser.add_argument('output_path', help='Output file path')
    parser.add_argument('--exclude-binary', action='store_true', help='Exclude binary files')
    parser.add_argument('--extensions', nargs='+', help='Include only specific extensions')
    parser.add_argument('--no-tree', action='store_true', help='Do not include directory tree structure')

    args = parser.parse_args()
    dump_directory(
        args.root_path,
        args.output_path,
        exclude_binary=args.exclude_binary,
        include_extensions=args.extensions,
        show_tree=not args.no_tree
    )


if __name__ == '__main__':
    main()
