---
title: "3. Deploy — GitHub Pages で公開する"
description: "コレクションと LP を GitHub Pages に配置し、世界に向けて公開する方法を学びます。"
order: 3
pubDate: 2026-09-11
---

## GitHub Pages で静的サイトを公開

Portolan は静的ファイルとして公開できるため、GitHub Pages との相性が抜群です。

## 公開の流れ

1. リポジトリを作成（例: `watanabe3tipapa/portolan-sandbox`）
2. `main` ブランチへ push
3. リポジトリ設定 → Pages → Source を **GitHub Actions** に設定
4. push のたびに自動ビルド・デプロイ

## 本プロジェクトのワークフロー

本リポジトリでは `.github/workflows/deploy.yml` により ASTRO の `dist/` を GitHub Pages へ自動デプロイしています。

## 次のステップ

- [チュートリアル一覧](./)