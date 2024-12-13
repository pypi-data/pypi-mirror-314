# mcp-datetime

[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![MCP Version](https://img.shields.io/badge/mcp-1.1.1-green.svg)](https://github.com/anaisbetts/mcp)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[English](README.md) | 日本語

Claude Desktop Application用のMCPサーバーとして実装された日時フォーマットサービスです。様々な形式での日時文字列生成をサポートしています。

## 特徴

- ✨ 各種の日時フォーマットをサポート
- 🇯🇵 日本語対応
- 📁 ファイル名生成に最適化された形式
- 🌏 タイムゾーンの正確な処理
- 🔧 Claude Desktop Appとのシームレスな連携

## MCPサーバーコンポーネント

### ツール

このサーバーは1つのツールを実装しています：

- `get_datetime`: 現在の日時を様々な形式で取得
  - "format"を必須の文字列引数として受け取ります
  - 指定された形式でフォーマットされた日時文字列を返します
  - 標準形式、日本語形式、ISO形式など、複数の形式タイプをサポート

## Claude Desktop Appでの使用方法

設定ファイルに以下を追加してください：

- 設定ファイルの場所:

  - MacOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
  - Windows: `%APPDATA%/Claude/claude_desktop_config.json`

  ```json
  {
    "mcpServers": {
      "mcp-datetime": {
        "command": "uvx",
        "args": ["mcp-datetime"]
      }
    }
  }
  ```

## インストールについて

通常はインストール作業は必要ありません。Claude デスクトップアプリの設定ファイルに設定を追加するだけで使用できます。 uvxが必要に応じてパッケージを自動的にダウンロードし実行します。

ソースコードの確認や開発目的など、パッケージを直接インストールする必要がある場合は、以下の方法でインストールできます：

- PyPIからインストール

  ```bash
  pip install mcp-datetime
  ```

- GitHubのソースコードからインストール

  ```bash
  git clone https://github.com/ZeparHyfar/mcp-datetime.git
  cd mcp-datetime
  pip install -e .
  ```

- 手動でインストールした場合の`claude_desktop_config.json`

  ```json
  {
    "mcpServers": {
      "mcp-datetime": {
        "command": "python",
        "args": ["-m", "mcp_datetime"],
        "env": {
          "PYTHON": "/path/to/your/python"
        }
      }
    }
  }
  ```

  - "/path/to/your/python"は実際のPythonインタプリタのパスに置き換えてください。

  - 例：
    - MacOS: "/usr/local/bin/python3" や "/Users/username/.pyenv/versions/3.12.0/bin/python3"
    - Windows: "C:\Python312\python.exe"

## 基本的な使用例

- コマンド形式

  ```
  # 標準的な日時形式
  call datetime-service.get_datetime {"format": "datetime"}
  # 結果: 2024-12-10 00:54:01

  # 日本語形式
  call datetime-service.get_datetime {"format": "datetime_jp"}
  # 結果: 2024年12月10日 00時54分01秒

  # ファイル名形式
  call datetime-service.get_datetime {"format": "filename_md"}
  # 結果: 20241210005401.md
  ```

- Claudeデスクトップアプリのプロンプト例

  - User

    ```
    今の時刻をdate_slash形式で教えてください
    ```

  - Claude

    ```
    date_slash形式で現在の日付を取得します。

    現在の日付は 2024/12/12 です。
    ```

## サポートされている形式

| 形式名       | 例                          | 説明                     |
| ------------ | --------------------------- | ------------------------ |
| date         | 2024-12-10                  | 標準的な日付形式         |
| date_slash   | 2024/12/10                  | スラッシュ区切りの日付   |
| date_jp      | 2024年12月10日              | 日本語の日付形式         |
| datetime     | 2024-12-10 00:54:01         | 標準的な日時形式         |
| datetime_jp  | 2024年12月10日 00時54分01秒 | 日本語の日時形式         |
| datetime_t   | 2024-12-10T00:54:01         | T区切りの日時形式        |
| compact      | 20241210005401              | ID用のコンパクト形式     |
| compact_date | 20241210                    | 日付のみのコンパクト形式 |
| compact_time | 005401                      | 時刻のみのコンパクト形式 |
| filename_md  | 20241210005401.md           | Markdownファイル名形式   |
| filename_txt | 20241210005401.txt          | テキストファイル名形式   |
| filename_log | 20241210005401.log          | ログファイル名形式       |
| iso          | 2024-12-10T00:54:01+0900    | ISO 8601形式             |
| iso_basic    | 20241210T005401+0900        | 基本ISO形式              |
| log          | 2024-12-10 00:54:01.123456  | マイクロ秒付きログ形式   |
| log_compact  | 20241210_005401             | コンパクトなログ形式     |
| time         | 00:54:01                    | 時刻のみの形式           |
| time_jp      | 00時54分01秒                | 日本語の時刻形式         |

## デバッグ

MCPサーバーはstdioを介して実行されるため、デバッグが難しい場合があります。[MCP Inspector](https://github.com/modelcontextprotocol/inspector)の使用を推奨します：

- PyPIパッケージを使用する場合

  ```
  npx @modelcontextprotocol/inspector uvx mcp-datetime
  ```

- GitHubからダウンロードしたソースコードを使用する場合

  ```
  git clone https://github.com/ZeparHyfar/mcp-datetime.git
  npx @modelcontextprotocol/inspector uvx --directory ./mcp-datetime run mcp-datetime
  ```

## ライセンス

このプロジェクトはMITライセンスの下で提供されています - 詳細は[LICENSE](LICENSE)ファイルを参照してください。
