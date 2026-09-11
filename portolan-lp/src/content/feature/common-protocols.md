---
title: "共通プロトコルの用例 — STAC・GeoParquet・PMTiles が開く横断参照"
description: "地図データを横断的に参照するための共通プロトコル（STAC・GeoParquet・COG・PMTiles）のユースケースを、コード例を交えて紹介します。"
pubDate: 2026-09-11
---

## なぜ共通プロトコルが必要か

地理空間データはこれまで、ポータル・専用 API・FTP という「それぞれ違う入り口」で配布されてきました。AI エージェントが自律的にデータを調達するには、入り口の差異を吸収する共通の読み口が必要です。

## 主要な共通プロトコル

### STAC（SpatioTemporal Asset Catalog）

衛星データや地図データに統一ラベルを付与し、横断検索を可能にする規格です。

```bash
# レジストリからカタログを検索する例
stac search --catalog https://example.org/collection.json \
  --bbox 139.0,35.0,140.0,36.0
```

Python での利用:

```python
import pystac_client

# STAC カタログを横断検索
catalog = pystac_client.Client.open("https://example.org/catalog.json")
items = catalog.search(
    bbox=[139.0, 35.0, 140.0, 36.0],
    datetime="2026-01-01/2026-09-11"
)
for item in items.items():
    print(item.id, item.datetime)
```

### GeoParquet

地理情報を Parquet 列指向形式で表現し、高速な空間フィルタを可能にします。

```python
import duckdb

duckdb.sql("""
  SELECT * FROM 'data.parquet'
  WHERE ST_Within(
    geom,
    ST_GeomFromText('POLYGON((139 35,139 36,140 36,140 35,139 35))')
  )
""")
```

GeoParquet の特徴:

| 特徴 | 効果 |
|---|---|
| 列指向 | 必要なカラムだけ効率よく読める |
| 空間インデックス | 高速な空間フィルタ |
| 1 ファイル | サーバー運用不要 |

### PMTiles

1 ファイルで済むタイルアーカイブ形式。サーバー運用なしに静的公開できます。

```text
PMTiles の特徴:
- Byte-Range Request で部分読み込み
- HTTP サーバー1台で公開可能
- GitHub Pages でも配信可能
```

### COG（Cloud Optimized GeoTIFF）

GeoTIFF をクラウドストレージ向けに最適化した形式。ベクターデータではなくラスターデータに使います。

```text
COG の特徴:
- HTTP レンジリクエストで部分読み込み
- ビジュアライザにそのまま配信可能
- 空間範囲クエリで特定部分だけ取得
```

## 各プロトコルの使い分け

| 用途 | 推奨形式 |
|---|---|
| ポイント・ライン・ポリゴン（ベクタ） | GeoParquet |
| タイル（ラスター表示） | PMTiles / COG |
| 横断検索・カタログ | STAC |
| ラスターの高速参照 | COG |

## Portolan との関係

Portolan 自体は新形式ではなく、**これらの標準を組み合わせたベストプラクティス**です。AGENTS.md が「どのプロトコルを使えば速いか」を教え、AI エージェントが最初から意図通りに使えるようにします。

```markdown
# AGENTS.md の例

## 推奨プロトコル
- ベクターデータ: GeoParquet（場所フィルタにこの形式を使うと速い）
- タイル: PMTiles（ビューワにそのまま配信）
- ラスター: COG（部分取得可能）
```

## 用例まとめ

- **横断検索**: STAC で複数組織のカタログを検索
- **高速フィルタ**: GeoParquet で空間フィルタを実行
- **軽量配信**: PMTiles でビューワに直接配信
- **AI 支援**: AGENTS.md で正しいクエリパターンを事前学習

```text
portolan
├── STAC カタログ   → 横断検索
├── GeoParquet      → 高速フィルタ
├── PMTiles         → タイル配信
├── COG             → ラスター参照
└── AGENTS.md       → エージェントへの指引
```