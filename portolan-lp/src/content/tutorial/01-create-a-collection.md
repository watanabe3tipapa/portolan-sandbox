---
title: "1. Create a Collection — 最初のコレクションを作る"
description: "collection.json の最小構成を理解し、オブジェクトストレージに置ける状態を整えます。"
order: 1
pubDate: 2026-09-11
---

## collection.json とは

コレクションは Portolan で公開するデータの単位です。`collection.json` がその目次（カタログ）として振る舞います。

## 最小構成

```bash
my-collection/
├── collection.json   # 機械可読
├── README.md         # 人間可読
└── AGENTS.md         # AI 可読
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
  "links": []
}
```

## 次のステップ

- [チュートリアル一覧](./)