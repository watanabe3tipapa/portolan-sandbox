---
title: "共通プロトコルの用例 — STAC・GeoParquet・PMTiles が開く横断参照"
description: "地図データを横断的に参照するための共通プロトコル（STAC・GeoParquet・COG・PMTiles）のユースケースを、コード例を交えて紹介します。"
pubDate: 2026-09-11
---

## なぜ共通プロトコルが必要か

地理空間データはこれまで、ポータル・専用API・FTP という「それぞれ違う入り口」で配布されてきました。AI エージェントが自律的にデータを調達するには、入り口の差異を吸収する共通の読み口が必要です。

## 主要な共通プロトコル

### STAC（SpatioTemporal Asset Catalog）

衛星データや地図データに統一ラベルを付与し、横断検索を可能にする規格です。

```bash
# レジストリからカタログを検索する例
stac search --catalog https://example.org/collection.json \
  --bbox 139.0,35.0,140.0,36.0
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

### PMTiles

1 ファイルで済むタイルアーカイブ形式。サーバー運用なしに静的公開できます。

## Portolan との関係

Portolan 自体は新形式ではなく、**これらの標準を組み合わせたベストプラクティス**です。AGENTS.md が「どのプロトコルを使えば速いか」を教え、AI エージェントが最初から意図通りに使えるようにします。

## 用例まとめ

- **横断検索**: STAC で複数組織のカタログを検索
- **高速フィルタ**: GeoParquet で空間フィルタを実行
- **軽量配信**: PMTiles でビューワに直接配信
- **AI 支援**: AGENTS.md で正しいクエリパターンを事前学習