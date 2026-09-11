---
title: "5. Local LLM — マウントしたローカル LLM でデータ解析する"
description: "Colab 上に Ollama をマウントし、データを外部 API に送らずローカルで空間解析する方法を学びます。"
order: 5
pubDate: 2026-09-11
---

## なぜローカル LLM を使うのか

クリティカルなデータほど「外部の AI API に送りたくない」という要望があります。行政・研究機関が持つデータを匿名化なしにクラウド AI へ渡すのは難しい。

Colab 上に**ローカル LLM（Ollama）**を構築すれば、モデルとデータが同じマシンにあり、外部へ送信されません。Google アカウントだけで、オープンモデルを使った解析が完結します。

## Ollama とは

Ollama はローカルで LLM を実行するためのツールです。モデルをダウンロードし、`ollama serve` で API サーバーを立ち上げれば、`curl` や Python から呼び出せるようになります。

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

## セットアップ（Colab の場合）

### 1. Ollama のインストール

```bash
!curl -fsSL https://ollama.com/install.sh | sh
```

### 2. モデルストアを Google Drive へマウント

デフォルトではモデルはランタイム（一時領域）に入るため、セッション終了で消えてしまいます。**モデルストアを Drive に指定**すると、再起動後も再利用できます。

```python
import os
os.environ['OLLAMA_MODELS'] = '/content/drive/MyDrive/ollama'
!mkdir -p /content/drive/MyDrive/ollama
```

### 3. サーバー起動とモデル取得

```bash
!nohup ollama serve > /tmp/ollama.log 2>&1 &
!sleep 5
!ollama pull qwen2.5:0.5b   # 約 500MB、初回のみ
```

## 本リポジトリの MCP ツール（検証済み）

`demos/colab-mcp-server/` に用意したツールで、ローカル解析を実行できます。

| ツール | 機能 |
|---|---|
| `ollama_status(model)` | バイナリの有無・モデル保持状況の確認 |
| `pull_local_llm(model)` | モデルのダウンロード |
| `ask_local_llm(question, model)` | ローカル LLM への直接質問 |
| `geo_analyze_local_llm(source, question, model)` | GeoParquet を読み、ローカル LLM で分析 |

実機での動作確認（2026-09-11、qwen2.5:0.5b）:

```text
> ollama_status('qwen2.5:0.5b')
model_present: true

> ask_local_llm('Name the CRS that uses meters for web maps.', 'qwen2.5:0.5b')
answer: "The system commonly used for web maps is UTM ..."

> geo_analyze_local_llm(PUBLIC/poi.parquet, 'What places are in this dataset?', 'qwen2.5:0.5b')
answer: "The dataset contains information about various locations ..."
```

## データを「ローカル」で分析する流れ

```text
GeoParquet（公開 URL または Drive）
   │  geopandas で読み込み（サンプル化）
   ▼
ローカル LLM（Ollama）
   │  質問 + サンプルデータ
   ▼
回答（外部 API へ送信されない）
```

`geo_analyze_local_llm` は、GeoParquet の先頭サンプルを JSON 化して LLM へ渡します。座標列 (`geometry`) は外して省トークン化しています。

## モデル選択のヒント

| モデル | サイズ | 用途 |
|---|---|---|
| qwen2.5:0.5b | 約 500MB | 軽量・超高速（検証向け） |
| llama3.2:1b | 約 1.3GB | 軽量・汎用 |
| qwen2.5:3b | 約 2GB | 日本語を含む中規模 |
| llama3.2:3b | 約 2GB | 汎用 |

実行時メモリが不足する場合は、さらに小さなモデルか `num_ctx` を調整します。

## セキュリティ上の注意

- ローカル LLM でもプロンプトや出力はログに残り得る
- Drive にデータを置く場合は、共有設定を再確認
- モデル自体は公開されていることに留意（機密情報を学習させる用途には不向き）

## 次のステップ

ローカル LLM は Portolan と組み合わせると、**データ主権を守りながら** AI 解析できます。
次の関心ごとに応じて、特集記事「[ケーススタディ — OGC Connect Helsinki](../../feature/helsinki-demo/)」や「[共通プロトコルの用例](../../feature/common-protocols/)」をご覧ください。

- [チュートリアル一覧に戻る](../)