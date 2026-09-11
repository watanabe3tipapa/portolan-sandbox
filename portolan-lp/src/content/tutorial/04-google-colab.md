---
title: "4. Google Colaboratory — パーソナル・開発サーバーとして使う"
description: "Portolan を Google アカウントだけで扱うための最初の一歩。Colab と Colab MCP server の位置付けを整理します。"
order: 4
pubDate: 2026-09-11
---

## 構想

「Google アカウントだけで全操作（認証・デプロイなど）を完結させる」ことを目指しています。その第一歩として、Google Colaboratory を検証環境として使います。

Colab はブラウザ上で動作するため、ローカルに Python や GIS ツールをインストールする必要がありません。Google アカウントでログインするだけで、（制限付きで）GPU / 高メモリのランタイムも利用できます。

## Colab の位置付け

- **認証**: Google アカウントでログイン → 追加の認証基盤が不要
- **実行環境**: ブラウザ上のノートブック + ランタイム（Python 標準 + 追加ライブラリ）
- **永続的なサーバー運用**: 不要（セッションはタイムアウトで断たれるが、コードはノートブックに残る）

| 項目 | Colab | 自前サーバー |
|---|---|---|
| コスト | 無料（時間制限あり） | 月額費用 |
| セットアップ | 不要 | 必要 |
| 常時稼働 | しない | する |
| アクセス制御 | Google アカウント | 鍵管理 |

## まず GeoPandas を動かす

Colab のノートブックで GeoParquet を触る最小例です。

```python
# -*- coding: utf-8 -*-
!pip install -q geopandas pyarrow

import geopandas as gpd

# サンプルの Parquet を読み込む
df = gpd.read_parquet("https://.../places.parquet")
print(df.head())
print(df.crs)  # 座標系を確認
```

これだけで、ダウンロードなしに「必要部分を直接読む」Portolan の体験を確認できます。

## GitHub / ドライブとの連携

認証は Google アカウントで完結します。

```python
# Google Drive をマウント（OAuth 認証）
from google.colab import drive
drive.mount('/content/drive')

# GitHub（公開リポジトリ）なら認証なしで clone
!git clone https://github.com/watanabe3tipapa/portolan-sandbox.git
```

GitHub トークンやベアラは使わないので、秘密情報をノートブックに載せずに済みます。

## Colab MCP server

Colab を MCP server として立ち上げることで、AI エージェントからファイル作成・実行・デプロイを行う個人開発サーバーとして利用できます。

- Colab ノートブックのセルを MCP のツールとして公開
- AI エージェント（Claude / その他 MCP クライアント）から呼び出し
- Drive・ランタイム上のファイル操作やコード実行をエージェントに委任

```text
AI エージェント ⇄ MCP プロトコル ⇄ Colab (MCP server)
                                     ├─ Google Drive 読み書き
                                     ├─ コード実行（GeoPandas 等）
                                     └─ デプロイ（GitHub API 等）
```

詳しくは特集記事「[Colab MCP server に期待できる機能](/feature/colab-mcp-server/)」を参照してください。

## 実践イメージ

```python
# 1) 公開 URL から collection.json を読む
import json, urllib.request

url = "https://<username>.github.io/my-collection/collection.json"
col = json.load(urllib.request.urlopen(url))
print(col["id"], col["license"])

# 2) リンク先の GeoParquet を直接読む
import geopandas as gpd
items = [l for l in col["links"] if l["rel"] == "items"]
df = gpd.read_parquet(items[0]["href"])
df.head()
```

## 課題と今後の展望

- Colab のセッションは数時間で切れるため、**永続ジョブには不向き**
- MCP server としての公開方法はプロトタイプ段階
- 認証・デプロイを「Google アカウントだけで」完結させるための仕組み化はこれから

次のステップは、特集記事の「[Colab MCP server に期待できる機能](/feature/colab-mcp-server/)」をご覧ください。

## このチュートリアルはおわり

全 5 ステップ（0〜4）を終えました。ここまでで「読む・作る・公開する」一連の流れを体験できました。

- [チュートリアル一覧に戻る](../)