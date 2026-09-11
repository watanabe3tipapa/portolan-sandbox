# Portolan Colab MCP server

「Google アカウントだけで完結する認証・デプロイ」の検証用デモ。FastMCP ベースの MCP server を Google Colaboratory 上で動かし、Portolan コレクションの作成・検証・GitHub Pages へのデプロイを行います。

## 構成

- `server.py` — FastMCP server（ツール定義）
- `pyproject.toml` / `uv.lock` — Python 依存（fastmcp, geopandas, pyarrow）
- `fixtures/collection.json` — 検証用のコレクション定義
- `colab_portolan_mcp.ipynb` — Colab でそのまま実行できるノートブック

## ツール一覧

| ツール | 機能 |
|---|---|
| `read_collection(url)` | 公開 URL の collection.json を読む |
| `read_geoparquet(source, crs_out, limit)` | GeoParquet を（URL/ローカル）から読み、CRS 変換して概要を返す |
| `convert_geoparquet(source, target, crs_out)` | GeoParquet を CRS 変換して書き出す |
| `validate_collection(path)` | collection.json を STAC/Portolan の基本で検証 |
| `deploy_to_github_pages(repo, file_path, content, message)` | GitHub Contents API でリポジトリのファイルを更新（push 不要） |
| `write_to_drive(filename, content)` | マウント済み Google Drive への書き込み |

## ローカルでの検証

```bash
cd demos/colab-mcp-server
uv sync
uv run python -c "from server import read_collection; print(read_collection('https://watanabe3tipapa.github.io/portolan-sandbox/demo-collection/collection.json'))"
```

GitHub ツールを使う場合は `gh auth login` 済みか、`GITHUB_TOKEN` 環境変数が必要です。

## Colab での使い方

1. [colab_portolan_mcp.ipynb](./colab_portolan_mcp.ipynb) を Google Drive にアップロード
2. セルを上から順に実行（Drive マウントで Google アカウント認証）
3. GitHub fine-grained token を入力
4. 最終セルで `deploy_to_github_pages` を呼ぶと GitHub Pages へ反映される

詳細な説明は [DEV-MEMO.md](../../DEV-MEMO.md) の「検証記録」と「追録」の節を参照してください。