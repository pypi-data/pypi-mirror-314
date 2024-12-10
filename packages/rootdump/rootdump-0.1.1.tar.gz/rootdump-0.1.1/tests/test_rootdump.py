import os
import tempfile
import pathlib
from rootdump import dump_directory
import pytest

def test_dump_directory():
    # テスト用の一時ディレクトリを作成
    with tempfile.TemporaryDirectory() as temp_dir:
        # テストファイルを作成
        test_files = {
            "test1.txt": "Hello World",
            "subdir/test2.txt": "Test content",
            "test3.py": "print('Hello')"
        }
        
        for path, content in test_files.items():
            file_path = pathlib.Path(temp_dir) / path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content)
        
        # 出力用の一時ファイル
        output_file = pathlib.Path(temp_dir) / "output.txt"
        
        # ダンプを実行
        dump_directory(temp_dir, str(output_file))
        
        # 結果を確認
        result = output_file.read_text()
        
        # 各ファイルの内容が含まれているか確認
        for path, content in test_files.items():
            assert path in result
            assert content in result

def test_exclude_binary():
    with tempfile.TemporaryDirectory() as temp_dir:
        # バイナリファイルを作成
        binary_file = pathlib.Path(temp_dir) / "test.bin"
        binary_file.write_bytes(b'\x00\x01\x02\x03')
        
        # テキストファイルを作成
        text_file = pathlib.Path(temp_dir) / "test.txt"
        text_file.write_text("Hello")
        
        output_file = pathlib.Path(temp_dir) / "output.txt"
        
        # バイナリファイル除外オプションを有効にしてダンプ
        dump_directory(temp_dir, str(output_file), exclude_binary=True)
        
        result = output_file.read_text()
        
        # バイナリファイルが除外され、テキストファイルのみ含まれているか確認
        assert "test.bin" not in result
        assert "test.txt" in result
        assert "Hello" in result

def test_include_extensions():
    with tempfile.TemporaryDirectory() as temp_dir:
        # 異なる拡張子のファイルを作成
        files = {
            "test.txt": "Text content",
            "test.py": "print('Hello')",
            "test.md": "# Markdown"
        }
        
        for path, content in files.items():
            file_path = pathlib.Path(temp_dir) / path
            file_path.write_text(content)
        
        output_file = pathlib.Path(temp_dir) / "output.txt"
        
        # .txtと.pyファイルのみを含めてダンプ
        dump_directory(
            temp_dir,
            str(output_file),
            include_extensions=[".txt", ".py"]
        )
        
        result = output_file.read_text()
        
        # 指定した拡張子のファイルのみが含まれているか確認
        assert "test.txt" in result
        assert "test.py" in result
        assert "test.md" not in result
