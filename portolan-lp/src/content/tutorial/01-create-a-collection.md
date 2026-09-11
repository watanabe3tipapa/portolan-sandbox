---
title: "1. Create a Collection — 最初のコレクションを作る"
description: "collection.json の最小構成を理解し、オブジェクトストレージに置ける状態を整えます。"
order: 1
pubDate: 2026-09-11
---

## collection.json とは

コレクションは Portolan で公開するデータの単位です。`collection.json` がその目次（カタログ）として振る舞います。Portolan は既存標準（STAC 互換のメタデータ）を使うため、既存の STAC エコシステムとそのまま連携できます。

## 最小構成

`collection.json` は 1 ファイルあればコレクションとして成立します。実際のデータ（GeoParquet・PMTiles など）はリンクで参照します。

```bash
my-collection/
├── collection.json   # 機械可読（ソフトウェア向け）
├── README.md         # 人間可読（データの意味・注意）
├── AGENTS.md         # AI 可読（クエリパターン等）
└── data/
    ├── places.parquet       # GeoParquet データ本体
    └── places.pmtiles       # （任意）タイル
```

## collection.json の例

```json
{
  "stac_version": "1.0.0",
  "type": "Collection",
  "id": "my-collection",
  "description": "サンプルコレクション",
  "license": "CC0-1.0",
  "extent": {
    "spatial": { "bbox": [[139.0, 35.0, 140.0, 36.0]] },
    "temporal": { "interval": [["2026-01-01T00:00:00Z", null]] }
  },
  "links": [
    {
      "rel": "items",
      "type": "application/x-parquet",
      "href": "data/places.parquet"
    },
    {
      "rel": "derived_from",
      "type": "text/markdown",
      "href": "README.md"
    },
    {
      "rel": "via",
      "type": "text/markdown",
      "href": "AGENTS.md"
    }
  ]
}
```

### 主要フィールド

| フィールド | 内容 |
|---|---|
| `stac_version` | STAC 仕様バージョン（例: 1.0.0） |
| `type` | `Collection` 固定 |
| `id` | コレクションの一意な ID |
| `description` | コレクションの説明（Markdown 可） |
| `license` | SPDX 式のライセンス ID（例: CC0-1.0, CC-BY-4.0） |
| `extent.spatial.bbox` | 空間範囲（経度・緯度の最小/最大） |
| `extent.temporal.interval` | 時間範囲（ISO 8601） |
| `links` | データ本体や関連ドキュメントへのリンク |

## データ本体（GeoParquet）を置く

Portolan では、データ本体は Parquet ベースの GeoParquet が推奨されます。カラムにジオメトリ（`geometry` 列）を持ち、通常の Parquet ツールで読みながら空間フィルタも可能です。

```bash
# GeoParquet として書き出す例（Python）
import geopandas as gpd

gdf = gpd.read_file("input.geojson")
gdf.to_parquet("data/places.parquet", schema_version="1.0.0")

# 1 ファイルで済むため、オブジェクトストレージや GitHub にそのまま配置可能
```

## オブジェクトストレージへの配置

Portolan は「サーバー運用不要」が基本です。以下のような静的な置き場に `collection.json` ごとアップロードします。

- Amazon S3 / Google Cloud Storage / Azure Blob（静的ホスティング）
- GitHub リポジトリ（GitHub Pages / raw）
- Cloudflare R2 など S3 互換ストレージ

配置後は、`collection.json` の URL をレジストリに登録すると、横断検索が可能になります。

## 検証

公開前に `collection.json` が正しいか軽く確認しましょう。STAC 互換なので、`stac` コマンドや簡単なスクリプトで検証できます。

```bash
# collection.json が読み込めるか
stac info ./collection.json
```

## 次のステップ

次のステップ: [AGENTS.md を書く](../02-agents-md/)