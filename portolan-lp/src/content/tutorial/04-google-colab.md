---
title: "4. Google Colaboratory — パーソナル・開発サーバーとして使う"
description: "Portolan を Google アカウントだけで扱うための最初の一歩。Colab と Colab MCP server の位置付けを整理します。"
order: 4
pubDate: 2026-09-11
---

## 構想

「Google アカウントだけで全操作（認証・デプロイなど）を完結させる」ことを目指しています。その第一歩として、Google Colaboratory を検証環境として使います。

## Colab の位置付け

- 認証: Google アカウントでログイン
- 実行環境: ブラウザ上のノートブック + ランタイム
- 永続的なサーバー運用は不要

## Colab MCP server

Colab を MCP server として立ち上げることで、AI エージェントからファイル作成・実行・デプロイを行う個人開発サーバーとして利用できます。

## 次のステップ

- [チュートリアル一覧](./)