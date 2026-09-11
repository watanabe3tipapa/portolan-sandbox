# portolan-sandbox

**「地図データを配る」時代の終わり——AIが直接読める空間インフラ「Portolan」を、多くの人々の手元へ。**

portolan-sandbox は、オープン仕様「Portolan」を身近に使えるようにするための手法を開拓する実験リポジトリです。Google アカウントだけで認証・デプロイまで対応できる構成を目指し、LP・構想メモ・要約記事をひとまとめに管理します。

[![Version](https://img.shields.io/badge/version-v0.1.0-blue.svg)](https://github.com/watanabe3tipapa/portolan-sandbox/releases)
[![GitHub](https://img.shields.io/github/issues/watanabe3tipapa/portolan-sandbox.svg)](https://github.com/watanabe3tipapa/portolan-sandbox/issues)

[日本語](README.md) | [English](README_en.md)

---

## 概要

Portolan は、地理空間データを「AI が直接読める形で、出版者が管理するストレージに置いたまま公開する」ためのオープン仕様です。本リポジトリは、この Portolan の啓発活動と具体的な活用方法の開拓を目的としています。

主な取り組み:

- ASTRO で構築したランディングページ（portolan-lp/）による啓発
- Google Colaboratory との連携手法の検討、Colab MCP server のパーソナル・開発サーバーとしての利活用
- Google アカウントだけで完了する認証・デプロイ手法の開拓
- 構想・アイデアを `DEV-MEMO.md` で整理

---

## コンセプト（なぜ「サンドボックス」か）

サンドボックス（砂場）は、安全な範囲で試行錯誤できる遊び場です。本リポジトリも同様に、Portolan を身近にするための手法や構成を、気軽に試して育てていく実験場として位置づけています。

---

## 主な特徴

- Portolan の概要をまとめた要約記事（Portolan_要約.html）
- ASTRO 製 LP と GitHub Pages への自動デプロイ（main への push で公開）
- 構想・アイデアの一元管理（DEV-MEMO.md）
- ゆくゆくは Google アカウントだけで完結するデプロイ構成を目標に検討

---

## 前提条件

| ツール | 必要バージョン | 確認コマンド |
|---|---:|---|
| Node.js | >= 22 | `node --version` |
| npm | >= 10 | `npm --version` |

---

## 開始手順

1. リポジトリをクローン:

```bash
git clone https://github.com/watanabe3tipapa/portolan-sandbox.git
```

2. LP をローカルで起動:

```bash
cd portolan-lp
npm install
npm run dev
```

3. ビルド:

```bash
npm run build
```

---

## リポジトリ構成（主なファイル・ディレクトリ）

- DEV-MEMO.md — 構想・アイデア・開発メモ
- Portolan_要約.html — GeoAI 第16回「地図データを配る」時代の終わり——の要約記事
- portolan-lp/ — ASTRO 製ランディングページ
- .github/workflows/deploy.yml — GitHub Pages 自動デプロイ用ワークフロー
- README.md / README_en.md — 本ドキュメント（日本語・英語）

---

## コントリビューション

コントリビューションは歓迎します。大きな変更は事前に issue を立ててください。

基本的なワークフロー:

1. リポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/your-feature`)
3. 変更をコミット (`git commit -m 'Add your change'`)
4. ブランチをプッシュし、Pull Request を作成

詳細はリポジトリの Issue ページを参照してください。

---

## 連絡先 / 公開サイト

- GitHub: https://github.com/watanabe3tipapa/portolan-sandbox
- LP (GitHub Pages): https://watanabe3tipapa.github.io/portolan-sandbox/

---

## ライセンス

ライセンスは未定です（MIT を検討中）。決定次第 LICENSE ファイルを追加します。

---

## 開発・保守状態

- リポジトリはアーカイブされていません。
- 最終更新: 2026-09-11 (本ドキュメント時点 / v0.1.0)