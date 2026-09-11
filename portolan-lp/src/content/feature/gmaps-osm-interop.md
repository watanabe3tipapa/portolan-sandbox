---
title: "Google Maps × OpenStreetMap — 二大マップサービスのデータ連携"
description: "Google Maps と OpenStreetMap（OSM）が持つデータの性質の違いと、Portolan が両者をつなぐ「共通の読み口」になりうる理由を整理します。"
pubDate: 2026-09-11
---

## 異なる世界観を持つ2つのマップ

| | Google Maps | OpenStreetMap |
|---|---|---|
| 運営 | 民間（Google） | コミュニティ |
| データ形式 | 独自（ベクタータイル等） | OSM XML / PBF |
| ライセンス | 固有契約 | ODbL |
| 更新 | プロプライエタリな収集 | クラウドソーシング |

両者は表現・許諾・更新方法が根本的に異なり、これまで「データを直接つなぐ」ことは難しかったと言えます。

## 両者の技術的な違い

### 座標系の差

- **Google Maps**: EPSG:3857（Web メルカトル投影法）
- **OpenStreetMap**: EPSG:4326（WGS 84）が基本。内部処理は EPSG:3857 を使う

この差を吸収しないと、ポイントの位置がずれます。Portolan では AGENTS.md に「このデータは EPSG:3857 なので、利用時は EPSG:4326 に変換すること」のように明記します。

### データ粒度

| 項目 | Google Maps | OpenStreetMap |
|---|---|---|
| 建物 | 3D モデル（ボリュームデータあり） | 2D ポリゴン（高度情報は限定的） |
| 観光 | 完全性が非常に高い | 都市部は高いが地方は偏りあり |
| ライセンス | Google に依存 | ODbL（再利用可能） |
| リアルタイム性 | 常に最新 | ボランティア依存で更新に差 |

## 共通プロトコルとしての Portolan

Portolan は地理空間データを「AI が直接読める形で公開する」ためのルール集です。以下の表現で両者を仲介できる可能性があります。

- **GeoParquet / PMTiles** — タイル・列指向形式による共通の「読み」基盤
- **collection.json** — メタデータを標準化し、どのマップ由来かを機械可読にする
- **AGENTS.md** — ライセンス条件や更新頻度の違いを、使う側に事前に伝える

## 共通の GeoParquet カラム設計

両者のデータを扱いやすくするため、共通カラムの設計が有効です。

```python
import geopandas as gpd
import pandas as pd

# OSM の POI を GeoParquet 化
osm = gpd.read_file("osm_poi.pbf")
osm["source"] = "openstreetmap"
osm["source_id"] = osm["osm_id"].astype(str)
osm.to_parquet("data/poi.parquet", schema_version="1.0.0")

# 同様に Google Maps 由来のデータを統合
# gmap.to_parquet(...) と同じ形式で統合
```

`source` カラムにより、どのマップ由来かをフィルタできます。

## 連携の用例

### 1. OSM 由来の POI データを GeoParquet 化し、Google 由来の境界データと同一コレクションで参照

```python
import duckdb

# OSM の POI と Google 由来の行政境界を結合
duckdb.sql("""
  SELECT p.name, b.admin_name
  FROM poi.parquet p
  JOIN boundary.parquet b
  ON ST_Within(p.geom, b.geom)
""")
```

### 2. STAC カタログで「由来の異なるデータ」を横断検索し、AI エージェントに出典付きで提供

```python
import json, urllib.request

# STAC カタログから由来の異なるデータを検索
catalog = json.load(urllib.request.urlopen(
    "https://example.org/catalog.json"
))
for item in catalog["items"]:
    print(item["properties"]["source"], item["id"])
```

### 3. 各社のタイルソースをそのまま参照（移動させず）し、ビューワ側で切り替え

```html
<!-- PMTiles を使った 2ソース切り替え例 -->
<script>
  const map = L.map("map");
  L.tileLayer("https://example.org/osm/{z}/{x}/{y}.pmtiles")
    .addTo(map);
  L.tileLayer("https://example.org/gmap/{z}/{x}/{y}.pmtiles")
    .addTo(map).setOpacity(0.5);
</script>
```

## 利用規約の違いを守る

| 規約 | Google Maps | OpenStreetMap |
|---|---|---|
| 商業利用 | Google の規約に従う | ODbL で再利用可 |
| 出典表示 | 必要（Google の表示規定） | 必要（ODbL の Attribution） |
| 再配布 | 制限あり | 自由（ODbL の ShareAlike に従う） |

Portolan の AGENTS.md では、この違いを明記します。

```markdown
## ライセンス条件

- Google Maps 由来データ: Google の規約に従い、出典表示が必要
- OpenStreetMap 由来データ: ODbL。再配布時は同一ライセンス
```

## このデモから読めること

Portolan が実現しようとしているのは、特定プラットフォームへの集約でも、データの取り込みでもありません。**「すべてのデータが、それぞれの場所に開かれた状態で存在する」世界**です。行政や研究機関が持つデータ主権を守りつつ、AI の力を借りられる、その可能性をこの記事は示しています。