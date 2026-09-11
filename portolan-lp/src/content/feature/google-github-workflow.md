---
title: "ケーススタディ — Google アカウント × GitHub アカウントの両立ワークフロー"
description: "Google と GitHub の両アカウントを持っている場合、Colab でのデータ準備と GitHub Pages での公開をどう組み合わせるかを整理します。"
pubDate: 2026-09-11
---

## 想定するユーザー

「Google アカウントだけで完結」という構想は、初学者や教育現場を想定したハードル下げのための極論です。**現実の典型ユーザーは Google と GitHub の両方を持っています。**

両方を持っている人が、Portolan のデータコレクションを「準備 → 公開 → AI に読ませる」まで一気通貫で行うためのワークフローを整理します。

## 役割分担

| レイヤー | Google アカウント（Colab） | GitHub アカウント（リポジトリ） |
|---|---|---|
| 認証 | OAuth でログイン、追加基盤不要 | GitHub 自体が認証基盤 |
| データ生成・検証 | GeoPandas で前処理・CRS 変換 | / |
| コンテンツ配信 | / | GitHub Pages（GitHub Actions） |
| メタデータ・カタログ | collection.json を生成 | Pages 上の公開 URL で配信 |
| AI 連携 | Colab MCP server（パーソナル・開発サーバー） | Pages 公開データを参照（認証不要） |
| 版管理・コラボ | / | git / PR / Issue |

## 一気通貫の流れ

```text
データ準備 (Colab)
  └─ GeoPandas で 3857 → 4326 変換などの前処理・検証
  └─ collection.json / AGENTS.md を生成
public/ に配置 → commit → push (GitHub アカウント)
  └─ GitHub Actions が自動で build → Pages デプロイ
AI エージェント（任意の MCP クライアント）
  └─ Pages 公開 URL (collection.json / *.parquet) を直接参照
  └─ Colab MCP server を経由すれば Google アカウントの状態も操作
```

## 実装例（本リポジトリの実績）

本リポジトリはこの両立ワークフローを実際に動かして検証済みです。

### 1. Colab でデータを整える

```python
# Colab 上で GeoDataFrame を EPSG:3857 から 4326 に変換し Parquet へ
import geopandas as gpd

gdf = gpd.read_parquet("data/poi.parquet")   # 3857 で保存済み
gdf = gdf.to_crs("EPSG:4326")
gdf.to_parquet("data/poi_4326.parquet", schema_version="1.0.0")
```

### 2. `public/` に置いて GitHub へ push

データは Astro プロジェクトの `public/` に置くだけで、ビルド時に `dist/` へコピーされ GitHub Pages でそのまま配信されます。

```text
portolan-lp/public/demo-collection/
├── collection.json   # メタデータ（機械可読）
├── README.md         # 人間向け説明
└── data/poi.parquet  # GeoParquet データ本体
```

```bash
git add -A
git commit -m "Add demo collection"
git push origin main
```

push 後、GitHub Actions が自動でビルドし、以下の URL で公開されます。

```text
https://<username>.github.io/<repo>/demo-collection/collection.json
```

### 3. AI エージェントから直接参照

コレクションは公開 URL として存在するため、AI エージェントが認証なしで読み取れます（AGENTS.md の「3 つの入り口」の通り）。

```python
# 公開 URL から直接読む（認証不要）
from server import read_collection

print(read_collection("https://<username>.github.io/<repo>/demo-collection/collection.json"))
```

## 使い分けの指針

| 状況 | 使うもの |
|---|---|
| 手元にいないがデータを確かめたい | Google アカウント + Colab（ブラウザだけで完結） |
| 公開・配信・版管理したい | GitHub アカウント（Pages / Actions / git） |
| エージェントに「読ませる」 | どちらでも可（Pages 公開 URL は認証不要） |
| 個人の開発サーバーにしたい | Google アカウント + Colab MCP server |
| データを外部 AI に渡さず解析したい | Google アカウント + ローカル LLM（Ollama） |

## このケースが示すこと

両アカウントの持ち主にとって、GitHub Pages は「公開・配信」の主役であり、Colab は「データ準備・検証・プライベート解析」の主役です。この二つを接続しているのが Portolan の考え方——**データは take down せず、開いた状態で公開しておく**——です。

Colab MCP server を使えば、この両者の橋渡し（GitHub Pages へのデプロイ含む）も、ローカル .git 環境がなくても実行できます。詳細は「[Colab MCP server に期待できる機能](/feature/colab-mcp-server/)」を参照してください。