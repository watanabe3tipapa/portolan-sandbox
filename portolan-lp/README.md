# Portolan LP

AIが直接読める空間インフラ「Portolan」のランディングページ

## 概要

地理空間データを「AIが直接読める形で」公開するための新しいオープン仕様「Portolan」を紹介するランディングページです。チュートリアル 6 本 + 事例 5 本の記事を掲載し、各記事には archify で生成した構成図（自己完結型 HTML）を iframe で埋め込んでいます。

## 開発環境

```sh
npm install
npm run dev
```

## ビルド

```sh
npm run build
```

## デプロイ

GitHub Pagesに自動デプロイされます。手動でデプロイする場合：

```sh
npm run deploy
```

## プロジェクト構造

```text
/
├── public/
│   ├── favicon.svg / favicon.ico
│   ├── demo-collection/     # デモ用データコレクション
│   └── diagrams/            # archify 図（自己完結型 HTML）
│       ├── tutorial-00.html … tutorial-05.html
│       └── colab-mcp-server.html, gmaps-osm-interop.html,
│           common-protocols.html, helsinki-demo.html,
│           google-github-workflow.html
└── src
    ├── layouts
    │   └── Layout.astro     # 共通レイアウト（.diagram 埋め込みスタイル）
    ├── content
    │   ├── tutorial/        # 記事 6 本（00 〜 05）
    │   └── feature/         # 事例 5 本
    └── pages
        ├── index.astro
        ├── tutorial/index.astro, tutorial/[...slug].astro
        └── feature/index.astro, feature/[...slug].astro
```

## 参考

- [Portolan 仕様](https://portolan.org)
- [Astro ドキュメント](https://docs.astro.build)
