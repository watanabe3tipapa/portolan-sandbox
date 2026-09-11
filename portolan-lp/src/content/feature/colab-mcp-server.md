---
title: "Colab MCP server に期待できる機能 — Google アカウントだけで完結する開発基盤"
description: "Google Colaboratory を MCP server として使う構想。認証・ストレージ・デプロイを Google アカウントだけで完結させるために期待できる機能を整理します。"
pubDate: 2026-09-11
---

## Colab を「サーバーとして」使う発想

Google Colaboratory（Colab）はブラウザ上で動く Jupyter ノートブック環境です。通常は「一時的な実行環境」として使われますが、**MCP（Model Context Protocol）server** として立ち上げることで、AI エージェントから操作できる個人開発サーバーにできます。

「Google アカウントだけで全ての操作を済ませたい」という構想において、Colab は認証・仮想環境・（間接的に）ストレージまで提供する要の存在です。

## MCP server とは

MCP は AI モデルと外部のデータ・ツールを接続するための共通プロトコルです。MCP server を用意すると、エージェントは「ファイルの読み書き」「ツールの実行」「データの参照」などを統一された方法で行えます。

```text
MCP クライアント（Claude 等）
        │ 標準化された手順（ツール呼び出し）
        ▼
MCP server（例: Colab 上で稼働）
        ├─ ツール定義（エージェントが呼べる関数）
        ├─ データ参照（Drive / ランタイムのファイル）
        └─ 実行（コード・シェル）
```

ツールは「名前」「説明」「入力スキーマ」だけで公開でき、エージェントはその説明を読んで自ら呼び出すか判断します。

## Colab MCP server に期待できる対応機能

### 1. Google アカウントによる認証

- OAuth によるログインをそのまま利用
- 追加の認証基盤（API キー発行など）が不要
- 接続者は「自分の Google アカウント」で制御可能

### 2. ファイル・ストレージ操作

- **Google Drive** への読み書き（マウント済みならパス操作）
- ローカルランタイム（セッション）上のファイル操作
- Cloud Storage へのアップロード・ダウンロード
- GitHub リポジトリの clone / push（公開リポジトリなら認証不要）

### 3. データ作成・検証

- 地理空間データの前処理・検証（GeoParquet / COG の生成やチェック）
- `collection.json`・`AGENTS.md` の雛形生成
- 準拠チェック（リンター）の実行
- GeoPandas による空間変換（EPSG 変換、バッファ、結合）

### 4. デプロイ・公開

- 静的サイト（GitHub Pages 等）へのデプロイ
- ファイルの「開いた状態での配置」＝ Portolan の公開フローそのもの
- ローカル検証 → 本番公開までの一連の流れをエージェントに任せる

### 5. Colab 内の開発ループ

- ノートブックでのスクラッチ試作 → エージェントとの対話で試行錯誤
- 結果をノートブック・Drive に保存
- 失敗してもセッション再起動でやり直し（環境が汚れない）

## 実装イメージ（FastMCP）

Python で MCP server を書く場合、`fastmcp` ライブラリでツールを数行で公開できます。

```python
# Colab 上のノートブックで動く MCP server のイメージ
from fastmcp import FastMCP

mcp = FastMCP("colab-dev-server")

@mcp.tool
def read_collection(url: str) -> str:
    """collection.json を読んで概要を返す"""
    import json, urllib.request
    return json.dumps(json.load(urllib.request.urlopen(url)), indent=2)

@mcp.tool
def convert_parquet(source: str, target: str) -> str:
    """GeoParquet を読み書きする（EPSG 変換等）"""
    import geopandas as gpd
    gdf = gpd.read_parquet(source)
    gdf = gdf.to_crs("EPSG:4326")
    gdf.to_parquet(target)
    return f"converted -> {target}"

mcp.run()  # transport は stdio / streamable HTTP を選択可能
```

このコードを Colab で実行し、`mcp.run()` のエンドポイントを MCP クライアントに登録すれば、エージェントから `read_collection()` や `convert_parquet()` を呼び出せます。

## 構想とのつながり

このリポジトリ（DEV-MEMO.md の「構想」節）では、次のように Colab MCP server の利活用を考察しています。

- Portolan と Google Colaboratory との連携手法
- Colab MCP server（パーソナル・開発サーバーとしての位置付け）の利活用
- Google アカウントだけで全ての措置（認証・デプロイなど）に対応

Colab MCP server は、その構想を現実化するための「要」になる存在です。

## ロードマップ（案）

1. Colab で FastMCP ベースの server を起動し、`read_*` 系ツールを公開（読む）
2. 変換・検証ツールを追加（作る）
3. GitHub Pages へのデプロイツールを公開（出す）
4. Google アカウント認証だけで接続できる形に整理（認証の一本化）

## 注意点

- Colab のセッションは実行中のみ稼働（数時間でリセット）
- 公開サーバーとしての利用には認証・CORS の設計が別途必要
- 重要なファイルは Drive / GitHub に置き、ローカルに置きっぱなしにしない