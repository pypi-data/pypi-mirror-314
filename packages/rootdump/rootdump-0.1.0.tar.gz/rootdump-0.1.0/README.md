# rootdump

rootdumpは、指定されたルートディレクトリ以下のすべてのファイルを探索し、それらのファイルの内容とパスを単一のファイルにダンプするPythonライブラリです。

## インストール

```bash
pip install rootdump
```

## 使用方法

```python
from rootdump import dump_directory

# ディレクトリの内容をダンプ
dump_directory("/path/to/root", "output.txt")

# バイナリファイルを除外してダンプ
dump_directory("/path/to/root", "output.txt", exclude_binary=True)

# 特定の拡張子のみをダンプ
dump_directory("/path/to/root", "output.txt", include_extensions=[".txt", ".py"])
```
