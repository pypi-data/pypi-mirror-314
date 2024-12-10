import os
import pathlib
from typing import List, Optional
import mimetypes


def is_binary_file(file_path: str) -> bool:
    """
    ファイルがバイナリかどうかを判定します。
    """
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        return True
    return not mime_type.startswith('text/')


def dump_directory(
    root_path: str,
    output_path: str,
    exclude_binary: bool = True,
    include_extensions: Optional[List[str]] = None,
) -> None:
    """
    指定されたディレクトリ以下のファイルをダンプします。

    Args:
        root_path (str): 探索を開始するルートディレクトリのパス
        output_path (str): 出力ファイルのパス
        exclude_binary (bool): バイナリファイルを除外するかどうか
        include_extensions (List[str], optional): 含める拡張子のリスト

    Returns:
        None
    """
    root_path = pathlib.Path(root_path).resolve()

    with open(output_path, 'w', encoding='utf-8') as f:
        for path in root_path.rglob('*'):
            if not path.is_file():
                continue

            if include_extensions and path.suffix not in include_extensions:
                continue

            if exclude_binary and is_binary_file(str(path)):
                continue

            try:
                relative_path = path.relative_to(root_path)

                # ファイル内容を読み込む
                with open(path, 'r', encoding='utf-8') as content_file:
                    content = content_file.read()

                # フォーマットに従って書き込み
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

    args = parser.parse_args()
    dump_directory(args.root_path, args.output_path,
                   exclude_binary=args.exclude_binary,
                   include_extensions=args.extensions)


if __name__ == '__main__':
    main()
